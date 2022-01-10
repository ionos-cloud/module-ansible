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
module: ipblock
short_description: Create or remove an IPBlock.
description:
     - This module allows you to create or remove an IPBlock.
version_added: "2.4"
options:
  name:
    description:
      - The name or ID of the IPBlock.
    required: false
  location:
    description:
      - The datacenter location.
    required: false
    default: us/las
    choices: [ "us/las", "us/ewr", "de/fra", "de/fkb", "de/txl", "gb/lhr" ]
  size:
    description:
      - The number of IP addresses to allocate in the IPBlock.
    required: false
    default: 1
  api_url:
    description:
      - The Ionos API base URL.
    required: false
    default: null
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
    choices: ["present", "absent"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
'''

EXAMPLES = '''
# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present

# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
    state: absent
'''

import re

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


LOCATIONS = ['us/las',
             'us/ewr',
             'de/fra',
             'de/fkb',
             'de/txl',
             'gb/lhr'
             ]


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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            size=dict(type='int', default=1),
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
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
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

    state = module.params.get('state')

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            try:
                (result) = delete_ipblock(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set IPBlock state: %s' % to_native(e))

        elif state == 'present':
            try:
                (ipblock_dict) = reserve_ipblock(module, api_client)
                module.exit_json(**ipblock_dict)
            except Exception as e:
                module.fail_json(msg='failed to set IPBlocks state: %s' % to_native(e))

        elif state == 'update':
            try:
                (ipblock_dict) = update_ipblock(module, api_client)
                module.exit_json(**ipblock_dict)
            except Exception as e:
                module.fail_json(msg='failed to set IPBlocks state: %s' % to_native(e))


if __name__ == '__main__':
    main()
