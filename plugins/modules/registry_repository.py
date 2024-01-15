from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_container_registry
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s'% (
    __version__, ionoscloud_container_registry.__version__,
)
DOC_DIRECTORY = 'container-registry'
STATES = ['absent']
OBJECT_NAME = 'Repository'
RETURNED_KEY = 'repository'


OPTIONS = {
    'repository': {
        'description': ['The name of an existing repository.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'registry': {
        'description': ['The ID or name of an existing Registry.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: registry_repository
short_description: Allows operations with Repositories.
description:
     - This is a module that supports creating, updating or destroying Repositories
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-container-registry >= 1.0.1"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'absent': '''- name: Delete Repository
    registry_repository:
        registry: RegistryName
        repository: testRepository
        state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class RepositoryModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_container_registry]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return False


    def _get_object_list(self, clients):
        client = clients[0]
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )
        return ionoscloud_container_registry.RepositoriesApi(client).registries_repositories_get(registry_id)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('repository')


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )
        repositories_api = ionoscloud_container_registry.RepositoriesApi(client)

        try:
            repositories_api.registries_repositories_delete(registry_id, existing_object.id)
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to remove the Repository: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = RepositoryModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_container_registry is required for this module, run `pip install ionoscloud_container_registry`')
    ionos_module.main()
