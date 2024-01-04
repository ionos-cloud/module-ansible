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
OBJECT_NAME = 'Artifacts'
RETURNED_KEY = 'artifacts'

OPTIONS = {
    'registry': {
        'description': ['The ID or name of an existing Registry.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'repository': {
        'description': ['The name of an existing Repository.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: registry_artifact_info
short_description: List Artifacts
description:
     - This is a simple module that supports listing existing Artifacts
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
    - name: List Artifacts
        registry_artifact_info:
            registry: "RegistryName"
            repository: "repositoryName"
        register: artifacts_response

    - name: Show Artifacts
        debug:
            var: artifacts_response.result
"""


def get_objects(module, client):
    registry_id = get_resource_id(
        module, 
        ionoscloud_container_registry.RegistriesApi(client).registries_get(),
        module.params.get('registry'),
    )
    if module.params.get('repository'):
        artifacts = ionoscloud_container_registry.ArtifactsApi(client).registries_repositories_artifacts_get(
            registry_id,
            module.params.get('repository'),
        )
    else:
        artifacts = ionoscloud_container_registry.ArtifactsApi(client).registries_artifacts_get(
            registry_id,
        )

    return artifacts


if __name__ == '__main__':
    default_main_info(
        ionoscloud_container_registry, 'ionoscloud_container_registry', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
