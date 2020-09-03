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
module: profitbricks_lan
short_description: Create, update or remove a LAN.
description:
     - This module allows you to create or remove a LAN.
version_added: "2.4"
options:
  datacenter:
    description:
      - The datacenter name or UUID in which to operate.
    required: true
  name:
    description:
      - The name or ID of the LAN.
    required: false
  public:
    description:
      - If true, the LAN will have public Internet access.
    required: false
    default: true
  ip_failover:
    description:
      - The IP failover group.
    required: false
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
# Create a LAN
- name: Create private LAN
  profitbricks_lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present

# Update a LAN
- name: Update LAN
  profitbricks_lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update

# Remove a LAN
- name: Remove LAN
  profitbricks_lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    state: absent
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import LAN
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


def create_lan(module, client):
    """
    Creates a LAN.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The LAN instance
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    public = module.params.get('public')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    lan_list = client.list_lans(datacenter_id)
    lan = None
    for i in lan_list['items']:
        if name == i['properties']['name']:
            lan = i
            break

    should_change = lan is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'lan': lan
        }

    try:
        lan = LAN(
            name=name,
            public=public
        )

        lan_response = client.create_lan(datacenter_id, lan)

        if wait:
            _wait_for_completion(client, lan_response,
                                 wait_timeout, "create_lan")

        return {
            'failed': False,
            'changed': True,
            'lan': lan_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the LAN: %s" % to_native(e))


def update_lan(module, client):
    """
    Updates a LAN.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The LAN instance
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    public = module.params.get('public')
    ip_failover = module.params.get('ip_failover')
    pcc_id = module.params.get('pcc_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Prefetch a list of LANs.
    lan_list = client.list_lans(datacenter_id)
    lan_id = _get_resource_id(lan_list, name, module, "LAN")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        failover_group = []
        for ip, nic_uuid in ip_failover.items():
            item = {
                'ip': ip,
                'nicUuid': nic_uuid
            }
            failover_group.append(item)

        lan_response = client.update_lan(
            datacenter_id, lan_id=lan_id, public=public, ip_failover=failover_group, pcc=pcc_id)

        if wait:
            _wait_for_completion(client, lan_response,
                                 wait_timeout, "update_lan")

        return {
            'failed': False,
            'changed': True,
            'lan': lan_response
        }

    except Exception as e:
        module.fail_json(msg="failed to update the LAN: %s" % to_native(e))


def delete_lan(module, client):
    """
    Removes a LAN

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the LAN was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate ID for LAN
    lan_list = client.list_lans(datacenter_id)
    lan_id = _get_resource_id(lan_list, name, module, "LAN")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        lan_response = client.delete_lan(datacenter_id, lan_id)
        return lan_response
    except Exception as e:
        module.fail_json(msg="failed to remove the LAN: %s" % to_native(e))


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
            datacenter=dict(type='str', required=True),
            name=dict(type='str'),
            public=dict(type='bool', default=True),
            ip_failover=dict(type='dict', default=dict()),
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
            (changed) = delete_lan(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set LAN state: %s' % to_native(e))

    elif state == 'present':
        try:
            (lan_dict) = create_lan(module, ionosenterprise)
            module.exit_json(**lan_dict)
        except Exception as e:
            module.fail_json(msg='failed to set LANs state: %s' % to_native(e))

    elif state == 'update':
        try:
            (lan_dict) = update_lan(module, ionosenterprise)
            module.exit_json(**lan_dict)
        except Exception as e:
            module.fail_json(msg='failed to update LAN: %s' % to_native(e))


if __name__ == '__main__':
    main()
