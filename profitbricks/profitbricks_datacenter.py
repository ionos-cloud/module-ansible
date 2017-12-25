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
    choices: [ "us/las", "us/ewr", "de/fra", "de/fkb" ]
  subscription_user:
    description:
      - The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable.
    required: false
  subscription_password:
    description:
      - THe ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable.
    required: false
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
      - create or terminate datacenters
    required: false
    default: 'present'
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "profitbricks >= 4.0.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''

# Create a Datacenter
- profitbricks_datacenter:
    datacenter: Tardis One
    wait_timeout: 500

# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
- profitbricks_datacenter:
    datacenter: Tardis One
    wait_timeout: 500
    state: absent

'''

import os
import re
import time

HAS_PB_SDK = True

try:
    from profitbricks import __version__ as sdk_version
    from profitbricks.client import ProfitBricksService, Datacenter
except ImportError:
    HAS_PB_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


LOCATIONS = ['us/las',
             'us/ewr',
             'de/fra',
             'de/fkb']

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _wait_for_completion(profitbricks, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = profitbricks.get_request(
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


def _remove_datacenter(module, profitbricks, datacenter):
    try:
        profitbricks.delete_datacenter(datacenter)
    except Exception as e:
        module.fail_json(msg="failed to remove the datacenter: %s" % to_native(e))


def _update_datacenter(module, profitbricks, datacenter, description):
    try:
        profitbricks.update_datacenter(datacenter, description=description)
        return True
    except Exception as e:
        module.fail_json(msg="failed to update the datacenter: %s" % to_native(e))

    return False


def create_datacenter(module, profitbricks):
    """
    Creates a Datacenter

    This will create a new Datacenter in the specified location.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        The datacenter ID if a new datacenter was created.
    """
    name = module.params.get('name')
    location = module.params.get('location')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    i = Datacenter(
        name=name,
        location=location,
        description=description
    )

    try:
        datacenter_response = profitbricks.create_datacenter(datacenter=i)

        if wait:
            _wait_for_completion(profitbricks, datacenter_response,
                                 wait_timeout, "_create_datacenter")

        results = {
            'datacenter_id': datacenter_response['id']
        }

        return results

    except Exception as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def update_datacenter(module, profitbricks):
    """
    Updates a Datacenter.

    This will update a datacenter.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if a new datacenter was updated, false otherwise
    """
    name = module.params.get('name')
    description = module.params.get('description')

    if description is None:
        return False

    changed = False

    if(uuid_match.match(name)):
        changed = _update_datacenter(module, profitbricks, name, description)
    else:
        datacenters = profitbricks.list_datacenters()

        for d in datacenters['items']:
            vdc = profitbricks.get_datacenter(d['id'])

            if name == vdc['properties']['name']:
                name = d['id']
                changed = _update_datacenter(module, profitbricks, name, description)

    return changed


def remove_datacenter(module, profitbricks):
    """
    Removes a Datacenter.

    This will remove a datacenter.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the datacenter was deleted, false otherwise
    """
    name = module.params.get('name')
    changed = False

    if(uuid_match.match(name)):
        _remove_datacenter(module, profitbricks, name)
        changed = True
    else:
        datacenters = profitbricks.list_datacenters()

        for d in datacenters['items']:
            vdc = profitbricks.get_datacenter(d['id'])

            if name == vdc['properties']['name']:
                name = d['id']
                _remove_datacenter(module, profitbricks, name)
                changed = True

    return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            description=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            subscription_user=dict(type='str', default=os.environ.get('PROFITBRICKS_USERNAME')),
            subscription_password=dict(type='str', default=os.environ.get('PROFITBRICKS_PASSWORD'), no_log=True),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        )
    )
    if not HAS_PB_SDK:
        module.fail_json(msg='profitbricks required for this module')

    if not module.params.get('subscription_user'):
        module.fail_json(msg='subscription_user parameter or ' +
                             'PROFITBRICKS_USERNAME environment variable is required.')
    if not module.params.get('subscription_password'):
        module.fail_json(msg='subscription_password parameter or ' +
                             'PROFITBRICKS_PASSWORD environment variable is required.')

    subscription_user = module.params.get('subscription_user')
    subscription_password = module.params.get('subscription_password')

    profitbricks = ProfitBricksService(
        username=subscription_user,
        password=subscription_password)

    user_agent = 'profitbricks-sdk-python/%s Ansible/%s' % (sdk_version, __version__)
    profitbricks.headers = {'User-Agent': user_agent}

    state = module.params.get('state')

    if state == 'absent':
        if not module.params.get('name'):
            module.fail_json(msg='name parameter is required deleting a virtual datacenter.')

        try:
            (changed) = remove_datacenter(module, profitbricks)
            module.exit_json(
                changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set datacenter state: %s' % to_native(e))

    elif state == 'present':
        if not module.params.get('name'):
            module.fail_json(msg='name parameter is required for a new datacenter')
        if not module.params.get('location'):
            module.fail_json(msg='location parameter is required for a new datacenter')

        try:
            (datacenter_dict_array) = create_datacenter(module, profitbricks)
            module.exit_json(**datacenter_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to set datacenter state: %s' % to_native(e))

    elif state == 'update':
        try:
            (changed) = update_datacenter(module, profitbricks)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to update datacenter: %s' % to_native(e))


if __name__ == '__main__':
    main()
