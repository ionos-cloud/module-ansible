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
  password:
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
  subscription_user:
    description:
      - The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable.
    required: false
  subscription_password:
    description:
      - The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable.
    required: false
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
    choices: ["present", "absent"]

requirements:
    - "python >= 2.6"
    - "profitbricks >= 4.1.0"
'''

EXAMPLES = '''
# Create a user
- name: Create user
  profitbricks_user:
    firstname: John
    lastname: Doe
    email: john.doe@example.com
    password: secretpassword123
    administrator: true
    groups:
      - Developers
      - Testers
    state: present

# Update a user
- name: Update user
  profitbricks_user:
    firstname: John II
    lastname: Doe
    email: john.doe@example.com
    administrator: false
    force_sec_auth: false
    groups: []
    state: present

# Remove a user
- name: Remove user
  profitbricks_user:
    email: john.doe@example.com
    state: absent
'''

import os
import time

HAS_PB_SDK = True

try:
    from profitbricks import __version__ as sdk_version
    from profitbricks.client import ProfitBricksService, User
except ImportError:
    HAS_PB_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


def _wait_for_completion(profitbricks, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = profitbricks.get_request(
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


def create_update_user(module, profitbricks):
    """
    Creates or updates a user.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        The user instance
    """
    firstname = module.params.get('firstname')
    lastname = module.params.get('lastname')
    email = module.params.get('email')
    password = module.params.get('password')
    administrator = module.params.get('administrator')
    force_sec_auth = module.params.get('force_sec_auth')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    try:
        user = None
        for resource in profitbricks.list_users()['items']:
            if email in (resource['properties']['email'], resource['id']):
                user = resource
                break

        if user:
            if not firstname:
                firstname = user['properties']['firstname']
            if not lastname:
                lastname = user['properties']['lastname']
            if administrator is None:
                administrator = user['properties']['administrator']
            if force_sec_auth is None:
                force_sec_auth = user['properties']['forceSecAuth']

            user_response = profitbricks.update_user(
                user_id=user['id'],
                firstname=firstname,
                lastname=lastname,
                email=email,
                administrator=administrator,
                force_sec_auth=force_sec_auth
            )
        else:
            if not firstname:
                module.fail_json(msg='firstname parameter is required')
            if not lastname:
                module.fail_json(msg='lastname parameter is required')
            if not password:
                module.fail_json(msg='password parameter is required')

            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password,
                administrator=administrator or False,
                force_sec_auth=force_sec_auth or False
            )
            user_response = profitbricks.create_user(user)

        if wait:
            _wait_for_completion(profitbricks, user_response, wait_timeout, "create_update_user")

        if module.params.get('groups') is not None:
            user = profitbricks.get_user(user_id=user_response['id'], depth=2)
            old_ug = []
            for g in user['entities']['groups']['items']:
                old_ug.append(g['id'])

            all_groups = profitbricks.list_groups()
            new_ug = []
            for g in module.params.get('groups'):
                group_id = _get_resource_id(all_groups, g)
                new_ug.append(group_id)

            for group_id in old_ug:
                if group_id not in new_ug:
                    profitbricks.remove_group_user(
                        group_id=group_id,
                        user_id=user['id']
                    )

            for group_id in new_ug:
                if group_id not in old_ug:
                    user_response = profitbricks.add_group_user(
                        group_id=group_id,
                        user_id=user['id']
                    )
                    _wait_for_completion(profitbricks, user_response, wait_timeout, "add_group_user")

        return {
            'failed': False,
            'changed': True,
            'user': user_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create or update the user: %s" % to_native(e))


def delete_user(module, profitbricks):
    """
    Removes a user

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the user was removed, false otherwise
    """
    email = module.params.get('email')

    # Locate UUID for the user
    user_list = profitbricks.list_users()
    user_id = _get_user_id(user_list, email)

    try:
        user_response = profitbricks.delete_user(user_id)
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


def _get_resource_id(resource_list, identity):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['name'], resource['id']):
            return resource['id']
    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            firstname=dict(type='str'),
            lastname=dict(type='str'),
            email=dict(type='str', required=True),
            password=dict(type='str', default=None, no_log=True),
            administrator=dict(type='bool', default=None),
            force_sec_auth=dict(type='bool', default=None),
            groups=dict(type='list', default=None),
            subscription_user=dict(type='str', default=os.environ.get('PROFITBRICKS_USERNAME')),
            subscription_password=dict(type='str', default=os.environ.get('PROFITBRICKS_PASSWORD'), no_log=True),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        )
    )

    if not HAS_PB_SDK:
        module.fail_json(msg='profitbricks required for this module')

    if not module.params.get('subscription_user'):
        module.fail_json(msg='subscription_user parameter or ' +
                             'PROFITBRICKS_USERNAME environment variable is required.')
    if not module.params.get('subscription_password'):
        module.fail_json(msg='subscription_password parameter or ' +
                             'PROFITBRICKS_PASSWORD environment variable is required.')

    subscription_user = module.params.get('subscription_user')
    subscription_password = module.params.get('subscription_password')

    profitbricks = ProfitBricksService(
        username=subscription_user,
        password=subscription_password)

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    profitbricks.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'absent':
        try:
            (changed) = delete_user(module, profitbricks)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))

    elif state == 'present':
        try:
            (user_dict) = create_update_user(module, profitbricks)
            module.exit_json(**user_dict)
        except Exception as e:
            module.fail_json(msg='failed to set user state: %s' % to_native(e))


if __name__ == '__main__':
    main()
