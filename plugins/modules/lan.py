#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import re
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Lan, LanPost, LanProperties, LanPropertiesPost
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'LAN'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'name': {
        'description': ['The name or ID of the LAN.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'pcc_id': {
        'description': ['The ID of the PCC.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'ip_failover': {
        'description': ['The IP failover group.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'public': {
        'description': ['If true, the LAN will have public Internet access.'],
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
module: lan
short_description: Create, update or remove a LAN.
description:
     - This module allows you to create or remove a LAN.
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
  'present' : '''# Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  ''',
  'update' : '''# Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  ''',
  'absent' : '''# Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
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


def create_lan(module, client):
    """
    Creates a LAN.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The LAN instance
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    public = module.params.get('public')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    lan_server = ionoscloud.LANsApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    lan_list = lan_server.datacenters_lans_get(datacenter_id, depth=2)
    lan = None
    for i in lan_list.items:
        if name == i.properties.name:
            lan = i
            break

    should_change = lan is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'failed': False,
            'action': 'create',
            'lan': lan.to_dict(),
        }
    lan_response = None
    try:
        lan_properties = LanPropertiesPost(name=name,
                                           public=public)

        lan = LanPost(properties=lan_properties)

        response = lan_server.datacenters_lans_post_with_http_info(datacenter_id=datacenter_id, lan=lan)
        (lan_response, _, headers) = response

        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'failed': False,
            'changed': True,
            'action': 'create',
            'lan': lan_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the LAN: %s" % to_native(e))


def update_lan(module, client):
    """
    Updates a LAN.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The LAN instance
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    public = module.params.get('public')
    ip_failover = module.params.get('ip_failover')
    pcc_id = module.params.get('pcc_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    lan_server = ionoscloud.LANsApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Prefetch a list of LANs.
    lan_list = lan_server.datacenters_lans_get(datacenter_id, depth=2)
    lan_id = _get_resource_id(lan_list, name, module, "LAN")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        if ip_failover:
            for elem in ip_failover:
                elem['nicUuid'] = elem.pop('nic_uuid')

        lan_properties = LanProperties(name=name, ip_failover=ip_failover, pcc=pcc_id, public=public)
        lan = Lan(properties=lan_properties)

        response = lan_server.datacenters_lans_put_with_http_info(datacenter_id=datacenter_id, lan_id=lan_id, lan=lan)
        (lan_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'failed': False,
            'changed': True,
            'action': 'update',
            'lan': lan_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the LAN: %s" % to_native(e))


def delete_lan(module, client):
    """
    Removes a LAN

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the LAN was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    lan_server = ionoscloud.LANsApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate ID for LAN
    lan_list = lan_server.datacenters_lans_get(datacenter_id=datacenter_id, depth=5)
    lan = _get_resource(lan_list, name)

    if not lan:
        module.exit_json(changed=False)

    lan_id = _get_resource_id(lan_list, name, module, "LAN")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        lan_server.datacenters_lans_delete(datacenter_id=datacenter_id, lan_id=lan_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': lan_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the LAN: %s" % to_native(e))


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
                module.exit_json(**delete_lan(module, api_client))
            elif state == 'present':
                module.exit_json(**create_lan(module, api_client))
            elif state == 'update':
                module.exit_json(**update_lan(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
