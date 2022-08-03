import re
import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['info']
OBJECT_NAME = 'Servers'

OPTIONS = {
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'upgrade_needed': {
        'description': ['Filter servers that can or that cannot be upgraded.'],
        'available': STATES,
        'type': 'bool',
    },
    'filters': {
        'description': [
            'Filter that can be used to list only objects which have a certain set of propeties. Filters '
            'should be a dict with a key containing keys and value pair in the following format:'
            "'properties.name': 'server_name'"
        ],
        'available': STATES,
        'type': 'dict',
    },
    'depth': {
        'description': ['The depth used when retrieving the items.'],
        'available': STATES,
        'type': 'int',
        'default': 1,
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
}


def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES)
    del val['available']
    del val['type']
    return val


DOCUMENTATION = '''
---
module: server_info
short_description: List Ionos Cloud servers of a given datacenter.
description:
     - This is a simple module that supports listing servers.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLES = '''
    - name: Get all servers for given datacenter
      server_info:
        datacenter: "{{ datacenter }}"
      register: server_list_response

    - name: Get only the servers that need to be upgraded
      server_info:
        datacenter: "{{ datacenter }}"
        upgrade_needed: true
      register: servers_list_upgrade_response

    - name: Show all servers for the created datacenter
      debug:
        var: server_list_response

    - name: Show servers that need an upgrade
      debug:
        var: servers_list_upgrade_response
'''

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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


def get_method_from_filter(filter):
    key, value = filter
    def method(item):
        current = item
        for key_part in key.split('.'):
            current = getattr(current, key_part)
        return current == value
    return method


def apply_filters_to_item(filter_list):
    def f(item):
        return all([f(item) for f in filter_list])
    return f


def apply_filters(module, item_list):
    filters = module.params.get('filters')
    if not filters:
        return item_list    
    filter_methods = list(map(get_method_from_filter, filters.items()))

    return filter(apply_filters_to_item(filter_methods), item_list)


def get_servers(module, client):
    datacenter = module.params.get('datacenter')
    servers_api = ionoscloud.ServersApi(client)
    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    upgrade_needed = module.params.get('upgrade_needed')
    depth = module.params.get('depth')

    # Locate UUID for Datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=1)
    datacenter = get_resource_id(module, datacenter_list, datacenter)

    try:
        server_items = servers_api.datacenters_servers_get(
            datacenter,
            upgrade_needed=upgrade_needed,
            depth=depth,
        )
        results = list(map(lambda x: x.to_dict(), apply_filters(module, server_items.items)))

        return {
            'action': 'info',
            'changed': False,
            'servers': results
        }

    except Exception as e:
        module.fail_json(msg="failed to list the servers: %s" % to_native(e))


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
    api_url = module.params.get('api_url')
    token = module.params.get('token')

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


def check_required_arguments(module, object_name):
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
        if 'info' in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for retrieving {object_name}'.format(
                    option_name=option_name,
                    object_name=object_name,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, OBJECT_NAME)

        try:
            module.exit_json(**get_servers(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME,
                                                                                             error=to_native(e),
                                                                                             state=state))


if __name__ == '__main__':
    main()
