from socket import timeout
import time
import re
import copy
import yaml


HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import KubernetesCluster, KubernetesClusterProperties, KubernetesNodePool, \
        KubernetesNodePoolProperties, KubernetesNodePoolPropertiesForPut, KubernetesNodePoolForPut
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'K8s Nodepool'
RETURNED_KEY = 'nodepool'

OPTIONS = {
    'k8s_cluster_id': {
        'description': ['The ID of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'k8s_nodepool': {
        'description': ['The ID or name of the K8s nodepool.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'nodepool_name': {
        'description': ['The name of the K8s Nodepool.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The Kubernetes version the nodepool is running.'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'datacenter_id': {
        'description': ['A valid ID of the data center, to which the user has access.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'lan_ids': {
        'description': ['Array of additional LANs attached to worker nodes.'],
        'available': ['update', 'present'],
        'type': 'list',
        'elements': 'int',
    },
    'node_count': {
        'description': ['The number of nodes that make up the node pool.'],
        'available': ['update', 'present'],
        'type': 'int',
    },
    'cpu_family': {
        'description': ['A valid CPU family name.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'cores_count': {
        'description': ['The number of cores for the node.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'ram_size': {
        'description': ['The RAM size for the node. Must be set in multiples of 1024 MB, with minimum size is of 2048 MB.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'availability_zone': {
        'description': ['The availability zone in which the target VM should be provisioned.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_type': {
        'description': ['The type of hardware for the volume.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_size': {
        'description': ['The size of the volume in GB. The size should be greater than 10GB.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'maintenance_window': {
        'description': [
            "The maintenance window is used for updating the software on the nodepool's nodes and for "
            "upgrading the nodepool's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default.",
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': ['Map of labels attached to node pool.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'annotations': {
        'description': ['Map of annotations attached to node pool.'],
        'available': ['present','update'],
        'type': 'dict',
    },
    'auto_scaling': {
        'description': ['Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'public_ips': {
        'description': [
            'Optional array of reserved public IP addresses to be used by the nodes. IPs must be from same location as the data center '
            'used for the node pool. The array must contain one more IP than maximum number possible number of nodes (nodeCount+1 for '
            'fixed number of nodes or maxNodeCount+1 when auto scaling is used). The extra IP is used when the nodes are rebuilt.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different'
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 3600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}

def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

DOCUMENTATION = '''
---
module: k8s_nodepool
short_description: Create or destroy K8s Nodepools
description:
     - This is a simple module that supports creating or removing K8s Nodepools.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter_id: "4d495548-e330-434d-83a9-251bfa645875"
      node_count: "1"
      cpu_family: "AMD_OPTERON"
      cores_count: "1"
      ram_size: "2048"
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: "100"
  ''',
  'update' : '''
  - name: Update k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      nodepool_id: "6e9efcc6-649a-4514-bee5-6165b614c89e"
      node_count: 1
      cores_count: "1"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      auto_scaling:
        min_node_count: 1
        max_node_count: 3
      state: update
  ''',
  'absent' : '''
  - name: Delete k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


def _should_replace_object(module, existing_object):
    return (
        module.params.get('nodepool_name') is not None
        and existing_object.properties.name != module.params.get('nodepool_name')
        or module.params.get('cpu_family') is not None
        and existing_object.properties.cpu_family != module.params.get('cpu_family')
        or module.params.get('cores_count') is not None
        and existing_object.properties.cores_count != module.params.get('cores_count')
        or module.params.get('ram_size') is not None
        and existing_object.properties.ram_size != module.params.get('ram_size')
        or module.params.get('availability_zone') is not None
        and existing_object.properties.availability_zone != module.params.get('availability_zone')
        or module.params.get('storage_type') is not None
        and existing_object.properties.storage_type != module.params.get('storage_type')
        or module.params.get('storage_size') is not None
        and existing_object.properties.storage_size != module.params.get('storage_size')
        or module.params.get('datacenter_id') is not None
        and existing_object.properties.datacenter_id != module.params.get('datacenter_id')
    )


def _should_update_object(module, existing_object):
    return (
        module.params.get('k8s_version') is not None
        and existing_object.properties.k8s_version != module.params.get('k8s_version')
        or module.params.get('maintenance_window') is not None
        and (
            existing_object.properties.maintenance_window.day_of_the_week != module.params.get('maintenance_window').get('day_of_the_week')
            or existing_object.properties.maintenance_window.time != module.params.get('maintenance_window').get('time')
        )
        or module.params.get('lan_ids') is not None
        and sorted(existing_object.properties.lan_ids.sort()) != sorted(module.params.get('lan_ids').sort())
        or module.params.get('public_ips') is not None
        and sorted(existing_object.properties.public_ips) != sorted(module.params.get('public_ips'))
        or module.params.get('node_count') is not None
        and existing_object.properties.node_count != module.params.get('node_count')
        or module.params.get('labels') is not None
        and existing_object.properties.labels != module.params.get('labels')
        or module.params.get('annotations') is not None
        and existing_object.properties.annotations != module.params.get('annotations')
        or module.params.get('auto_scaling') is not None
        and (
            existing_object.properties.auto_scaling.min_node_count != module.params.get('auto_scaling').get('min_node_count')
            or existing_object.properties.auto_scaling.max_node_count != module.params.get('auto_scaling').get('max_node_count')
        )
    )


def _get_object_list(module, client):
    return ionoscloud.KubernetesApi(client).k8s_nodepools_get(module.params.get('k8s_cluster_id'), depth=1)


def _get_object_name(module):
    return module.params.get('nodepool_name')


def _get_object_identifier(module):
    return module.params.get('k8s_nodepool')


def _create_object(module, client, existing_object=None):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    k8s_version = module.params.get('k8s_version')
    nodepool_name = module.params.get('nodepool_name')
    lan_ids = module.params.get('lan_ids')
    datacenter_id = module.params.get('datacenter_id')
    node_count = module.params.get('node_count')
    cpu_family = module.params.get('cpu_family')
    cores_count = module.params.get('cores_count')
    ram_size = module.params.get('ram_size')
    availability_zone = module.params.get('availability_zone')
    storage_type = module.params.get('storage_type')
    storage_size = module.params.get('storage_size')
    maintenance = module.params.get('maintenance_window')
    auto_scaling_dict = module.params.get('auto_scaling')
    labels = module.params.get('labels')
    annotations = module.params.get('annotations')
    wait = module.params.get('wait')
    public_ips = module.params.get('public_ips')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    auto_scaling = None
    if auto_scaling_dict:
        auto_scaling = dict(auto_scaling_dict)
        auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
        auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

    if existing_object is not None:
        nodepool_name = existing_object.properties.name if nodepool_name is None else nodepool_name
        k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
        lan_ids = existing_object.properties.lans if lan_ids is None else lan_ids
        datacenter_id = existing_object.properties.datacenter_id if datacenter_id is None else datacenter_id
        node_count = existing_object.properties.node_count if node_count is None else node_count
        cpu_family = existing_object.properties.cpu_family if cpu_family is None else cpu_family
        cores_count = existing_object.properties.cores_count if cores_count is None else cores_count
        ram_size = existing_object.properties.ram_size if ram_size is None else ram_size
        availability_zone = existing_object.properties.availability_zone if availability_zone is None else availability_zone
        storage_type = existing_object.properties.storage_type if storage_type is None else storage_type
        storage_size = existing_object.properties.storage_size if storage_size is None else storage_size
        labels = existing_object.properties.labels if labels is None else labels
        annotations = existing_object.properties.annotations if annotations is None else annotations
        maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance
        auto_scaling = existing_object.properties.auto_scaling if auto_scaling is None else auto_scaling

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    k8s_nodepool_properties = KubernetesNodePoolProperties(
        name=nodepool_name,
        datacenter_id=datacenter_id,
        node_count=node_count,
        cpu_family=cpu_family,
        cores_count=cores_count,
        ram_size=ram_size,
        availability_zone=availability_zone,
        storage_type=storage_type,
        storage_size=storage_size,
        k8s_version=k8s_version,
        maintenance_window=maintenance_window,
        auto_scaling=auto_scaling,
        lans=lan_ids,
        labels=labels,
        annotations=annotations,
        public_ips=public_ips,
    )
    k8s_nodepool = KubernetesNodePool(properties=k8s_nodepool_properties)

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        k8s_response = k8s_api.k8s_nodepools_post(k8s_cluster_id=k8s_cluster_id, kubernetes_node_pool=k8s_nodepool)

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                    k8s_cluster_id,
                    k8s_response.id,
                ).metadata.state,
                fn_check=lambda r: r == 'ACTIVE',
                scaleup=10000,
                timeout=wait_timeout,
            )
    except ApiException as e:
        module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
    return k8s_response


def _update_object(module, client, existing_object):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    node_count = module.params.get('node_count')
    maintenance = module.params.get('maintenance_window')
    auto_scaling_dict = module.params.get('auto_scaling')
    lan_ids = module.params.get('lan_ids')
    k8s_version = module.params.get('k8s_version')
    public_ips = module.params.get('public_ips')
    labels = module.params.get('labels')
    annotations = module.params.get('annotations')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    if not node_count:
        node_count = existing_object.properties.node_count

    auto_scaling = None
    if auto_scaling_dict:
        auto_scaling = dict(auto_scaling_dict)
        auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
        auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
        
    k8s_nodepool_properties = KubernetesNodePoolPropertiesForPut(
        node_count=node_count,
        k8s_version=k8s_version,
        maintenance_window=maintenance_window,
        auto_scaling=auto_scaling,
        lans=lan_ids,
        public_ips=public_ips,
        labels=labels,
        annotations=annotations,
    )

    k8s_nodepool = KubernetesNodePoolForPut(properties=k8s_nodepool_properties)

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        k8s_response = k8s_api.k8s_nodepools_put(
            k8s_cluster_id=k8s_cluster_id,
            nodepool_id=existing_object.id,
            kubernetes_node_pool=k8s_nodepool,
        )

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                    k8s_cluster_id,
                    k8s_response.id,
                ).metadata.state,
                fn_check=lambda r: r == 'ACTIVE',
                scaleup=10000,
                timeout=wait_timeout,
            )

        return k8s_response
    except ApiException as e:
        module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    k8s_cluster_id = module.params.get('k8s_cluster_id')

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        if existing_object.metadata.state != 'DESTROYING':
            k8s_api.k8s_nodepools_delete_with_http_info(k8s_cluster_id=k8s_cluster_id, nodepool_id=existing_object.id)

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=1),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == existing_object.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000,
                timeout=wait_timeout,
            )
    except Exception as e:
        module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

    existing_object = get_resource(module, object_list, _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(module, object_list, object_name)

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
    }


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
      arguments[option_name] = {
        'type': option['type'],
      }
      for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
        if option.get(key) is not None:
          arguments[option_name][key] = option.get(key)

      if option.get('env_fallback'):
        arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

      if len(option.get('required', [])) == len(STATES):
        arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments())

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)
        if state == 'present' and not module.params.get('node_count') and not module.params.get('auto_scaling'):
            module.fail_json(
                msg='either node_count or auto_scaling parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME),
            )
        try:
            if state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'absent':
                module.exit_json(**remove_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
