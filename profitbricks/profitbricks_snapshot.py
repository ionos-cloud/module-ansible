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
short_description: Create, restore, update or remove a snapshot.
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
  cpu_hot_plug:
    description:
      - Boolean value indicating the volume is capable of CPU hot plug (no reboot required).
    required: false
    default: None
  cpu_hot_unplug:
    description:
      - Boolean value indicating the volume is capable of CPU hot unplug (no reboot required).
    required: false
    default: None
  ram_hot_plug:
    description:
      - Boolean value indicating the volume is capable of memory hot plug (no reboot required).
    required: false
    default: None
  ram_hot_unplug:
    description:
      - Boolean value indicating the volume is capable of memory hot unplug (no reboot required).
    required: false
    default: None
  nic_hot_plug:
    description:
      - Boolean value indicating the volume is capable of NIC hot plug (no reboot required).
    required: false
    default: None
  nic_hot_unplug:
    description:
      - Boolean value indicating the volume is capable of NIC hot unplug (no reboot required).
    required: false
    default: None
  disc_virtio_hot_plug:
    description:
      - Boolean value indicating the volume is capable of VirtIO drive hot plug (no reboot required).
    required: false
    default: None
  disc_virtio_hot_unplug:
    description:
      - Boolean value indicating the volume is capable of VirtIO drive hot unplug (no reboot required).
    required: false
    default: None
  disc_scsi_hot_plug:
    description:
      - Boolean value indicating the volume is capable of SCSI drive hot plug (no reboot required).
    required: false
    default: None
  disc_scsi_hot_unplug:
    description:
      - Boolean value indicating the volume is capable of SCSI drive hot unplug (no reboot required).
    required: false
    default: None
  api_url:
    description:
      - The ProfitBricks API base URL.
    required: false
    default: null
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
    choices: ["present", "absent", "restore", "update"]

requirements:
    - "python >= 2.6"
    - "ionosenterprise >= 5.2.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
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
    state: restore

# Remove a snapshot
- name: Remove snapshot
  profitbricks_snapshot:
    name: master-Snapshot-11/30/2017
    state: absent
