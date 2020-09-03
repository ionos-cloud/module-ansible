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
module: profitbricks_firewall_rule
short_description: Create, update or remove a firewall rule.
description:
     - This module allows you to create, update or remove a firewall rule.
version_added: "2.2"
options:
  datacenter:
    description:
      - The datacenter name or UUID in which to operate.
    required: true
  server:
    description:
      - The server name or UUID.
    required: true
  nic:
    description:
      - The NIC name or UUID.
    required: true
  name:
    description:
      - The name or UUID of the firewall rule.
    required: false
  protocol:
    description:
      - The protocol for the firewall rule.
    choices: [ "TCP", "UDP", "ICMP", "ANY" ]
    required: true
  source_mac:
    description:
      - Only traffic originating from the respective MAC address is allowed. No value allows all source MAC addresses.
    required: false
  source_ip:
    description:
      - Only traffic originating from the respective IPv4 address is allowed. No value allows all source IPs.
    required: false
  target_ip:
    description:
      - In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed.
        No value allows all target IPs.
    required: false
  port_range_start:
    description:
      - Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave value empty to allow all ports.
    required: false
  port_range_end:
    description:
      - Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave value empty to allow all ports.
    required: false
  icmp_type:
    description:
      - Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. No value allows all types.
    required: false
  icmp_code:
    description:
      - Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. No value allows all codes.
    required: false
  api_url:
    description:
      - The ProfitBricks API base URL.
    required: false
    default: null
    version_added: "2.4"
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
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''
# Create a firewall rule
- name: Create SSH firewall rule
  profitbricks_firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow SSH
    protocol: TCP
    source_ip: 0.0.0.0
    port_range_start: 22
    port_range_end: 22
    state: present

- name: Create ping firewall rule
  profitbricks_firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow Ping
    protocol: ICMP
    source_ip: 0.0.0.0
    icmp_type: 8
    icmp_code: 0
    state: present

# Update a firewall rule
- name: Allow SSH access
  profitbricks_firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update

# Remove a firewall rule
- name: Remove public ping firewall rule
  profitbricks_firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: aa6c261b9c
    name: Allow Ping
    state: absent
'''

RETURN = '''
---
id:
  description: UUID of the firewall rule.
  returned: success
  type: string
  sample: be60aa97-d9c7-4c22-bebe-f5df7d6b675d
name:
  description: Name of the firewall rule.
  returned: success
  type: string
  sample: Allow SSH
protocol:
  description: Protocol of the firewall rule.
  returned: success
  type: string
  sample: TCP
source_mac:
  description: MAC address of the firewall rule.
  returned: success
  type: string
  sample: 02:01:97:d7:ed:49
source_ip:
  description: Source IP of the firewall rule.
  returned: success
  type: string
  sample: tcp
target_ip:
  description: Target IP of the firewall rule.
  returned: success
  type: string
  sample: 10.0.0.1
port_range_start:
  description: Start port of the firewall rule.
  returned: success
  type: int
  sample: 80
port_range_end:
  description: End port of the firewall rule.
  returned: success
  type: int
  sample: 80
icmp_type:
  description: ICMP type of the firewall rule.
  returned: success
  type: int
  sample: 8
icmp_code:
  description: ICMP code of the firewall rule.
  returned: success
  type: int
  sample: 0
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import FirewallRule
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

PROTOCOLS = ['TCP',
             'UDP',
             'ICMP',
             'ANY']


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


