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
    state: present

# Remove shares
- name: Remove shares
  profitbricks_share:
    group: Demo
    resource_ids:
      - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      - ba7efccb-a761-11e7-90a7-525400f64d8d
    state: absent
'''

import os
import time

HAS_PB_SDK = True

try:
    from profitbricks import __version__ as sdk_version
    from profitbricks.client import ProfitBricksService
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


def create_update_shares(module, profitbricks):
    """
    Create or update shares.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        The share instance
    """
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = profitbricks.list_groups()
    group_id = _get_resource_id(group_list, group)

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    try:
        share_list = profitbricks.list_shares(group_id=group_id)

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

                share_response = profitbricks.update_share(
                    group_id=group_id,
                    resource_id=uuid,
                    edit_privilege=edit_privilege,
                    share_privilege=share_privilege
                )
            else:
                share_response = profitbricks.add_share(
                    group_id=group_id,
                    resource_id=uuid,
                    edit_privilege=edit_privilege or False,
                    share_privilege=share_privilege or False
                )

            if wait:
                _wait_for_completion(profitbricks, share_response,
                                     wait_timeout, "create_update_shares")
            responses.append(share_response)

        return {
            'failed': False,
            'changed': True,
            'shares': responses
        }

    except Exception as e:
        module.fail_json(msg="failed to create or update the shares: %s" % to_native(e))


def delete_shares(module, profitbricks):
    """
    Remove shares

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the share was removed, false otherwise
    """
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = profitbricks.list_groups()
    group_id = _get_resource_id(group_list, group)

    try:
        response = None
        for uuid in module.params.get('resource_ids'):
            response = profitbricks.delete_share(group_id=group_id, resource_id=uuid)

        return response
    except Exception as e:
        module.fail_json(msg="failed to remove the shares: %s" % to_native(e))


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
            group=dict(type='str', required=True),
            edit_privilege=dict(type='bool', default=None),
            share_privilege=dict(type='bool', default=None),
            resource_ids=dict(type='list', required=True),
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
            (changed) = delete_shares(module, profitbricks)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))

    elif state == 'present':
        try:
            (share_dict) = create_update_shares(module, profitbricks)
            module.exit_json(**share_dict)
        except Exception as e:
            module.fail_json(msg='failed to set state of the shares: %s' % to_native(e))


if __name__ == '__main__':
    main()
