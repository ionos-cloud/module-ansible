from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info
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
OBJECT_NAME = 'Mongo Cluster Users'
RETURNED_KEY = 'mongo_clusters'

OPTIONS = {
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: mongo_cluster_info
short_description: List Mongo Cluster Users
description:
     - This is a simple module that supports listing existing the users in a Mongo Cluster
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
    - name: List Mongo Cluster Users
        mongo_cluster_user_info:
        register: mongo_cluster_users_response

    - name: Show Mongo Cluster Users
        debug:
            var: mongo_cluster_users_response.result
"""


def get_objects(module, client):    
    return ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mongo, 'ionoscloud_dbaas_mongo', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
