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
module: snapshot
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
    choices: ["present", "absent", "restore", "update"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - Nurfet Becirevic (@nurfet-becirevic)
    - Ethan Devenport (@edevenport)
'''

EXAMPLES = '''
# Create a snapshot
- name: Create snapshot
  snapshot:
    datacenter: production DC
    volume: master
    name: boot volume image
    state: present

# Restore a snapshot
- name: Restore snapshot
  snapshot:
    datacenter: production DC
    volume: slave
    name: boot volume image
    state: restore

# Remove a snapshot
- name: Remove snapshot
  snapshot:
    name: master-Snapshot-11/30/2017
    state: absent
'''

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Snapshot, SnapshotProperties
    from ionoscloud import ApiClient
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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_snapshot(module, client):
    """
    Creates a snapshot.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The snapshot instance
    """
    datacenter = module.params.get('datacenter')
    volume = module.params.get('volume')
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    volume_server = ionoscloud.VolumeApi(api_client=client)
    snapshot_server = ionoscloud.SnapshotApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for volume
    volume_list = volume_server.datacenters_volumes_get(datacenter_id=datacenter_id, depth=2)
    volume_id = _get_resource_id(volume_list, volume, module, "Volume")

    snapshot_list = snapshot_server.snapshots_get(depth=2)
    snapshot = None
    for s in snapshot_list.items:
        if name == s.properties.name:
            snapshot = s
            break

    should_change = snapshot is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'snapshot': snapshot.to_dict()
        }

    try:
        response = volume_server.datacenters_volumes_create_snapshot_post_with_http_info(datacenter_id=datacenter_id,
                                                                                         volume_id=volume_id, name=name,
                                                                                         description=description)
        (snapshot_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'snapshot': snapshot_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the snapshot: %s" % to_native(e))


def restore_snapshot(module, client):
    """
    Restores a snapshot.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the snapshot started restoring, false otherwise
    """
    datacenter = module.params.get('datacenter')
    volume = module.params.get('volume')
    name = module.params.get('name')
    wait = module.params.get('wait')

    datacenter_server = ionoscloud.DataCenterApi(api_client=client)
    volume_server = ionoscloud.VolumeApi(api_client=client)
    snapshot_server = ionoscloud.SnapshotApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = _get_resource_id(datacenter_list, datacenter, module, "Data center")

    # Locate UUID for volume
    volume_list = volume_server.datacenters_volumes_get(datacenter_id=datacenter_id, depth=2)
    volume_id = _get_resource_id(volume_list, volume, module, "Volume")

    # Locate UUID for snapshot
    snapshot_list = snapshot_server.snapshots_get(depth=2)
    snapshot_id = _get_resource_id(snapshot_list, name, module, "Snapshot")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        response = volume_server.datacenters_volumes_restore_snapshot_post_with_http_info(datacenter_id=datacenter_id,
                                                                                          volume_id=volume_id,
                                                                                          snapshot_id=snapshot_id)
        (snapshot_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)

        return {
            'changed': True,
            'failed': False,
            'action': 'restore',
            'snapshot': snapshot_response
        }

    except Exception as e:
        module.fail_json(msg="failed to restore the snapshot: %s" % to_native(e))


def update_snapshot(module, client):
    """
    Updates a snapshot.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The snapshot instance
    """
    snapshot_server = ionoscloud.SnapshotApi(api_client=client)

    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = snapshot_server.snapshots_get(depth=2)
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
    wait_timeout = module.params.get('wait_timeout')

    if cpu_hot_plug is None:
        cpu_hot_plug = snapshot.properties.cpu_hot_plug
    if cpu_hot_unplug is None:
        cpu_hot_unplug = snapshot.properties.cpu_hot_unplug
    if ram_hot_plug is None:
        ram_hot_plug = snapshot.properties.ram_hot_plug
    if ram_hot_unplug is None:
        ram_hot_unplug = snapshot.properties.ram_hot_unplug
    if nic_hot_plug is None:
        nic_hot_plug = snapshot.properties.nic_hot_plug
    if nic_hot_unplug is None:
        nic_hot_unplug = snapshot.properties.nic_hot_unplug
    if disc_virtio_hot_plug is None:
        disc_virtio_hot_plug = snapshot.properties.disc_virtio_hot_plug
    if disc_virtio_hot_unplug is None:
        disc_virtio_hot_unplug = snapshot.properties.disc_virtio_hot_unplug
    if disc_scsi_hot_plug is None:
        disc_scsi_hot_plug = snapshot.properties.disc_scsi_hot_plug
    if disc_scsi_hot_unplug is None:
        disc_scsi_hot_unplug = snapshot.properties.disc_scsi_hot_unplug
    if licence_type is None:
        licence_type = snapshot.properties.licence_type

    try:
        snapshot_properties = SnapshotProperties(
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
            licence_type=licence_type)

        response = snapshot_server.snapshots_put_with_http_info(snapshot.id, Snapshot(properties=snapshot_properties))
        (snapshot_response, _, headers) = response
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'snapshot': snapshot_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the snapshot: %s" % to_native(e))


def delete_snapshot(module, client):
    """
    Removes a snapshot

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the snapshot was removed, false otherwise
    """

    snapshot_server = ionoscloud.SnapshotApi(api_client=client)
    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = snapshot_server.snapshots_get(depth=2)
    snapshot_id = _get_resource_id(snapshot_list, name, module, "Snapshot")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        snapshot_server.snapshots_delete(snapshot_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': snapshot_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the snapshot: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': snapshot_id
        }


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


def _get_resource_instance(resource_list, identity):
    """
    Find and return the resource instance regardless of whether the name or UUID is passed.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
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

    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

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
            try:
                (changed) = delete_snapshot(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('datacenter'):
                module.fail_json(msg='datacenter parameter is required')
            if not module.params.get('volume'):
                module.fail_json(msg='volume parameter is required')

            try:
                (snapshot_dict) = create_snapshot(module, api_client)
                module.exit_json(**snapshot_dict)
            except Exception as e:
                module.fail_json(msg='failed to set snapshot state: %s' % to_native(e))

        elif state == 'restore':
            if not module.params.get('datacenter'):
                module.fail_json(msg='datacenter parameter is required')
            if not module.params.get('volume'):
                module.fail_json(msg='volume parameter is required')

            try:
                (changed) = restore_snapshot(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to restore snapshot: %s' % to_native(e))

        elif state == 'update':
            try:
                (snapshot_dict) = update_snapshot(module, api_client)
                module.exit_json(**snapshot_dict)
            except Exception as e:
                module.fail_json(msg='failed to update snapshot: %s' % to_native(e))


if __name__ == '__main__':
    main()
