import re

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


#######################################################
# Methods used to search for a resource inside a list #
#######################################################

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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def get_users(api, all_users, depth=2):
    offset = 0
    limit = 100

    users = api.um_users_get(depth=depth, limit=limit, offset=offset)
    all_users.items += users.items
    while(users.links.next is not None):
        offset += limit
        users = api.um_users_get(depth=depth, limit=limit, offset=offset)
        all_users.items += users.items

    return all_users

#########################################
# Methods used to initialize the module #
#########################################

def get_module_arguments(options, states):
    arguments = {}

    for option_name, option in options.items():
        arguments[option_name] = {
            'type': option['type'],
        }
        for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
            if option.get(key) is not None:
                arguments[option_name][key] = option.get(key)

        if option.get('env_fallback'):
            arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

        if len(option.get('required', [])) == len(states):
            arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name, options):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in options.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


################################################
# Methods used to filter info module responses #
################################################

def get_method_from_filter(filter):
    '''
    Returns the method which check a filter for one object. Such a method would work in the following way:
    for filter = ('properties.name', 'server_name') the resulting method would be
    def method(item):
        return item.properties.name == 'server_name'

    Parameters:
            filter (touple): Key, value pair representing the filter.

    Returns:
            the wanted method
    '''
    key, value = filter
    def method(item):
        current = item
        for key_part in key.split('.'):
            current = getattr(current, key_part)
        return current == value
    return method


def get_method_to_apply_filters_to_item(filter_list):
    '''
    Returns the method which applies a list of filtering methods obtained using get_method_from_filter to 
    one object and returns true if all the filters return true
    Parameters:
            filter_list (list): List of filtering methods
    Returns:
            the wanted method
    '''
    def f(item):
        return all([f(item) for f in filter_list])
    return f


def apply_filters(module, item_list):
    '''
    Creates a list of filtering methods from the filters module parameter, filters item_list to keep only the
    items for which every filter matches using get_method_to_apply_filters_to_item to make that check and returns
    those items
    Parameters:
            module: The current Ansible module
            item_list (list): List of items to be filtered
    Returns:
            List of items which match the filters
    '''
    filters = module.params.get('filters')
    if not filters:
        return item_list    
    filter_methods = list(map(get_method_from_filter, filters.items()))

    return filter(get_method_to_apply_filters_to_item(filter_methods), item_list)


def default_main_info(ionos_module, ionos_module_name, user_agent, has_sdk, options, states, object_name, returned_key, get_objects):
    module = AnsibleModule(argument_spec=get_module_arguments(options, states), supports_check_mode=True)

    if not has_sdk:
        module.fail_json(
            msg='{module_name} is required for this module, run `pip install {module_name}}`'.format(ionos_module_name))

    state = module.params.get('state')
    with ionos_module.ApiClient(get_sdk_config(module, ionos_module)) as api_client:
        api_client.user_agent = user_agent
        check_required_arguments(module, 'info', object_name, options)

        try:
            try:
                results = list(map(lambda x: x.to_dict(), apply_filters(module, get_objects(module, api_client).items)))
                return module.exit_json(**{
                    'changed': False,
                    returned_key: results
                })

            except Exception as e:
                module.fail_json(msg='failed to list the {object_name}: {error}'.format(
                    object_name=object_name, error=to_native(e),
                ))
            
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=object_name, error=to_native(e), state=state,
            ))