'''

import time

HAS_SDK = True

try:
    from ionosenterprise import __version__ as sdk_version
    from ionosenterprise.client import IonosEnterpriseService
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


LICENCE_TYPES = ['LINUX',
                 'WINDOWS',
                 'UNKNOWN',
                 'OTHER',
                 'WINDOWS2016']


def _wait_for_completion(client, promise, wait_timeout, msg):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = client.get_request(
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


def create_snapshot(module, client):
    """
    Creates a snapshot.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

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
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for volume
    volume_list = client.list_volumes(datacenter_id)
    volume_id = _get_resource_id(volume_list, volume, module, "Volume")

    snapshot_list = client.list_snapshots()
    snapshot = None
    for s in snapshot_list['items']:
        if name == s['properties']['name']:
            snapshot = s
            break

    should_change = snapshot is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'snapshot': snapshot
        }

    try:
        snapshot_resp = client.create_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            name=name,
            description=description
        )

        if wait:
            _wait_for_completion(client, snapshot_resp, wait_timeout, "create_snapshot")

        return {
            'failed': False,
            'changed': True,
            'snapshot': snapshot_resp
        }

    except Exception as e:
        module.fail_json(msg="failed to create the snapshot: %s" % to_native(e))


def restore_snapshot(module, client):
    """
    Restores a snapshot.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the snapshot started restoring, false otherwise
    """
    datacenter = module.params.get('datacenter')
    volume = module.params.get('volume')
    name = module.params.get('name')

    # Locate UUID for virtual datacenter
    datacenter_list = client.list_datacenters()
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for volume
    volume_list = client.list_volumes(datacenter_id)
    volume_id = _get_resource_id(volume_list, volume, module, "Volume")

    # Locate UUID for snapshot
    snapshot_list = client.list_snapshots()
    snapshot_id = _get_resource_id(snapshot_list, name, module, "Snapshot")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        snapshot_resp = client.restore_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            snapshot_id=snapshot_id
        )

        return {
            'changed': True,
            'snapshot': snapshot_resp
        }

    except Exception as e:
        module.fail_json(msg="failed to restore the snapshot: %s" % to_native(e))


def update_snapshot(module, client):
    """
    Updates a snapshot.

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        The snapshot instance
    """
    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = client.list_snapshots()
    snapshot = _get_resource_instance(snapshot_list, name)
    if not snapshot:
        module.fail_json(msg='Snapshot \'%s\' not found.' % name)

    if module.check_mode:
        module.exit_json(changed=True)

    cpu_hot_plug = module.params.get('cpu_hot_plug')
    cpu_hot_unplug = module.params.get('cpu_hot_unplug')
    ram_hot_plug = module.params.get('ram_hot_plug')
    ram_hot_unplug = module.params.get('ram_hot_unplug')
    nic_hot_plug = module.params.get('nic_hot_plug')
    nic_hot_unplug = module.params.get('nic_hot_unplug')
    disc_virtio_hot_plug = module.params.get('disc_virtio_hot_plug')
    disc_virtio_hot_unplug = module.params.get('disc_virtio_hot_unplug')
    disc_scsi_hot_plug = module.params.get('disc_scsi_hot_plug')
    disc_scsi_hot_unplug = module.params.get('disc_scsi_hot_unplug')
    licence_type = module.params.get('licence_type')

    if cpu_hot_plug is None:
        cpu_hot_plug = snapshot['properties']['cpuHotPlug']
    if cpu_hot_unplug is None:
        cpu_hot_unplug = snapshot['properties']['cpuHotUnplug']
    if ram_hot_plug is None:
        ram_hot_plug = snapshot['properties']['ramHotPlug']
    if ram_hot_unplug is None:
        ram_hot_unplug = snapshot['properties']['ramHotUnplug']
    if nic_hot_plug is None:
        nic_hot_plug = snapshot['properties']['nicHotPlug']
    if nic_hot_unplug is None:
        nic_hot_unplug = snapshot['properties']['nicHotUnplug']
    if disc_virtio_hot_plug is None:
        disc_virtio_hot_plug = snapshot['properties']['discVirtioHotPlug']
    if disc_virtio_hot_unplug is None:
        disc_virtio_hot_unplug = snapshot['properties']['discVirtioHotUnplug']
    if disc_scsi_hot_plug is None:
        disc_scsi_hot_plug = snapshot['properties']['discScsiHotPlug']
    if disc_scsi_hot_unplug is None:
        disc_scsi_hot_unplug = snapshot['properties']['discScsiHotUnplug']
    if licence_type is None:
        licence_type = snapshot['properties']['licenceType']

    try:
        snapshot_resp = client.update_snapshot(
            snapshot_id=snapshot['id'],
            cpu_hot_plug=cpu_hot_plug,
            cpu_hot_unplug=cpu_hot_unplug,
            ram_hot_plug=ram_hot_plug,
            ram_hot_unplug=ram_hot_unplug,
            nic_hot_plug=nic_hot_plug,
            nic_hot_unplug=nic_hot_unplug,
            disc_virtio_hot_plug=disc_virtio_hot_plug,
            disc_virtio_hot_unplug=disc_virtio_hot_unplug,
            disc_scsi_hot_plug=disc_scsi_hot_plug,
            disc_scsi_hot_unplug=disc_scsi_hot_unplug,
            licence_type=licence_type
        )

        return {
            'changed': True,
            'snapshot': snapshot_resp
        }

    except Exception as e:
        module.fail_json(msg="failed to update the snapshot: %s" % to_native(e))


def delete_snapshot(module, client):
    """
    Removes a snapshot

    module : AnsibleModule object
    client: authenticated ionosenterprise object.

    Returns:
        True if the snapshot was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = client.list_snapshots()
    snapshot_id = _get_resource_id(snapshot_list, name, module, "Snapshot")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        snapshot_resp = client.delete_snapshot(snapshot_id)
        return snapshot_resp
    except Exception as e:
        module.fail_json(msg="failed to remove the snapshot: %s" % to_native(e))


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['name'], resource['id']):
            return resource['id']

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


def _get_resource_instance(resource_list, identity):
    """
    Find and return the resource instance regardless of whether the name or UUID is passed.
    """
    for resource in resource_list['items']:
        if identity in (resource['properties']['name'], resource['id']):
            return resource
    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter=dict(type='str'),
            volume=dict(type='str'),
            name=dict(type='str', default=''),
            description=dict(type='str', default=''),
            licence_type=dict(type='str', choices=LICENCE_TYPES, default=None),
            cpu_hot_plug=dict(type='bool', default=None),
            cpu_hot_unplug=dict(type='bool', default=None),
            ram_hot_plug=dict(type='bool', default=None),
            ram_hot_unplug=dict(type='bool', default=None),
            nic_hot_plug=dict(type='bool', default=None),
            nic_hot_unplug=dict(type='bool', default=None),
            disc_virtio_hot_plug=dict(type='bool', default=None),
            disc_virtio_hot_unplug=dict(type='bool', default=None),
            disc_scsi_hot_plug=dict(type='bool', default=None),
            disc_scsi_hot_unplug=dict(type='bool', default=None),
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
        try:
            (changed) = delete_snapshot(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))

    elif state == 'present':
        if not module.params.get('datacenter'):
            module.fail_json(msg='datacenter parameter is required')
        if not module.params.get('volume'):
            module.fail_json(msg='volume parameter is required')

        try:
            (snapshot_dict) = create_snapshot(module, ionosenterprise)
            module.exit_json(**snapshot_dict)
        except Exception as e:
            module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))

    elif state == 'restore':
        if not module.params.get('datacenter'):
            module.fail_json(msg='datacenter parameter is required')
        if not module.params.get('volume'):
            module.fail_json(msg='volume parameter is required')

        try:
            (changed) = restore_snapshot(module, ionosenterprise)
            module.exit_json(changed=changed)
        except Exception as e:
            module.fail_json(msg='failed to restore snapshot: %s' % to_native(e))

    elif state == 'update':
        try:
            (snapshot_dict) = update_snapshot(module, ionosenterprise)
            module.exit_json(**snapshot_dict)
        except Exception as e:
            module.fail_json(msg='failed to update snapshot: %s' % to_native(e))


if __name__ == '__main__':
    main()
