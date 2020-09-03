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
module: profitbricks_group
short_description: Create, update or remove a group.
description:
     - This module allows you to create, update or remove a group.
version_added: "2.4"
options:
  name:
    description:
      - The name or ID of the group.
    required: true
  create_datacenter:
    description:
      - Boolean value indicating if the group is allowed to create virtual data centers.
    required: false
    default: None
  create_snapshot:
    description:
      - Boolean value indicating if the group is allowed to create snapshots.
    required: false
    default: None
  reserve_ip:
    description:
      - Boolean value indicating if the group is allowed to reserve IP addresses.
    required: false
    default: None
  access_activity_log:
    description:
      - Boolean value indicating if the group is allowed to access the activity log.
    required: false
    default: None
  users:
    description:
      - A list of (non-administrator) user IDs or emails to associate with the group.
        Set to empty list ([]) to remove all users from the group.
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
# Create a group
- name: Create group
  profitbricks_group:
    name: guests
    create_datacenter: true
    create_snapshot: true
    reserve_ip: false
    access_activity_log: false
    state: present

# Update a group
- name: Update group
  profitbricks_group:
    name: guests
    create_datacenter: false
    users:
      - john.smith@test.com
    state: update

# Remove a group
- name: Remove group
  profitbricks_group:
    name: guests
    state: absent
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import Group
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


def create_group(module, client):
    """
    Creates a group.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The group instance
    """
    name = module.params.get('name')
    create_datacenter = module.params.get('create_datacenter')
    create_snapshot = module.params.get('create_snapshot')
    reserve_ip = module.params.get('reserve_ip')
    access_activity_log = module.params.get('access_activity_log')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    group = None
    for g in client.list_groups()['items']:
        if name == g['properties']['name']:
            group = g
            break

    should_change = group is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'group': group
        }

    try:
        group = Group(
            name=name,
            create_datacenter=create_datacenter or False,
            create_snapshot=create_snapshot or False,
            reserve_ip=reserve_ip or False,
            access_activity_log=access_activity_log or False
        )
        group_response = client.create_group(group)

        if wait:
            _wait_for_completion(client, group_response,
                                 wait_timeout, "create_group")

        return {
            'failed': False,
            'changed': True,
            'group': group_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the group: %s" % to_native(e))


def update_group(module, client):
    """
    Updates a group.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The group instance
    """
    name = module.params.get('name')
    create_datacenter = module.params.get('create_datacenter')
    create_snapshot = module.params.get('create_snapshot')
    reserve_ip = module.params.get('reserve_ip')
    access_activity_log = module.params.get('access_activity_log')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    try:
        group = None
        for resource in client.list_groups()['items']:
            if name in (resource['properties']['name'], resource['id']):
                group = resource
                break

        if group:
            if module.check_mode:
                module.exit_json(changed=True)

            if create_datacenter is None:
                create_datacenter = group['properties']['createDataCenter']
            if create_snapshot is None:
                create_snapshot = group['properties']['createSnapshot']
            if reserve_ip is None:
                reserve_ip = group['properties']['reserveIp']
            if access_activity_log is None:
                access_activity_log = group['properties']['accessActivityLog']

            group_response = client.update_group(
                group_id=group['id'],
                name=name,
                create_datacenter=create_datacenter,
                create_snapshot=create_snapshot,
                reserve_ip=reserve_ip,
                access_activity_log=access_activity_log
            )
        else:
            module.fail_json(msg='Group \'%s\' not found.' % str(name))

        if wait:
            _wait_for_completion(client, group_response,
                                 wait_timeout, "update_group")

        if module.params.get('users') is not None:
            group = client.get_group(group_id=group_response['id'], depth=2)
            old_gu = []
            for u in group['entities']['users']['items']:
                old_gu.append(u['id'])

            all_users = client.list_users()
            new_gu = []
            for u in module.params.get('users'):
                user_id = _get_user_id(all_users, u)
                new_gu.append(user_id)

            for user_id in old_gu:
                if user_id not in new_gu:
                    client.remove_group_user(
                        group_id=group['id'],
                        user_id=user_id
                    )

            for user_id in new_gu:
                if user_id not in old_gu:
                    user_response = client.add_group_user(
                        group_id=group['id'],
                        user_id=user_id
                    )
                    _wait_for_completion(client, user_response, wait_timeout, "add_group_user")

        return {
            'failed': False,
            'changed': True,
            'group': group_response
        }

    except Exception as e:
        module.fail_json(msg="failed to update the group: %s" % to_native(e))


def delete_group(module, client):
    """
    Removes a group

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the group was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for the group
    group_list = client.list_groups()
    group_id = _get_resource_id(group_list, name, module, "Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        group_response = client.delete_group(group_id)
        return group_response
    except Exception as e:
        module.fail_json(msg="failed to remove the group: %s" % to_native(e))


def _get_user_id(resource_list, identity):
    """
    Return the UUID of a user regardless of whether the email or UUID is passed.
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
            name=dict(type='str', required=True),
            create_datacenter=dict(type='bool', default=None),
            create_snapshot=dict(type='bool', default=None),
            reserve_ip=dict(type='bool', default=None),
            access_activity_log=dict(type='bool', default=None),
            users=dict(type='list', default=None),
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
            (changed) = delete_group(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set group state: %s' % to_native(e))

    elif state == 'present':
        try:
            (group_dict) = create_group(module, ionosenterprise)
            module.exit_json(**group_dict)
        except Exception as e:
            module.fail_json(msg='failed to set group state: %s' % to_native(e))

    elif state == 'update':
        try:
            (group_dict) = update_group(module, ionosenterprise)
            module.exit_json(**group_dict)
        except Exception as e:
            module.fail_json(msg='failed to update group: %s' % to_native(e))


if __name__ == '__main__':
    main()
