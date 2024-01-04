from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dbaas_mongo
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dbaas-mongo/%s' % (
    __version__, ionoscloud_dbaas_mongo.__version__)
DOC_DIRECTORY = 'dbaas-mongo'
STATES = ['info']
OBJECT_NAME = 'Mongo Clusters'
RETURNED_KEY = 'mongo_cluster_users'

OPTIONS = {
    'mongo_cluster': {
        'description': ['The UUID or name of an existing Mongo Cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: mongo_cluster_info
short_description: List Mongo Clusters
description:
     - This is a simple module that supports listing existing Mongo Clusters
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-dbaas-mongo >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List Mongo Clusters
        mongo_cluster_info:
        register: mongo_clusters_response

    - name: Show Mongo Clusters
        debug:
            var: mongo_clusters_response.result
"""


def get_objects(module, client):
    mongo_cluster_id = get_resource_id(
        module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
        module.params.get('mongo_cluster'),
        [['id'], ['properties', 'display_name']],
    )
    return ionoscloud_dbaas_mongo.UsersApi(client).clusters_users_get(mongo_cluster_id)


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mongo, 'ionoscloud_dbaas_mongo', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
