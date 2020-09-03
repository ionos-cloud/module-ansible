import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


EXAMPLES = '''
    - name: Create backupunit
      profitbricks_backupunit:
        backupunit_email: "{{ email }}"
        backupunit_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a backupunit
      profitbricks_backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        backupunit_email: "{{ updated_email }}"
        backupunit_password:  "{{ updated_password }}"
        state: update

    - name: Remove backupunit
      profitbricks_backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        state: absent
'''


HAS_SDK = True
try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import BackupUnit
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


def create_backupunit(module, client):
    name = module.params.get('name')
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')

    backupunit = BackupUnit(name, password=password, email=email)

    try:
        backupunit_response = client.create_backupunit(backupunit)

        results = {
            'backupunit': backupunit_response['id'],
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the backupunit: %s" % to_native(e))


def delete_backupunit(module, client):
    backupunit_id = module.params.get('backupunit_id')
    changed = False

    try:
        client.delete_backupunit(backupunit_id)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to delete the backupunit: %s" % to_native(e))

    return changed


def update_backupunit(module, client):
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')
    backupunit_id = module.params.get('backupunit_id')

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_backupunit(backupunit_id, email=email, password=password)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the backupunit: %s" % to_native(e))
        changed = False

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            backupunit_password=dict(type='str'),
            backupunit_email=dict(type='str'),
            backupunit_id=dict(type='str'),
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
        if not module.params.get('name'):
            module.fail_json(msg='name parameter is required for a new backupunit')
        if not module.params.get('backupunit_email'):
            module.fail_json(msg='backupunit_email parameter is required for a new backupunit')
        if not module.params.get('backupunit_password'):
            module.fail_json(msg='backupunit_password parameter is required for a new backupunit')

        try:
            (backupunit_dict_array) = create_backupunit(module, ionosenterprise)
            module.exit_json(**backupunit_dict_array)

        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'absent':
        if not module.params.get('backupunit_id'):
            module.fail_json(msg='backupunit_id parameter is required for deleting a backupunit.')

        try:
            (changed) = delete_backupunit(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))

    elif state == 'update':
        if not module.params.get('backupunit_id'):
            module.fail_json(msg='backupunit_id parameter is required for updating a backupunit.')

        try:
            (changed) = update_backupunit(module, ionosenterprise)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))


if __name__ == '__main__':
    main()
