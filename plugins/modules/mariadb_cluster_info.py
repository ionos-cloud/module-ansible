from ansible import __version__

from ..module_utils.common_ionos_methods import default_main_info
from ..module_utils.common_ionos_options import get_info_default_options


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
OBJECT_NAME = 'MariaDB Clusters'
RETURNED_KEY = 'mariadb_clusters'

OPTIONS = {
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: mariadb_cluster_info
short_description: List MariaDB Clusters
description:
     - This is a simple module that supports listing existing MariaDB Clusters
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
    - "ionoscloud-dbaas-mariadb >= 1.0.1"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List MariaDB Clusters
        mariadb_cluster_info:
        register: mariadb_clusters_response

    - name: Show MariaDB Clusters
        debug:
            var: mariadb_clusters_response.result
"""


def get_objects(module, client):
    return ionoscloud_dbaas_mariadb.ClustersApi(client).clusters_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mariadb, 'ionoscloud_dbaas_mariadb', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
