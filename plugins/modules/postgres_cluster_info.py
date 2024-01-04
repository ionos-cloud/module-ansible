from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-postgres/%s' % (
    __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['info']
OBJECT_NAME = 'Postgres Clusters'
RETURNED_KEY = 'postgres_clusters'

OPTIONS = {
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: postgres_cluster_info
short_description: List Postgres Clusters
description:
     - This is a simple module that supports listing existing Postgres Clusters
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-dbaas-postgres >= 1.0.1"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List Postgres Clusters
        postgres_cluster_info:
        register: postgres_clusters_response

    - name: Show Postgres Clusters
        debug:
            var: postgres_clusters_response.result
"""


def get_objects(module, client):
    return ionoscloud_dbaas_postgres.ClustersApi(client).clusters_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_postgres, 'ionoscloud_dbaas_postgres', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
