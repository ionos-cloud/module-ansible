import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


EXAMPLES = '''
    - name: Create pcc
      profitbricks_pcc:
        name: "{{ name }}"
        description: "{{ description }}"

    - name: Update pcc
      profitbricks_pcc:
        pcc_id: "49e73efd-e1ea-11ea-aaf5-5254001a8838"
        name: "{{ new_name }}"
        description: "{{ new_description }}"
        state: update

    - name: Remove pcc
      profitbricks_pcc:
        pcc_id: "2851af0b-e1ea-11ea-aaf5-5254001a8838"
        state: absent
'''


HAS_SDK = True
try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import PrivateCrossConnect
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


def create_pcc(module, client):
    name = module.params.get('name')
    description = module.params.get('description')

    pcc = PrivateCrossConnect(name=name, description=description)

    try:
        pcc_response = client.create_pcc(pcc)

        results = {
            'pcc_id': pcc_response['id'],
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the pcc: %s" % to_native(e))


def delete_pcc(module, client):
    pcc_id = module.params.get('pcc_id')

    changed = False

    try:
        client.delete_pcc(pcc_id)
        changed = True
    except Exception as e:
        module.fail_json(msg="failed to delete the pcc: %s" % to_native(e))

    return changed


def update_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    name = module.params.get('name')
    description = module.params.get('description')

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_pcc(pcc_id, name=name, description=description)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to update the pcc: %s" % to_native(e))
        changed = False

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            pcc_id=dict(type='str'),
            name=dict(type='str'),
            description=dict(type='str'),
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
        pass
        if not module.params.get('name'):
            module.fail_json(msg='name parameter is required for a new pcc')
        if not module.params.get('description'):
            module.fail_json(msg='description parameter is required for a new pcc')
        try:
            (pcc_dict_array) = create_pcc(module, ionosenterprise)
            module.exit_json(**pcc_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'absent':
        if not module.params.get('pcc_id'):
            module.fail_json(msg='pcc_id parameter is required for deleting a pcc.')
        try:
            (changed) = delete_pcc(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set pcc state: %s' % to_native(e))

    elif state == 'update':
        if not module.params.get('pcc_id'):
            module.fail_json(msg='pcc_id parameter is required for updating a pcc.')
        try:
            (changed) = update_pcc(module, ionosenterprise)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set pcc state: %s' % to_native(e))


if __name__ == '__main__':
    main()