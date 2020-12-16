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
module: group
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
      - The Ionos Cloud API base URL.
    required: false
    default: null
  username:
    description:
      - The Ionos Cloud username. Overrides the IONOS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The Ionos Cloud password. Overrides the IONOS_PASSWORD environment variable.
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
# Create a group
- name: Create group
  group:
    name: guests
    create_datacenter: true
    create_snapshot: true
    reserve_ip: false
    access_activity_log: false
    state: present

# Update a group
- name: Update group
  group:
    name: guests
    create_datacenter: false
    users:
      - john.smith@test.com
    state: update

# Remove a group
- name: Remove group
  group:
    name: guests
    state: absent
'''

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, UserProperties, Group, GroupProperties
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


def create_group(module, client):
    """
    Creates a group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

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
    create_pcc = module.params.get('create_pcc')
    s3_privilege = module.params.get('s3_privilege')
    create_backup_unit = module.params.get('create_backup_unit')
    create_internet_access = module.params.get('create_internet_access')
    create_k8s_cluster = module.params.get('create_k8s_cluster')
    local_vars_configuration = module.params.get('local_vars_configuration')

    user_management_server = ionoscloud.UserManagementApi(client)

    group = None
    groups = user_management_server.um_groups_get(depth=2)
    for g in groups.items:
        if name == g.properties.name:
            group = g
            break

    should_change = group is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'group': group.to_dict()
        }

    try:
        group_properties = GroupProperties(name=name,
                                           create_data_center=create_datacenter or False,
                                           create_snapshot=create_snapshot or False,
                                           reserve_ip=reserve_ip or False,
                                           access_activity_log=access_activity_log or False,
                                           create_pcc=create_pcc or False,
                                           s3_privilege=s3_privilege or False,
                                           create_backup_unit=create_backup_unit or False,
                                           create_internet_access=create_internet_access or False,
                                           create_k8s_cluster=create_k8s_cluster or False,
                                           local_vars_configuration=local_vars_configuration or False)

        group = Group(properties=group_properties)
        response = user_management_server.um_groups_post_with_http_info(group)
        (group_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'group': group_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the group: %s" % to_native(e))


def update_group(module, client):
    """
    Updates a group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

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

    user_management_server = ionoscloud.UserManagementApi(client)

    try:
        group = None
        group_id = None
        groups = user_management_server.um_groups_get(depth=2)
        for g in groups.items:
            if name == g.properties.name:
                group = g
                group_id = g.id
                break

        if group:
            if module.check_mode:
                module.exit_json(changed=True)

            if create_datacenter is None:
                create_datacenter = group.properties.create_data_center
            if create_snapshot is None:
                create_snapshot = group.properties.create_snapshot
            if reserve_ip is None:
                reserve_ip = group.properties.reserve_ip
            if access_activity_log is None:
                access_activity_log = group.properties.access_activity_log

            group_properties = GroupProperties(name=name,
                                               create_data_center=create_datacenter,
                                               create_snapshot=create_snapshot,
                                               reserve_ip=reserve_ip,
                                               access_activity_log=access_activity_log)

            group = Group(properties=group_properties)

            response = user_management_server.um_groups_put_with_http_info(group_id=group_id, group=group)
            (group_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            if module.params.get('users') is not None:

                group = user_management_server.um_groups_find_by_id(group_id=group_response.id, depth=2)
                old_gu = []
                for u in group.entities.users.items:
                    old_gu.append(u.id)

                all_users = user_management_server.um_users_get(depth=2)
                new_gu = []

                for u in module.params.get('users'):
                    user_id = _get_user_id(all_users, u)
                    new_gu.append(user_id)

                for user_id in old_gu:
                    if user_id not in new_gu:
                        user_management_server.um_groups_users_delete(
                            group_id=group.id,
                            user_id=user_id
                        )

                for user_id in new_gu:
                    if user_id not in old_gu:
                        response = user_management_server.um_groups_users_post_with_http_info(
                            group_id=group.id,
                            user=User(id=user_id)
                        )
                        (user_response, _, headers) = response
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                'group': group_response.to_dict()
            }
        else:
            module.fail_json(msg='Group \'%s\' not found.' % str(name))

    except Exception as e:
        module.fail_json(msg="failed to update the group: %s" % to_native(e))


def delete_group(module, client):
    """
    Removes a group

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the group was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for the group
    group_list = client.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, name, module, "Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        client.um_groups_delete(group_id=group_id)
        return {
            'action': 'delete',
            'changed': False,
            'id': group_id
        }

    except Exception as e:
        module.fail_json(msg="failed to remove the group: %s" % to_native(e))


def _get_user_id(resource_list, identity):
    """
    Return the UUID of a user regardless of whether the email or UUID is passed.
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
                (result) = delete_group(module, api_instance)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set group state: %s' % to_native(e))

        elif state == 'present':
            try:
                (group_dict) = create_group(module, api_client)
                module.exit_json(**group_dict)
            except Exception as e:
                module.fail_json(msg='failed to set group state: %s' % to_native(e))

        elif state == 'update':
            try:
                (group_dict) = update_group(module, api_client)
                module.exit_json(**group_dict)
            except Exception as e:
                module.fail_json(msg='failed to update group: %s' % to_native(e))


if __name__ == '__main__':
    main()
