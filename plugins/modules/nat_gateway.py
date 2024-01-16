#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import NatGateway, NatGatewayProperties, NatGatewayLanProperties
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
OBJECT_NAME = 'NAT Gateway'
RETURNED_KEY = 'nat_gateway'

OPTIONS = {
    'name': {
        'description': ['Name of the NAT Gateway.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'public_ips': {
        'description': ['Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
    },
    'lans': {
        'description': ['Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway': {
        'description': ['The ID or name of the NAT Gateway.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}


DOCUMENTATION = """
module: nat_gateway
short_description: Create or destroy a Ionos Cloud NATGateway.
description:
     - This is a simple module that supports creating or removing NATGateways.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    allow_replace:
        default: false
        description:
        - Boolean indicating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
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
    lans:
        description:
        - Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet
            mask. If no IP is provided, the system will generate an IP with /24 subnet.
        required: false
    name:
        description:
        - Name of the NAT Gateway.
        required: false
    nat_gateway:
        description:
        - The ID or name of the NAT Gateway.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    public_ips:
        description:
        - Collection of public IP addresses of the NAT Gateway. Should be customer reserved
            IP addresses in that location.
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
  - name: Create NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: NATGatewayName
      public_ips:
        - <ip1>
        - <ip2>
      lans:
        - id: 1
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  ''',
  'update' : '''
  - name: Update NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: "NATGatewayName - UPDATED"
      public_ips:
        - <ip1>
        - <ip2>
      nat_gateway: NATGatewayName
      wait: true
      state: update
    register: nat_gateway_response_update
  ''',
  'absent' : '''
  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway: NATGatewayName
      datacenter: DatacenterName
      wait: true
      wait_timeout: 2000
      state: absent
  ''',
}

EXAMPLES = """
  - name: Create NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: NATGatewayName
      public_ips:
        - <ip1>
        - <ip2>
      lans:
        - id: 1
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  

  - name: Update NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: "NATGatewayName - UPDATED"
      public_ips:
        - <ip1>
        - <ip2>
      nat_gateway: NATGatewayName
      wait: true
      state: update
    register: nat_gateway_response_update
  

  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway: NATGatewayName
      datacenter: DatacenterName
      wait: true
      wait_timeout: 2000
      state: absent
"""

class NatGatewayModule(CommonIonosModule):
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
        if self.module.params.get('lans'):
            existing_lans = list(map(
                lambda x: { 'gateway_ips': sorted(x.gateway_ips), 'id': str(x.id) },
                existing_object.properties.lans
            ))
            new_lans = list(map(
                lambda x: { 'gateway_ips': sorted(x['gateway_ips']), 'id': x['id'] },
                self.module.params.get('lans')
            ))

        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('public_ips') is not None
            and sorted(existing_object.properties.public_ips) != sorted(self.module.params.get('public_ips'))
            or self.module.params.get('lans') is not None
            and new_lans != existing_lans
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        return ionoscloud.NATGatewaysApi(client).datacenters_natgateways_get(datacenter_id, depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('nat_gateway')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        public_ips = self.module.params.get('public_ips')
        lans = self.module.params.get('lans')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            public_ips = existing_object.properties.public_ips if public_ips is None else public_ips
            lans = existing_object.properties.lans if lans is None else lans

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)
        
        nat_gateway_lans = []
        if lans:
            for lan in lans:
                nat_gateway_lans.append(NatGatewayLanProperties(id=lan['id'], gateway_ips=lan['gateway_ips']))

        nat_gateway_properties = NatGatewayProperties(name=name, public_ips=public_ips, lans=nat_gateway_lans)
        nat_gateway = NatGateway(properties=nat_gateway_properties)

        try:
            nat_gateway_response, _, headers = nat_gateways_api.datacenters_natgateways_post_with_http_info(
                datacenter_id, nat_gateway,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new NAT Gateway: %s" % to_native(e))
        return nat_gateway_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        public_ips = self.module.params.get('public_ips')
        lans = self.module.params.get('lans')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)

        nat_gateway_lans = []
        if lans:
            for lan in lans:
                nat_gateway_lans.append(NatGatewayLanProperties(id=lan['id'], gateway_ips=lan['gateway_ips']))
        nat_gateway_properties = NatGatewayProperties(name=name, public_ips=public_ips, lans=nat_gateway_lans)

        try:
            nat_gateway_response, _, headers = nat_gateways_api.datacenters_natgateways_patch_with_http_info(
                datacenter_id, existing_object.id, nat_gateway_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return nat_gateway_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the NAT Gateway: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        nat_gateways_api = ionoscloud.NATGatewaysApi(client)

        try:
            _, _, headers = nat_gateways_api.datacenters_natgateways_delete_with_http_info(
                datacenter_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the NAT Gateway: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NatGatewayModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
