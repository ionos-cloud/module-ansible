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
module: firewall_rule
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
      - The Ionos API base URL.
    required: false
    default: null
    version_added: "2.4"
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
  token:
    description:
      - The Ionos token. Overrides the IONOS_TOKEN environment variable.
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
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''
# Create a firewall rule
- name: Create SSH firewall rule
  firewall_rule:
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
  firewall_rule:
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
  firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update

# Remove a firewall rule
- name: Remove public ping firewall rule
  firewall_rule:
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

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import FirewallRule, FirewallruleProperties, Nic, NicProperties
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

PROTOCOLS = ['TCP',
             'UDP',
             'ICMP',
             'ANY']


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_firewall_rule(module, client):
    """
    Creates a firewall rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

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

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    server_server = ionoscloud.ServerApi(api_client=client)
    nic_server = ionoscloud.NicApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for server
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=2)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    fw_list = nic_server.datacenters_servers_nics_firewallrules_get(datacenter_id=datacenter_id, server_id=server_id,
                                                                    nic_id=nic_id, depth=2)
    f = None
    for fw in fw_list.items:
        if name == fw.properties.name:
            f = fw
            break

    should_change = f is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'failed': False,
            'action': 'create',
            'firewall_rule': f.to_dict()
        }

    try:

        current_nic = nic_server.datacenters_servers_nics_find_by_id(datacenter_id=datacenter_id, server_id=server_id,
                                                                     nic_id=nic_id)
        nic = Nic(properties=NicProperties(firewall_active=True, lan=current_nic.properties.lan))
        nic_server.datacenters_servers_nics_put(datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id,
                                                nic=nic)

    except Exception as e:
        module.fail_json(msg='Unable to activate the NIC firewall.' % to_native(e))

    firewall_properties = FirewallruleProperties(name=name, protocol=protocol, source_mac=source_mac,
                                                 source_ip=source_ip,
                                                 target_ip=target_ip, icmp_code=icmp_code, icmp_type=icmp_type,
                                                 port_range_start=port_range_start,
                                                 port_range_end=port_range_end)

    firewall_rule = FirewallRule(properties=firewall_properties)

    try:
        response = nic_server.datacenters_servers_nics_firewallrules_post_with_http_info(datacenter_id=datacenter_id,
                                                                                         server_id=server_id,
                                                                                         nic_id=nic_id,
                                                                                         firewallrule=firewall_rule)
        (firewall_rule_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'firewall_rule': firewall_rule_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the firewall rule: %s" % to_native(e))


def update_firewall_rule(module, client):
    """
    Updates a firewall rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

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

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    server_server = ionoscloud.ServerApi(api_client=client)
    nic_server = ionoscloud.NicApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for server
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=2)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    # Locate UUID for firewall rule
    fw_list = nic_server.datacenters_servers_nics_firewallrules_get(datacenter_id=datacenter_id, server_id=server_id,
                                                                    nic_id=nic_id, depth=2)
    fw_id = _get_resource_id(fw_list, name, module, "Firewall rule")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        firewall_rule_properties = FirewallruleProperties(source_mac=source_mac,
                                                          source_ip=source_ip,
                                                          target_ip=target_ip)

        if port_range_start or port_range_end:
            firewall_rule_properties.port_range_start = port_range_start
            firewall_rule_properties.port_range_end = port_range_end

        if icmp_type or icmp_code:
            firewall_rule_properties.icmp_code = icmp_code
            firewall_rule_properties.icmp_type = icmp_type

        response = nic_server.datacenters_servers_nics_firewallrules_patch_with_http_info(datacenter_id=datacenter_id,
                                                                                          server_id=server_id,
                                                                                          nic_id=nic_id,
                                                                                          firewallrule_id=fw_id,
                                                                                          firewallrule=firewall_rule_properties)

        (firewall_rule_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'firewall_rule': firewall_rule_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the firewall rule: %s" % to_native(e))


def delete_firewall_rule(module, client):
    """
    Removes a firewall rule

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the firewall rule was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    nic = module.params.get('nic')
    name = module.params.get('name')
    datacenter_server = ionoscloud.DataCenterApi(client)
    server_server = ionoscloud.ServerApi(client)
    nic_server = ionoscloud.NicApi(client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Datacenter")

    # Locate UUID for server
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=2)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    # Locate UUID for firewall rule
    firewall_rule_list = nic_server.datacenters_servers_nics_firewallrules_get(datacenter_id=datacenter_id,
                                                                               server_id=server_id, nic_id=nic_id,
                                                                               depth=2)
    firewall_rule_id = _get_resource(firewall_rule_list, name)
    if not firewall_rule_id:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        nic_server.datacenters_servers_nics_firewallrules_delete(datacenter_id=datacenter_id,
                                                                 server_id=server_id,
                                                                 nic_id=nic_id,
                                                                 firewallrule_id=firewall_rule_id)

        return {
            'changed': True,
            'action': 'delete',
            'id': firewall_rule_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the firewall rule: %s" % to_native(e))


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
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
            token=dict(
                type='str',
                required=True,
                fallback=(env_fallback, ['IONOS_TOKEN']),
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
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

    state = module.params.get('state')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
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
                (result) = delete_firewall_rule(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set firewall rule state: %s' % to_native(e))

        elif state == 'present':
            try:
                (firewall_rule_dict) = create_firewall_rule(module, api_client)
                module.exit_json(**firewall_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to set firewall rules state: %s' % to_native(e))

        elif state == 'update':
            try:
                (firewall_rule_dict) = update_firewall_rule(module, api_client)
                module.exit_json(**firewall_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to update firewall rule: %s' % to_native(e))


if __name__ == '__main__':
    main()
