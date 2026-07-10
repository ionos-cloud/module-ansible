from ansible import __version__
from functools import partial

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id, get_paginated
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
OBJECT_NAME = 'In-Memory DB Cluster Snapshots (v2)'
RETURNED_KEY = 'inmemorydb_snapshots'

OPTIONS = {
    'inmemorydb_cluster': {
        'description': ['The ID or name of an existing In-Memory DB Cluster. If set, only snapshots belonging to this cluster are returned.'],
        'available': STATES,
        'type': 'str',
    },
    'location': {
        'description': ['The location (region) whose regional endpoint will be queried. Possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/fra". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: inmemorydb_snapshot_v2_info
short_description: List In-Memory DB Cluster snapshots (DBaaS In-Memory DB v2 API)
description:
     - This is a simple module that supports listing existing In-Memory DB Cluster snapshots using
       the DBaaS In-Memory DB v2 API. There is no per-cluster snapshots endpoint, so when
       I(inmemorydb_cluster) is provided the account-wide snapshot list is filtered by cluster id
       server-side via the API's filter parameter.
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
    inmemorydb_cluster:
        description:
        - The ID or name of an existing In-Memory DB Cluster. If set, only snapshots belonging
            to this cluster are returned.
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
name: List In-Memory DB Cluster Snapshots (all)
ionoscloudsdk.ionoscloud.inmemorydb_snapshot_v2_info:
  location: ''
register: inmemorydb_snapshot_response
"""


def get_objects(module, client):
    snapshots_api = ionoscloud_dbaas_inmemorydb.SnapshotsApi(client)
    inmemorydb_cluster = module.params.get('inmemorydb_cluster')

    if inmemorydb_cluster:
        clusters_api = ionoscloud_dbaas_inmemorydb.ClustersApi(client)
        inmemorydb_cluster_id = get_resource_id(
            module,
            get_paginated(clusters_api.clusters_get, depth=None),
            inmemorydb_cluster,
            [['id'], ['properties', 'name']],
            fail_not_found=True,
        )
        return get_paginated(
            partial(snapshots_api.snapshots_get, filter_cluster_id=inmemorydb_cluster_id),
            depth=None,
        )

    return get_paginated(snapshots_api.snapshots_get, depth=None)


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_inmemorydb, 'ionoscloud_dbaas_inmemorydb', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
