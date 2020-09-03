import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

HAS_SDK = True

EXAMPLES = '''
- name: Create k8s cluster
  profitbricks_k8s_cluster:
    name: "{{ cluster_name }}"

- name: Delete k8s cluster
  profitbricks_k8s_cluster:
    k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
    state: absent

- name: Update k8s cluster
  profitbricks_k8s_cluster:
    k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
    maintenance_window:
      day: 'Tuesday'
      time: '13:03:00'
    k8s_version: 1.17.8
    state: update
'''

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


def create_k8s_cluster(module, client):
    cluster_name = module.params.get('cluster_name')

    try:
        k8s_response = client.create_k8s_cluster(cluster_name)

        client.wait_for(
            fn_request=lambda: client.list_k8s_clusters(),
            fn_check=lambda r: list(filter(
                lambda e: e['properties']['name'] == cluster_name,
                r['items']
            ))[0]['metadata']['state'] == 'ACTIVE',
            console_print='.',
            scaleup=10000
        )

        results = {
            'k8s_id': k8s_response['id'],
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the k8s cluster: %s" % to_native(e))


def delete_k8s_cluster(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')

    changed = False

    try:
        client.delete_k8s_cluster(k8s_cluster_id)
        changed = True
    except Exception as e:
        module.fail_json(msg="failed to delete the k8s cluster: %s" % to_native(e))

    return changed


def update_k8s_cluster(module, client):
    cluster_name = module.params.get('cluster_name')
    k8s_version = module.params.get('k8s_version')
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    maintenance = module.params.get('maintenance_window')

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day')

    properties = {
        'name': cluster_name,
        'k8sVersion': k8s_version,
        'maintenanceWindow': maintenance_window
    }

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_k8s_cluster(k8s_cluster_id, properties=properties)
        changed = True
    except Exception as e:
        module.fail_json(msg="failed to update the k8s cluster: %s" % to_native(e))
        changed = False

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cluster_name=dict(type='str'),
            k8s_cluster_id=dict(type='str'),
            k8s_version=dict(type='str'),
            maintenance_window=dict(
                type='dict',
                day=dict(type='str'),
                time=dict(type='str')
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
        client = IonosEnterpriseService(username=username, password=password)
    else:
        client = IonosEnterpriseService(
            username=username,
            password=password,
            host_base=api_url
        )

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    client.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'present':
        if not module.params.get('cluster_name'):
            module.fail_json(msg='cluster_name parameter is required for a new k8s cluster')
        try:
            (k8s_cluster_dict_array) = create_k8s_cluster(module, client)
            module.exit_json(**k8s_cluster_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set k8s cluster state: %s' % to_native(e))

    elif state == 'absent':
        if not module.params.get('k8s_cluster_id'):
            module.fail_json(msg='k8s_cluster_id parameter is required for deleting a k8s cluster.')
        try:
            (changed) = delete_k8s_cluster(module, client)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set k8s cluster state: %s' % to_native(e))

    elif state == 'update':
        error_message = "%s parameter is required updating a k8s cluster."
        if not module.params.get('k8s_cluster_id'):
            module.fail_json(msg=error_message % 'k8s_cluster_id')
        if not module.params.get('cluster_name'):
            module.fail_json(msg=error_message % 'cluster_name')
        if not module.params.get('k8s_version'):
            module.fail_json(msg=error_message % 'k8s_version')
        if not module.params.get('maintenance_window'):
            module.fail_json(msg=error_message % 'maintenance_window')

        try:
            (changed) = update_k8s_cluster(module, client)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set k8s cluster state: %s' % to_native(e))


if __name__ == '__main__':
    main()
