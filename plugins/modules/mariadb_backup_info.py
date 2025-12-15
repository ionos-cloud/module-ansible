from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
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
OBJECT_NAME = 'MariaDB Cluster Backups'
RETURNED_KEY = 'mariadb_backups'

OPTIONS = {
    'mariadb_cluster': {
        'description': ['The ID or name of an existing MariaDB Cluster.'],
        'available': STATES,
        'type': 'str',
    },
    'location': {
        'description': ['The location from which to retrieve clusters and backups. Different service endpoints are used based on location, possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/txl".'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: mariadb_backup_info
short_description: List MariaDB Cluster backups.
description:
     - This is a simple module that supports listing existing MariaDB Cluster backups
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
        - 'The location from which to retrieve clusters and backups. Different service
            endpoints are used based on location, possible options are: "de/fra", "de/txl",
            "es/vit", "fr/par", "gb/lhr", "us/ewr", "us/las", "us/mci". If not set, the
            endpoint will be the one corresponding to "de/txl".'
        required: false
    mariadb_cluster:
        description:
        - The ID or name of an existing MariaDB Cluster.
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
    - "python >= 2.6"
    - "ionoscloud-dbaas-mariadb >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List MariaDB Cluster Backups
        mariadb_cluster_backup_info:
            mariadb_cluster: backuptest-04
        register: mariadb_backups_response

    - name: Show MariaDB Cluster Backups
        debug:
            var: mariadb_backups_response.result
"""


def get_objects(module, client):
    backups_api = ionoscloud_dbaas_mariadb.BackupsApi(client)
    mariadb_cluster = module.params.get('mariadb_cluster')

    if mariadb_cluster:
        mariadb_clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(client)
        mariadb_cluster_id = get_resource_id(
            module,
            mariadb_clusters_api.clusters_get(),
            mariadb_cluster,
            [['id'], ['properties', 'display_name']],
        )

        backups = backups_api.cluster_backups_get(mariadb_cluster_id)
    else:
        backups = backups_api.backups_get()
    return backups


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mariadb, 'ionoscloud_dbaas_mariadb', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
