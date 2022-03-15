#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, UserProperties, UserPropertiesPost, UserPropertiesPut, UserPost, UserPut
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'User'

OPTIONS = {
    'firstname': {
        'description': ["The user's first name."],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'lastname': {
        'description': ["The user's last name."],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'email': {
        'description': ["The user's email"],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'user_password': {
        'description': ['A password for the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'administrator': {
        'description': ['Boolean value indicating if the user has administrative rights.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'force_sec_auth': {
        'description': ['Boolean value indicating if secure (two-factor) authentication should be forced for the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'groups': {
        'description': [
            'A list of group IDs or names where the user (non-administrator) is to be added.'
            'Set to empty list ([]) to remove the user from all groups.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'sec_auth_active': {
        'description': ['Indicates if secure authentication is active for the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    's3_canonical_user_id': {
        'description': ['Canonical (S3) ID of the user for a given identity.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
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
module: user
short_description: Create, update or remove a user.
description:
     - This module allows you to create, update or remove a user.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: john.doe@example.com
      user_password: secretpassword123
      administrator: true
      state: present
  ''',
  'update' : '''# Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: john.doe@example.com
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  ''',
  'absent' : '''# Remove a user
  - name: Remove user
    user:
      email: john.doe@example.com
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_user(module, client, api_client):
    """
    Creates a user.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The user instance
    """
    firstname = module.params.get('firstname')
    lastname = module.params.get('lastname')
    email = module.params.get('email')
    user_password = module.params.get('user_password')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    user = None

    users = client.um_users_get(depth=2)
    for u in users.items:
        if email == u.properties.email:
            user = u
            break

    should_change = user is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'user': user.to_dict()
        }

    try:
        user_properties = UserPropertiesPost(firstname=firstname, lastname=lastname, email=email,
                                             administrator=administrator or False,
                                             force_sec_auth=force_sec_auth or False,
                                             password=user_password)

        user = UserPost(properties=user_properties)
        response = client.um_users_post_with_http_info(user)
        (user_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            api_client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'user': user_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the user: %s" % to_native(e))


def update_user(module, client, api_client):
    """
    Updates a user.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The user instance
    """
    firstname = module.params.get('firstname')
    lastname = module.params.get('lastname')
    email = module.params.get('email')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    user_password = module.params.get('user_password')


    try:
        user = None
        user_response = None
        users = client.um_users_get(depth=2)
        for resource in users.items:
            if email in (resource.properties.email, resource.id):
                user = resource
                break

        if user:
            if module.check_mode:
                module.exit_json(changed=True)

            if not firstname:
                firstname = user.properties.firstname
            if not lastname:
                lastname = user.properties.lastname
            if administrator is None:
                administrator = user.properties.administrator
            if force_sec_auth is None:
                force_sec_auth = user.properties.force_sec_auth

            user_properties = UserPropertiesPut(firstname=firstname,
                                                lastname=lastname,
                                                email=email,
                                                administrator=administrator or False,
                                                force_sec_auth=force_sec_auth or False)
            if user_password:
                user_properties.password = user_password
            new_user = UserPut(properties=user_properties)
            response = client.um_users_put_with_http_info(user_id=user.id, user=new_user)
            (user_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                api_client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        else:
            module.fail_json(msg='User \'%s\' not found.' % str(email))

        if module.params.get('groups') is not None:
            user = client.um_users_find_by_id(user_id=user_response.id, depth=2)
            old_ug = []
            for g in user.entities.groups.items:
                old_ug.append(g.id)

            all_groups = client.um_groups_get(depth=2)
            new_ug = []
            for g in module.params.get('groups'):
                group_id = _get_resource_id(all_groups, g, module, "Group")
                new_ug.append(group_id)

            for group_id in old_ug:
                if group_id not in new_ug:
                    client.um_groups_users_delete(
                        group_id=group_id,
                        user_id=user.id
                    )

            for group_id in new_ug:
                if group_id not in old_ug:
                    response = client.um_groups_users_post_with_http_info(
                        group_id=group_id,
                        user=User(id=user.id)
                    )
                    (user_response, _, headers) = response
                    request_id = _get_request_id(headers['Location'])
                    api_client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'user': user_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create or update the user: %s" % to_native(e))


def delete_user(module, client):
    """
    Removes a user

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the user was removed, false otherwise
    """
    email = module.params.get('email')

    # Locate UUID for the user
    user_list = client.um_users_get(depth=2)
    user_id = _get_user_id(user_list, email)

    if not user_id:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        client.um_users_delete(user_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': user_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the user: %s" % to_native(e))


def _get_user_id(resource_list, identity):
    """
    Fetch and return the UUID of a user regardless of whether the email or
    UUID is passed.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.email, resource.id):
            return resource.id
    return None


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


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
        api_instance = ionoscloud.UserManagementApi(api_client)

        try:
            if state == 'absent':
                module.exit_json(**delete_user(module, api_instance))
            elif state == 'present':
                module.exit_json(**create_user(module, api_instance, api_client))
            elif state == 'update':
                module.exit_json(**update_user(module, api_instance, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
