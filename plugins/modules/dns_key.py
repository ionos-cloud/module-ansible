import copy
from distutils.command.config import config
from operator import mod
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re
import uuid

HAS_SDK = True
try:
    import ionoscloud_dns
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DNS_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dns/%s'% (
    __version__, ionoscloud_dns.__version__,
)
DOC_DIRECTORY = 'dns'
STATES = ['present', 'absent']
OBJECT_NAME = 'Zone Key'
RETURNED_KEY = 'zone_key'
REPO_URL = "https://github.com/ionos-cloud/module-ansible"


OPTIONS = {
    'validity': {
        'description': ['Signature validity in days'],
        'available': ['present'], 
        'required': ['present'], 
        'type': 'int',
    },
    'algorithm': {
        'description': ['Algorithm used to generate signing keys (both Key Signing Keys and Zone Signing Keys).'],
        'available': ['present'],
        'required': ['present'], 
        'type': 'str',
    },
    'ksk_bits': {
        'description': ['Key signing key length in bits. kskBits >= zskBits'],
        'available': ['present'],
        'required': ['present'],  
        'type': 'int',
    },
    'zsk_bits': {
        'description': ['Zone signing key length in bits.'],
        'available': ['present'],
        'required': ['present'], 
        'type': 'int',
    },
    'nsec_mode': {
        'description': ['NSEC mode.'],
        'available': ['present'],
        'required': ['present'], 
        'type': 'str',
    },
    'nsec3_iterations': {
        'description': ['Number of iterations for NSEC3. (between 0 and 50)'],
        'available': ['present'],
        'required': ['present'], 
        'type': 'int',
    },
    'nsec3_salt_bits': {
        'description': ['Salt length in bits for NSEC3. (between 64 and 128, multiples of 8)'],
        'available': ['present'],
        'required': ['present'], 
        'type': 'int',
    },
    'zone': {
        'description': ['The ID or name of an existing Zone.'],
        'available': ['present', 'absent'],
        'required': ['present', 'absent'],
        'type': 'str',
    },
    'allow_replace': {
        'description': [
            'Boolean indincating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
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
module: dns_key
short_description: Allows operations with Ionos Cloud DNS Zone Keys.
description:
     - This is a module that supports creating or destroying DNS Zone Keys
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dns >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Zone Key
    dns_key:
      zone: example.com
      validity: 100
      algorithm: RSASHA256
      ksk_bits: 4096
      zsk_bits: 2048
      nsec_mode: NSEC
      nsec3_iterations: 2
      nsec3_salt_bits: 64
    register: key_response
  ''',
    'absent': '''- name: Delete Zone Keys
    dns_zone:
      zone: example.com
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


def create_object(module, client):
    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )


    zone_key = ionoscloud_dns.DnssecKeyCreate(
        properties=ionoscloud_dns.DnssecKeyParameters(
            validity=module.params.get('validity'),
            key_parameters=ionoscloud_dns.KeyParameters(
                algorithm=module.params.get('algorithm'),
                ksk_bits=module.params.get('kskBits'),
                zsk_bits=module.params.get('zskBits'),
            ),
            nsec_parameters=ionoscloud_dns.NsecParameters(
                nsec_mode=module.params.get('nsec_mode'),
                nsec3_iterations=module.params.get('nsec3_iterations'),
                nsec3_salt_bits=module.params.get('nsec3_salt_bits'),
            )
        )
    )

    result = ionoscloud_dns.DNSSECApi(client).zones_keys_post(zone_id, zone_key)

    return {
        'action': 'create',
        'changed': True,
        RETURNED_KEY: result
    }


def remove_object(module, client):
    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )

    ionoscloud_dns.DNSSECApi(client).zones_keys_delete(zone_id)

    return {
        'action': 'delete',
        'changed': True,
        'id': zone_id,
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
        module.fail_json(msg='ionoscloud_dns is required for this module, '
                             'run `pip install ionoscloud_dns`')


    client = ionoscloud_dns.ApiClient(get_sdk_config(module, ionoscloud_dns))
    client.user_agent = DNS_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()
