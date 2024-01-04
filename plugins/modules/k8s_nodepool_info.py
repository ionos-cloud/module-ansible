HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options_with_depth


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['info']
OBJECT_NAME = 'K8s Nodepools'
RETURNED_KEY = 'nodepools'

OPTIONS = {
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_info_default_options_with_depth(STATES),
}

DOCUMENTATION = """
module: k8s_nodepool_info
short_description: List Ionos Cloud k8s nodepools.
description:
     - This is a simple module that supports listing k8s nodepools.
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all k8s nodepools in a cluster
      k8s_nodepool_info:
      register: k8s_nodepool_list_response
"""


def get_objects(module, client):
    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    # Locate UUID for the cluster
    cluster_list = k8s_api.k8s_get(depth=1)
    k8s_cluster_id = get_resource_id(module, cluster_list, module.params.get('k8s_cluster'))

    return k8s_api.k8s_nodepools_get(k8s_cluster_id, depth=module.params.get('depth'))


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )