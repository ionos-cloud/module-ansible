HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options_with_depth


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['info']
OBJECT_NAME = 'Firewall Rules'
RETURNED_KEY = 'firewall_rules'

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
    **get_info_default_options_with_depth(STATES),
}


DOCUMENTATION = """
module: firewall_rule_info
short_description: List Ionos Cloud Firewall Rules of a given NIC.
description:
     - This is a simple module that supports listing Firewall Rules.
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
        - The datacenter name or UUID in which to operate.
        required: true
    depth:
        default: 1
        description:
        - The depth used when retrieving the items.
        required: false
    filters:
        description:
        - 'Filter that can be used to list only objects which have a certain set of propeties.
            Filters should be a dict with a key containing keys and value pair in the
            following format: ''properties.name'': ''server_name'''
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
    server:
        description:
        - The server name or UUID.
        required: true
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
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all volumes for a given datacenter
      firewall_rule_info:
        datacenter: "AnsibleDatacenter"
        server: "AnsibleServer"
        nic: "AnsibleNIC"
      register: firewall_rule_list_response
"""


def get_objects(module, client):
    firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)
    datacenters_api = ionoscloud.DataCentersApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    # Locate UUID for Server
    server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    # Locate UUID for NIC
    nic_list = nics_api.datacenters_servers_nics_get(datacenter_id, server_id, depth=1)
    nic_id = get_resource_id(module, nic_list, module.params.get('nic'))
    
    return firewall_rules_api.datacenters_servers_nics_firewallrules_get(
        datacenter_id, server_id, nic_id, depth=module.params.get('depth'),
    )


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
