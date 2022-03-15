#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import copy
import re
import yaml

from uuid import uuid4

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Nic, NicProperties
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
OBJECT_NAME = 'NIC'

OPTIONS = {
    'name': {
        'description': ['The name of the NIC.'],
        'available': STATES,
        'required': ['absent'],
        'type': 'str',
    },
    'id': {
        'description': ['The ID of the NIC.'],
        'available': ['update'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'server': {
        'description': ['The server name or UUID.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'lan': {
        'description': ["The LAN to place the NIC on. You can pass a LAN that doesn't exist and it will be created. Required on create."],
        'required': ['present'],
        'available': ['update'],
        'type': 'str',
    },
    'dhcp': {
        'description': ['Boolean value indicating if the NIC is using DHCP or not.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'firewall_active': {
        'description': ['Boolean value indicating if the firewall is active.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'ips': {
        'description': ['A list of IPs to be assigned to the NIC.'],
        'available': ['present', 'update'],
        'type': 'list',
        'version_added': '2.4',
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
module: nic
short_description: Create, Update or Remove a NIC.
description:
     - This module allows you to create, update or remove a NIC.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    lan: 2
    wait_timeout: 500
    state: present
  ''',
  'update' : '''# Update a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    lan: 1
    ips:
      - 158.222.103.23
      - 158.222.103.24
    dhcp: false
    state: update
  ''',
  'absent' : '''# Remove a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    wait_timeout: 500
    state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nic(module, client):
    """
    Creates a NIC.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The NIC instance being created
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    lan = module.params.get('lan')
    dhcp = module.params.get('dhcp')
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    if not (uuid_match.match(datacenter)):
        datacenter_list = datacenter_server.datacenters_get(depth=2)
        for d in datacenter_list.items:
            dc = datacenter_server.datacenters_find_by_id(datacenter_id=d.id)
            if datacenter == dc.properties.name:
                datacenter = d.id
                break

    # Locate UUID for Server
    if not (uuid_match.match(server)):
        server_list = server_server.datacenters_servers_get(datacenter, depth=2)
        for s in server_list.items:
            if server == s.properties.name:
                server = s.id
                break

    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter, server_id=server, depth=2)
    nic = None
    for n in nic_list.items:
        if name == n.properties.name:
            nic = n
            break

    should_change = nic is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'nic': nic.to_dict()
        }

    try:
        nic_properties = NicProperties(name=name, ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active)
        nic = Nic(properties=nic_properties)

        response = nic_server.datacenters_servers_nics_post_with_http_info(datacenter_id=datacenter, server_id=server,
                                                                           nic=nic)
        (nic_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            nic_response = nic_server.datacenters_servers_nics_find_by_id(datacenter_id=datacenter, server_id=server,
                                                                     nic_id=nic_response.id)


        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'nic': nic_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the NIC: %s" % to_native(e))


def update_nic(module, client):
    """
    Updates a NIC.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The NIC instance being updated
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    lan = module.params.get('lan')
    dhcp = module.params.get('dhcp')
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    id = module.params.get('id')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    if not (uuid_match.match(datacenter)):
        datacenter_list = datacenter_server.datacenters_get(depth=2)
        for d in datacenter_list.items:
            dc = datacenter_server.datacenters_find_by_id(datacenter_id=d.id)
            if datacenter == dc.properties.name:
                datacenter = d.id
                break

    # Locate UUID for Server
    if not (uuid_match.match(server)):
        server_list = server_server.datacenters_servers_get(datacenter, depth=2)
        for s in server_list.items:
            if server == s.properties.name:
                server = s.id
                break

    nic = None
    # Locate NIC to update
    nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter, server_id=server, depth=2)
    for n in nic_list.items:
        if name == n.properties.name or id == n.id:
            nic = n
            break

    if not nic:
        module.fail_json(msg="NIC could not be found.")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        if lan is None:
            lan = nic.properties.lan
        if firewall_active is None:
            firewall_active = nic.properties.firewall_active
        if dhcp is None:
            dhcp = nic.properties.dhcp

        nic_properties = NicProperties(ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active,
                                       name=name)

        response = nic_server.datacenters_servers_nics_patch_with_http_info(datacenter_id=datacenter, server_id=server,
                                                                            nic_id=nic.id, nic=nic_properties)
        (nic_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            nic_response = nic_server.datacenters_servers_nics_find_by_id(datacenter_id=datacenter, server_id=server,
                                                                     nic_id=nic_response.id)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'nic': nic_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the NIC: %s" % to_native(e))


def delete_nic(module, client):
    """
    Removes a NIC

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NIC was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    if not (uuid_match.match(datacenter)):
        datacenter_list = datacenter_server.datacenters_get(depth=2)
        for d in datacenter_list.items:
            dc = datacenter_server.datacenters_find_by_id(datacenter_id=d.id)
            if datacenter == dc.properties.name:
                datacenter = d.id
                break

    # Locate UUID for Server
    server_found = False
    if not (uuid_match.match(server)):
        server_list = server_server.datacenters_servers_get(datacenter, depth=2)
        for s in server_list.items:
            if server == s.properties.name:
                server_found = True
                server = s.id
                break

        if not server_found:
            return {
                'action': 'delete',
                'changed': False,
                'id': name
            }

    # Locate UUID for NIC
    nic_found = False
    if not (uuid_match.match(name)):
        nic_list = nic_server.datacenters_servers_nics_get(datacenter_id=datacenter, server_id=server, depth=2)
        for n in nic_list.items:
            if name == n.properties.name:
                nic_found = True
                name = n.id
                break

        if not nic_found:
            module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = nic_server.datacenters_servers_nics_delete_with_http_info(datacenter_id=datacenter, server_id=server,
                                                                             nic_id=name)
        (nic_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'action': 'delete',
            'changed': True,
            'id': name
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the NIC: %s" % to_native(e))


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
                module.exit_json(**delete_nic(module, api_client))
            elif state == 'present':
                module.exit_json(**create_nic(module, api_client))
            elif state == 'update':
                module.exit_json(**update_nic(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
