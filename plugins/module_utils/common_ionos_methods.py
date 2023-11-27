from ansible.module_utils.basic import env_fallback


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


def check_required_arguments(module, object_name, options):
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

    for option_name, option in options.items():
        if 'info' in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for retrieving {object_name}'.format(
                    option_name=option_name,
                    object_name=object_name,
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
