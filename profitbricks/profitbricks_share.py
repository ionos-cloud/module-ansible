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
module: profitbricks_share
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
# Create shares
- name: Create share
  profitbricks_share:
    group: Demo
    edit_privilege: true
    share_privilege: true
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      - ba7efccb-a761-11e7-90a7-525400f64d8d
    state: present

# Update shares
- name: Update shares
  profitbricks_share:
    group: Demo
    edit_privilege: false
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
    state: update

# Remove shares
- name: Remove shares
  profitbricks_share:
    group: Demo
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      - ba7efccb-a761-11e7-90a7-525400f64d8d
    state: absent
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
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


def create_shares(module, client):
    """
    Create shares.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The share instance
    """
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = client.list_groups()
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    share_list = client.list_shares(group_id=group_id)['items']
    for share in share_list:
        if share['id'] in resource_ids:
            resource_ids.remove(share['id'])

    should_change = True

    if not resource_ids:
        should_change = False

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'shares': share_list
        }

    try:
        for uuid in resource_ids:
            share_response = client.add_share(
                group_id=group_id,
                resource_id=uuid,
                edit_privilege=edit_privilege or False,
                share_privilege=share_privilege or False
            )

            if wait:
                _wait_for_completion(client, share_response,
                                     wait_timeout, "create_shares")

        share_list = client.list_shares(group_id=group_id)['items']

        return {
            'failed': False,
            'changed': True,
            'shares': share_list
        }

    except Exception as e:
        module.fail_json(msg="failed to create the shares: %s" % to_native(e))


def update_shares(module, client):
    """
    Update shares.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The share instances
    """
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = client.list_groups()
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        share_list = client.list_shares(group_id=group_id)

        existing = dict()
        for share in share_list['items']:
            existing[share['id']] = share

        responses = []

        for uuid in resource_ids:
            if uuid in existing.keys():
                share = existing[uuid]
                if edit_privilege is None:
                    edit_privilege = share['properties']['editPrivilege']
                if share_privilege is None:
                    share_privilege = share['properties']['sharePrivilege']

                share_response = client.update_share(
                    group_id=group_id,
                    resource_id=uuid,
                    edit_privilege=edit_privilege,
                    share_privilege=share_privilege
                )

            if wait:
                _wait_for_completion(client, share_response,
                                     wait_timeout, "update_shares")
            responses.append(share_response)

        return {
            'failed': False,
            'changed': True,
            'shares': responses
        }

    except Exception as e:
        module.fail_json(msg="failed to update the shares: %s" % to_native(e))


def delete_shares(module, client):
    """
    Remove shares

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the share was removed, false otherwise
    """
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = client.list_groups()
    group_id = _get_resource_id(group_list, group, module, "Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        response = None
        for uuid in module.params.get('resource_ids'):
            response = client.delete_share(group_id=group_id, resource_id=uuid)

        return response
    except Exception as e:
        module.fail_json(msg="failed to remove the shares: %s" % to_native(e))


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
            group=dict(type='str', required=True),
            edit_privilege=dict(type='bool', default=None),
            share_privilege=dict(type='bool', default=None),
            resource_ids=dict(type='list', required=True),
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
            (changed) = delete_shares(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))

    elif state == 'present':
        try:
            (share_dict) = create_shares(module, ionosenterprise)
            module.exit_json(**share_dict)
        except Exception as e:
            module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))

    elif state == 'update':
        try:
            (share_dict) = update_shares(module, ionosenterprise)
            module.exit_json(**share_dict)
        except Exception as e:
            module.fail_json(msg='failed to update share: %s' % to_native(e))


if __name__ == '__main__':
    main()
