import time

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


EXAMPLES = '''
    - name: Create backupunit
      ionos-cloud_backupunit:
        backupunit_email: "{{ email }}"
        backupunit_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a backupunit
      ionos-cloud_backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        backupunit_email: "{{ updated_email }}"
        backupunit_password:  "{{ updated_password }}"
        state: update

    - name: Remove backupunit
      ionos-cloud_backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        state: absent
'''


HAS_SDK = True
try:
    import ionos_cloud_sdk
    from ionos_cloud_sdk import __version__ as sdk_version
    from ionos_cloud_sdk.models import BackupUnit
    from ionos_cloud_sdk.rest import ApiException
    from ionos_cloud_sdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def create_backupunit(module, client):
    name = module.params.get('name')
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')

    properties = {
        'name': name,
        'password': password,
        'email': email
    }

    backupunit = BackupUnit(properties=properties)

    try:
        backupunit_response = client.backupunits_post(backupunit)

        results = {
            'id': backupunit_response.id,
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the backupunit: %s" % to_native(e))


def delete_backupunit(module, client):
    backupunit_id = module.params.get('backupunit_id')
    changed = False

    try:
        client.backupunits_delete(backupunit_id)
        changed = True

    except Exception as e:
        module.fail_json(msg="failed to delete the backupunit: %s" % to_native(e))

    return changed


def update_backupunit(module, client):
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')
    backupunit_id = module.params.get('backupunit_id')

    properties = {
        'password': password,
        'email': email
    }

    backupunit = BackupUnit(properties=properties)

    try:
        client.backupunits_put(backupunit_id, backupunit)
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

    state = module.params.get('state')

    configuration = ionos_cloud_sdk.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        api_instance = ionos_cloud_sdk.BackupUnitApi(api_client)

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new backupunit')
            if not module.params.get('backupunit_email'):
                module.fail_json(msg='backupunit_email parameter is required for a new backupunit')
            if not module.params.get('backupunit_password'):
                module.fail_json(msg='backupunit_password parameter is required for a new backupunit')

            try:
                (backupunit_dict_array) = create_backupunit(module, api_instance)
                module.exit_json(**backupunit_dict_array)

            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('backupunit_id'):
                module.fail_json(msg='backupunit_id parameter is required for deleting a backupunit.')

            try:
                (changed) = delete_backupunit(module, api_instance)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('backupunit_id'):
                module.fail_json(msg='backupunit_id parameter is required for updating a backupunit.')

            try:
                (changed) = update_backupunit(module, api_instance)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))


if __name__ == '__main__':
    main()
