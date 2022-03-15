#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import re
import yaml

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import IpBlock, IpBlockProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient, IPBlocksApi
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'update', 'absent']
OBJECT_NAME = 'IP Block'

OPTIONS = {
    'name': {
        'description': ['The name or ID of the IPBlock.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'location': {
        'description': ['The IP Block location.'],
        'required': ['present'],
        'choices': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'],
        'default': 'us/las',
        'available': ['present'],
        'type': 'str',
    },
    'size': {
        'description': ['The number of IP addresses to allocate in the IPBlock.'],
        'available': ['present'],
        'default': 1,
        'type': 'int',
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
module: ipblock
short_description: Create or remove an IPBlock.
description:
     - This module allows you to create or remove an IPBlock.
version_added: "2.4"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  ''',
  'update': '''# Update an IPBlock
- name: Update ipblock
  ipblock:
    name: "staging - updated"
    location: "us/ewr"
    state: update
  ''',
  'absent' : '''# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
    state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def reserve_ipblock(module, client):
    """
    Creates an IPBlock.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The IPBlock instance
    """
    name = module.params.get('name')
    location = module.params.get('location')
    size = module.params.get('size')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    ipblock_server = ionoscloud.IPBlocksApi(client)
    ip_list = ipblock_server.ipblocks_get(depth=2)
    ip = None
    for i in ip_list.items:
        if name == i.properties.name:
            ip = i
            break

    should_change = ip is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'ipblock': ip.to_dict()
        }

    try:
        ipblock_properties = IpBlockProperties(location=location, size=size, name=name)
        ipblock = IpBlock(properties=ipblock_properties)

        response = ipblock_server.ipblocks_post_with_http_info(ipblock)
        (ipblock_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'ipblock': ipblock_response.to_dict()
        }


    except Exception as e:
        module.fail_json(msg="failed to create the IPBlock: %s" % to_native(e))


def update_ipblock(module, client):
    """
    Creates an IPBlock.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The IPBlock instance
    """
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    ipblock_server = ionoscloud.IPBlocksApi(client)
    ip_list = ipblock_server.ipblocks_get(depth=2)
    ip = None
    for i in ip_list.items:
        if name == i.properties.name:
            ip = i
            break

    if ip:
        try:
            ipblock_properties = IpBlockProperties(name=name)
            ipblock = IpBlock(properties=ipblock_properties)

            response = ipblock_server.ipblocks_put_with_http_info(ip.id, ipblock)
            (ipblock_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                'ipblock': ipblock_response.to_dict()
            }

        except Exception as e:
            module.fail_json(msg="failed to create the IPBlock: %s" % to_native(e))
    else:
        module.fail_json(msg='Ipblock \'%s\' not found.' % str(name))


def delete_ipblock(module, client):
    """
    Removes an IPBlock

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the IPBlock was removed, false otherwise
    """
    name = module.params.get('name')
    ipblock_server = ionoscloud.IPBlocksApi(client)

    # Locate UUID for the IPBlock
    ipblock_list = ipblock_server.ipblocks_get(depth=2)
    ipblock = _get_resource(ipblock_list, name)

    if not ipblock:
        module.exit_json(changed=False)


    id = _get_resource_id(ipblock_list, name, module, "IP Block")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        ipblock_server.ipblocks_delete(id)
        return {
            'action': 'delete',
            'changed': True,
            'id': id
        }

    except Exception as e:
        module.fail_json(msg="failed to remove the IPBlock: %s" % to_native(e))


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


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
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
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
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'absent':
                module.exit_json(**delete_ipblock(module, api_client))
            elif state == 'present':
                module.exit_json(**reserve_ipblock(module, api_client))
            elif state == 'update':
                module.exit_json(**update_ipblock(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