def create_firewall_rule(module, client):
    """
    Creates a firewall rule.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The firewall rule instance being created
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    nic = module.params.get('nic')
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    source_mac = module.params.get('source_mac')
    source_ip = module.params.get('source_ip')
    target_ip = module.params.get('target_ip')
    port_range_start = module.params.get('port_range_start')
    port_range_end = module.params.get('port_range_end')
    icmp_type = module.params.get('icmp_type')
    icmp_code = module.params.get('icmp_code')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for server
    server_list = client.list_servers(datacenter_id)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = client.list_nics(datacenter_id, server_id)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    fw_list = client.get_firewall_rules(datacenter_id, server_id, nic_id)
    f = None
    for fw in fw_list['items']:
        if name == fw['properties']['name']:
            f = fw
            break

    should_change = f is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'firewall_rule': f
        }

    try:
        client.update_nic(datacenter_id, server_id, nic_id,
                          firewall_active=True)
    except Exception as e:
        module.fail_json(msg='Unable to activate the NIC firewall.' % to_native(e))

    f = FirewallRule(
        name=name,
        protocol=protocol,
        source_mac=source_mac,
        source_ip=source_ip,
        target_ip=target_ip,
        port_range_start=port_range_start,
        port_range_end=port_range_end,
        icmp_type=icmp_type,
        icmp_code=icmp_code
    )

    try:
        firewall_rule_response = client.create_firewall_rule(
            datacenter_id, server_id, nic_id, f
        )

        if wait:
            _wait_for_completion(client, firewall_rule_response,
                                 wait_timeout, "create_firewall_rule")
        return {
            'changed': True,
            'firewall_rule': firewall_rule_response
        }

    except Exception as e:
        module.fail_json(msg="failed to create the firewall rule: %s" % to_native(e))


def update_firewall_rule(module, client):
    """
    Updates a firewall rule.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The firewall rule instance being updated
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    nic = module.params.get('nic')
    name = module.params.get('name')
    source_mac = module.params.get('source_mac')
    source_ip = module.params.get('source_ip')
    target_ip = module.params.get('target_ip')
    port_range_start = module.params.get('port_range_start')
    port_range_end = module.params.get('port_range_end')
    icmp_type = module.params.get('icmp_type')
    icmp_code = module.params.get('icmp_code')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for server
    server_list = client.list_servers(datacenter_id)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = client.list_nics(datacenter_id, server_id)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    # Locate UUID for firewall rule
    fw_list = client.get_firewall_rules(datacenter_id, server_id, nic_id)
    fw_id = _get_resource_id(fw_list, name, module, "Firewall rule")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        firewall_rule_response = client.update_firewall_rule(
            datacenter_id,
            server_id,
            nic_id,
            fw_id,
            source_mac=source_mac,
            source_ip=source_ip,
            target_ip=target_ip,
            port_range_start=port_range_start,
            port_range_end=port_range_end,
            icmp_type=icmp_type,
            icmp_code=icmp_code
        )

        if wait:
            _wait_for_completion(client, firewall_rule_response,
                                 wait_timeout, "update_firewall_rule")
        return {
            'changed': True,
            'firewall_rule': firewall_rule_response
        }

    except Exception as e:
        module.fail_json(msg="failed to update the firewall rule: %s" % to_native(e))


def delete_firewall_rule(module, client):
    """
    Removes a firewall rule

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the firewall rule was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    nic = module.params.get('nic')
    name = module.params.get('name')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Datacenter")

    # Locate UUID for server
    server_list = client.list_servers(datacenter_id)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = client.list_nics(datacenter_id, server_id)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    # Locate UUID for firewall rule
    firewall_rule_list = client.get_firewall_rules(datacenter_id, server_id, nic_id)
    firewall_rule_id = _get_resource_id(firewall_rule_list, name, module, "Firewall rule")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        firewall_rule_response = client.delete_firewall_rule(
            datacenter_id, server_id, nic_id, firewall_rule_id
        )
        return firewall_rule_response
    except Exception as e:
        module.fail_json(msg="failed to remove the firewall rule: %s" % to_native(e))


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
            server=dict(type='str', required=True),
            nic=dict(type='str', required=True),
            name=dict(type='str', required=True),
            protocol=dict(type='str', choices=PROTOCOLS, required=False),
            source_mac=dict(type='str', default=None),
            source_ip=dict(type='str', default=None),
            target_ip=dict(type='str', default=None),
            port_range_start=dict(type='int', default=None),
            port_range_end=dict(type='int', default=None),
            icmp_type=dict(type='int', default=None),
            icmp_code=dict(type='int', default=None),
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
            (changed) = delete_firewall_rule(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set firewall rule state: %s' % to_native(e))

    elif state == 'present':
        try:
            (firewall_rule_dict) = create_firewall_rule(module, ionosenterprise)
            module.exit_json(**firewall_rule_dict)
        except Exception as e:
            module.fail_json(msg='failed to set firewall rules state: %s' % to_native(e))

    elif state == 'update':
        try:
            (firewall_rule_dict) = update_firewall_rule(module, ionosenterprise)
            module.exit_json(**firewall_rule_dict)
        except Exception as e:
            module.fail_json(msg='failed to update firewall rule: %s' % to_native(e))


if __name__ == '__main__':
    main()
