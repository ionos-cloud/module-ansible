import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create an s3key
      profitbricks_s3key:
        user_id: "{{ user_id }}"

    - name: Update an s3key
      profitbricks_s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        active: False
        state: update

    - name: Remove an s3key
      profitbricks_s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        state: absent
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


def create_s3key(module, client):
    user_id = module.params.get('user_id')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    try:
        s3key_response = client.create_s3key(user_id)

        if wait:
            _wait_for_completion(client, s3key_response,
                                 wait_timeout, "create_s3key")

        results = {
            's3key_id': s3key_response['id'],
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the s3key: %s" % to_native(e))


def delete_s3key(module, client):
    user_id = module.params.get('user_id')
    key_id = module.params.get('key_id')

    changed = False

    try:
        client.delete_s3key(user_id, key_id)
        changed = True
    except Exception as e:
        module.fail_json(msg="failed to delete the s3key: %s" % to_native(e))

    return changed


def update_s3key(module, client):
    user_id = module.params.get('user_id')
    key_id = module.params.get('key_id')
    active = module.params.get('active')

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_s3key(user_id, key_id, active=active)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the s3key: %s" % to_native(e))
        changed = False

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            active=dict(type='bool'),
            user_id=dict(type='str'),
            key_id=dict(type='str'),
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
        ionosenteprise = IonosEnterpriseService(username=username, password=password)
    else:
        ionosenteprise = IonosEnterpriseService(
            username=username,
            password=password,
            host_base=api_url
        )

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    ionosenteprise.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'present':
        if not module.params.get('user_id'):
            module.fail_json(msg='user_id parameter is required for a new s3key')
        try:
            (s3key_dict_array) = create_s3key(module, ionosenteprise)
            module.exit_json(**s3key_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'absent':
        if not module.params.get('user_id'):
            module.fail_json(msg='user_id parameter is required for deleting an s3key.')
        if not module.params.get('key_id'):
            module.fail_json(msg='key_id parameter is required for deleting an s3key.')

        try:
            (changed) = delete_s3key(module, ionosenteprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'update':
        if not module.params.get('user_id'):
            module.fail_json(msg='user_id parameter is required for updating an s3key.')
        if not module.params.get('key_id'):
            module.fail_json(msg='key_id parameter is required for updating an s3key.')

        try:
            (changed) = update_s3key(module, ionosenteprise)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set s3key state: %s' % to_native(e))


if __name__ == '__main__':
    main()