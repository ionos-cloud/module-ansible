#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: user
short_description: Create, update or remove a user.
description:
     - This module allows you to create, update or remove a user.
version_added: "2.4"
options:
  firstname:
    description:
      - The user's first name.
    required: true
    default: None
  lastname:
    description:
      - The user's last name.
    required: true
    default: None
  email:
    description:
      - The user's email.
    required: true
    default: None
  user_password:
    description:
      - A password for the user.
    required: true
    default: None
  administrator:
    description:
      - Boolean value indicating if the user has administrative rights.
    required: false
    default: None
  force_sec_auth:
    description:
      - Boolean value indicating if secure (two-factor) authentication should be forced for the user.
    required: false
    default: None
  groups:
    description:
      - A list of group IDs or names where the user (non-administrator) is to be added.
        Set to empty list ([]) to remove the user from all groups.
    required: false
    default: None
  api_url:
    description:
      - The Ionos API base URL.
    required: false
    default: null
  username:
    description:
      - The Ionos username. Overrides the IONOS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
    required: false
    aliases: subscription_password
  wait:
    description:
      - wait for the operation to complete before returning
    required: false
    default: "yes"
    choices: [ "yes", "no" ]
  wait_timeout:
    description:
      - how long before wait gives up, in seconds
    default: 600
  state:
    description:
      - Indicate desired state of the resource
    required: false
    default: "present"
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
'''

EXAMPLES = '''
# Create a user
- name: Create user
  user:
    firstname: John
    lastname: Doe
    email: john.doe@example.com
    user_password: secretpassword123
    administrator: true
    state: present

# Update a user
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

# Remove a user
- name: Remove user
  user:
    email: john.doe@example.com
    state: absent
'''

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, UserProperties
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



def create_user(module, client, api_client):
    """
    Creates a user.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The user instance
    """
    firstname = module.params.get('firstname')
    if not firstname:
        module.fail_json(msg='firstname parameter is required')
    lastname = module.params.get('lastname')
    if not lastname:
        module.fail_json(msg='lastname parameter is required')
    email = module.params.get('email')
    user_password = module.params.get('user_password')
    if not user_password:
        module.fail_json(msg='user_password parameter is required')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    s3_canonical_user_id = module.params.get('s3_canonical_user_id')

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
        user_properties = UserProperties(firstname=firstname, lastname=lastname, email=email,
                                         administrator=administrator or False,
                                         force_sec_auth=force_sec_auth or False,
                                         s3_canonical_user_id=s3_canonical_user_id,
                                         password=user_password)

        user = User(properties=user_properties)
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

            user_properties = UserProperties(firstname=firstname,
                                             lastname=lastname,
                                             email=email,
                                             administrator=administrator or False,
                                             force_sec_auth=force_sec_auth or False)

            new_user = User(properties=user_properties)
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            firstname=dict(type='str'),
            lastname=dict(type='str'),
            email=dict(type='str', required=True),
            user_password=dict(type='str', default=None, no_log=True),
            administrator=dict(type='bool', default=None),
            force_sec_auth=dict(type='bool', default=None),
            groups=dict(type='list', default=None),
            api_url=dict(type='str', default=None),
            sec_auth_active=dict(type='bool', default=False),
            s3_canonical_user_id=dict(type='str'),
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

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        api_instance = ionoscloud.UserManagementApi(api_client)

        if state == 'absent':
            try:
                (result) = delete_user(module, api_instance)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'present':
            try:
                (user_dict) = create_user(module, api_instance, api_client)
                module.exit_json(**user_dict)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'update':
            try:
                (user_dict) = update_user(module, api_instance, api_client)
                module.exit_json(**user_dict)
            except Exception as e:
                module.fail_json(msg='failed to update user: %s' % to_native(e))


if __name__ == '__main__':
    main()
