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
CONTAINER_REGISTRY_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s' % (
__version__, ionoscloud_container_registry.__version__)
DOC_DIRECTORY = 'container-registry'
STATES = ['info']
OBJECT_NAME = 'Repositories'
RETURNED_KEY = 'repositories'

OPTIONS = {
    'registry': {
        'description': ['The ID or name of an existing Registry.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: registry_repository_info
short_description: List Repositories
description:
     - This is a simple module that supports listing existing Repositories
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
    - name: List Repositories
        registry_repository_info:
            registry: "RegistryName"
        register: repositories_response


    - name: Show Repositories
        debug:
            var: repositories_response.result
"""


def get_objects(module, client):
    registry_id = get_resource_id(
        module, 
        ionoscloud_container_registry.RegistriesApi(client).registries_get(),
        module.params.get('registry'),
    )
    return ionoscloud_container_registry.RepositoriesApi(client).registries_repositories_get(registry_id)

if __name__ == '__main__':
    default_main_info(
        ionoscloud_container_registry, 'ionoscloud_container_registry', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
