
import copy
import yaml


def get_default_options(states):
    return {
        'allow_replace': {
            'description': ['Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead'],
            'available': ['present', 'update'],
            'default': False,
            'type': 'bool',
        },
        'api_url': {
            'description': ['The Ionos API base URL.'],
            'version_added': '2.4',
            'env_fallback': 'IONOS_API_URL',
            'available': states,
            'type': 'str',
        },
        'certificate_fingerprint': {
            'description': ['The Ionos API certificate fingerprint.'],
            'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
            'available': states,
            'type': 'str',
        },
        'username': {
            # Required if no token, checked manually
            'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
            'aliases': ['subscription_user'],
            'env_fallback': 'IONOS_USERNAME',
            'available': states,
            'type': 'str',
        },
        'password': {
            # Required if no token, checked manually
            'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
            'aliases': ['subscription_password'],
            'available': states,
            'no_log': True,
            'env_fallback': 'IONOS_PASSWORD',
            'type': 'str',
        },
        'token': {
            # If provided, then username and password no longer required
            'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
            'available': states,
            'no_log': True,
            'env_fallback': 'IONOS_TOKEN',
            'type': 'str',
        },
        'wait': {
            'description': ['Wait for the resource to be created before returning.'],
            'default': True,
            'available': states,
            'choices': [True, False],
            'type': 'bool',
        },
        'wait_timeout': {
            'description': ['How long before wait gives up, in seconds.'],
            'default': 600,
            'available': states,
            'type': 'int',
        },
        'state': {
            'description': ['Indicate desired state of the resource.'],
            'default': 'present',
            'choices': states,
            'available': states,
            'type': 'str',
        },
    }


def get_info_default_options_with_depth(states):
    return {
        'depth': {
            'description': ['The depth used when retrieving the items.'],
            'available': states,
            'type': 'int',
            'default': 1,
        },
        **get_info_default_options(states),
    }


def get_info_default_options(states):
    return {
        'filters': {
            'description': ["Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'"],
            'available': states,
            'type': 'dict',
        },
        'api_url': {
            'description': ['The Ionos API base URL.'],
            'version_added': '2.4',
            'env_fallback': 'IONOS_API_URL',
            'available': states,
            'type': 'str',
        },
        'certificate_fingerprint': {
            'description': ['The Ionos API certificate fingerprint.'],
            'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
            'available': states,
            'type': 'str',
        },
        'username': {
            # Required if no token, checked manually
            'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
            'aliases': ['subscription_user'],
            'env_fallback': 'IONOS_USERNAME',
            'available': states,
            'type': 'str',
        },
        'password': {
            # Required if no token, checked manually
            'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
            'aliases': ['subscription_password'],
            'available': states,
            'no_log': True,
            'env_fallback': 'IONOS_PASSWORD',
            'type': 'str',
        },
        'token': {
            # If provided, then username and password no longer required
            'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
            'available': states,
            'no_log': True,
            'env_fallback': 'IONOS_TOKEN',
            'type': 'str',
        },
    }


def transform_for_documentation(val, states):
    if type(val.get('required', [])) == list:
        val['required'] = len(val.get('required', [])) == len(states)
    if 'available' in val:
        del val['available']
    if 'type' in val:
        del val['type']
    return val


def transform_options_for_ducumentation(options, states):
    return yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v, states) for k, v in copy.deepcopy(options).items()})), default_flow_style=False, indent=4).replace('\n', '\n    ')[:-5]
