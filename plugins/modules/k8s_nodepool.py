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

OPTIONS = {
    'nodepool_name': {
        'description': ['The name of the K8s Nodepool.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_cluster_id': {
        'description': ['The ID of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The Kubernetes version the nodepool is running.'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'nodepool_id': {
        'description': ['The ID of the K8s nodepool.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
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
        'description': ['The availability zone in which the target VM should be provisioned.'],
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
            "upgrading the nodepool's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default.",
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': ['Map of labels attached to node pool.'],
        'available': ['present',],
        'type': 'dict',
    },
    'annotations': {
        'description': ['Map of annotations attached to node pool.'],
        'available': ['present',],
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
    'gateway_ip': {
        'description': [
            "Public IP address for the gateway performing source NAT for the node pool's nodes belonging to a private cluster. "
            "Required only if the node pool belongs to a private cluster.",
        ],
        'available': ['present'],
        'type': 'str',
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
module: k8s_nodepool
short_description: Create or destroy K8s Nodepools
description:
     - This is a simple module that supports creating or removing K8s Nodepools.
       This module has a dependency on ionos-cloud >= 6.0.0
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_k8s_cluster_nodepool(module, client):
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
    gateway_ip = module.params.get('gateway_ip')

    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    auto_scaling = None
    if auto_scaling_dict:
        auto_scaling = dict(auto_scaling_dict)
        auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
        auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    try:
        k8s_nodepool_properties = KubernetesNodePoolProperties(name=nodepool_name, datacenter_id=datacenter_id,
                                                               node_count=node_count,
                                                               cpu_family=cpu_family, cores_count=cores_count,
                                                               ram_size=ram_size,
                                                               availability_zone=availability_zone,
                                                               storage_type=storage_type,
                                                               storage_size=storage_size, k8s_version=k8s_version,
                                                               maintenance_window=maintenance_window,
                                                               auto_scaling=auto_scaling, lans=lan_ids,
                                                               labels=labels, annotations=annotations,
                                                               public_ips=public_ips, gateway_ip=gateway_ip)

        k8s_nodepool = KubernetesNodePool(properties=k8s_nodepool_properties)

        response = k8s_server.k8s_nodepools_post_with_http_info(k8s_cluster_id=k8s_cluster_id,
                                                                kubernetes_node_pool=k8s_nodepool)
        (k8s_response, _, headers) = response

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_server.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=2),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == nodepool_name,
                    r.items
                ))[0].metadata.state == 'ACTIVE',
                scaleup=10000
            )

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'nodepool': k8s_response.to_dict()
        }
        return results

    except Exception as e:
        module.fail_json(msg="failed to create the k8s cluster nodepool: %s" % to_native(e))


def delete_k8s_cluster_nodepool(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    nodepool_id = module.params.get('nodepool_id')

    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    k8s_nodepool_list = k8s_server.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=5)
    k8s_nodepool = _get_resource(k8s_nodepool_list, nodepool_id)

    if not k8s_nodepool:
        module.exit_json(changed=False)

    changed = False

    try:
        response = k8s_server.k8s_nodepools_delete_with_http_info(k8s_cluster_id=k8s_cluster_id,
                                                                  nodepool_id=nodepool_id)
        (k8s_response, _, headers) = response
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: k8s_server.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=2),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == nodepool_id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000
            )
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to delete the k8s cluster: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'nodepool_id': nodepool_id
    }


def update_k8s_cluster_nodepool(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    nodepool_id = module.params.get('nodepool_id')
    node_count = module.params.get('node_count')
    maintenance = module.params.get('maintenance_window')
    auto_scaling_dict = module.params.get('auto_scaling')
    wait = module.params.get('wait')
    nodepool_name = module.params.get('nodepool_name')
    lan_ids = module.params.get('lan_ids')
    k8s_version = module.params.get('k8s_version')
    public_ips = module.params.get('public_ips')

    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    auto_scaling = None
    if auto_scaling_dict:
        auto_scaling = dict(auto_scaling_dict)
        auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
        auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    if not node_count:
        nodepool = k8s_server.k8s_nodepools_find_by_id(k8s_cluster_id=k8s_cluster_id, nodepool_id=nodepool_id, depth=2)
        node_count = nodepool.properties.nodeCount

    k8s_response = None

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        k8s_nodepool_properties = KubernetesNodePoolPropertiesForPut(
            name=nodepool_name, node_count=node_count,
            k8s_version=k8s_version, maintenance_window=maintenance_window,
            auto_scaling=auto_scaling, lans=lan_ids, public_ips=public_ips)

        k8s_nodepool = KubernetesNodePoolForPut(properties=k8s_nodepool_properties)
        k8s_response = k8s_server.k8s_nodepools_put(k8s_cluster_id=k8s_cluster_id, nodepool_id=nodepool_id,
                                                               kubernetes_node_pool=k8s_nodepool)

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_server.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=5),
                fn_check=lambda r: list(filter(
                    lambda e: e.id == nodepool_id,
                    r.items
                ))[0].metadata.state == 'ACTIVE',
                scaleup=10000
            )

        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the nodepool: %s" % to_native(e))
        changed = False

    return {
        'changed': changed,
        'failed': False,
        'action': 'update',
        'nodepool': k8s_response.to_dict()
    }


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


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
                module.exit_json(**create_k8s_cluster_nodepool(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_k8s_cluster_nodepool(module, api_client))
            elif state == 'update':
                module.exit_json(**update_k8s_cluster_nodepool(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
