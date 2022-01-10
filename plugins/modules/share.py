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
module: share
short_description: Add, update or remove shares.
description:
     - This module allows you to add, update or remove resource shares.
version_added: "2.4"
options:
  group:
    description:
      - The name or ID of the group.
    required: true
  resource_ids:
    description:
      - A list of resource IDs to add, update or remove as shares.
    required: true
  edit_privilege:
    description:
      - Boolean value indicating that the group has permission to edit privileges on the resource.
    required: false
    default: None
  share_privilege:
    description:
      - Boolean value indicating that the group has permission to share the resource.
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
# Create shares
- name: Create share
  share:
    group: Demo
    edit_privilege: true
    share_privilege: true
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      - ba7efccb-a761-11e7-90a7-525400f64d8d
    state: present

# Update shares
- name: Update shares
  share:
    group: Demo
    edit_privilege: false
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
    state: update

# Remove shares
- name: Remove shares
  share:
    group: Demo
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      - ba7efccb-a761-11e7-90a7-525400f64d8d
    state: absent
'''

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import GroupShare, GroupShareProperties
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


def create_shares(module, client):
    """
    Create shares.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The share instance
    """
    user_management_server = ionoscloud.UserManagementApi(api_client=client)
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2).items
    for share in share_list:
        if share.id in resource_ids:
            resource_ids.remove(share.id)

    should_change = True

    if not resource_ids:
        should_change = False

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'shares': [s.to_dict() for s in share_list],
        }

    try:
        for uuid in resource_ids:
            share_properties = GroupShareProperties(edit_privilege=edit_privilege or False,
                                                    share_privilege=share_privilege or False)
            share = GroupShare(properties=share_properties)
            response = user_management_server.um_groups_shares_post_with_http_info(group_id=group_id, resource_id=uuid,
                                                                                   resource=share)
            (share_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2).items

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'shares': [s.to_dict() for s in share_list]
        }

    except Exception as e:
        module.fail_json(msg="failed to create the shares: %s" % to_native(e))


def update_shares(module, client):
    """
    Update shares.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The share instances
    """
    group = module.params.get('group')
    user_management_server = ionoscloud.UserManagementApi(api_client=client)

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2)
        existing = dict()
        for share in share_list.items:
            existing[share.id] = share

        responses = []

        for uuid in resource_ids:
            if uuid in existing.keys():
                share = existing[uuid]
                if edit_privilege is None:
                    edit_privilege = share.properties.edit_privilege
                if share_privilege is None:
                    share_privilege = share.properties.share_privilege

                share_properties = GroupShareProperties(edit_privilege=edit_privilege or False,
                                                        share_privilege=share_privilege or False)
                share = GroupShare(properties=share_properties)

                response = user_management_server.um_groups_shares_put_with_http_info(group_id=group_id,
                                                                                      resource_id=uuid, resource=share)
                (share_response, _, headers) = response
                if wait:
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                'share': [s.to_dict() for s in responses]
            }

    except Exception as e:
        module.fail_json(msg="failed to update the shares: %s" % to_native(e))


def delete_shares(module, client):
    """
    Remove shares

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the share was removed, false otherwise
    """
    group = module.params.get('group')
    user_management_server = ionoscloud.UserManagementApi(api_client=client)

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:

        for uuid in module.params.get('resource_ids'):
            user_management_server.um_groups_shares_delete(group_id=group_id, resource_id=uuid)

        return {
            'action': 'delete',
            'changed': True,
            'id': group_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the shares: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': group_id
        }


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
            group=dict(type='str', required=True),
            edit_privilege=dict(type='bool', default=None),
            share_privilege=dict(type='bool', default=None),
            resource_ids=dict(type='list', required=True),
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

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            try:
                (result) = delete_shares(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))

        elif state == 'present':
            try:
                (share_dict) = create_shares(module, api_client)
                module.exit_json(**share_dict)
            except Exception as e:
                module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))

        elif state == 'update':
            try:
                (share_dict) = update_shares(module, api_client)
                module.exit_json(**share_dict)
            except Exception as e:
                module.fail_json(msg='failed to update share: %s' % to_native(e))


if __name__ == '__main__':
    main()
