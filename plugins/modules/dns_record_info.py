HAS_SDK = True
try:
    import ionoscloud_dns
    from ionoscloud_dns import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dns/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'dns'
STATES = ['info']
OBJECT_NAME = 'DNS Records'
RETURNED_KEY = 'records'

OPTIONS = {
    'zone': {
        'description': ['The ID or name of an existing Zone. Will be prioritized if both this and secondary_zone are set.'],
        'available': STATES,
        'type': 'str',
    },
    'secondary_zone': {
        'description': ['The ID or name of an existing Secondary Zone.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: dns_record_info
short_description: List Ionos Cloud DNS Records.
description:
     - This is a simple module that supports listing DNS Records.
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
    secondary_zone:
        description:
        - The ID or name of an existing Secondary Zone.
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
    zone:
        description:
        - The ID or name of an existing Zone. Will be prioritized if both this and secondary_zone
            are set.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all DNS Records
      dns_record_info:
      register: dns_record_list_response

    - name: Get all DNS Records in a Zone
      dns_record_info:
        zone: example.com
      register: dns_record_list_response

    - name: Get all DNS Records in a Secondary Zone
      dns_record_info:
        secondary_zone: example.com
      register: dns_record_list_response
"""


def get_objects(module, client):
    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )
    secondary_zone_id = get_resource_id(
        module, ionoscloud_dns.SecondaryZonesApi(client).secondaryzones_get(),
        module.params.get('secondary_zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )
    if zone_id:
        dns_records = ionoscloud_dns.RecordsApi(client).zones_records_get(zone_id=zone_id)
    elif secondary_zone_id:
        dns_records = ionoscloud_dns.RecordsApi(client).secondaryzones_records_get(secondary_zone_id)
    else:
        dns_records = ionoscloud_dns.RecordsApi(client).records_get()

    return dns_records


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dns, 'ionoscloud_dns', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
