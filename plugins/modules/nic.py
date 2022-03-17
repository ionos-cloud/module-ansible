#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nic
short_description: Create, Update or Remove a NIC.
description:
     - This module allows you to create, update or remove a NIC.
version_added: "2.0"
options:
  datacenter:
    description:
      - The datacenter in which to operate.
    required: true
  server:
    description:
      - The server name or ID.
    required: true
  name:
    description:
      - The name or ID of the NIC. This is only required on deletes, but not on create.
    required: true
  lan:
    description:
      - The LAN to place the NIC on. You can pass a LAN that doesn't exist and it will be created. Required on create.
    required: true
    default: None
  nat:
    description:
      - Boolean value indicating if the private IP address has outbound access to the public internet.
    required: false
    default: None
    version_added: "2.3"
  dhcp:
    description:
      - Boolean value indicating if the NIC is using DHCP or not.
    required: false
    default: None
    version_added: "2.4"
  firewall_active:
    description:
      - Boolean value indicating if the firewall is active.
    required: false
    default: None
    version_added: "2.4"
  ips:
    description:
      - A list of IPs to be assigned to the NIC.
    required: false
    default: None
    version_added: "2.4"
  api_url:
    description:
      - The Ionos API base URL.
    required: false
    default: null
    version_added: "2.4"
  username:
    description:
      - The Ionos username. Overrides the IONOS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
    required: false
    aliases: subscription_password
  token:
    description:
      - The Ionos token. Overrides the IONOS_TOKEN environment variable.
    required: false
  wait:
    description:
      - wait for the operation to complete before returning
    required: false
    default: "yes"
    choices: [ "yes", "no" ]
  wait_timeout:
    description:
      - how long before wait gives up, in seconds
    default: 600
  state:
    description:
      - Indicate desired state of the resource
    required: false
    default: "present"
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''

# Create a NIC
- nic:
    datacenter: Tardis One
    server: node002
    lan: 2
    wait_timeout: 500
    state: present

# Update a NIC
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

# Remove a NIC
- nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    wait_timeout: 500
    state: absent

'''

import re

from uuid import uuid4

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Nic, NicProperties
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

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
    nat = module.params.get('nat') or False
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    server_server = ionoscloud.ServerApi(api_client=client)
    nic_server = ionoscloud.NicApi(api_client=client)

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
        nic_properties = NicProperties(name=name, ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active,
                                       nat=nat)
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
    nat = module.params.get('nat')
    dhcp = module.params.get('dhcp')
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    id = module.params.get('id')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    server_server = ionoscloud.ServerApi(api_client=client)
    nic_server = ionoscloud.NicApi(api_client=client)

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
        if nat is None:
            nat = nic.properties.nat
        if dhcp is None:
            dhcp = nic.properties.dhcp

        nic_properties = NicProperties(ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active,
                                       nat=nat, name=name)

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

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    server_server = ionoscloud.ServerApi(api_client=client)
    nic_server = ionoscloud.NicApi(api_client=client)

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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter=dict(type='str'),
            server=dict(type='str'),
            name=dict(type='str'),
            id=dict(type='str', default=str(uuid4()).replace('-', '')[:10]),
            lan=dict(type='int', default=None),
            dhcp=dict(type='bool', default=None),
            nat=dict(type='bool', default=None),
            firewall_active=dict(type='bool', default=None),
            ips=dict(type='list', default=None),
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            token=dict(
                type='str',
                required=True,
                fallback=(env_fallback, ['IONOS_TOKEN']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    if not module.params.get('datacenter'):
        module.fail_json(msg='datacenter parameter is required')
    if not module.params.get('server'):
        module.fail_json(msg='server parameter is required')

    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

    state = module.params.get('state')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    configuration = ionoscloud.Configuration(**conf)

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required')

            try:
                (changed) = delete_nic(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set nic state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('lan'):
                module.fail_json(msg='lan parameter is required')

            try:
                (nic_dict) = create_nic(module, api_client)
                module.exit_json(**nic_dict)
            except Exception as e:
                module.fail_json(msg='failed to set nic state: %s' % to_native(e))

        elif state == 'update':
            try:
                (nic_dict) = update_nic(module, api_client)
                module.exit_json(**nic_dict)
            except Exception as e:
                module.fail_json(msg='failed to update nic: %s' % to_native(e))


if __name__ == '__main__':
    main()
