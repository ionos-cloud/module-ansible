#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import re
import time
import yaml


HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import FirewallRule, FirewallruleProperties, Nic, NicProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Firewall Rule'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'server': {
        'description': ['The server name or UUID.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'nic': {
        'description': ['The NIC name or UUID.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'name': {
        'description': ['The name or UUID of the firewall rule.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'protocol': {
        'description': ['The protocol for the firewall rule.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'choices': ['TCP', 'UDP', 'ICMP', 'ANY'],
        'type': 'str',
    },
    'source_mac': {
        'description': ['Only traffic originating from the respective MAC address is allowed. No value allows all source MAC addresses.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'source_ip': {
        'description': ['Only traffic originating from the respective IPv4 address is allowed. No value allows all source IPs.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'target_ip': {
        'description': [
            'In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed.'
            'No value allows all target IPs.',
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'port_range_start': {
        'description': [
            'Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave value empty to allow all ports.',
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'port_range_end': {
        'description': [
            'Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave value empty to allow all ports.',
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_type': {
        'description': ['Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. No value allows all types.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_code': {
        'description': ['Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. No value allows all codes.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}

def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

DOCUMENTATION = '''
---
module: firewall_rule
short_description: Create, update or remove a firewall rule.
description:
     - This module allows you to create, update or remove a firewall rule.
version_added: "2.2"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a firewall rule
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
  ''',
  'update' : '''# Update a firewall rule
- name: Allow SSH access
  firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update
  ''',
  'absent' : '''# Remove a firewall rule
- name: Remove public ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: aa6c261b9c
    name: Allow Ping
    state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)
    firewall_rules_server = ionoscloud.FirewallRulesApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for server
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    server_id = _get_resource_id(server_list, server, module, "Server")

    # Locate UUID for NIC
    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=2)
    nic_id = _get_resource_id(nic_list, nic, module, "NIC")

    fw_list = firewall_rules_server.datacenters_servers_nics_firewallrules_get(datacenter_id, server_id,
                                                                    nic_id, depth=2)
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
        response = firewall_rules_server.datacenters_servers_nics_firewallrules_post_with_http_info(datacenter_id=datacenter_id,
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

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)
    firewall_rules_server = ionoscloud.FirewallRulesApi(api_client=client)

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
    fw_list = firewall_rules_server.datacenters_servers_nics_firewallrules_get(datacenter_id=datacenter_id, server_id=server_id,
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

        response = firewall_rules_server.datacenters_servers_nics_firewallrules_patch_with_http_info(datacenter_id=datacenter_id,
                                                                                          server_id=server_id,
                                                                                          nic_id=nic_id,
                                                                                          firewallrule_id=fw_id,
                                                                                          firewallrule=firewall_rule_properties)

        (firewall_rule_response, _, headers) = response
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

    datacenter_server = ionoscloud.DataCentersApi(client)
    server_server = ionoscloud.ServersApi(client)
    nic_server = ionoscloud.NetworkInterfacesApi(client)
    firewall_rules_server = ionoscloud.FirewallRulesApi(api_client=client)

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
    firewall_rule_list = firewall_rules_server.datacenters_servers_nics_firewallrules_get(datacenter_id=datacenter_id,
                                                                               server_id=server_id, nic_id=nic_id,
                                                                               depth=2)
    firewall_rule_id = _get_resource(firewall_rule_list, name)
    if not firewall_rule_id:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        firewall_rules_server.datacenters_servers_nics_firewallrules_delete(datacenter_id=datacenter_id,
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


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
      arguments[option_name] = {
        'type': option['type'],
      }
      for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
        if option.get(key) is not None:
          arguments[option_name][key] = option.get(key)

      if option.get('env_fallback'):
        arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

      if len(option.get('required', [])) == len(STATES):
        arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')

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

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'absent':
                module.exit_json(**delete_firewall_rule(module, api_client))
            elif state == 'present':
                module.exit_json(**create_firewall_rule(module, api_client))
            elif state == 'update':
                module.exit_json(**update_firewall_rule(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
