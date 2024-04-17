#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import NetworkLoadBalancerForwardingRule, NetworkLoadBalancerForwardingRuleProperties
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
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Network Loadbalancer forwarding rule'
RETURNED_KEY = 'forwarding_rule'

OPTIONS = {
    'name': {
        'description': ['The name of the Network Load Balancer forwarding rule.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'algorithm': {
        'description': ['Balancing algorithm'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['Balancing protocol'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'listener_ip': {
        'description': ['Listening (inbound) IP.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'listener_port': {
        'description': ['Listening (inbound) port number; valid range is 1 to 65535.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'health_check': {
        'description': ['Health check properties for Network Load Balancer forwarding rule.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'targets': {
        'description': ['Array of items in the collection.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'network_load_balancer': {
        'description': ['The ID or name of the Network Loadbalancer.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'forwarding_rule': {
        'description': ['The ID or name of the Network Loadbalancer forwarding rule.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: network_load_balancer_rule
short_description: Create or destroy a Ionos Cloud NetworkLoadbalancer Flowlog rule.
description:
     - This is a simple module that supports creating or removing NATGateway Flowlog rules.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    algorithm:
        description:
        - Balancing algorithm
        required: false
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
        - The ID or name of the datacenter.
        required: true
    forwarding_rule:
        description:
        - The ID or name of the Network Loadbalancer forwarding rule.
        required: false
    health_check:
        description:
        - Health check properties for Network Load Balancer forwarding rule.
        required: false
    listener_ip:
        description:
        - Listening (inbound) IP.
        required: false
    listener_port:
        description:
        - Listening (inbound) port number; valid range is 1 to 65535.
        required: false
    name:
        description:
        - The name of the Network Load Balancer forwarding rule.
        required: false
    network_load_balancer:
        description:
        - The ID or name of the Network Loadbalancer.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    protocol:
        description:
        - Balancing protocol
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
    targets:
        description:
        - Array of items in the collection.
        elements: dict
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
  'present' : '''
name: Create Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  name: 'AnsibleAutoTestNLB'
  algorithm: ROUND_ROBIN
  protocol: TCP
  listener_ip: 10.12.118.224
  listener_port: '8081'
  targets:
  - ip: 22.231.2.2
    port: '8080'
    weight: '123'
  health_check:
    client_timeout: 50
    connect_timeout: 5000
    target_timeout: 5000
    retries: 1
  datacenter: ''
  network_load_balancer: ''
  wait: true
register: nlb_forwarding_rule_response
''',
  'update' : '''
name: Update Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  datacenter: ''
  network_load_balancer: ''
  forwarding_rule: ''
  name: 'AnsibleAutoTestNLB - UPDATED'
  algorithm: ROUND_ROBIN
  protocol: TCP
  wait: true
  state: update
register: nlb_forwarding_rule_update_response
''',
  'absent' : '''
name: Delete Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  datacenter: ''
  network_load_balancer: ''
  forwarding_rule: ''
  state: absent
''',
}

EXAMPLES = """
name: Create Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  name: 'AnsibleAutoTestNLB'
  algorithm: ROUND_ROBIN
  protocol: TCP
  listener_ip: 10.12.118.224
  listener_port: '8081'
  targets:
  - ip: 22.231.2.2
    port: '8080'
    weight: '123'
  health_check:
    client_timeout: 50
    connect_timeout: 5000
    target_timeout: 5000
    retries: 1
  datacenter: ''
  network_load_balancer: ''
  wait: true
register: nlb_forwarding_rule_response


name: Update Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  datacenter: ''
  network_load_balancer: ''
  forwarding_rule: ''
  name: 'AnsibleAutoTestNLB - UPDATED'
  algorithm: ROUND_ROBIN
  protocol: TCP
  wait: true
  state: update
register: nlb_forwarding_rule_update_response


name: Delete Network Load Balancer Forwarding Rule
ionoscloudsdk.ionoscloud.network_load_balancer_rule:
  datacenter: ''
  network_load_balancer: ''
  forwarding_rule: ''
  state: absent
"""


def _get_health_check(health_check_param):
    health_check = None
    if health_check_param:
        health_check = ionoscloud.models.NetworkLoadBalancerForwardingRuleHealthCheck()
        if 'client_timeout' in health_check_param:
            health_check.client_timeout = health_check_param.get('client_timeout')
        if 'connect_timeout' in health_check_param:
            health_check.connect_timeout = health_check_param.get('connect_timeout')
        if 'target_timeout' in health_check_param:
            health_check.target_timeout = health_check_param.get('target_timeout')
        if 'retries' in health_check_param:
            health_check.retries = health_check_param.get('retries')

    return health_check


class NetworkLoadBalancerRuleModule(CommonIonosModule):
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
        new_health_check = _get_health_check(self.module.params.get('health_check'))

        def sort_func(el):
            return el['ip'], el['port']

        if self.module.params.get('targets'):
            existing_targets = sorted(map(
                lambda x: { 'ip': x.ip, 'port': x.port, 'weight': x.weight },
                existing_object.properties.targets
            ), key=sort_func)
            new_targets = sorted(self.module.params.get('targets'), key=sort_func)

        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('algorithm') is not None
            and existing_object.properties.algorithm != self.module.params.get('algorithm')
            or self.module.params.get('protocol') is not None
            and existing_object.properties.protocol != self.module.params.get('protocol')
            or self.module.params.get('listener_ip') is not None
            and existing_object.properties.listener_ip != self.module.params.get('listener_ip')
            or self.module.params.get('listener_port') is not None
            and existing_object.properties.listener_port != self.module.params.get('listener_port')
            or self.module.params.get('target_subnet') is not None
            and existing_object.properties.target_subnet != self.module.params.get('target_subnet')
            or self.module.params.get('target_port_range') is not None
            and existing_object.properties.target_port_range != self.module.params.get('target_port_range')
            or self.module.params.get('targets') is not None
            and new_targets != existing_targets
            or self.module.params.get('health_check') is not None
            and (
                existing_object.properties.health_check.client_timeout != new_health_check.client_timeout
                or existing_object.properties.health_check.connect_timeout != new_health_check.connect_timeout
                or existing_object.properties.health_check.target_timeout != new_health_check.target_timeout
                or existing_object.properties.health_check.retries != new_health_check.retries
            )
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        return ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_forwardingrules_get(
            datacenter_id, network_load_balancer_id, depth=1,
        )


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('forwarding_rule')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        algorithm = self.module.params.get('algorithm')
        protocol = self.module.params.get('protocol')
        listener_ip = self.module.params.get('listener_ip')
        listener_port = self.module.params.get('listener_port')
        health_check_param = _get_health_check(self.module.params.get('health_check'))
        targets = self.module.params.get('targets')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            algorithm = existing_object.properties.algorithm if algorithm is None else algorithm
            protocol = existing_object.properties.protocol if protocol is None else protocol
            listener_ip = existing_object.properties.listener_ip if listener_ip is None else listener_ip
            listener_port = existing_object.properties.listener_port if listener_port is None else listener_port
            health_check_param = existing_object.properties.health_check if health_check_param is None else health_check_param
            targets = existing_object.properties.targets if targets is None else targets


        nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)
        
        nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(
            name=name, algorithm=algorithm,
            protocol=protocol,
            listener_ip=listener_ip,
            listener_port=listener_port,
            health_check=health_check_param,
            targets=targets,
        )
        nlb_forwarding_rule = NetworkLoadBalancerForwardingRule(properties=nlb_forwarding_rule_properties)

        try:
            response, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_post_with_http_info(
                datacenter_id, network_load_balancer_id, nlb_forwarding_rule,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Network Loadbalancer Rule: %s" % to_native(e))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        algorithm = self.module.params.get('algorithm')
        protocol = self.module.params.get('protocol')
        listener_ip = self.module.params.get('listener_ip')
        listener_port = self.module.params.get('listener_port')
        health_check = _get_health_check(self.module.params.get('health_check'))
        targets = self.module.params.get('targets')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)

        nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(
            name=name, algorithm=algorithm,
            protocol=protocol,
            listener_ip=listener_ip,
            listener_port=listener_port,
            health_check=health_check,
            targets=targets,
        )

        try:
            response, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_patch_with_http_info(
                datacenter_id, network_load_balancer_id, existing_object.id, nlb_forwarding_rule_properties,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Network Loadbalancer Rule: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)

        try:
            _, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_delete_with_http_info(
                datacenter_id, network_load_balancer_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Network Loadbalancer Rule: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NetworkLoadBalancerRuleModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
