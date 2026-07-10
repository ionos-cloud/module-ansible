from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_paginated
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dbaas_inmemorydb
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-in-memory-db/%s' % (
    __version__, ionoscloud_dbaas_inmemorydb.__version__)
DOC_DIRECTORY = 'dbaas-in-memory-db'
STATES = ['info']
OBJECT_NAME = 'In-Memory DB Snapshot Locations (v2)'
RETURNED_KEY = 'inmemorydb_snapshot_locations'

OPTIONS = {
    'location': {
        'description': ['The location (region) whose regional endpoint will be queried. Possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/fra". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: inmemorydb_snapshot_location_v2_info
short_description: List In-Memory DB snapshot locations (DBaaS In-Memory DB v2 API)
description:
     - This is a simple module that supports listing the Object Storage locations supported for
       In-Memory DB snapshots using the DBaaS In-Memory DB v2 API. The region is selected through
       the I(location) option; set I(api_url) (e.g. C(https://in-memory-db.de-fra.ionos.com/v2))
       to override it directly.
version_added: "2.0"
options:
    location:
        description:
        - 'The location (region) whose regional endpoint will be queried. Possible options
            are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr",
            "us/las", "us/mci". If not set, the endpoint will be the one corresponding to
            "de/fra". The api_url, if set, overrides this.'
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
    filters:
        description:
        - 'Filter that can be used to list only objects which have a certain set of properties.
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
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
requirements:
    - "python >= 3.8"
    - "ionoscloud-dbaas-inmemorydb >= 1.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
name: List In-Memory DB Snapshot Locations
ionoscloudsdk.ionoscloud.inmemorydb_snapshot_location_v2_info:
  location: ''
register: inmemorydb_snapshot_locations_response
"""


def get_objects(module, client):
    return get_paginated(ionoscloud_dbaas_inmemorydb.SnapshotLocationsApi(client).snapshotlocations_get, depth=None)


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_inmemorydb, 'ionoscloud_dbaas_inmemorydb', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
