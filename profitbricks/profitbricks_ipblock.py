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
    choices: [ "us/las", "us/ewr", "de/fra", "de/fkb", "de/txl", "gb/lhr" ]
  size:
    description:
      - The number of IP addresses to allocate in the IPBlock.
    required: false
    default: 1
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
    choices: ["present", "absent"]

requirements:
    - "python >= 2.6"
    - "ionosenterprise >= 5.2.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
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

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import IPBlock
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


LOCATIONS = ['us/las',
             'us/ewr',
             'de/fra',
             'de/fkb',
             'de/txl',
             'gb/lhr'
             ]


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


def reserve_ipblock(module, client):
    """
    Creates an IPBlock.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The IPBlock instance
    """
    name = module.params.get('name')
    location = module.params.get('location')
    size = module.params.get('size')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    ip_list = client.list_ipblocks()
    ip = None
    for i in ip_list['items']:
        if name == i['properties']['name']:
            ip = i
            break

    should_change = ip is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'ipblock': ip
        }

    try:
        ipblock = IPBlock(
            name=name,
            location=location,
            size=size
        )

        ipblock_response = client.reserve_ipblock(ipblock)

        if wait:
            _wait_for_completion(client, ipblock_response,
                                 wait_timeout, "reserve_ipblock")

        return {
            'failed': False,
            'changed': True,
            'ipblock': ipblock_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the IPBlock: %s" % to_native(e))


def delete_ipblock(module, client):
    """
    Removes an IPBlock

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the IPBlock was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for the IPBlock
    ipblock_list = client.list_ipblocks()
    id = _get_resource_id(ipblock_list, name, module, "IP Block")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        ipblock_response = client.delete_ipblock(id)
        return ipblock_response
    except Exception as e:
        module.fail_json(msg="failed to remove the IPBlock: %s" % to_native(e))


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
            name=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            size=dict(type='int', default=1),
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
            (changed) = delete_ipblock(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set IPBlock state: %s' % to_native(e))

    elif state == 'present':
        try:
            (ipblock_dict) = reserve_ipblock(module, ionosenterprise)
            module.exit_json(**ipblock_dict)
        except Exception as e:
            module.fail_json(msg='failed to set IPBlocks state: %s' % to_native(e))


if __name__ == '__main__':
    main()
