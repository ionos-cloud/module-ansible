import re
import copy
import yaml

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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'S3 Key'
RETURNED_KEY = 's3key'

OPTIONS = {
    'active': {
        'description': ['Denotes weather the S3 key is active.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'user': {
        'description': ['The ID or email of the user'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'key_id': {
        'description': ['The ID of the S3 key.'],
        'available': ['present', 'absent', 'update'],
        'required': ['absent', 'update'],
        'type': 'str',
    },
    'idempotency': {
        'description': ['Flag that dictates respecting idempotency. If an s3key already exists, returns with already existing key instead of creating more.'],
        'default': False,
        'available': 'present',
        'choices': [True, False],
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}


def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES)
    del val['available']
    del val['type']
    return val


DOCUMENTATION = '''
---
module: s3key
short_description: Create or destroy a Ionos Cloud S3Key.
description:
     - This is a simple module that supports creating or removing S3Keys.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''
  - name: Create an s3key
    s3key:
      user: <user_id/email>
  ''',
    'update': '''
  - name: Update an s3key
    s3key:
      user: <user_id/email>
      key_id: "00ca413c94eecc56857d
      active: False
      state: update
  ''',
    'absent': '''
  - name: Remove an s3key
    s3key:
      user: <user_id/email>
      key_id: 00ca413c94eecc56857d
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
        identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
        resource_identity = []

        for identity_path in identity_paths:
            current = resource
            for el in identity_path:
                current = getattr(current, el)
            resource_identity.append(current)

        return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


def get_users(client):
    all_users = ionoscloud.Users(items=[])
    offset = 0
    limit = 100

    users = client.um_users_get(depth=2, limit=limit, offset=offset)
    all_users.items += users.items
    while(users.links.next is not None):
        offset += limit
        users = client.um_users_get(depth=2, limit=limit, offset=offset)
        all_users.items += users.items

    return all_users


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_s3key(module, client):
    user_id = get_resource_id(
        module,
        get_users(ionoscloud.UserManagementApi(client)), 
        module.params.get('user'),
        [['id'], ['properties', 'email']],
    )
    do_idempotency = module.params.get('idempotency')
    key_id = module.params.get('key_id')
    active = module.params.get('active')
    wait_timeout = int(module.params.get('wait_timeout'))
    changed = False

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)
    s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id, depth=1)

    try:
        s3key = get_resource(module, s3key_list, key_id, [['id']])

        if not s3key and do_idempotency and len(s3key_list.items) > 0:
            s3key = s3key_list.items[0]

        if not s3key:
            changed = True
            s3key, _, headers = user_s3keys_server.um_users_s3keys_post_with_http_info(user_id=user_id)

            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        if s3key.properties.active != active:
            changed = True
            s3key, _, headers = user_s3keys_server.um_users_s3keys_put_with_http_info(
                user_id, s3key.id, S3Key(properties=S3KeyProperties(active=active)),
            )

            if module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': changed,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: s3key.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the s3key: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create',
        }


def delete_s3key(module, client):
    user_id = get_resource_id(
        module,
        get_users(ionoscloud.UserManagementApi(client)), 
        module.params.get('user'),
        [['id'], ['properties', 'email']],
    )
    key_id = module.params.get('key_id')

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)

    s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id)
    s3key_id = get_resource_id(module, s3key_list, key_id, [['id']])

    if not s3key_id:
        module.exit_json(changed=False)

    try:
        user_s3keys_server.um_users_s3keys_delete(user_id, s3key_id)
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
    user_id = get_resource_id(
        module,
        get_users(ionoscloud.UserManagementApi(client)), 
        module.params.get('user'),
        [['id'], ['properties', 'email']],
    )
    key_id = module.params.get('key_id')
    active = module.params.get('active')

    changed = False

    user_s3keys_server = ionoscloud.UserS3KeysApi(client)
    s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id, depth=1)
    s3key = get_resource(module, s3key_list, key_id, [['id']])

    if not s3key:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        if s3key.properties.active != active:
            changed = True
            s3key, _, headers = user_s3keys_server.um_users_s3keys_put_with_http_info(
                user_id, s3key.id, S3Key(properties=S3KeyProperties(active=active)),
            )

            if module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=module.params.get('wait_timeout'))

        return {
            'changed': changed,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: s3key.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the s3key: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
        }


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
        arguments[option_name] = {
            'type': option['type'],
        }
        for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
            if option.get(key) is not None:
                arguments[option_name][key] = option.get(key)

        if option.get('env_fallback'):
            arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

        if len(option.get('required', [])) == len(STATES):
            arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    certificate_fingerprint = module.params.get('certificate_fingerprint')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'present':
                module.exit_json(**create_s3key(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_s3key(module, api_client))
            elif state == 'update':
                module.exit_json(**update_s3key(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME,
                                                                                             error=to_native(e),
                                                                                             state=state))


if __name__ == '__main__':
    main()
