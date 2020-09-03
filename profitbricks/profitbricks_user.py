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
module: profitbricks_user
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
      - The ProfitBricks API base URL.
    required: false
    default: null
  username:
    description:
      - The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable.
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
    - "ionosenterprise >= 5.2.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
'''

EXAMPLES = '''
# Create a user
- name: Create user
  profitbricks_user:
    firstname: John
    lastname: Doe
    email: john.doe@example.com
    user_password: secretpassword123
    administrator: true
    state: present

# Update a user
- name: Update user
  profitbricks_user:
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
  profitbricks_user:
    email: john.doe@example.com
    state: absent
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import User
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


def create_user(module, client):
    """
    Creates a user.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

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

    user = None
    for u in client.list_users()['items']:
        if email == u['properties']['email']:
            user = u
            break

    should_change = user is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'user': user
        }

    try:
        user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=user_password,
            administrator=administrator or False,
            force_sec_auth=force_sec_auth or False
        )
        user_response = client.create_user(user)

        if wait:
            _wait_for_completion(client, user_response, wait_timeout, "create_user")

        return {
            'failed': False,
            'changed': True,
            'user': user_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the user: %s" % to_native(e))


def update_user(module, client):
    """
    Updates a user.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

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
        for resource in client.list_users()['items']:
            if email in (resource['properties']['email'], resource['id']):
                user = resource
                break

        if user:
            if module.check_mode:
                module.exit_json(changed=True)

            if not firstname:
                firstname = user['properties']['firstname']
            if not lastname:
                lastname = user['properties']['lastname']
            if administrator is None:
                administrator = user['properties']['administrator']
            if force_sec_auth is None:
                force_sec_auth = user['properties']['forceSecAuth']

            user_response = client.update_user(
                user_id=user['id'],
                firstname=firstname,
                lastname=lastname,
                email=email,
                administrator=administrator,
                force_sec_auth=force_sec_auth
            )
        else:
            module.fail_json(msg='User \'%s\' not found.' % str(email))

        if wait:
            _wait_for_completion(client, user_response, wait_timeout, "update_user")

        if module.params.get('groups') is not None:
            user = client.get_user(user_id=user_response['id'], depth=2)
            old_ug = []
            for g in user['entities']['groups']['items']:
                old_ug.append(g['id'])

            all_groups = client.list_groups()
            new_ug = []
            for g in module.params.get('groups'):
                group_id = _get_resource_id(all_groups, g, module, "Group")
                new_ug.append(group_id)

            for group_id in old_ug:
                if group_id not in new_ug:
                    client.remove_group_user(
                        group_id=group_id,
                        user_id=user['id']
                    )

            for group_id in new_ug:
                if group_id not in old_ug:
                    user_response = client.add_group_user(
                        group_id=group_id,
                        user_id=user['id']
                    )
                    _wait_for_completion(client, user_response, wait_timeout, "add_group_user")

        return {
            'failed': False,
            'changed': True,
            'user': user_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create or update the user: %s" % to_native(e))


def delete_user(module, client):
    """
    Removes a user

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the user was removed, false otherwise
    """
    email = module.params.get('email')

    # Locate UUID for the user
    user_list = client.list_users()
    user_id = _get_user_id(user_list, email)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        user_response = client.delete_user(user_id)
        return user_response
    except Exception as e:
        module.fail_json(msg="failed to remove the user: %s" % to_native(e))


def _get_user_id(resource_list, identity):
    """
    Fetch and return the UUID of a user regardless of whether the email or
    UUID is passed.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['email'], resource['id']):
            return resource['id']
    return None


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['name'], resource['id']):
            return resource['id']

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

    if state == 'absent':
        try:
            (changed) = delete_user(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'present':
        try:
            (user_dict) = create_user(module, ionosenterprise)
            module.exit_json(**user_dict)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'update':
        try:
            (user_dict) = update_user(module, ionosenterprise)
            module.exit_json(**user_dict)
        except Exception as e:
            module.fail_json(msg='failed to update user: %s' % to_native(e))


if __name__ == '__main__':
    main()
