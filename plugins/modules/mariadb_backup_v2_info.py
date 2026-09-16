from ansible import __version__
from functools import partial

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id, get_paginated
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dbaas_mariadb
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-mariadb/%s' % (
    __version__, ionoscloud_dbaas_mariadb.__version__)
DOC_DIRECTORY = 'dbaas-mariadb'
STATES = ['info']
OBJECT_NAME = 'MariaDB Cluster Backups (v2)'
RETURNED_KEY = 'mariadb_backups'

OPTIONS = {
    'mariadb_cluster': {
        'description': ['The ID or name of an existing MariaDB Cluster. If set, only backups belonging to this cluster are returned.'],
        'available': STATES,
        'type': 'str',
    },
    'location': {
        'description': ['The location (region) whose regional endpoint will be queried. Possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/txl". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: mariadb_backup_v2_info
short_description: List MariaDB Cluster backups (DBaaS MariaDB v2 API)
description:
     - This is a simple module that supports listing existing MariaDB Cluster backups using
       the DBaaS MariaDB v2 API. There is no per-cluster backups endpoint, so when
       I(mariadb_cluster) is provided the account-wide backup list is filtered by cluster id
       server-side via the API's filter parameter.
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
        - 'Filter that can be used to list only objects which have a certain set of properties.
            Filters should be a dict with a key containing keys and value pair in the
            following format: ''properties.name'': ''server_name'''
        required: false
    location:
        description:
        - 'The location (region) whose regional endpoint will be queried. Possible options
            are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr",
            "us/las", "us/mci". If not set, the endpoint will be the one corresponding
            to "de/txl". The api_url, if set, overrides this.'
        required: false
    mariadb_cluster:
        description:
        - The ID or name of an existing MariaDB Cluster. If set, only backups belonging
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
    - "ionoscloud-dbaas-mariadb >= 3.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
name: List MariaDB Cluster Backups (all)
ionoscloudsdk.ionoscloud.mariadb_backup_v2_info:
  location: 'de/fra'
register: mariadb_backup_response
"""


def get_objects(module, client):
    backups_api = ionoscloud_dbaas_mariadb.BackupsApi(client)
    mariadb_cluster = module.params.get('mariadb_cluster')

    if mariadb_cluster:
        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(client)
        mariadb_cluster_id = get_resource_id(
            module,
            get_paginated(clusters_api.clusters_get, depth=None),
            mariadb_cluster,
            [['id'], ['properties', 'name']],
            fail_not_found=True,
        )
        return get_paginated(
            partial(backups_api.backups_get, filter_cluster_id=mariadb_cluster_id),
            depth=None,
        )

    return get_paginated(backups_api.backups_get, depth=None)


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mariadb, 'ionoscloud_dbaas_mariadb', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
