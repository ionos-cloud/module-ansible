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
OBJECT_NAME = 'Postgres Cluster Backups'
RETURNED_KEY = 'postgres_backups'

OPTIONS = {
    'postgres_cluster': {
        'description': ['The ID or name of an existing Postgres Cluster.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: postgres_backup_info
short_description: List Postgres Cluster backups.
description:
     - This is a simple module that supports listing existing Postgres Cluster backups
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-dbaas-postgres >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List Postgres Cluster Backups
        postgres_cluster_info:
            postgres_cluster: backuptest-04
        register: postgres_clusters_response

    - name: Show Postgres Cluster Backups
        debug:
            var: postgres_clusters_response.result
"""


def get_objects(module, client):
    backups_api = ionoscloud_dbaas_postgres.BackupsApi(client)
    postgres_cluster = module.params.get('postgres_cluster')

    if postgres_cluster:
        postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)
        postgres_cluster_id = get_resource_id(
            module,
            postgres_cluster_server.clusters_get(),
            postgres_cluster,
            [['id'], ['properties', 'display_name']],
        )

        backups = backups_api.cluster_backups_get(postgres_cluster_id)
    else:
        backups = backups_api.clusters_backups_get()
    return backups


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_postgres, 'ionoscloud_dbaas_postgres', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
