#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties
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
OBJECT_NAME = 'Network Loadbalancer'
RETURNED_KEY = 'network_load_balancer'

OPTIONS = {
    'name': {
        'description': ['The name of the Network Load Balancer.'],
        'available': STATES,
        'required': ['present', 'update'],
        'type': 'str',
    },
    'listener_lan': {
        'description': ['ID of the listening LAN (inbound).'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'ips': {
        'description': ['Collection of the Network Load Balancer IP addresses. (Inbound and outbound) IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'target_lan': {
        'description': ['ID of the balanced private target LAN (outbound).'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'lb_private_ips': {
        'description': ['Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'network_load_balancer': {
        'description': ['The ID or name of the Network Loadbalancer.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: network_load_balancer
short_description: Create or destroy a Ionos Cloud NetworkLoadbalancer.
description:
     - This is a simple module that supports creating or removing NetworkLoadbalancers.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
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
        - The ID or name of the datacenter.
        required: true
    ips:
        description:
        - Collection of the Network Load Balancer IP addresses. (Inbound and outbound)
            IPs of the listenerLan must be customer-reserved IPs for public Load Balancers,
            and private IPs for private Load Balancers.
        required: false
    lb_private_ips:
        description:
        - Collection of private IP addresses with subnet mask of the Network Load Balancer.
            IPs must contain a valid subnet mask. If no IP is provided, the system will
            generate an IP with /24 subnet.
        required: false
    listener_lan:
        description:
        - ID of the listening LAN (inbound).
        required: false
    name:
        description:
        - The name of the Network Load Balancer.
        required: false
    network_load_balancer:
        description:
        - The ID or name of the Network Loadbalancer.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
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
    target_lan:
        description:
        - ID of the balanced private target LAN (outbound).
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
name: Create Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  datacenter: ''
  name: 'AnsibleAutoTestNLB'
  ips:
  - 10.12.118.224
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
register: nlb_response
''',
  'update' : '''
name: Update Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  datacenter: ''
  network_load_balancer: ''
  name: 'AnsibleAutoTestNLB - UPDATE'
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
  state: update
register: nlb_response_update
''',
  'absent' : '''
name: Remove Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  network_load_balancer: ''
  datacenter: ''
  wait: false
  wait_timeout: 2000
  state: absent
''',
}

EXAMPLES = """
name: Create Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  datacenter: ''
  name: 'AnsibleAutoTestNLB'
  ips:
  - 10.12.118.224
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
register: nlb_response


name: Update Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  datacenter: ''
  network_load_balancer: ''
  name: 'AnsibleAutoTestNLB - UPDATE'
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
  state: update
register: nlb_response_update


name: Remove Network Load Balancer
ionoscloudsdk.ionoscloud.network_load_balancer:
  network_load_balancer: ''
  datacenter: ''
  wait: false
  wait_timeout: 2000
  state: absent
"""

class NetworkLoadBalancerFlowlogModule(CommonIonosModule):
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
            or self.module.params.get('ips') is not None
            and sorted(existing_object.properties.ips) != sorted(self.module.params.get('ips'))
            or self.module.params.get('lb_private_ips') is not None
            and sorted(existing_object.properties.lb_private_ips) != sorted(self.module.params.get('lb_private_ips'))
            or self.module.params.get('listener_lan') is not None
            and existing_object.properties.listener_lan != self.module.params.get('listener_lan')
            or self.module.params.get('target_lan') is not None
            and existing_object.properties.target_lan != self.module.params.get('target_lan')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        return ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(datacenter_id, depth=1)



    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('network_load_balancer')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        ips = self.module.params.get('ips')
        listener_lan = self.module.params.get('listener_lan')
        target_lan = self.module.params.get('target_lan')
        lb_private_ips = self.module.params.get('lb_private_ips')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            ips = existing_object.properties.ips if ips is None else ips
            listener_lan = existing_object.properties.listener_lan if listener_lan is None else listener_lan
            target_lan = existing_object.properties.target_lan if target_lan is None else target_lan
            lb_private_ips = existing_object.properties.lb_private_ips if lb_private_ips is None else lb_private_ips

        network_loadbalancers_api = ionoscloud.NetworkLoadBalancersApi(client)
        
        nlb_properties = NetworkLoadBalancerProperties(
            name=name, listener_lan=listener_lan, ips=ips,
            target_lan=target_lan, lb_private_ips=lb_private_ips,
        )
        network_load_balancer = NetworkLoadBalancer(properties=nlb_properties)

        try:
            response, _, headers = network_loadbalancers_api.datacenters_networkloadbalancers_post_with_http_info(
                datacenter_id, network_load_balancer,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Network Loadbalancer: %s" % to_native(e))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        ips = self.module.params.get('ips')
        listener_lan = self.module.params.get('listener_lan')
        target_lan = self.module.params.get('target_lan')
        lb_private_ips = self.module.params.get('lb_private_ips')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)
        
        nlb_properties = NetworkLoadBalancerProperties(
            name=name, listener_lan=listener_lan, ips=ips,
            target_lan=target_lan, lb_private_ips=lb_private_ips,
        )

        try:
            response, _, headers = nlbs_api.datacenters_networkloadbalancers_patch_with_http_info(
                datacenter_id, existing_object.id, nlb_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Network Loadbalancer: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)

        try:
            _, _, headers = nlbs_api.datacenters_networkloadbalancers_delete_with_http_info(
                datacenter_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Network Loadbalancer: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NetworkLoadBalancerFlowlogModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
