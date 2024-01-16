#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Nic, NicProperties
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


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'NIC'
RETURNED_KEY = 'nic'

OPTIONS = {
    'name': {
        'description': ['The name of the  resource.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'nic': {
        'description': ['The ID or name of an existing NIC.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
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
    'lan': {
        'description': ['The LAN ID the NIC will be on. If the LAN ID does not exist, it will be implicitly created.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'dhcp': {
        'description': ['Indicates if the NIC will reserve an IP using DHCP.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'dhcpv6': {
        'description': ["Indicates if the NIC will receive an IPv6 using DHCP. It can be set to \'true\' or \'false\' only if this NIC is connected to an IPv6 enabled LAN."],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'firewall_active': {
        'description': ['Activate or deactivate the firewall. By default, an active firewall without any defined rules will block all incoming network traffic except for the firewall rules that explicitly allows certain protocols, IP addresses and ports.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'ips': {
        'description': ['Collection of IP addresses, assigned to the NIC. Explicitly assigned public IPs need to come from reserved IP blocks. Passing value null or empty array will assign an IP address automatically.'],
        'available': ['present', 'update'],
        'type': 'list',
        'version_added': '2.4',
    },
    'ipv6_ips': {
        'description': ["If this NIC is connected to an IPv6 enabled LAN then this property contains the IPv6 IP addresses of the NIC. The maximum number of IPv6 IP addresses per NIC is 50, if you need more, contact support. If you leave this property \'null\' when adding a NIC, when changing the NIC\'s IPv6 CIDR block, when changing the LAN\'s IPv6 CIDR block or when moving the NIC to a different IPv6 enabled LAN, then we will automatically assign the same number of IPv6 addresses which you had before from the NICs new CIDR block. If you leave this property \'null\' while not changing the CIDR block, the IPv6 IP addresses won\'t be changed either. You can also provide your own self choosen IPv6 addresses, which then must be inside the IPv6 CIDR block of this NIC."],
        'available': ['present', 'update'],
        'type': 'list',
        'version_added': '2.4',
    },
    'ipv6_cidr': {
        'description': ["If this NIC is connected to an IPv6 enabled LAN then this property contains the /80 IPv6 CIDR block of the NIC. If you leave this property \'null\' when adding a NIC to an IPv6-enabled LAN, then an IPv6 CIDR block will automatically be assigned to the NIC, but you can also specify an /80 IPv6 CIDR block for the NIC on your own, which must be inside the /64 IPv6 CIDR block of the LAN and unique. This value can only be set, if the LAN already has an IPv6 CIDR block assigned. An IPv6-enabled LAN is limited to a maximum of 65,536 NICs."],
        'available': ['present', 'update'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: nic
short_description: Create, Update or Remove a NIC.
description:
     - This module allows you to create, update or remove a NIC.
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''# Create a NIC
    - name: Create NIC
      nic:
       name: NicName
       datacenter: DatacenterName
       server: ServerName
       lan: 2
       dhcp: true
       firewall_active: true
       ips:
         - 10.0.0.1
       wait: true
       wait_timeout: 600
       state: present
      register: ionos_cloud_nic
  ''',
    'update': '''# Update a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      lan: 1
      ips:
        - 158.222.103.23
        - 158.222.103.24
      dhcp: false
      state: update
  ''',
    'absent': '''# Remove a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      wait_timeout: 500
      state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class NicModule(CommonIonosModule):
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
            self.module.params.get('ips') is not None
            and sorted(existing_object.properties.ips) != sorted(self.module.params.get('ips'))
            or self.module.params.get('ipv6_cidr') is not None
            and existing_object.properties.ipv6_cidr_block != self.module.params.get('ipv6_cidr')
            or self.module.params.get('ipv6_ips') is not None
            and sorted(existing_object.properties.ipv6_ips) != sorted(self.module.params.get('ipv6_ips'))
            or self.module.params.get('dhcp') is not None
            and existing_object.properties.dhcp != self.module.params.get('dhcp')
            or self.module.params.get('dhcpv6') is not None
            and existing_object.properties.dhcpv6 != self.module.params.get('dhcpv6')
            or self.module.params.get('lan') is not None
            and int(existing_object.properties.lan) != int(self.module.params.get('lan'))
            or self.module.params.get('firewall_active') is not None
            and existing_object.properties.firewall_active != self.module.params.get('firewall_active')
            or self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter = self.module.params.get('datacenter')
        server = self.module.params.get('server')

        datacenters_api = ionoscloud.DataCentersApi(api_client=client)
        servers_api = ionoscloud.ServersApi(api_client=client)
        nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

        # Locate UUID for Datacenter
        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter = get_resource_id(self.module, datacenter_list, datacenter)

        # Locate UUID for Server
        server_list = servers_api.datacenters_servers_get(datacenter, depth=1)
        server = get_resource_id(self.module, server_list, server)

        return nics_api.datacenters_servers_nics_get(datacenter_id=datacenter, server_id=server, depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('nic')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        lan = self.module.params.get('lan')
        dhcp = self.module.params.get('dhcp')
        dhcpv6 = self.module.params.get('dhcpv6')
        firewall_active = self.module.params.get('firewall_active')
        ips = self.module.params.get('ips')
        ipv6_ips = self.module.params.get('ipv6_ips')
        ipv6_cidr = self.module.params.get('ipv6_cidr')
        name = self.module.params.get('name')
        if existing_object is not None:
            lan = existing_object.properties.lan if lan is None else lan
            dhcp = existing_object.properties.dhcp if dhcp is None else dhcp
            dhcpv6 = existing_object.properties.dhcpv6 if dhcpv6 is None else dhcpv6
            firewall_active = existing_object.properties.firewall_active if firewall_active is None else firewall_active
            ips = existing_object.properties.ips if ips is None else ips
            ipv6_ips = existing_object.properties.ipv6_ips if ipv6_ips is None else ipv6_ips
            ipv6_cidr = existing_object.properties.ipv6_cidr_block if ipv6_cidr is None else ipv6_cidr
            name = existing_object.properties.name if name is None else name

        datacenters_api = ionoscloud.DataCentersApi(api_client=client)
        servers_api = ionoscloud.ServersApi(api_client=client)
        nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

        # Locate UUID for Datacenter
        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        # Locate UUID for Server
        server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        nic = Nic(properties=NicProperties(
            name=name, ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active,
            dhcpv6=dhcpv6, ipv6_ips=ipv6_ips, ipv6_cidr_block=ipv6_cidr,
        ))

        try:
            nic_response, _, headers = nics_api.datacenters_servers_nics_post_with_http_info(
                datacenter_id=datacenter_id, server_id=server_id, nic=nic,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
                nic_response = nics_api.datacenters_servers_nics_find_by_id(
                    datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_response.id,
                )
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new NIC: %s" % to_native(e))
        return nic_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        lan = self.module.params.get('lan')
        dhcp = self.module.params.get('dhcp')
        firewall_active = self.module.params.get('firewall_active')
        ips = self.module.params.get('ips')
        name = self.module.params.get('name')
        dhcpv6 = self.module.params.get('dhcpv6')
        ipv6_ips = self.module.params.get('ipv6_ips')
        ipv6_cidr = self.module.params.get('ipv6_cidr')

        datacenters_api = ionoscloud.DataCentersApi(api_client=client)
        servers_api = ionoscloud.ServersApi(api_client=client)
        nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

        # Locate UUID for Datacenter
        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        # Locate UUID for Server
        server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        if lan is None:
            lan = existing_object.properties.lan
        if firewall_active is None:
            firewall_active = existing_object.properties.firewall_active
        if dhcp is None:
            dhcp = existing_object.properties.dhcp
        if dhcpv6 is None:
            dhcpv6 = existing_object.properties.dhcpv6

        nic_properties = NicProperties(
            ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active, name=name,
            dhcpv6=dhcpv6, ipv6_ips=ipv6_ips, ipv6_cidr_block=ipv6_cidr,
        )

        try:
            nic_response, _, headers = nics_api.datacenters_servers_nics_patch_with_http_info(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=existing_object.id, nic=nic_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
                nic_response = nics_api.datacenters_servers_nics_find_by_id(
                    datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_response.id,
                )

            return nic_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the NIC: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenters_api = ionoscloud.DataCentersApi(api_client=client)
        servers_api = ionoscloud.ServersApi(api_client=client)
        nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

        # Locate UUID for Datacenter
        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        # Locate UUID for Server
        server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
        server_id = get_resource_id(self.module, server_list, self.module.params.get('server'))

        try:
            _, _, headers = nics_api.datacenters_servers_nics_delete_with_http_info(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the NIC: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NicModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
