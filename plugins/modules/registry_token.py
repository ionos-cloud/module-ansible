import copy
from distutils.command.config import config
from operator import mod
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

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

CONTAINER_REGISTRY_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s'% (
    __version__, ionoscloud_container_registry.__version__,
)
DOC_DIRECTORY = 'container-registry'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Registry Token'


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
        'available': ['present', 'update', 'absent'],
        'required': ['present'],
        'type': 'str',
    },
    'token_id': {
        'description': ['The ID of an existing token.'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'registry_id': {
        'description': ['The ID of an existing Registry.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'required': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}


def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES)
    del val['available']
    del val['type']
    return val


DOCUMENTATION = '''
---
module: registry_token
short_description: Allows operations with Ionos Cloud Registry Tokens.
description:
     - This is a module that supports creating, updating or destroying Registry Tokens
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-container-registry >= 1.0.1"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Registry Token
    registry_token:
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
        name: test_registry_token
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
        name: test_registry_token
        state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None

def scope_dict_to_object(scope_dict):
    return ionoscloud_container_registry.Scope(
        actions=scope_dict['actions'],
        name=scope_dict['name'],
        type=scope_dict['type'],
    )

def create_registry_token(module, container_registry_client):
    name = module.params.get('name')
    registry_id = module.params.get('registry_id')

    tokens_server = ionoscloud_container_registry.TokensApi(container_registry_client)

    tokens_list = tokens_server.registries_tokens_get(registry_id)

    existing_token_by_name = get_resource(module, tokens_list, name)

    if existing_token_by_name is not None:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'token': existing_token_by_name.to_dict(),
        }

    registry_properties = ionoscloud_container_registry.PostRegistryProperties(
        name=name,
        expiry_date=module.params.get('expiry_date'),
        status=module.params.get('status'),
        scopes=list(map(scope_dict_to_object, module.params.get('scopes'))),
    )

    token = ionoscloud_container_registry.PostRegistryInput(properties=registry_properties)

    try:
        token = tokens_server.registries_tokens_post(registry_id, token)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'token': token.to_dict(),
        }
    except Exception as e:
        module.fail_json(msg="failed to create the Token: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create',
        }


def delete_registry_token(module, container_registry_client):
    tokens_server = ionoscloud_container_registry.TokensApi(container_registry_client)

    registry_id = module.params.get('registry_id')
    token_id = module.params.get('token_id')
    token_name = module.params.get('name')

    tokens_list = tokens_server.registries_tokens_get(registry_id)


    if token_id:
        token = get_resource(module, tokens_list, token_id)
    else:
        token = get_resource(module, tokens_list, token_name)

    try:
        tokens_server.registries_tokens_delete(registry_id, token.id)

        return {
            'action': 'delete',
            'changed': True,
            'id': token.id,
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the Token: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': token.id,
        }


def update_registry_token(module, container_registry_client):
    tokens_server = ionoscloud_container_registry.TokensApi(container_registry_client)

    registry_id = module.params.get('registry_id')
    token_id = module.params.get('token_id')
    token_name = module.params.get('name')

    tokens_list = tokens_server.registries_tokens_get(registry_id)

    if token_id:
        token = get_resource(module, tokens_list, token_id)
    else:
        token = get_resource(module, tokens_list, token_name)

    token_properties = ionoscloud_container_registry.PatchTokenInput(
        expiry_date=module.params.get('expiry_date'),
        status=module.params.get('status'),
        scopes=list(map(scope_dict_to_object, module.params.get('scopes'))),
    )

    try:
        token = tokens_server.registries_patch(
            registry_id=registry_id,
            token_id=token.id,
            patch_registry_input=token_properties,
        )

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'token': token.to_dict(),
        }

    except Exception as e:
        module.fail_json(msg="failed to update the Token: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
        }


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
        arguments[option_name] = {
            'type': option['type'],
        }
        for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
            if option.get(key) is not None:
                arguments[option_name][key] = option.get(key)

        if option.get('env_fallback'):
            arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

        if len(option.get('required', [])) == len(STATES):
            arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_container_registry is required for this module, '
                             'run `pip install ionoscloud_container_registry`')

    container_registry_api_client = ionoscloud_container_registry.ApiClient(get_sdk_config(module, ionoscloud_container_registry))
    container_registry_api_client.user_agent = CONTAINER_REGISTRY_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_registry_token(module, container_registry_api_client))
        elif state == 'absent':
            module.exit_json(**delete_registry_token(module, container_registry_api_client))
        elif state == 'update':
            module.exit_json(**update_registry_token(module, container_registry_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e),
                                                                            state=state))


if __name__ == '__main__':
    main()
