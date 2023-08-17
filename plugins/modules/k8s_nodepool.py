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
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
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
    'name': {
        'description': ['The name of the K8s Nodepool.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'lans': {
        'description': ['The array of existing private LANs to attach to worker nodes.'],
        'available': ['update', 'present'],
        'type': 'list',
        'elements': 'dict',
    },
    'node_count': {
        'description': ['The number of worker nodes of the node pool.'],
        'available': ['update', 'present'],
        'type': 'int',
    },
    'cpu_family': {
        'description': ['The CPU type for the nodes.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'cores_count': {
        'description': ['The total number of cores for the nodes.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'ram_size': {
        'description': ['The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB.'],
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
        'description': ['The storage type for the nodes.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_size': {
        'description': ['The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'maintenance_window': {
        'description': ['The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': ['The labels attached to the node pool.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'annotations': {
        'description': ['The annotations attached to the node pool.'],
        'available': ['present','update'],
        'type': 'dict',
    },
    'auto_scaling': {
        'description': ['Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'public_ips': {
        'description': ['Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool\'s data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    'allow_replace': {
        'description': [
            'Boolean indincating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
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
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter: "4d495548-e330-434d-83a9-251bfa645875"
      node_count: 1
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
      k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      k8s_nodepool: "6e9efcc6-649a-4514-bee5-6165b614c89e"
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
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      k8s_nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
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

def _get_lans(lans_param):
    if lans_param is None:
        return []
    def _get_routes(routes_param):
        return [
            ionoscloud.KubernetesNodePoolLanRoutes(
                network=route['network'],
                gateway_ip=route['gateway_ip'],
            ) for route in routes_param
        ]
    return [
        ionoscloud.KubernetesNodePoolLan(
            id=lan_param['id'],
            dhcp=lan_param['dhcp'],
            routes=_get_routes(lan_param.get('routes', [])),
        ) for lan_param in lans_param
    ]

def _should_replace_object(module, existing_object, client):
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
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
        or datacenter_id is not None
        and existing_object.properties.datacenter_id != datacenter_id
    )


def _should_update_object(module, existing_object):
    def sort_func(el):
        return el['id']
    def sort_func_routes(el):
        return el['gateway_ip'], el['network']

    if module.params.get('lans'):
        existing_lans = sorted(map(
            lambda x: {
                'id': str(x.id),
                'dhcp': x.dhcp,
                'routes': sorted(
                    map(
                        lambda y: {
                            'gateway_ip': y.gateway_ip,
                            'network': y.network,
                        },
                        x.routes if x.routes else [],
                    ),
                    key=sort_func_routes,
                ),
            },
            existing_object.properties.lans,
        ), key=sort_func)
        lans_input = module.params.get('lans')
        for lan_input in lans_input:
            lan_input['routes'] = sorted(lan_input.get('routes', []), key=sort_func_routes)
        new_lans = sorted(module.params.get('lans'), key=sort_func)

    return (
        module.params.get('k8s_version') is not None
        and existing_object.properties.k8s_version != module.params.get('k8s_version')
        or module.params.get('maintenance_window') is not None
        and (
            existing_object.properties.maintenance_window.day_of_the_week != module.params.get('maintenance_window').get('day_of_the_week')
            or existing_object.properties.maintenance_window.time != module.params.get('maintenance_window').get('time')
        )
        or module.params.get('lans') is not None
        and existing_lans != new_lans
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
    k8s_cluster_id = get_resource_id(
        module, 
        ionoscloud.KubernetesApi(client).k8s_get(depth=1),
        module.params.get('k8s_cluster'),
    )

    return ionoscloud.KubernetesApi(client).k8s_nodepools_get(k8s_cluster_id, depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('k8s_nodepool')


def _create_object(module, client, existing_object=None):
    k8s_cluster_id = get_resource_id(
        module, 
        ionoscloud.KubernetesApi(client).k8s_get(depth=1),
        module.params.get('k8s_cluster'),
    )
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    k8s_version = module.params.get('k8s_version')
    name = module.params.get('name')
    lans = _get_lans(module.params.get('lans'))
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
        name = existing_object.properties.name if name is None else name
        k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
        lans = existing_object.properties.lans if lans is None else lans
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
        maintenance_window = existing_object.properties.maintenance_window if maintenance is None else maintenance_window
        auto_scaling = existing_object.properties.auto_scaling if auto_scaling is None else auto_scaling
        public_ips = existing_object.properties.public_ips if public_ips is None else public_ips

    k8s_nodepool_properties = KubernetesNodePoolProperties(
        name=name,
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
        lans=lans,
        labels=labels,
        annotations=annotations,
        public_ips=public_ips,
    )
    k8s_nodepool = KubernetesNodePool(properties=k8s_nodepool_properties)

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        k8s_response = k8s_api.k8s_nodepools_post(k8s_cluster_id=k8s_cluster_id, kubernetes_node_pool=k8s_nodepool)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                    k8s_cluster_id,
                    k8s_response.id,
                ).metadata.state,
                fn_check=lambda r: r == 'ACTIVE',
                scaleup=10000,
                timeout=int(module.params.get('wait_timeout')),
            )
    except ApiException as e:
        module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
    return k8s_response


def _update_object(module, client, existing_object):
    k8s_cluster_id = get_resource_id(
        module, 
        ionoscloud.KubernetesApi(client).k8s_get(depth=1),
        module.params.get('k8s_cluster'),
    )
    node_count = module.params.get('node_count')
    maintenance = module.params.get('maintenance_window')
    auto_scaling_dict = module.params.get('auto_scaling')
    lans = _get_lans(module.params.get('lans'))
    k8s_version = module.params.get('k8s_version')
    public_ips = module.params.get('public_ips')
    labels = module.params.get('labels')
    annotations = module.params.get('annotations')

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
        lans=lans,
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

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                    k8s_cluster_id,
                    k8s_response.id,
                ).metadata.state,
                fn_check=lambda r: r == 'ACTIVE',
                scaleup=10000,
                timeout=int(module.params.get('wait_timeout')),
            )

        return k8s_response
    except ApiException as e:
        module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


def _remove_object(module, client, existing_object):
    k8s_cluster_id = get_resource_id(
        module, 
        ionoscloud.KubernetesApi(client).k8s_get(depth=1),
        module.params.get('k8s_cluster'),
    )

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        if existing_object.metadata.state != 'DESTROYING':
            k8s_api.k8s_nodepools_delete_with_http_info(k8s_cluster_id=k8s_cluster_id, nodepool_id=existing_object.id)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=1),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == existing_object.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )
    except Exception as e:
        module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object, client):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

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
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

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
