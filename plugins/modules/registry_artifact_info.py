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
    registry:
        description:
        - The ID or name of an existing Registry.
        required: true
    repository:
        description:
        - The name of an existing Repository.
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
