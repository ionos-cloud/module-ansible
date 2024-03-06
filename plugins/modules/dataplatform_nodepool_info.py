from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dataplatform
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (
    __version__, ionoscloud_dataplatform.__version__)
DOC_DIRECTORY = 'dataplatform'
STATES = ['info']
OBJECT_NAME = 'DataPlatform Nodepools'
RETURNED_KEY = 'dataplatform_nodepools'


OPTIONS = { 
    'cluster': {
        'description': ['The ID of the Data Platform cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: dataplatform_nodepool_info
short_description: List DataPlatform Nodepools
description:
     - This is a simple module that supports listing existing DataPlatform Nodepools
     - ⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.
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
    cluster:
        description:
        - The ID of the Data Platform cluster.
        required: true
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
    - "ionoscloud-dataplatform >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """name: Get all DataPlaform nodepools from a specific cluster
ionoscloudsdk.ionoscloud.dataplatform_nodepool_info:
  cluster: ''
register: nodepool_list_response
"""


def get_objects(module, client):
    cluster = module.params.get('cluster')
    dataplatform_clusters = ionoscloud_dataplatform.DataPlatformClusterApi(
        api_client=client).get_clusters()
    dataplatform_cluster_id = get_resource_id(module, dataplatform_clusters, cluster, [['id'], ['properties', 'name']])
    if dataplatform_cluster_id is None:
        module.fail_json(msg="Could not find Data Platform cluster '{}'".format(cluster))

    return ionoscloud_dataplatform.DataPlatformNodePoolApi(client).get_cluster_nodepools(
            cluster_id=dataplatform_cluster_id)


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dataplatform, 'ionoscloud_dataplatform', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
