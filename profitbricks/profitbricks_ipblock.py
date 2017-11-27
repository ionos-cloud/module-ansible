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
module: profitbricks_ipblock
short_description: Create or remove an IPBlock.
description:
     - This module allows you to create or remove an IPBlock.
version_added: "2.4"
options:
  name:
    description:
      - The name or ID of the IPBlock.
    required: false
  location:
    description:
      - The datacenter location.
    required: false
    default: us/las
    choices: [ "us/las", "us/ewr", "de/fra", "de/fkb" ]
  size:
    description:
      - The number of IP addresses to allocate in the IPBlock.
    required: false
    default: 1
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
    - "profitbricks >= 4.0.0"
'''

EXAMPLES = '''
# Create an IPBlock
- name: Create IPBlock
  profitbricks_ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present

# Remove an IPBlock
- name: Remove IPBlock
  profitbricks_ipblock:
    name: staging
    state: absent
'''

import os
import time

HAS_PB_SDK = True

try:
    from profitbricks import __version__ as sdk_version
    from profitbricks.client import ProfitBricksService, IPBlock
except ImportError:
    HAS_PB_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


LOCATIONS = ['us/las',
             'us/ewr',
             'de/fra',
             'de/fkb']


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


def reserve_ipblock(module, profitbricks):
    """
    Creates an IPBlock.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        The IPBlock instance
    """
    name = module.params.get('name')
    location = module.params.get('location')
    size = module.params.get('size')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    try:
        ipblock = IPBlock(
            name=name,
            location=location,
            size=size
        )

        ipblock_response = profitbricks.reserve_ipblock(ipblock)

        if wait:
            _wait_for_completion(profitbricks, ipblock_response,
                                 wait_timeout, "reserve_ipblock")

        return {
            'failed': False,
            'changed': True,
            'ipblock': ipblock_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the IPBlock: %s" % to_native(e))


def delete_ipblock(module, profitbricks):
    """
    Removes an IPBlock

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the IPBlock was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for the IPBlock
    ipblock_list = profitbricks.list_ipblocks()
    id = _get_resource_id(ipblock_list, name)

    try:
        ipblock_response = profitbricks.delete_ipblock(id)
        return ipblock_response
    except Exception as e:
        module.fail_json(msg="failed to remove the IPBlock: %s" % to_native(e))


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
            name=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            size=dict(type='int', default=1),
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
            (changed) = delete_ipblock(module, profitbricks)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set IPBlock state: %s' % to_native(e))

    elif state == 'present':
        try:
            (ipblock_dict) = reserve_ipblock(module, profitbricks)
            module.exit_json(**ipblock_dict)
        except Exception as e:
            module.fail_json(msg='failed to set IPBlocks state: %s' % to_native(e))


if __name__ == '__main__':
    main()
