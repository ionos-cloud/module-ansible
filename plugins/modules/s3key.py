import re

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create an s3key
      s3key:
        user_id: "{{ user_id }}"

    - name: Update an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        active: False
        state: update

    - name: Remove an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        state: absent
'''

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import S3Key
    from ionoscloud.models import S3KeyProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_s3key(module, client):
    user_id = module.params.get('user_id')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)

    try:
        response = user_s3keys_server.um_users_s3keys_post_with_http_info(user_id=user_id)
        (s3key_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            's3key': s3key_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the s3key: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create',
        }


def delete_s3key(module, client):
    user_id = module.params.get('user_id')
    key_id = module.params.get('key_id')

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)

    s3key_list = user_management_server.um_users_s3keys_get(user_id=user_id, depth=5)
    s3key = _get_resource(s3key_list, key_id)

    if not s3key:
        module.exit_json(changed=False)

    try:
        user_s3keys_server.um_users_s3keys_delete(user_id, key_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': key_id
        }

    except Exception as e:
        module.fail_json(msg="failed to delete the s3key: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': key_id
        }


def update_s3key(module, client):
    user_id = module.params.get('user_id')
    key_id = module.params.get('key_id')
    active = module.params.get('active')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)

    properties = S3KeyProperties(active=active)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = user_s3keys_server.um_users_s3keys_put_with_http_info(user_id, key_id, S3Key(properties=properties))
        (s3key_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            's3key': s3key_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the s3key: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
        }


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.secret_key, resource.id):
            return resource.id

    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            active=dict(type='bool'),
            user_id=dict(type='str'),
            key_id=dict(type='str'),
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
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
    api_url = module.params.get('api_url')

    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    configuration = ionoscloud.Configuration(**conf)

    state = module.params.get('state')

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'present':
            if not module.params.get('user_id'):
                module.fail_json(msg='user_id parameter is required for a new s3key')
            try:
                (s3key_dict_array) = create_s3key(module, api_client)
                module.exit_json(**s3key_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('user_id'):
                module.fail_json(msg='user_id parameter is required for deleting an s3key.')
            if not module.params.get('key_id'):
                module.fail_json(msg='key_id parameter is required for deleting an s3key.')

            try:
                (changed) = delete_s3key(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('user_id'):
                module.fail_json(msg='user_id parameter is required for updating an s3key.')
            if not module.params.get('key_id'):
                module.fail_json(msg='key_id parameter is required for updating an s3key.')

            try:
                (changed) = update_s3key(module, api_client)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set s3key state: %s' % to_native(e))


if __name__ == '__main__':
    main()