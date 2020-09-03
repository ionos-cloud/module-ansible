import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
- name: Create k8s cluster nodepool
  profitbricks_k8s_nodepools:
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
  profitbricks_k8s_nodepools:
    k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
    nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
    state: absent

- name: Update k8s cluster nodepool
  profitbricks_k8s_nodepools:
    cluster_name: "{{ name }}"
    k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    nodepool_id: "6e9efcc6-649a-4514-bee5-6165b614c89e"
    node_count: 1
    cores_count: "1"
    maintenance_window:
      day: 'Tuesday'
      time: '13:03:00'
    auto_scaling:
      min_node_count: 1
      max_node_count: 3
    state: update
'''


HAS_SDK = True
try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def _wait_for_completion(client, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = client.get_request(
            request_id=promise['requestId'],
            status=True)

        if operation_result['metadata']['status'] == 'DONE':
            return
        elif operation_result['metadata']['status'] == 'FAILED':
            raise Exception(
                'Request failed to complete ' + msg + ' "' + str(
                    promise['requestId']) + '" to complete.')

    raise Exception('Timed out waiting for async operation ' + msg + ' "' +
                    str(promise['requestId']) + '" to complete.')


def create_k8s_cluster_nodepool(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    cluster_name = module.params.get('cluster_name')
    datacenter_id = module.params.get('datacenter_id')
    node_count = module.params.get('node_count')
    cpu_family = module.params.get('cpu_family')
    cores_count = module.params.get('cores_count')
    ram_size = module.params.get('ram_size')
    availability_zone = module.params.get('availability_zone')
    storage_type = module.params.get('storage_type')
    storage_size = module.params.get('storage_size')

    try:
        k8s_response = client.create_k8s_cluster_nodepool(k8s_cluster_id, cluster_name, datacenter_id, node_count,
                                                          cpu_family, cores_count, ram_size, availability_zone,
                                                          storage_type, storage_size)

        client.wait_for(
            fn_request=lambda: client.list_k8s_cluster_nodepools(k8s_cluster_id),
            fn_check=lambda r: list(filter(
                lambda e: e['properties']['name'] == cluster_name,
                r['items']
            ))[0]['metadata']['state'] == 'ACTIVE',
            console_print='.',
            scaleup=10000
        )

        results = {
            'k8s_nodepool_id': k8s_response['id'],
            'changed': True
        }
        return results

    except Exception as e:
        module.fail_json(msg="failed to create the k8s cluster nodepool: %s" % to_native(e))


def delete_k8s_cluster_nodepool(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    nodepool_id = module.params.get('nodepool_id')

    changed = False

    try:
        client.delete_k8s_cluster_nodepool(k8s_cluster_id, nodepool_id)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to delete the k8s cluster: %s" % to_native(e))

    return changed


def update_k8s_cluster_nodepool(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    nodepool_id = module.params.get('nodepool_id')
    node_count = module.params.get('node_count')
    maintenance_day = module.params.get('maintenance_window')['day']
    maintenance_time = module.params.get('maintenance_window')['time']
    min_node_count = module.params.get('auto_scaling')['min_node_count']
    max_node_count = module.params.get('auto_scaling')['max_node_count']

    auto_scaling = {
        'minNodeCount': min_node_count,
        'maxNodeCount': max_node_count
    }

    maintenance_window = {
        'dayOfTheWeek': maintenance_day,
        'time': maintenance_time
    }

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_k8s_cluster_nodepool(k8s_cluster_id, nodepool_id,
                                           node_count,
                                           maintenance_window, auto_scaling)

        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the nodepool: %s" % to_native(e))
        changed = False

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cluster_name=dict(type='str'),
            k8s_cluster_id=dict(type='str'),
            nodepool_id=dict(type='str'),
            datacenter_id=dict(type='str'),
            node_count=dict(type='int'),
            cpu_family=dict(type='str'),
            cores_count=dict(type='str'),
            ram_size=dict(type='str'),
            availability_zone=dict(type='str'),
            storage_type=dict(type='str'),
            storage_size=dict(type='str'),
            maintenance_window=dict(
                type='dict',
                day=dict(type='int'),
                time=dict(type='int')
            ),
            auto_scaling=dict(
                type='dict',
                min_node_count=dict(type='str'),
                max_node_count=dict(type='str')
            ),
            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['PROFITBRICKS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['PROFITBRICKS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionosenterprise is required for this module, run `pip install ionosenterprise`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')

    if not api_url:
        ionosenterprise = IonosEnterpriseService(username=username, password=password)
    else:
        ionosenterprise = IonosEnterpriseService(
            username=username,
            password=password,
            host_base=api_url
        )

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    ionosenterprise.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'present':
        error_message = "%s parameter is required updating a k8s cluster."
        if not module.params.get('cluster_name'):
            module.fail_json(msg=error_message % 'cluster_name')
        if not module.params.get('k8s_cluster_id'):
            module.fail_json(msg=error_message % 'k8s_cluster_id')
        if not module.params.get('datacenter_id'):
            module.fail_json(msg=error_message % 'datacenter_id')
        if not module.params.get('node_count'):
            module.fail_json(msg=error_message % 'node_count')
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
            (k8s_cluster_dict_array) = create_k8s_cluster_nodepool(module, ionosenterprise)
            module.exit_json(**k8s_cluster_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set k8s cluster nodepool state: %s' % to_native(e))

    elif state == 'absent':
        if not module.params.get('k8s_cluster_id'):
            module.fail_json(msg='k8s_cluster_id parameter is required deleting a k8s nodepool.')
        if not module.params.get('nodepool_id'):
            module.fail_json(msg='nodepool_id parameter is required deleting a k8s nodepool.')

        try:
            (changed) = delete_k8s_cluster_nodepool(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set k8s nodepool state: %s' % to_native(e))

    elif state == 'update':
        if not module.params.get('k8s_cluster_id'):
            module.fail_json(msg='k8s_cluster_id parameter is required updating a nodepool.')
        if not module.params.get('nodepool_id'):
            module.fail_json(msg='nodepool_id parameter is required updating a nodepool.')
        if not module.params.get('node_count'):
            module.fail_json(msg='node_count parameter is required updating a nodepool.')
        try:
            (changed) = update_k8s_cluster_nodepool(module, ionosenterprise)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set k8s nodepool state: %s' % to_native(e))


if __name__ == '__main__':
    main()
