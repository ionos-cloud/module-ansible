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
OBJECT_NAME = 'Servers'
RETURNED_KEY = 'servers'

OPTIONS = {
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'upgrade_needed': {
        'description': ['Filter servers that can or that cannot be upgraded.'],
        'available': STATES,
        'type': 'bool',
    },
    **get_info_default_options_with_depth(STATES),
}


DOCUMENTATION = """
module: server_info
short_description: List Ionos Cloud servers of a given datacenter.
description:
     - This is a simple module that supports listing servers.
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
    upgrade_needed:
        description:
        - Filter servers that can or that cannot be upgraded.
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
    - name: Get all servers for a given datacenter
      server_info:
        datacenter: AnsibleDatacenter
      register: server_list_response

    - name: Get only the servers that need to be upgraded
      server_info:
        datacenter: AnsibleDatacenter
        upgrade_needed: true
      register: servers_list_upgrade_response

    - name: Show all servers for the created datacenter
      debug:
        var: server_list_response

    - name: Show servers that need an upgrade
      debug:
        var: servers_list_upgrade_response
"""


def get_objects(module, client):
    datacenter = module.params.get('datacenter')
    servers_api = ionoscloud.ServersApi(client)
    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    upgrade_needed = module.params.get('upgrade_needed')
    depth = module.params.get('depth')

    # Locate UUID for Datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=1)
    datacenter = get_resource_id(module, datacenter_list, datacenter)

    return servers_api.datacenters_servers_get(
        datacenter,
        upgrade_needed=upgrade_needed,
        depth=depth,
    )


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
