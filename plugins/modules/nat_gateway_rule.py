#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import NatGatewayRule, NatGatewayRuleProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'natgateway'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'NAT Gateway rule'
RETURNED_KEY = 'nat_gateway_rule'

OPTIONS = {
    'name': {
        'description': ['The name of the NAT Gateway rule.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'type': {
        'description': ['Type of the NAT Gateway rule.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ["Protocol of the NAT Gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set."],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'source_subnet': {
        'description': ['Source subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets source IP address.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'public_ip': {
        'description': ['Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'target_subnet': {
        'description': ['Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'target_port_range': {
        'description': ['Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway': {
        'description': ['The ID or name of the NAT Gateway.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway_rule': {
        'description': ['The ID or name of the NAT Gateway rule.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: nat_gateway_rule
short_description: Create or destroy a Ionos Cloud NATGateway rule.
description:
     - This is a simple module that supports creating or removing NATGateway rules.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    ilowuerhfgwoqrghbqwoguh
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      name: RuleName
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: <ip>
      wait: true
    register: nat_gateway_rule_response
  ''',
  'update' : '''
  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: RuleName
      public_ip: <newIp>
      name: "RuleName - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  ''',
  'absent' : '''
  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: "RuleName - UPDATED"
      state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""

class NatFlowlogModule(CommonIonosModule):
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
            or self.module.params.get('type') is not None
            and existing_object.properties.type != self.module.params.get('type')
            or self.module.params.get('protocol') is not None
            and existing_object.properties.protocol != self.module.params.get('protocol')
            or self.module.params.get('source_subnet') is not None
            and existing_object.properties.source_subnet != self.module.params.get('source_subnet')
            or self.module.params.get('public_ip') is not None
            and existing_object.properties.public_ip != self.module.params.get('public_ip')
            or self.module.params.get('target_subnet') is not None
            and existing_object.properties.target_subnet != self.module.params.get('target_subnet')
            or self.module.params.get('target_port_range') is not None
            and existing_object.properties.target_port_range != self.module.params.get('target_port_range')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        nat_gateway_id = get_resource_id(
            self.module, 
            ionoscloud.NATGatewaysApi(client).datacenters_natgateways_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('nat_gateway'),
        )

        return ionoscloud.NATGatewaysApi(client).datacenters_natgateways_rules_get(
            datacenter_id, nat_gateway_id, depth=1,
        )


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('nat_gateway_rule')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        nat_gateway_type = self.module.params.get('type')
        protocol = self.module.params.get('protocol')
        source_subnet = self.module.params.get('source_subnet')
        public_ip = self.module.params.get('public_ip')
        target_subnet = self.module.params.get('target_subnet')
        target_port_range = self.module.params.get('target_port_range')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        nat_gateway_id = get_resource_id(
            self.module, 
            ionoscloud.NATGatewaysApi(client).datacenters_natgateways_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('nat_gateway'),
        )

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            nat_gateway_type = existing_object.properties.type if nat_gateway_type is None else nat_gateway_type
            protocol = existing_object.properties.protocol if protocol is None else protocol
            source_subnet = existing_object.properties.source_subnet if source_subnet is None else source_subnet
            public_ip = existing_object.properties.public_ip if public_ip is None else public_ip
            target_subnet = existing_object.properties.target_subnet if target_subnet is None else target_subnet
            target_port_range = existing_object.properties.target_port_range if target_port_range is None else target_port_range
            target_subnet = existing_object.properties.target_subnet if target_subnet is None else target_subnet

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)
        
        nat_gateway_rule_properties = NatGatewayRuleProperties(
            name=name, type=nat_gateway_type, protocol=protocol,
            source_subnet=source_subnet, public_ip=public_ip,
            target_subnet=target_subnet,
            target_port_range=target_port_range,
        )
        nat_gateway_rule = NatGatewayRule(properties=nat_gateway_rule_properties)

        try:
            nat_gateway_rule_response, _, headers = nat_gateways_api.datacenters_natgateways_rules_post_with_http_info(
                datacenter_id, nat_gateway_id, nat_gateway_rule,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new NAT Gateway Rule: %s" % to_native(e))
        return nat_gateway_rule_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        nat_gateway_type = self.module.params.get('type')
        protocol = self.module.params.get('protocol')
        source_subnet = self.module.params.get('source_subnet')
        public_ip = self.module.params.get('public_ip')
        target_subnet = self.module.params.get('target_subnet')
        target_port_range = self.module.params.get('target_port_range')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        nat_gateway_id = get_resource_id(
            self.module, 
            ionoscloud.NATGatewaysApi(client).datacenters_natgateways_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('nat_gateway'),
        )

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)

        nat_gateway_rule_properties = NatGatewayRuleProperties(
            name=name, type=nat_gateway_type, protocol=protocol,
            source_subnet=source_subnet, public_ip=public_ip,
            target_subnet=target_subnet,
            target_port_range=target_port_range,
        )

        try:
            response, _, headers = nat_gateways_api.datacenters_natgateways_rules_patch_with_http_info(
                datacenter_id, nat_gateway_id, existing_object.id, nat_gateway_rule_properties,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the NAT Gateway Rule: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        nat_gateway_id = get_resource_id(
            self.module, 
            ionoscloud.NATGatewaysApi(client).datacenters_natgateways_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('nat_gateway'),
        )

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)

        try:
            _, _, headers = nat_gateways_api.datacenters_natgateways_rules_delete_with_http_info(
                datacenter_id, nat_gateway_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the NAT Gateway Rule: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NatFlowlogModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
