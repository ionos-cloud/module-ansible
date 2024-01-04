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
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['info']
OBJECT_NAME = 'Network Loadbalancers Flowlogs'
RETURNED_KEY = 'flowlogs'

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
module: network_load_balancer_flowlog_info
short_description: List Ionos Cloud Flowlogs of a given Network Loadbalancer.
description:
     - This is a simple module that supports listing Flowlogs.
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all Flowlogs for a Network Loadbalancer
      network_load_balancer_flowlog_info:
        datacenter: "AnsibleDatacenter"
        network_load_balancer: "AnsibleNlb"
      register: flowlog_list_response
"""


def get_objects(module, client):
    datacenter = module.params.get('datacenter')
    nlb = module.params.get('network_load_balancer')
    nlbs_api = ionoscloud.NetworkLoadBalancersApi(api_client=client)
    datacenters_api = ionoscloud.DataCentersApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)

    # Locate UUID for Nlb
    nlb_list = nlbs_api.datacenters_networkloadbalancers_get(datacenter_id, depth=1)
    nlb_id = get_resource_id(module, nlb_list, nlb)

    return nlbs_api.datacenters_networkloadbalancers_flowlogs_get(
        datacenter_id, nlb_id, depth=module.params.get('depth'),
    )


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
