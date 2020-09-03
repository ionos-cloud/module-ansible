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
module: profitbricks_datacenter
short_description: Create or destroy a ProfitBricks Virtual Datacenter.
description:
     - This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers.
       This module has a dependency on profitbricks >= 1.0.0
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
      - The ProfitBricks API base URL.
    required: false
    default: null
    version_added: "2.4"
  username:
    description:
      - The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable.
    required: false
    aliases: subscription_user
  password:
    description:
      - The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable.
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
    - "ionosenterprise >= 5.2.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''

# Create a Datacenter
- profitbricks_datacenter:
    name: Example DC
    location: us/las
    wait_timeout: 500

# Update a datacenter description
- profitbricks_datacenter:
    name: Example DC
    description: test data center
    state: update

# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
- profitbricks_datacenter:
    name: Example DC
    wait_timeout: 500
    state: absent

'''

import re
import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
    from ionosenterprise.items import Datacenter
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

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _wait_for_completion(client, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = client.get_request(
            request_id=promise['requestId'],
            status=True)

        if operation_result['metadata']['status'] == "DONE":
            return
        elif operation_result['metadata']['status'] == "FAILED":
            raise Exception(
                'Request failed to complete ' + msg + ' "' + str(
                    promise['requestId']) + '" to complete.')

    raise Exception('Timed out waiting for async operation ' + msg + ' "' +
                    str(promise['requestId']) + '" to complete.')


def _remove_datacenter(module, client, datacenter):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.delete_datacenter(datacenter)
    except Exception as e:
        module.fail_json(msg="failed to remove the datacenter: %s" % to_native(e))


def _update_datacenter(module, client, datacenter, description):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        client.update_datacenter(datacenter, description=description)
        return True
    except Exception as e:
        module.fail_json(msg="failed to update the datacenter: %s" % to_native(e))

    return False


def create_datacenter(module, client):
    """
    Creates a Datacenter

    This will create a new Datacenter in the specified location.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The datacenter ID if a new datacenter was created.
    """
    name = module.params.get('name')
    location = module.params.get('location')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenters = client.list_datacenters()

    for dc in datacenters['items']:
        if name == dc['properties']['name']:
            return {
                'datacenter_id': dc['id'],
                'changed': False
            }

    i = Datacenter(
        name=name,
        location=location,
        description=description
    )

    try:
        datacenter_response = client.create_datacenter(datacenter=i)

        if wait:
            _wait_for_completion(client, datacenter_response,
                                 wait_timeout, "_create_datacenter")

        results = {
            'datacenter_id': datacenter_response['id'],
            'changed': True
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def update_datacenter(module, client):
    """
    Updates a Datacenter.

    This will update a datacenter.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if a new datacenter was updated, false otherwise
    """
    name = module.params.get('name')
    description = module.params.get('description')

    if description is None:
        return False

    changed = False

    if(uuid_match.match(name)):
        changed = _update_datacenter(module, client, name, description)
    else:
        datacenters = client.list_datacenters()

        for d in datacenters['items']:
            vdc = client.get_datacenter(d['id'])

            if name == vdc['properties']['name']:
                name = d['id']
                changed = _update_datacenter(module, client, name, description)

    return changed


def remove_datacenter(module, client):
    """
    Removes a Datacenter.

    This will remove a datacenter.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the datacenter was deleted, false otherwise
    """
    name = module.params.get('name')
    changed = False

    if(uuid_match.match(name)):
        _remove_datacenter(module, client, name)
        changed = True
    else:
        datacenters = client.list_datacenters()

        for d in datacenters['items']:
            vdc = client.get_datacenter(d['id'])

            if name == vdc['properties']['name']:
                name = d['id']
                _remove_datacenter(module, client, name)
                changed = True

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            description=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['PROFITBRICKS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['PROFITBRICKS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionosenterprise is required for this module, run `pip install ionosenterprise`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')

    if not api_url:
        ionosenterprise = IonosEnterpriseService(username=username, password=password)
    else:
        ionosenterprise = IonosEnterpriseService(
            username=username,
            password=password,
            host_base=api_url
        )

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    ionosenterprise.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'absent':
        if not module.params.get('name'):
            module.fail_json(msg='name parameter is required deleting a virtual datacenter.')

        try:
            (changed) = remove_datacenter(module, ionosenterprise)
            module.exit_json(
                changed=changed)
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
            (datacenter_dict_array) = create_datacenter(module, ionosenterprise)
            module.exit_json(**datacenter_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set datacenter state: %s' % to_native(e))

    elif state == 'update':
        try:
            (changed) = update_datacenter(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to update datacenter: %s' % to_native(e))


if __name__ == '__main__':
    main()
