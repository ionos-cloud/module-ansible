#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Lan, LanProperties
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'LAN'
RETURNED_KEY = 'lan'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'lan': {
        'description': ['The LAN name or UUID.'],
        'available': ['absent', 'update'],
        'required': ['absent', 'update'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'pcc': {
        'description': ['The unique identifier of the Cross Connect the LAN is connected to, if any. It needs to be ensured that IP addresses of the NICs of all LANs connected to a given Cross Connect is not duplicated and belongs to the same subnet range.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'ip_failover': {
        'description': ['IP failover configurations for lan'],
        'available': ['update'],
        'type': 'list',
        'elements': 'dict',
    },
    'public': {
        'description': ['Indicates if the LAN is connected to the internet or not.'],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'ipv6_cidr': {
        'description': ["For a GET request, this value is either \'null\' or contains the LAN\'s /64 IPv6 CIDR block if this LAN is IPv6 enabled. For POST/PUT/PATCH requests, \'AUTO\' will result in enabling this LAN for IPv6 and automatically assign a /64 IPv6 CIDR block to this LAN and /80 IPv6 CIDR blocks to the NICs and one /128 IPv6 address to each connected NIC. If you choose the IPv6 CIDR block for the LAN on your own, then you must provide a /64 block, which is inside the IPv6 CIDR block of the virtual datacenter and unique inside all LANs from this virtual datacenter. If you enable IPv6 on a LAN with NICs, those NICs will get a /80 IPv6 CIDR block and one IPv6 address assigned to each automatically, unless you specify them explicitly on the LAN and on the NICs. A virtual data center is limited to a maximum of 256 IPv6-enabled LANs."],
        'available': ['present', 'update'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: lan
short_description: Create, update or remove a LAN.
description:
     - This module allows you to create or remove a LAN.
version_added: "2.4"
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
    ip_failover:
        description:
        - IP failover configurations for lan
        elements: dict
        required: false
    ipv6_cidr:
        description:
        - For a GET request, this value is either 'null' or contains the LAN's /64 IPv6
            CIDR block if this LAN is IPv6 enabled. For POST/PUT/PATCH requests, 'AUTO'
            will result in enabling this LAN for IPv6 and automatically assign a /64 IPv6
            CIDR block to this LAN and /80 IPv6 CIDR blocks to the NICs and one /128 IPv6
            address to each connected NIC. If you choose the IPv6 CIDR block for the LAN
            on your own, then you must provide a /64 block, which is inside the IPv6 CIDR
            block of the virtual datacenter and unique inside all LANs from this virtual
            datacenter. If you enable IPv6 on a LAN with NICs, those NICs will get a /80
            IPv6 CIDR block and one IPv6 address assigned to each automatically, unless
            you specify them explicitly on the LAN and on the NICs. A virtual data center
            is limited to a maximum of 256 IPv6-enabled LANs.
        required: false
    lan:
        description:
        - The LAN name or UUID.
        required: false
    name:
        description:
        - The name of the  resource.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    pcc:
        description:
        - The unique identifier of the Cross Connect the LAN is connected to, if any.
            It needs to be ensured that IP addresses of the NICs of all LANs connected
            to a given Cross Connect is not duplicated and belongs to the same subnet
            range.
        required: false
    public:
        default: false
        description:
        - Indicates if the LAN is connected to the internet or not.
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
name: Create LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  public: false
register: ionos_cloud_lan
''',
  'update' : '''
name: Update LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  pcc: ''
  state: update
''',
  'absent' : '''
name: Remove LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  state: absent
  wait: true
''',
}

EXAMPLES = """
name: Create LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  public: false
register: ionos_cloud_lan


name: Update LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  pcc: ''
  state: update


name: Remove LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  state: absent
  wait: true
"""


class LanModule(CommonIonosModule):
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
        pcc_id = get_resource_id(
            self.module, 
            ionoscloud.PrivateCrossConnectsApi(clients[0]).pccs_get(depth=1),
            self.module.params.get('pcc'),
        )

        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('public') is not None
            and existing_object.properties.public != self.module.params.get('public')
            or self.module.params.get('ipv6_cidr') is not None
            and existing_object.properties.ipv6_cidr_block != self.module.params.get('ipv6_cidr')
            or self.module.params.get('ip_failover') is not None
            and existing_object.properties.ip_failover != list(map(lambda el: {'ip': el.ip, 'nic_uuid': el.nic_uuid}, self.module.params.get('ip_failover')))
            or pcc_id is not None
            and existing_object.properties.pcc != pcc_id
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_list = ionoscloud.DataCentersApi(api_client=client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        return ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('lan')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        public = self.module.params.get('public')
        ipv6_cidr = self.module.params.get('ipv6_cidr')

        pcc_id = get_resource_id(
            self.module, 
            ionoscloud.PrivateCrossConnectsApi(client).pccs_get(depth=1),
            self.module.params.get('pcc'),
        )
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            public = existing_object.properties.public if public is None else public
            ipv6_cidr = existing_object.properties.ipv6_cidr_block if ipv6_cidr is None else ipv6_cidr
            pcc_id = existing_object.properties.pcc if pcc_id is None else pcc_id

        datacenters_api = ionoscloud.DataCentersApi(client)
        lans_api = ionoscloud.LANsApi(client)

        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        lan = Lan(properties=LanProperties(
            name=name, pcc=pcc_id, public=public,
            ipv6_cidr_block=ipv6_cidr,
        ))

        try:
            lan_response, _, headers = lans_api.datacenters_lans_post_with_http_info(datacenter_id, lan=lan)
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new LAN: %s" % to_native(e))
        return lan_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        public = self.module.params.get('public')
        ip_failover = self.module.params.get('ip_failover')
        ipv6_cidr = self.module.params.get('ipv6_cidr')

        pcc_id = get_resource_id(
            self.module, 
            ionoscloud.PrivateCrossConnectsApi(client).pccs_get(depth=1),
            self.module.params.get('pcc'),
        )

        datacenters_api = ionoscloud.DataCentersApi(client)
        lans_api = ionoscloud.LANsApi(client)

        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        if ip_failover:
            for elem in ip_failover:
                elem['nicUuid'] = elem.pop('nic_uuid')

        lan_properties = LanProperties(
            name=name, ip_failover=ip_failover,
            pcc=pcc_id, public=public,
            ipv6_cidr_block=ipv6_cidr,
        )

        try:
            lan_response, _, headers = lans_api.datacenters_lans_patch_with_http_info(
                datacenter_id, existing_object.id, lan_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return lan_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the LAN: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenters_api = ionoscloud.DataCentersApi(client)
        lans_api = ionoscloud.LANsApi(client)

        datacenter_list = datacenters_api.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))

        try:
            _, _, headers = lans_api.datacenters_lans_delete_with_http_info(datacenter_id, existing_object.id)
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the LAN: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = LanModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
