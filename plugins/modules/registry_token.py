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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s'% (
    __version__, ionoscloud_container_registry.__version__,
)
DOC_DIRECTORY = 'container-registry'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Registry Token'
RETURNED_KEY = 'registry_token'


OPTIONS = {
    'scopes': {
        'description': ['List of scopes for the token'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'expiry_date': {
        'description': ['The expiry date for the token in iso format'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'status': {
        'description': ['The status of the token'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of your token.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'registry_token': {
        'description': ['The ID or name of an existing token.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'registry': {
        'description': ['The ID or name of an existing Registry.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "name", "note": "" },
]


DOCUMENTATION = """
module: registry_token
short_description: Allows operations with Ionos Cloud Registry Tokens.
description:
     - This is a module that supports creating, updating or destroying Registry Tokens
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
    'present': '''- name: Create Registry Token
    registry_token:
        registry: RegistryName
        name: test_registry_token
        scopes:
            - actions: 
                    - pull
                      push
                      delete
                name: repo1
                type: repositry
        status: enabled
        expiry_date: 2022-06-24T17:04:10+03:00
    register: registry_token_response
  ''',
    'update': '''- name: Update Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        scopes:
            - actions: 
                    - pull
                name: repo2
                type: repositry
        status: disbled
        expiry_date: 2022-07-24T17:04:10+03:00
    register: updated_registry_token_response
  ''',
    'absent': '''- name: Delete Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


def scope_dict_to_object(scope_dict):
    return ionoscloud_container_registry.Scope(
        actions=scope_dict['actions'],
        name=scope_dict['name'],
        type=scope_dict['type'],
    )


class RegistryTokenModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_container_registry]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
        )


    def _should_update_object(self, existing_object, clients):
        existing_scopes=list(map(scope_dict_to_object, self.module.params.get('scopes'))),

        def sort_func(el):
            return el['name'], el['type']

        if self.module.params.get('scopes'):
            existing_scopes = sorted(map(
                lambda x: {
                    'name': x.name,
                    'type': x.type,
                    'actions': sorted(x.actions),
                },
                existing_object.properties.scopes
            ), key=sort_func)
            new_scopes = sorted(self.module.params.get('scopes'), key=sort_func)
            for new_scope in new_scopes:
                if new_scope.get('actions'):
                    new_scope['actions'] = sorted(new_scope['actions'])

        return (
            self.module.params.get('expiry_date') is not None
            and existing_object.properties.expiry_date != self.module.params.get('expiry_date')
            or self.module.params.get('status') is not None
            and existing_object.properties.status != self.module.params.get('status')
            or self.module.params.get('scopes') is not None
            and new_scopes != existing_scopes
        )


    def _get_object_list(self, clients):
        client = clients[0]
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )
        return ionoscloud_container_registry.TokensApi(client).registries_tokens_get(registry_id)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('registry_token')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        expiry_date = self.module.params.get('expiry_date')
        status = self.module.params.get('status')
        name = self.module.params.get('name')
        scopes = list(map(scope_dict_to_object, self.module.params.get('scopes')))
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            expiry_date = existing_object.properties.expiry_date if expiry_date is None else expiry_date
            status = existing_object.properties.status if status is None else status
            scopes = existing_object.properties.scopes if scopes is None else scopes

        tokens_api = ionoscloud_container_registry.TokensApi(client)

        registry_properties = ionoscloud_container_registry.PostTokenProperties(
            name=name,
            expiry_date=self.module.params.get('expiry_date'),
            status=self.module.params.get('status'),
            scopes=list(map(scope_dict_to_object, self.module.params.get('scopes'))),
        )

        token = ionoscloud_container_registry.PostTokenInput(properties=registry_properties)

        try:
            token = tokens_api.registries_tokens_post(registry_id, token)
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to create the new Registry Token: %s" % to_native(e))
        return token


    def _update_object(self, existing_object, clients):
        client = clients[0]
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )

        tokens_api = ionoscloud_container_registry.TokensApi(client)
        
        token_properties = ionoscloud_container_registry.PatchTokenInput(
            expiry_date=self.module.params.get('expiry_date'),
            status=self.module.params.get('status'),
            scopes=list(map(scope_dict_to_object, self.module.params.get('scopes'))),
        )

        try:
            token = tokens_api.registries_tokens_patch(
                registry_id=registry_id,
                token_id=existing_object.id,
                patch_token_input=token_properties,
            )

            return token
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to update the Registry Token: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        registry_id = get_resource_id(
            self.module, 
            ionoscloud_container_registry.RegistriesApi(client).registries_get(),
            self.module.params.get('registry'),
        )
        tokens_api = ionoscloud_container_registry.TokensApi(client)

        try:
            tokens_api.registries_tokens_delete(registry_id, existing_object.id)
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to remove the Registry Token: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = RegistryTokenModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_container_registry is required for this module, run `pip install ionoscloud_container_registry`')
    ionos_module.main()
