from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_container_registry
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s' % (
__version__, ionoscloud_container_registry.__version__)
DOC_DIRECTORY = 'container-registry'
STATES = ['info']
OBJECT_NAME = 'Registries'
RETURNED_KEY = 'registries'

OPTIONS = {
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: registry_info
short_description: List Registries
description:
     - This is a simple module that supports listing existing Registries
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-container-registry >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: List Registries
        registry_info:
        register: registries_response

    - name: Show Registries
        debug:
            var: registries_response.result
"""


def get_objects(module, client):
    return ionoscloud_container_registry.RegistriesApi(client).registries_get()

if __name__ == '__main__':
    default_main_info(
        ionoscloud_container_registry, 'ionoscloud_container_registry', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
