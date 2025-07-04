#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible import __version__
import re


HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import FirewallRule, FirewallruleProperties, Nic, NicProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, _get_request_id, get_resource_id, get_paginated
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (
    __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Firewall Rule'
RETURNED_KEY = 'firewall_rule'

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
    'firewall_rule': {
        'description': ['The Firewall Rule name or UUID.'],
        'required': ['update', 'absent'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['The protocol for the rule. Property cannot be modified after it is created (disallowed in update requests).'],
        'required': ['present'],
        'available': ['present', 'update'],
        'choices': ['TCP', 'UDP', 'ICMP', 'ICMPv6', 'GRE', 'VRRP', 'ESP', 'AH', 'ANY'],
        'type': 'str',
    },
    'source_mac': {
        'description': ['Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'source_ip': {
        'description': ['Only traffic originating from the respective IP address (or CIDR block) is allowed. Value null allows traffic from any IP address (according to the selected ipVersion).'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'target_ip': {
        'description': ['If the target NIC has multiple IP addresses, only the traffic directed to the respective IP address (or CIDR block) of the NIC is allowed. Value null allows traffic to any target IP address (according to the selected ipVersion).'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'port_range_start': {
        'description': ['Defines the start range of the allowed port (from 1 to 65535) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'port_range_end': {
        'description': ['Defines the end range of the allowed port (from 1 to 65535) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_type': {
        'description': ['Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen. Value null allows all types.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_code': {
        'description': ['Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen. Value null allows all codes.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'ip_version': {
        'description': [
            'The IP version for this rule. If sourceIp or targetIp are specified, you can omit this '
            'value - the IP version will then be deduced from the IP address(es) used; if you specify '
            'it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp '
            'are specified, this rule allows traffic only for the specified IP version. If neither '
            'sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic.',
        ],
        'available': ['present', 'update'],
        'choices': ['IPv4', 'IPv6'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: firewall_rule
short_description: Create, update or remove a firewall rule.
description:
     - This module allows you to create, update or remove a firewall rule.
version_added: "2.2"
options:
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    datacenter:
        description:
        - The datacenter name or UUID in which to operate.
        required: true
    firewall_rule:
        description:
        - The Firewall Rule name or UUID.
        required: false
    icmp_code:
        description:
        - Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen.
            Value null allows all codes.
        required: false
    icmp_type:
        description:
        - Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen.
            Value null allows all types.
        required: false
    ip_version:
        choices:
        - IPv4
        - IPv6
        description:
        - The IP version for this rule. If sourceIp or targetIp are specified, you can
            omit this value - the IP version will then be deduced from the IP address(es)
            used; if you specify it anyway, it must match the specified IP address(es).
            If neither sourceIp nor targetIp are specified, this rule allows traffic only
            for the specified IP version. If neither sourceIp, targetIp nor ipVersion
            are specified, this rule will only allow IPv4 traffic.
        required: false
    name:
        description:
        - The name of the  resource.
        required: false
    nic:
        description:
        - The NIC name or UUID.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    port_range_end:
        description:
        - Defines the end range of the allowed port (from 1 to 65535) if the protocol
            TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow
            all ports.
        required: false
    port_range_start:
        description:
        - Defines the start range of the allowed port (from 1 to 65535) if protocol TCP
            or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow
            all ports.
        required: false
    protocol:
        choices:
        - TCP
        - UDP
        - ICMP
        - ICMPv6
        - GRE
        - VRRP
        - ESP
        - AH
        - ANY
        description:
        - The protocol for the rule. Property cannot be modified after it is created (disallowed
            in update requests).
        required: false
    server:
        description:
        - The server name or UUID.
        required: true
    source_ip:
        description:
        - Only traffic originating from the respective IP address (or CIDR block) is allowed.
            Value null allows traffic from any IP address (according to the selected ipVersion).
        required: false
    source_mac:
        description:
        - 'Only traffic originating from the respective MAC address is allowed. Valid
            format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address.'
        required: false
    state:
        choices:
        - present
        - absent
        - update
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    target_ip:
        description:
        - If the target NIC has multiple IP addresses, only the traffic directed to the
            respective IP address (or CIDR block) of the NIC is allowed. Value null allows
            traffic to any target IP address (according to the selected ipVersion).
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create a firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  name: SSH
  protocol: ICMPv6
  source_mac: 01:23:45:67:89:00
  ip_version: IPv6
  state: present
''',
    'update': '''
name: Update firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  port_range_start: 22
  port_range_end: 23
  state: update
''',
    'absent': '''
name: Remove firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  wait: true
  wait_timeout: '500'
  state: absent
''',
}

EXAMPLES = """
name: Create a firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  name: SSH
  protocol: ICMPv6
  source_mac: 01:23:45:67:89:00
  ip_version: IPv6
  state: present


name: Update firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  port_range_start: 22
  port_range_end: 23
  state: update


name: Remove firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  wait: true
  wait_timeout: '500'
  state: absent
"""

class FirewallRuleModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('protocol') is not None
            and existing_object.properties.protocol != self.module.params.get('protocol')
            or self.module.params.get('source_mac') is not None
            and existing_object.properties.source_mac != self.module.params.get('source_mac')
            or self.module.params.get('source_ip') is not None
            and existing_object.properties.source_ip != self.module.params.get('source_ip')
            or self.module.params.get('target_ip') is not None
            and existing_object.properties.target_ip != self.module.params.get('target_ip')
            or self.module.params.get('port_range_start') is not None
            and existing_object.properties.port_range_start != self.module.params.get('port_range_start')
            or self.module.params.get('port_range_end') is not None
            and existing_object.properties.port_range_end != self.module.params.get('port_range_end')
            or self.module.params.get('icmp_type') is not None
            and existing_object.properties.icmp_type != self.module.params.get('icmp_type')
            or self.module.params.get('icmp_code') is not None
            and existing_object.properties.icmp_code != self.module.params.get('icmp_code')
            or self.module.params.get('ip_version') is not None
            and existing_object.properties.ip_version != self.module.params.get('ip_version')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter = self.module.params.get('datacenter')
        server = self.module.params.get('server')
        nic = self.module.params.get('nic')
        datacenter_api = ionoscloud.DataCentersApi(api_client=client)
        server_api = ionoscloud.ServersApi(api_client=client)
        nic_api = ionoscloud.NetworkInterfacesApi(api_client=client)
        firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

        # Locate UUID for virtual datacenter
        datacenter_list = get_paginated(datacenter_api.datacenters_get)
        datacenter_id = get_resource_id(self.module, datacenter_list, datacenter)

        # Locate UUID for server
        server_list = server_api.datacenters_servers_get(
            datacenter_id=datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, server)

        # Locate UUID for NIC
        nic_list = nic_api.datacenters_servers_nics_get(
            datacenter_id=datacenter_id, server_id=server_id, depth=1)
        nic_id = get_resource_id(self.module, nic_list, nic)

        return firewall_rules_api.datacenters_servers_nics_firewallrules_get(datacenter_id, server_id, nic_id, depth=2)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('firewall_rule')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        protocol = self.module.params.get('protocol')
        source_mac = self.module.params.get('source_mac')
        source_ip = self.module.params.get('source_ip')
        target_ip = self.module.params.get('target_ip')
        port_range_start = self.module.params.get('port_range_start')
        port_range_end = self.module.params.get('port_range_end')
        icmp_type = self.module.params.get('icmp_type')
        icmp_code = self.module.params.get('icmp_code')
        ip_version = self.module.params.get('ip_version')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            protocol = existing_object.properties.protocol if protocol is None else protocol
            source_mac = existing_object.properties.source_mac if source_mac is None else source_mac
            source_ip = existing_object.properties.source_ip if source_ip is None else source_ip
            target_ip = existing_object.properties.target_ip if target_ip is None else target_ip
            port_range_start = existing_object.properties.port_range_start if port_range_start is None else port_range_start
            port_range_end = existing_object.properties.port_range_end if port_range_end is None else port_range_end
            icmp_type = existing_object.properties.icmp_type if icmp_type is None else icmp_type
            icmp_code = existing_object.properties.icmp_code if icmp_code is None else icmp_code
            ip_version = existing_object.properties.ip_version if ip_version is None else ip_version

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        datacenters_api = ionoscloud.DataCentersApi(client)
        nic_api = ionoscloud.NetworkInterfacesApi(api_client=client)
        servers_api = ionoscloud.ServersApi(api_client=client)
        firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

        datacenter_list = get_paginated(datacenters_api.datacenters_get)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
        nic_id = get_resource_id(self.module, nic_list, self.module.params.get('nic'))

        firewall_rule = FirewallRule(properties=FirewallruleProperties(
            name=name, protocol=protocol, source_mac=source_mac,
            source_ip=source_ip, ip_version=ip_version,
            target_ip=target_ip, icmp_code=icmp_code, icmp_type=icmp_type,
            port_range_start=port_range_start, port_range_end=port_range_end,
        ))

        try:
            current_nic = nic_api.datacenters_servers_nics_find_by_id(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id,
            )
            nic = Nic(properties=NicProperties(firewall_active=True, lan=current_nic.properties.lan))
            nic_api.datacenters_servers_nics_put(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, nic=nic,
            )

        except Exception as e:
            self.module.fail_json(msg='Unable to activate the NIC firewall.' % to_native(e))

        try:
            response, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_post_with_http_info(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, firewallrule=firewall_rule,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        except ApiException as e:
            self.module.fail_json(msg="failed to create the firewall rule: %s" % to_native(e))

        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        source_mac = self.module.params.get('source_mac')
        source_ip = self.module.params.get('source_ip')
        target_ip = self.module.params.get('target_ip')
        port_range_start = self.module.params.get('port_range_start')
        port_range_end = self.module.params.get('port_range_end')
        icmp_type = self.module.params.get('icmp_type')
        icmp_code = self.module.params.get('icmp_code')
        ip_version = self.module.params.get('ip_version')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        datacenters_api = ionoscloud.DataCentersApi(client)
        servers_api = ionoscloud.ServersApi(client)
        nic_api = ionoscloud.NetworkInterfacesApi(client)
        firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

        datacenter_list = get_paginated(datacenters_api.datacenters_get)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
        nic_id = get_resource_id(self.module, nic_list, self.module.params.get('nic'))

        firewall_rule_properties = FirewallruleProperties(
            name=name,
            source_mac=source_mac,
            source_ip=source_ip,
            target_ip=target_ip,
            ip_version=ip_version,
        )

        if port_range_start or port_range_end:
            firewall_rule_properties.port_range_start = port_range_start
            firewall_rule_properties.port_range_end = port_range_end

        if icmp_type or icmp_code:
            firewall_rule_properties.icmp_code = icmp_code
            firewall_rule_properties.icmp_type = icmp_type

        try:
            response, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_patch_with_http_info(
                datacenter_id=datacenter_id,
                server_id=server_id,
                nic_id=nic_id,
                firewallrule_id=existing_object.id,
                firewallrule=firewall_rule_properties
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the firewall rule: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        datacenters_api = ionoscloud.DataCentersApi(client)
        servers_api = ionoscloud.ServersApi(client)
        nic_api = ionoscloud.NetworkInterfacesApi(client)
        firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

        datacenter_list = get_paginated(datacenters_api.datacenters_get)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
        nic_id = get_resource_id(self.module, nic_list, self.module.params.get('nic'))

        try:
            _, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_delete_with_http_info(
                datacenter_id=datacenter_id,
                server_id=server_id,
                nic_id=nic_id,
                firewallrule_id=existing_object.id,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(
                msg="failed to remove the firewall rule: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = FirewallRuleModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
