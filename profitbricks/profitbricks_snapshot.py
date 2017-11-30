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
module: profitbricks_snapshot
short_description: Create or remove a snapshot.
description:
     - This module allows you to create or remove a snapshot.
version_added: "2.4"
options:
  datacenter:
    description:
      - The datacenter in which the volumes reside.
    required: true
  volume:
    description:
      - The name or UUID of the volume.
    required: true
  name:
    description:
      - The name of the snapshot.
    required: false
  description:
    description:
      - The description of the snapshot.
    required: false
  restore:
    description:
      - Boolean value indicating the snapshot restore action.
    required: false
    default: false
  subscription_user:
    description:
      - The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable.
    required: false
  subscription_password:
    description:
      - The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable.
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
    choices: ["present", "absent"]

requirements:
    - "python >= 2.6"
    - "profitbricks >= 4.0.0"
'''

EXAMPLES = '''
# Create a snapshot
- name: Create snapshot
  profitbricks_snapshot:
    datacenter: production DC
    volume: master
    name: boot volume image
    state: present

# Restore a snapshot
- name: Restore snapshot
  profitbricks_snapshot:
    datacenter: production DC
    volume: slave
    name: boot volume image
    restore: true
    state: present

# Remove a snapshot
- name: Remove snapshot
  profitbricks_snapshot:
    name: master-Snapshot-11/30/2017
    state: absent
'''

import os
import time

HAS_PB_SDK = True

try:
    from profitbricks import __version__ as sdk_version
    from profitbricks.client import ProfitBricksService
except ImportError:
    HAS_PB_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


def _wait_for_completion(profitbricks, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = profitbricks.get_request(
            request_id=promise['requestId'],
            status=True)

        if operation_result['metadata']['status'] == 'DONE':
            return
        elif operation_result['metadata']['status'] == 'FAILED':
            raise Exception(
                'Request failed to complete ' + msg + ' "' + str(
                    promise['requestId']) + '" to complete.')

    raise Exception('Timed out waiting for async operation ' + msg + ' "' +
                    str(promise['requestId']) + '" to complete.')


def create_snapshot(module, profitbricks):
    """
    Creates a snapshot.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        The snapshot instance
    """
    datacenter = module.params.get('datacenter')
    volume = module.params.get('volume')
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    # Locate UUID for virtual datacenter
    datacenter_list = profitbricks.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % datacenter)

    # Locate UUID for volume
    volume_list = profitbricks.list_volumes(datacenter_id)
    volume_id = _get_resource_id(volume_list, volume)
    if not volume_id:
        module.fail_json(msg='Volume \'%s\' not found.' % volume)

    try:
        snapshot_resp = profitbricks.create_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            name=name,
            description=description
        )

        if wait:
            _wait_for_completion(profitbricks, snapshot_resp, wait_timeout, "create_snapshot")

        return {
            'failed': False,
            'changed': True,
            'snapshot': snapshot_resp
        }

    except Exception as e:
        module.fail_json(msg="failed to create the snapshot: %s" % to_native(e))


def restore_snapshot(module, profitbricks):
    """
    Restores a snapshot.

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the snapshot started restoring, false otherwise
    """
    datacenter = module.params.get('datacenter')
    volume = module.params.get('volume')
    name = module.params.get('name')

    # Locate UUID for virtual datacenter
    datacenter_list = profitbricks.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % datacenter)

    # Locate UUID for volume
    volume_list = profitbricks.list_volumes(datacenter_id)
    volume_id = _get_resource_id(volume_list, volume)
    if not volume_id:
        module.fail_json(msg='Volume \'%s\' not found.' % volume)

    # Locate UUID for snapshot
    snapshot_list = profitbricks.list_snapshots()
    snapshot_id = _get_resource_id(snapshot_list, name)
    if not snapshot_id:
        module.fail_json(msg='Snapshot \'%s\' not found.' % name)

    try:
        snapshot_resp = profitbricks.restore_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            snapshot_id=snapshot_id
        )

        return snapshot_resp

    except Exception as e:
        module.fail_json(msg="failed to restore the snapshot: %s" % to_native(e))


def delete_snapshot(module, profitbricks):
    """
    Removes a snapshot

    module : AnsibleModule object
    profitbricks: authenticated profitbricks object.

    Returns:
        True if the snapshot was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = profitbricks.list_snapshots()
    snapshot_id = _get_resource_id(snapshot_list, name)

    try:
        snapshot_resp = profitbricks.delete_snapshot(snapshot_id)
        return snapshot_resp
    except Exception as e:
        module.fail_json(msg="failed to remove the snapshot: %s" % to_native(e))


def _get_resource_id(resource_list, identity):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['name'], resource['id']):
            return resource['id']
    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter=dict(type='str'),
            volume=dict(type='str'),
            name=dict(type='str', default=''),
            description=dict(type='str', default=''),
            restore=dict(type='bool', default=False),
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
        try:
            (changed) = delete_snapshot(module, profitbricks)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))

    elif state == 'present':
        if not module.params.get('datacenter'):
            module.fail_json(msg='datacenter parameter is required')
        if not module.params.get('volume'):
            module.fail_json(msg='volume parameter is required')

        try:
            if module.params.get('restore'):
                (snapshot_dict) = restore_snapshot(module, profitbricks)
            else:
                (snapshot_dict) = create_snapshot(module, profitbricks)

            module.exit_json(**snapshot_dict)
        except Exception as e:
            module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))


if __name__ == '__main__':
    main()
