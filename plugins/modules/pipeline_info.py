from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_logging
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-logging/%s' % (
__version__, ionoscloud_logging.__version__)
DOC_DIRECTORY = 'logging'
STATES = ['info']
OBJECT_NAME = 'Pipelines'
RETURNED_KEY = 'pipelines'

OPTIONS = {
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: pipeline_info
short_description: List Pipelines
description:
     - This is a simple module that supports listing existing Pipelines
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-logging >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List Pipelines
        pipeline_info:
        register: pipelines_response

    - name: Show Pipelines
        debug:
            var: pipelines_response.result
"""


def get_objects(module, client):
    return ionoscloud_logging.PipelinesApi(client).pipelines_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_logging, 'ionoscloud_logging', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
