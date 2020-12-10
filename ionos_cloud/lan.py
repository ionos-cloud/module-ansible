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
module: lan
short_description: Create, update or remove a LAN.
description:
     - This module allows you to create or remove a LAN.
version_added: "2.4"
options:
  datacenter:
    description:
      - The datacenter name or UUID in which to operate.
    required: true
  name:
    description:
      - The name or ID of the LAN.
    required: false
  public:
    description:
      - If true, the LAN will have public Internet access.
    required: false
    default: true
  ip_failover:
    description:
      - The IP failover group.
    required: false
  api_url:
    description:
      - The Ionos Cloud API base URL.
    required: false
    default: null
  username:
    description:
      - The Ionos Cloud username. Overrides the IONOS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The Ionos Cloud password. Overrides the IONOS_PASSWORD environment variable.
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
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionossdk >= 5.2.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
'''

EXAMPLES = '''
# Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present

# Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update

# Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    state: absent
'''

import re

HAS_SDK = True

try:
    import ionossdk
    from ionossdk import __version__ as sdk_version
    from ionossdk.models import Lan, LanPost, LanProperties, LanPropertiesPost
    from ionossdk.rest import ApiException
    from ionossdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


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
    client: authenticated ionossdk object.

    Returns:
        The LAN instance
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    public = module.params.get('public')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionossdk.DataCenterApi(api_client=client)
    lan_server = ionossdk.LanApi(api_client=client)

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
    client: authenticated ionossdk object.

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

    datacenter_server = ionossdk.DataCenterApi(api_client=client)
    lan_server = ionossdk.LanApi(api_client=client)

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
    client: authenticated ionossdk object.

    Returns:
        True if the LAN was removed, false otherwise
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')

    datacenter_server = ionossdk.DataCenterApi(api_client=client)
    lan_server = ionossdk.LanApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate ID for LAN
    lan_list = lan_server.datacenters_lans_get(datacenter_id, depth=2)
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter=dict(type='str', required=True),
            name=dict(type='str'),
            pcc_id=dict(type='str'),
            public=dict(type='bool', default=False),
            ip_failover=dict(type='list', elements='dict'),
            api_url=dict(type='str', default=None),
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
        module.fail_json(msg='ionossdk is required for this module, run `pip install ionossdk`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ionossdk-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionossdk.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            try:
                (result) = delete_lan(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set LAN state: %s' % to_native(e))

        elif state == 'present':
            try:
                (lan_dict) = create_lan(module, api_client)
                module.exit_json(**lan_dict)
            except Exception as e:
                module.fail_json(msg='failed to set LANs state: %s' % to_native(e))

        elif state == 'update':
            try:
                (lan_dict) = update_lan(module, api_client)
                module.exit_json(**lan_dict)
            except Exception as e:
                module.fail_json(msg='failed to update LAN: %s' % to_native(e))


if __name__ == '__main__':
    main()
