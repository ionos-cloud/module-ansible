import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
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

- name: Delete k8s cluster nodepool
  k8s_nodepools:
    k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
    nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
    state: absent

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
'''

HAS_SDK = True
try:
    import ionossdk
    from ionossdk import __version__ as sdk_version
    from ionossdk.models import KubernetesCluster, KubernetesClusterProperties, KubernetesNodePool, \
        KubernetesNodePoolProperties, KubernetesNodePoolPropertiesForPut
    from ionossdk.rest import ApiException
    from ionossdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re


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

    k8s_server = ionossdk.KubernetesApi(api_client=client)

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
                                                               public_ips=public_ips)

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
    k8s_server = ionossdk.KubernetesApi(api_client=client)

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

    k8s_server = ionossdk.KubernetesApi(api_client=client)

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

        k8s_nodepool = KubernetesNodePool(properties=k8s_nodepool_properties)
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            nodepool_name=dict(type='str'),
            k8s_cluster_id=dict(type='str'),
            k8s_version=dict(type='str'),
            nodepool_id=dict(type='str'),
            datacenter_id=dict(type='str'),
            lan_ids=dict(type='list', elements='int'),
            node_count=dict(type='int'),
            cpu_family=dict(type='str'),
            cores_count=dict(type='str'),
            ram_size=dict(type='str'),
            availability_zone=dict(type='str'),
            storage_type=dict(type='str'),
            storage_size=dict(type='str'),
            maintenance_window=dict(
                type='dict',
                day_of_the_week=dict(type='int'),
                time=dict(type='int')
            ),
            labels=dict(type='dict'),
            annotations=dict(type='dict'),
            auto_scaling=dict(
                type='dict',
                min_node_count=dict(type='str'),
                max_node_count=dict(type='str')
            ),
            public_ips=dict(type='list', elements='str'),
            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionossdk is required for this module, run `pip install ionossdk`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ionossdk-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionossdk.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'present':
            error_message = "%s parameter is required updating a k8s nodepool"
            if not module.params.get('nodepool_name'):
                module.fail_json(msg=error_message % 'nodepool_name')
            if not module.params.get('k8s_cluster_id'):
                module.fail_json(msg=error_message % 'k8s_cluster_id')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg=error_message % 'datacenter_id')
            if not (module.params.get('node_count') or module.params.get('auto_scaling')) :
                module.fail_json(msg=error_message % 'node_count or auto_scaling')
            if not module.params.get('cpu_family'):
                module.fail_json(msg=error_message % 'cpu_family')
            if not module.params.get('cores_count'):
                module.fail_json(msg=error_message % 'cores_count')
            if not module.params.get('ram_size'):
                module.fail_json(msg=error_message % 'ram_size')
            if not module.params.get('availability_zone'):
                module.fail_json(msg=error_message % 'availability_zone')
            if not module.params.get('storage_type'):
                module.fail_json(msg=error_message % 'storage_type')
            if not module.params.get('storage_size'):
                module.fail_json(msg=error_message % 'storage_size')
            try:
                (k8s_nodepool_dict_array) = create_k8s_cluster_nodepool(module, api_client)
                module.exit_json(**k8s_nodepool_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set k8s cluster nodepool state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('k8s_cluster_id'):
                module.fail_json(msg='k8s_cluster_id parameter is required deleting a k8s nodepool.')
            if not module.params.get('nodepool_id'):
                module.fail_json(msg='nodepool_id parameter is required deleting a k8s nodepool.')

            try:
                (result) = delete_k8s_cluster_nodepool(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set k8s nodepool state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('k8s_cluster_id'):
                module.fail_json(msg='k8s_cluster_id parameter is required updating a nodepool.')
            if not module.params.get('nodepool_id'):
                module.fail_json(msg='nodepool_id parameter is required updating a nodepool.')
            try:
                (k8s_nodepool_dict_array) = update_k8s_cluster_nodepool(module, api_client)
                module.exit_json(**k8s_nodepool_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set k8s nodepool state: %s' % to_native(e))


if __name__ == '__main__':
    main()
