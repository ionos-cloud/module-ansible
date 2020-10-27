import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create pcc
      ionos-cloud_pcc:
        name: "{{ name }}"
        description: "{{ description }}"

    - name: Update pcc
      ionos-cloud_pcc:
        pcc_id: "49e73efd-e1ea-11ea-aaf5-5254001a8838"
        name: "{{ new_name }}"
        description: "{{ new_description }}"
        state: update

    - name: Remove pcc
      ionos-cloud_pcc:
        pcc_id: "2851af0b-e1ea-11ea-aaf5-5254001a8838"
        state: absent
'''

HAS_SDK = True
try:
    import ionos_cloud_sdk
    from ionos_cloud_sdk import __version__ as sdk_version
    from ionos_cloud_sdk.models import PrivateCrossConnect
    from ionos_cloud_sdk.models import PrivateCrossConnectProperties
    from ionos_cloud_sdk.rest import ApiException
    from ionos_cloud_sdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def create_pcc(module, client):
    name = module.params.get('name')
    description = module.params.get('description')

    properties = {
        'name': name,
        'description': description
    }
    pcc = PrivateCrossConnect(properties=properties)

    try:
        pcc_response = client.pccs_post(pcc)

        results = {
            'pcc_id': pcc_response.id,
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the pcc: %s" % to_native(e))


def delete_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    changed = False

    try:
        client.pccs_delete(pcc_id)
        changed = True
    except Exception as e:
        module.fail_json(msg="failed to delete the pcc: %s" % to_native(e))

    return changed


def update_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    name = module.params.get('name')
    description = module.params.get('description')

    pcc = PrivateCrossConnectProperties(name=name, description=description)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.pccs_patch(pcc_id, pcc)
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
        module.fail_json(msg='ionos_cloud_sdk is required for this module, run `pip install ionos_cloud_sdk`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ionos_cloud_sdk-python/%s Ansible/%s' % (sdk_version, __version__)


    configuration = ionos_cloud_sdk.Configuration(
        username=username,
        password=password
    )

    state = module.params.get('state')

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        api_instance = ionos_cloud_sdk.PrivateCrossConnectApi(api_client)

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new pcc')
            if not module.params.get('description'):
                module.fail_json(msg='description parameter is required for a new pcc')
            try:
                (pcc_dict_array) = create_pcc(module, api_instance)
                module.exit_json(**pcc_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('pcc_id'):
                module.fail_json(msg='pcc_id parameter is required for deleting a pcc.')
            try:
                (changed) = delete_pcc(module, api_instance)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set pcc state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('pcc_id'):
                module.fail_json(msg='pcc_id parameter is required for updating a pcc.')
            try:
                (changed) = update_pcc(module, api_instance)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set pcc state: %s' % to_native(e))


if __name__ == '__main__':
    main()
