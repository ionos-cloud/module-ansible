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
module: datacenter
short_description: Create or destroy a Ionos Cloud Virtual Datacenter.
description:
     - This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers.
       This module has a dependency on ionos-cloud >= 1.0.0
version_added: "2.0"
options:
  name:
    description:
      - The name of the virtual datacenter.
    required: true
  description:
    description:
      - The description of the virtual datacenter.
    required: false
  location:
    description:
      - The datacenter location.
    required: false
    default: us/las
    choices: [ "us/las", "us/ewr", "de/fra", "de/fkb", "de/txl", "gb/lhr" ]
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
  wait:
    description:
      - wait for the datacenter to be created before returning
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
    default: 'present'
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionossdk >= 5.2.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''

# Create a Datacenter
- datacenter:
    name: Example DC
    location: us/las
    wait_timeout: 500

# Update a datacenter description
- datacenter:
    name: Example DC
    description: test data center
    state: update

# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
- datacenter:
    name: Example DC
    wait_timeout: 500
    state: absent

'''

import re
import json

HAS_SDK = True

try:
    import ionossdk
    from ionossdk import __version__ as sdk_version
    from ionossdk.models import Datacenter, DatacenterProperties
    from ionossdk.rest import ApiException
    from ionossdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)

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


def _remove_datacenter(module, datacenter_server, datacenter):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        datacenter_server.datacenters_delete(datacenter)
    except Exception as e:
        module.fail_json(msg="failed to remove the datacenter: %s" % to_native(e))


def _update_datacenter(module, datacenter_server, client, id, datacenter, wait):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = datacenter_server.datacenters_put_with_http_info(datacenter_id=id, datacenter=datacenter)
        (datacenter_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)

        return {
            'changed': True,
            'failed': False,
            'datacenter': datacenter_response.to_dict()
        }
    except ApiException as e:
        module.fail_json(msg="failed to update the datacenter: %s" % to_native(e))
    return {
        'changed': False,
        'failed': True,
    }


def create_datacenter(module, client):
    """
    Creates a Datacenter

    This will create a new Datacenter in the specified location.

    module : AnsibleModule object
    client: authenticated ionossdk object.

    Returns:
        The datacenter ID if a new datacenter was created.
    """
    name = module.params.get('name')
    location = module.params.get('location')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenter_server = ionossdk.DataCenterApi(client)
    datacenters = datacenter_server.datacenters_get(depth=2)

    for dc in datacenters.items:
        if name == dc.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'datacenter': dc.to_dict()
            }

    datacenter_properties = DatacenterProperties(name=name, description=description, location=location)
    datacenter = Datacenter(properties=datacenter_properties)

    try:
        response = datacenter_server.datacenters_post_with_http_info(datacenter=datacenter)
        (datacenter_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'datacenter': datacenter_response.to_dict()
        }

        return results

    except ApiException as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def update_datacenter(module, client):
    """
    Updates a Datacenter.

    This will update a datacenter.

    module : AnsibleModule object
    client: authenticated ionossdk object.

    Returns:
        True if a new datacenter was updated, false otherwise
    """
    name = module.params.get('name')
    description = module.params.get('description')
    datacenter_id = module.params.get('id')
    wait = module.params.get('wait')
    datacenter_server = ionossdk.DataCenterApi(client)

    if description is None:
        return {
            'action': 'update',
            'changed': False
        }

    changed = False
    response = None

    if datacenter_id:
        datacenter = Datacenter(properties={'name': name, 'description': description})
        response = _update_datacenter(module, datacenter_server, client, datacenter_id, datacenter, wait)
        changed = response['changed']
    else:
        datacenters = datacenter_server.datacenters_get(depth=2)
        for d in datacenters.items:
            vdc = datacenter_server.datacenters_find_by_id(d.id)
            if name == vdc.properties.name:
                datacenter = Datacenter(
                    properties={'name': name, 'description': description})
                response = _update_datacenter(module, datacenter_server, client, datacenter_id, datacenter, wait)
                changed = response['changed']

    if not changed:
        module.fail_json(msg="failed to update the datacenter: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': response['failed'],
        'datacenter': response['datacenter']
    }


def remove_datacenter(module, client):
    """
    Removes a Datacenter.

    This will remove a datacenter.

    module : AnsibleModule object
    client: authenticated ionossdk object.

    Returns:
        True if the datacenter was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('id')
    datacenter_server = ionossdk.DataCenterApi(client)
    changed = False

    if datacenter_id:
        _remove_datacenter(module, datacenter_server, datacenter_id)
        changed = True

    else:
        datacenters = datacenter_server.datacenters_get(depth=2)
        for d in datacenters.items:
            vdc = datacenter_server.datacenters_find_by_id(d.id)
            if name == vdc.properties.name:
                datacenter_id = d.id
                _remove_datacenter(module, datacenter_server, datacenter_id)
                changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': datacenter_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            description=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            id=dict(type='str'),
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
    state = module.params.get('state')
    user_agent = 'ionossdk-python/%s Ansible/%s' % (sdk_version, __version__)

    configuration = ionossdk.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not module.params.get('name') and not module.params.get('id'):
                module.fail_json(msg='name parameter or id parameter are required deleting a virtual datacenter.')

            try:
                (result) = remove_datacenter(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set datacenter state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new datacenter')
            if not module.params.get('location'):
                module.fail_json(msg='location parameter is required for a new datacenter')

            if module.check_mode:
                module.exit_json(changed=True)

            try:
                (datacenter_dict_array) = create_datacenter(module, api_client)
                module.exit_json(**datacenter_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set datacenter state: %s' % to_native(e))

        elif state == 'update':
            try:
                (datacenter_dict_array) = update_datacenter(module, api_client)
                module.exit_json(**datacenter_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update datacenter: %s' % to_native(e))


if __name__ == '__main__':
    main()
