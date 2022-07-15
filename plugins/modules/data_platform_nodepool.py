import time
import re
import copy
import yaml


HAS_SDK = True

try:
    import ionoscloud_dsaas
    from ionoscloud_dsaas import __version__ as sdk_version
    from ionoscloud_dsaas import ApiClient
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
DSAAS_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dsaas/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'data-platform'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Data Platform Nodepool'

OPTIONS = {
    'nodepool_name': {
        'description': [
          'The name of your node pool. Must be 63 characters or less and must be empty or begin and end with '
          'an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics '
          'between.',
        ],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'data_platform_cluster_id': {
        'description': ['The ID of the Data Platform cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'data_platform_nodepool_id': {
        'description': ['The ID of the Data Platform nodepool.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'node_count': {
        'description': ['The number of nodes that make up the node pool.'],
        'available': ['update', 'present'],
        'type': 'int',
    },
    'cpu_family': {
        'description': [
          'A valid CPU family name or `AUTO` if the platform shall choose the best fitting option.'
          'Available CPU architectures can be retrieved from the datacenter resource.',
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'cores_count': {
        'description': ['The number of cores for the node.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'ram_size': {
        'description': ['The RAM size for the node. Must be set in multiples of 1024 MB, with minimum size is of 2048 MB.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'availability_zone': {
        'description': [
          'The availability zone of the virtual datacenter region where the node pool resources '
          'should be provisioned.',
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_type': {
        'description': ['The type of hardware for the volume.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_size': {
        'description': ['The size of the volume in GB. The size should be greater than 10GB.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': [
            "The maintenance window is used for updating the software on the nodepool's nodes and for "
            "upgrading the nodepool's K8s version. If no value is given, one is chosen dynamically, so "
            "there is no fixed default.",
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': [
          'Key-value pairs attached to the node pool resource as '
          '[Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)',
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'annotations': {
        'description': [
          'Key-value pairs attached to node pool resource as '
          '[Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)',
        ],
        'available': ['present','update'],
        'type': 'dict',
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
        'default': 600,
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
module: data_platform_nodepool
short_description: Create or destroy Data Platform Nodepools
description:
     - This is a simple module that supports creating or removing Data Platform Nodepools.
       This module has a dependency on ionoscloud_dsaas >= 1.0.0
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud_dsaas >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create Dsaas Platform nodepool
    data_platform_nodepool:
      cluster_name: "{{ name }}"
      data_platform_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      node_count: "1"
      cpu_family: "AMD_OPTERON"
      cores_count: "1"
      ram_size: "2048"
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: "100"
  ''',
  'update' : '''
  - name: Update Dsaas Platform nodepool
    data_platform_nodepool:
      cluster_name: "{{ name }}"
      data_platform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
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
  - name: Delete Dsaas Platform nodepool
    data_platform_nodepool:
      data_platform_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      data_platform_nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
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


def create_data_platform_nodepool(module, client):
    data_platform_cluster_id = module.params.get('data_platform_cluster_id')
    data_platform_version = module.params.get('data_platform_version')
    nodepool_name = module.params.get('nodepool_name')
    node_count = module.params.get('node_count')
    cpu_family = module.params.get('cpu_family')
    cores_count = module.params.get('cores_count')
    ram_size = module.params.get('ram_size')
    availability_zone = module.params.get('availability_zone')
    storage_type = module.params.get('storage_type')
    storage_size = module.params.get('storage_size')
    maintenance = module.params.get('maintenance_window')
    labels = module.params.get('labels')
    annotations = module.params.get('annotations')
    wait = module.params.get('wait')

    dsaas_nodepool_server = ionoscloud_dsaas.DataPlatformNodePoolApi(api_client=client)

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    nodepool_list = dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id)

    existing_nodepool = get_resource(module, nodepool_list, nodepool_name)

    if existing_nodepool:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'data_platform_nodepool': existing_nodepool.to_dict()
        }

    try:
        data_platform_nodepool_properties = ionoscloud_dsaas.CreateNodePoolProperties(
            name=nodepool_name,
            node_count=node_count,
            cpu_family=cpu_family,
            cores_count=cores_count,
            ram_size=ram_size,
            availability_zone=availability_zone,
            storage_type=storage_type,
            storage_size=storage_size,
            data_platform_version=data_platform_version,
            maintenance_window=maintenance_window,
            labels=labels,
            annotations=annotations,
        )

        dsaas_nodepool = ionoscloud_dsaas.CreateNodePoolRequest(properties=data_platform_nodepool_properties)

        dsaas_response= dsaas_nodepool_server.create_cluster_nodepool(data_platform_cluster_id, dsaas_nodepool)

        if wait:
            client.wait_for(
                fn_request=lambda: dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == nodepool_name,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000
            )

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'data_platform_nodepool': dsaas_response.to_dict()
        }
        return results

    except Exception as e:
        module.fail_json(msg="failed to create the Data Platform nodepool: %s" % to_native(e))


def delete_data_platform_nodepool(module, client):
    data_platform_cluster_id = module.params.get('data_platform_cluster_id')
    nodepool_id = module.params.get('data_platform_nodepool_id')
    nodepool_name = module.params.get('nodepool_name')

    dsaas_nodepool_server = ionoscloud_dsaas.DataPlatformNodePoolApi(api_client=client)
    nodepool_list = dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id)
    dsaas_nodepool = get_resource(module, nodepool_list, nodepool_id if nodepool_id else nodepool_name)

    if not dsaas_nodepool:
        module.exit_json(changed=False)

    changed = False

    try:
        if dsaas_nodepool.metadata.state == 'AVAILABLE':
            dsaas_nodepool_server.delete_cluster_nodepool(data_platform_cluster_id, nodepool_id)
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == nodepool_id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000
            )
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to delete the Data Platform Nodepool: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'data_platform_nodepool_id': nodepool_id
    }


def update_data_platform_nodepool(module, client):
    data_platform_cluster_id = module.params.get('data_platform_cluster_id')
    nodepool_id = module.params.get('nodepool_id')
    node_count = module.params.get('node_count')
    maintenance = module.params.get('maintenance_window')
    wait = module.params.get('wait')
    nodepool_name = module.params.get('nodepool_name')
    data_platform_version = module.params.get('data_platform_version')
    labels = module.params.get('labels')
    annotations = module.params.get('annotations')

    dsaas_nodepool_server = ionoscloud_dsaas.DataPlatformNodePoolApi(api_client=client)

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    nodepool_list = dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id)
    existing_nodepool_by_name = get_resource(module, nodepool_list, nodepool_name)

    if nodepool_id is not None and existing_nodepool_by_name is not None and existing_nodepool_by_name.id != nodepool_id:
        module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
            OBJECT_NAME, nodepool_name,
        ))

    if not node_count:
        node_count = existing_nodepool_by_name.properties.node_count

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        data_platform_nodepool_properties = ionoscloud_dsaas.PatchNodePoolProperties(
            name=nodepool_name,
            node_count=node_count,
            data_platform_version=data_platform_version,
            maintenance_window=maintenance_window,
            labels=labels,
            annotations=annotations,
        )

        k8s_nodepool = ionoscloud_dsaas.PatchNodePoolRequest(properties=data_platform_nodepool_properties)
        dsaas_response = dsaas_nodepool_server.patch_cluster_nodepool(
            data_platform_cluster_id, nodepool_id, kubernetes_node_pool=k8s_nodepool,
        )

        if wait:
            client.wait_for(
                fn_request=lambda: dsaas_nodepool_server.get_cluster_nodepools(data_platform_cluster_id),
                fn_check=lambda r: list(filter(
                    lambda e: e.id == nodepool_id,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000
            )

        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the Data Platform nodepool: %s" % to_native(e))
        changed = False

    return {
        'changed': changed,
        'failed': False,
        'action': 'update',
        'data_plaform_nodepool': dsaas_response.to_dict()
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
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dsaas is required for this module, run `pip install ionoscloud_dsaas`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud_dsaas)) as api_client:
        api_client.user_agent = DSAAS_USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)
        if state == 'present' and not module.params.get('node_count') and not module.params.get('auto_scaling'):
            module.fail_json(
                msg='either node_count or auto_scaling parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME),
            )
        try:
            if state == 'present':
                module.exit_json(**create_data_platform_nodepool(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_data_platform_nodepool(module, api_client))
            elif state == 'update':
                module.exit_json(**update_data_platform_nodepool(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
