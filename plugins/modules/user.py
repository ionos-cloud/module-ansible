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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'User'
RETURNED_KEY = 'user'

OPTIONS = {
    'firstname': {
        'description': ['The first name of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'lastname': {
        'description': ['The last name of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'email': {
        'description': ['The email address of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'user': {
        'description': ['The ID or name of the user.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
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
        'description': ['Indicates if the user has admin rights.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'force_sec_auth': {
        'description': ['Indicates if secure authentication should be forced on the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'groups': {
        'description': ['A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'sec_auth_active': {
        'description': ['Indicates if secure authentication is active for the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'allow_replace': {
        'description': [
            'Boolean indicating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
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
module: user
short_description: Create, update or remove a user.
description:
     - This module allows you to create, update or remove a user.
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
    'present': '''# Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: <email>
      user_password: <password>
      administrator: true
      state: present
  ''',
    'update': '''# Update a user
  - name: Update user
    user:
      user: <email>
      firstname: John II
      lastname: Doe
      email: <new_email>
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  ''',
    'absent': '''# Remove a user
  - name: Remove user
    user:
      user: <email>
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


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    return (
        module.params.get('lastname') is not None
        and existing_object.properties.lastname != module.params.get('lastname')
        or module.params.get('firstname') is not None
        and existing_object.properties.firstname != module.params.get('firstname')
        or module.params.get('email') is not None
        and existing_object.properties.email != module.params.get('email')
        or module.params.get('administrator') is not None
        and existing_object.properties.administrator != module.params.get('administrator')
        or module.params.get('force_sec_auth') is not None
        and existing_object.properties.force_sec_auth != module.params.get('force_sec_auth')
        or module.params.get('user_password') is not None
        or module.params.get('groups') is not None
    )


def _get_object_list(module, client):
    return get_users(ionoscloud.UserManagementApi(client))


def _get_object_name(module):
    return module.params.get('email')


def _get_object_identifier(module):
    return module.params.get('user')


def _create_object(module, client, existing_object=None):
    firstname = module.params.get('firstname')
    lastname = module.params.get('lastname')
    email = module.params.get('email')
    user_password = module.params.get('user_password')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')

    if existing_object is not None:
        firstname = existing_object.properties.firstname if firstname is None else firstname
        lastname = existing_object.properties.lastname if lastname is None else lastname
        email = existing_object.properties.email if email is None else email
        user_password = existing_object.properties.user_password if user_password is None else user_password
        administrator = existing_object.properties.administrator if administrator is None else administrator
        force_sec_auth = existing_object.properties.force_sec_auth if force_sec_auth is None else force_sec_auth

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    um_api = ionoscloud.UserManagementApi(client)

    user = UserPost(properties=UserPropertiesPost(
        firstname=firstname, lastname=lastname, email=email,
        administrator=administrator or False,
        force_sec_auth=force_sec_auth or False,
        password=user_password,
    ))

    try:
        user_response, _, headers = um_api.um_users_post_with_http_info(user)

        if wait or module.params.get('groups') is not None:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        
        if module.params.get('groups') is not None:
            # Get IDs of current groups of the user
            old_user_group_ids = []
            for g in um_api.um_users_groups_get(user_response.id).items:
                old_user_group_ids.append(g.id)

            all_groups = um_api.um_groups_get(depth=2)
            # Get IDs of groups that user needs to have at the end of update
            new_user_group_ids = []
            for g in module.params.get('groups'):
                group_id = get_resource_id(module, all_groups, g)
                new_user_group_ids.append(group_id)

            # Delete groups user not supposed to be in at end of update
            for group_id in old_user_group_ids:
                if group_id not in new_user_group_ids:
                    um_api.um_groups_users_delete(
                        group_id=group_id,
                        user_id=user_response.id
                    )

            # Post groups that weren't assigned to the user before
            for group_id in new_user_group_ids:
                if group_id not in old_user_group_ids:
                    response = um_api.um_groups_users_post_with_http_info(
                        group_id=group_id,
                        user=User(id=user_response.id)
                    )
                    (user_response, _, headers) = response
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            # update to reflect new group changes
            user_response = um_api.um_users_find_by_id(user_response.id, depth=2)
    except ApiException as e:
        module.fail_json(msg="failed to create the new user: %s" % to_native(e))
    return user_response


def _update_object(module, client, existing_object):
    firstname = module.params.get('firstname')
    lastname = module.params.get('lastname')
    email = module.params.get('email')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')
    user_password = module.params.get('user_password')

    email = existing_object.properties.email if email is None else email
    firstname = existing_object.properties.firstname if firstname is None else firstname
    lastname = existing_object.properties.lastname if lastname is None else lastname
    administrator = existing_object.properties.administrator if administrator is None else administrator
    force_sec_auth = existing_object.properties.force_sec_auth if force_sec_auth is None else force_sec_auth

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    um_api = ionoscloud.UserManagementApi(client)

    user_properties = UserPropertiesPut(
        firstname=firstname,
        lastname=lastname,
        email=email,
        administrator=administrator or False,
        force_sec_auth=force_sec_auth or False,
    )
    if user_password:
        user_properties.password = user_password
    
    new_user = UserPut(properties=user_properties)

    try:
        user_response, _, headers = um_api.um_users_put_with_http_info(
            existing_object.id, new_user,
        )

        if wait or module.params.get('groups') is not None:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        
        if module.params.get('groups') is not None:
            # Get IDs of current groups of the user
            old_user_group_ids = []
            for g in um_api.um_users_groups_get(user_response.id).items:
                old_user_group_ids.append(g.id)

            all_groups = um_api.um_groups_get(depth=2)
            # Get IDs of groups that user needs to have at the end of update
            new_user_group_ids = []
            for g in module.params.get('groups'):
                group_id = get_resource_id(module, all_groups, g)
                new_user_group_ids.append(group_id)

            # Delete groups user not supposed to be in at end of update
            for group_id in old_user_group_ids:
                if group_id not in new_user_group_ids:
                    um_api.um_groups_users_delete(
                        group_id=group_id,
                        user_id=user_response.id
                    )

            # Post groups that weren't assigned to the user before
            for group_id in new_user_group_ids:
                if group_id not in old_user_group_ids:
                    response = um_api.um_groups_users_post_with_http_info(
                        group_id=group_id,
                        user=User(id=user_response.id)
                    )
                    (user_response, _, headers) = response
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            # update to reflect new group changes
            user_response = um_api.um_users_find_by_id(user_response.id, depth=2)

        return user_response
    except ApiException as e:
        module.fail_json(msg="failed to update the user: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    um_api = ionoscloud.UserManagementApi(client)

    try:
        _, _, headers = um_api.um_users_delete_with_http_info(existing_object.id)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the user: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, client):
    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_name(module),
        [['id'], ['properties', 'email']],
    )

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

    existing_object = get_resource(
        module, object_list, _get_object_identifier(module),
        [['id'], ['properties', 'email']],
    )

    if existing_object is None:
        module.exit_json(changed=False)
        return

    existing_object_id_by_new_name = get_resource_id(
        module, object_list, object_name,
        [['id'], ['properties', 'email']],
    )

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired email ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_identifier(module),
        [['id'], ['properties', 'email']],
    )

    if existing_object is None:
        module.exit_json(changed=False)
        return

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
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
            if state == 'absent':
                module.exit_json(**remove_object(module, api_client))
            elif state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()
