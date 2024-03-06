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
OBJECT_NAME = 'DataPlatform Clusters'
RETURNED_KEY = 'dataplatform_clusters'


OPTIONS = {
    **get_info_default_options(STATES),
}



DOCUMENTATION = """
module: dataplatform_cluster_info
short_description: List DataPlatform Clusters
description:
     - This is a simple module that supports listing existing DataPlatform Clusters
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

EXAMPLES = """name: Get all Data Platform clusters
ionoscloudsdk.ionoscloud.dataplatform_cluster_info: null
register: cluster_list_response
"""


def get_objects(module, client):
    return ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dataplatform, 'ionoscloud_dataplatform', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
