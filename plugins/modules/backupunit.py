ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create backupunit
      backupunit:
        backupunit_email: "{{ email }}"
        backupunit_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a backupunit
      backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        backupunit_email: "{{ updated_email }}"
        backupunit_password:  "{{ updated_password }}"
        state: update

    - name: Remove backupunit
      backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        state: absent
'''

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import BackupUnit, BackupUnitProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_backupunit(module, client):
    name = module.params.get('name')
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    backupunit_server = ionoscloud.BackupUnitApi(client)

    backupunit_properties = BackupUnitProperties(name=name, password=password, email=email)
    backupunit = BackupUnit(properties=backupunit_properties)

    try:
        response = backupunit_server.backupunits_post_with_http_info(backupunit)
        (backupunit_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'backupunit': backupunit_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the backupunit: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create'
        }


def delete_backupunit(module, client):
    backupunit_id = module.params.get('backupunit_id')
    backupunit_server = ionoscloud.BackupUnitApi(client)

    try:
        backupunit_server.backupunits_delete(backupunit_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': backupunit_id
        }

    except Exception as e:
        module.fail_json(msg="failed to delete the backupunit: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': backupunit_id
        }


def update_backupunit(module, client):
    password = module.params.get('backupunit_password')
    email = module.params.get('backupunit_email')
    backupunit_id = module.params.get('backupunit_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    backupunit_server = ionoscloud.BackupUnitApi(client)

    backupunit_properties = BackupUnitProperties(password=password, email=email)
    backupunit = BackupUnit(properties=backupunit_properties)

    try:
        response = backupunit_server.backupunits_put_with_http_info(backupunit_id=backupunit_id, backup_unit=backupunit)
        (backupunit_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'backupunit': backupunit_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the backupunit: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update'
        }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            backupunit_password=dict(type='str', no_log=True),
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
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new backupunit')
            if not module.params.get('backupunit_email'):
                module.fail_json(msg='backupunit_email parameter is required for a new backupunit')
            if not module.params.get('backupunit_password'):
                module.fail_json(msg='backupunit_password parameter is required for a new backupunit')

            try:
                (backupunit_dict_array) = create_backupunit(module, api_client)
                module.exit_json(**backupunit_dict_array)

            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('backupunit_id'):
                module.fail_json(msg='backupunit_id parameter is required for deleting a backupunit.')

            try:
                (result) = delete_backupunit(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('backupunit_id'):
                module.fail_json(msg='backupunit_id parameter is required for updating a backupunit.')

            try:
                (backupunit_dict_array) = update_backupunit(module, api_client)
                module.exit_json(**backupunit_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set backupunit state: %s' % to_native(e))


if __name__ == '__main__':
    main()
