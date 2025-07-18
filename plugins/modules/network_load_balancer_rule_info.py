HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id, get_paginated
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options_with_depth


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['info']
OBJECT_NAME = 'Network Loadbalancer forwarding rules'
RETURNED_KEY = 'forwarding_rules'

OPTIONS = {
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
    **get_info_default_options_with_depth(STATES),
}

DOCUMENTATION = """
module: network_load_balancer_rule_info
short_description: List Ionos Cloud Network Loadbalancer forwarding rules of a given Network Loadbalancer.
description:
     - This is a simple module that supports listing Network Loadbalancer forwarding rules.
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
name: List Network Load Balancer Forwarding rules
ionoscloudsdk.ionoscloud.network_load_balancer_rule_info:
  datacenter: ''
  network_load_balancer: ''
register: nlb_forwardingrule_list_response
"""


def get_objects(module, client):
    datacenter = module.params.get('datacenter')
    nlb = module.params.get('network_load_balancer')
    nlbs_api = ionoscloud.NetworkLoadBalancersApi(api_client=client)
    datacenters_api = ionoscloud.DataCentersApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = get_paginated(datacenters_api.datacenters_get)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)

    # Locate UUID for Nlb
    nlb_list = nlbs_api.datacenters_networkloadbalancers_get(datacenter_id, depth=1)
    nlb_id = get_resource_id(module, nlb_list, nlb)

    return nlbs_api.datacenters_networkloadbalancers_forwardingrules_get(
        datacenter_id, nlb_id, depth=module.params.get('depth'),
    )

if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
