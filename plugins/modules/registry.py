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

CONTAINER_REGISTRY_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s'% (
    __version__, ionoscloud_container_registry.__version__,
)
DOC_DIRECTORY = 'container-registry'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Registry'

OPTIONS = {
    'maintenance_window': {
        'description': [
            'Dict containing "time" (the time of the day when to perform the maintenance) '
            'and "days" (the days when to perform the maintenance).',
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'garbage_collection_schedule': {
        'description': [
            'Dict containing "time" (the time of the day when to perform the garbage_collection) '
            'and "days" (the days when to perform the garbage_collection).',
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'location': {
        'description': ['The location of your registry'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of your registry.'],
        'available': ['present', 'update', 'absent'],
        'required': ['present'],
        'type': 'str',
    },
    'registry_id': {
        'description': ['The ID of an existing Registry.'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
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
module: registry
short_description: Allows operations with Ionos Cloud Registries.
description:
     - This is a module that supports creating, updating or destroying Registries
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-container-registry >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Registry
    registry:
      name: test_registry
      location: es/vit
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: registry_response
  ''',
    'update': '''- name: Update Registry
    registry:
      name: test_registry
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: updated_registry_response
  ''',
    'absent': '''- name: Delete Registry
    registry:
      name: test_registry
      wait: true
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


def create_registry(module, container_registry_client):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = ionoscloud_container_registry.WeeklySchedule(
            days=maintenance_window.pop('days'),
            time=maintenance_window.pop('time'),
        )

    garbage_collection_schedule = module.params.get('garbage_collection_schedule')
    if garbage_collection_schedule:
        garbage_collection_schedule = ionoscloud_container_registry.WeeklySchedule(
            days=garbage_collection_schedule.pop('days'),
            time=garbage_collection_schedule.pop('time'),
        )
    name = module.params.get('name')
    location = module.params.get('location')

    registries_server = ionoscloud_container_registry.RegistriesApi(container_registry_client)

    registries_list = registries_server.registries_get()

    existing_registry_by_name = get_resource(module, registries_list, name)

    if existing_registry_by_name is not None:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'registry': existing_registry_by_name.to_dict(),
        }

    registry_properties = ionoscloud_container_registry.PostRegistryProperties(
        name=name,
        location=location,
        garbage_collection_schedule=garbage_collection_schedule,
        maintenance_window=maintenance_window,
    )

    registry = ionoscloud_container_registry.PostRegistryInput(properties=registry_properties)

    try:
        registry = registries_server.registries_post(registry)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'registry': registry.to_dict(),
        }
    except Exception as e:
        module.fail_json(msg="failed to create the Registry: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create',
        }


def delete_registry(module, container_registry_client):
    registries_server = ionoscloud_container_registry.RegistriesApi(container_registry_client)
    names_server = ionoscloud_container_registry.NamesApi(container_registry_client)

    registry_id = module.params.get('registry_id')
    registry_name = module.params.get('name')

    registries_list = registries_server.registries_get()

    if registry_id:
        registry = get_resource(module, registries_list, registry_id)
    else:
        registry = get_resource(module, registries_list, registry_name)

    try:
        registries_server.registries_delete(registry.id)

        if module.params.get('wait'):
            try:
                container_registry_client.wait_for(
                    fn_request=lambda: names_server.names_find_by_name(registry.properties.name),
                    fn_check=lambda _: False,
                    scaleup=10000,
                )
            except ionoscloud_container_registry.ApiException as e:
                if e.status != 404:
                    raise e

        return {
            'action': 'delete',
            'changed': True,
            'id': registry.id,
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the Registry: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': registry.id,
        }


def update_registry(module, container_registry_client):
    registries_server = ionoscloud_container_registry.RegistriesApi(container_registry_client)

    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(maintenance_window)
        maintenance_window['days'] = maintenance_window.pop('days')
        maintenance_window['time'] = maintenance_window.pop('time')

    garbage_collection_schedule = module.params.get('garbage_collection_schedule')
    if garbage_collection_schedule:
        garbage_collection_schedule = dict(garbage_collection_schedule)
        garbage_collection_schedule['days'] = garbage_collection_schedule.pop('days')
        garbage_collection_schedule['time'] = garbage_collection_schedule.pop('time')

    registry_id = module.params.get('registry_id')
    registry_name = module.params.get('name')

    registries_list = registries_server.registries_get()

    if registry_id:
        registry = get_resource(module, registries_list, registry_id)
    else:
        registry = get_resource(module, registries_list, registry_name)

    registry_properties = ionoscloud_container_registry.PatchRegistryInput(
        garbage_collection_schedule=garbage_collection_schedule,
        maintenance_window=maintenance_window,
    )

    try:
        registry = registries_server.registries_patch(
            registry_id=registry.id,
            patch_registry_input=registry_properties,
        )

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'registry': registry.to_dict(),
        }

    except Exception as e:
        module.fail_json(msg="failed to update the Registry: %s" % to_native(e))
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
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name}'.format(
                object_name=object_name,
            ),
        )
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
            module.exit_json(**create_registry(module, container_registry_api_client))
        elif state == 'absent':
            module.exit_json(**delete_registry(module, container_registry_api_client))
        elif state == 'update':
            module.exit_json(**update_registry(module, container_registry_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e),
                                                                            state=state))


if __name__ == '__main__':
    main()
