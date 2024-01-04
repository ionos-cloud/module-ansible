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
OBJECT_NAME = 'Mongo Cluster Templates'
RETURNED_KEY = 'mongo_cluster_templates'

OPTIONS = {
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: mongo_cluster_template_info
short_description: List Mongo Cluster Templates
description:
     - This is a simple module that supports listing existing Mongo Cluster Templates
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
    - name: List Mongo Cluster Templates
        mongo_cluster_templates_info:
        register: mongo_cluster_templates_response

    - name: Show Mongo Cluster Templates
        debug:
            var: mongo_cluster_templates_response.result
"""


def get_objects(module, client):
    return ionoscloud_dbaas_mongo.TemplatesApi(client).templates_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_mongo, 'ionoscloud_dbaas_mongo', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )