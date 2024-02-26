#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Snapshot, SnapshotProperties
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id, get_resource,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Snapshot'
RETURNED_KEY = 'snapshot'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter in which the volumes reside.'],
        'available': ['present', 'restore'],
        'required': ['present', 'restore'],
        'type': 'str',
    },
    'volume': {
        'description': ['The name or UUID of the volume.'],
        'available': ['present', 'restore'],
        'required': ['present', 'restore'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'available': ['create'],
        'required': ['create'],
        'type': 'str',
    },
    'snapshot': {
        'description': ['The ID or name of an existing snapshot.'],
        'available': ['restore', 'update', 'absent'],
        'required': ['restore', 'update', 'absent'],
        'type': 'str',
    },
    'description': {
        'description': ['Human-readable description.'],
        'available': ['present'],
        'type': 'str',
    },
    'licence_type': {
        'description': ['OS type of this snapshot'],
        'choices': ['UNKNOWN', 'WINDOWS', 'WINDOWS2016', 'WINDOWS2022', 'RHEL', 'LINUX', 'OTHER'],
        'available': ['update'],
        'type': 'str',
    },
    'cpu_hot_plug': {
        'description': ['Hot-plug capable CPU (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'cpu_hot_unplug': {
        'description': ['Hot-unplug capable CPU (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'ram_hot_plug': {
        'description': ['Hot-plug capable RAM (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'ram_hot_unplug': {
        'description': ['Hot-unplug capable RAM (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'nic_hot_plug': {
        'description': ['Hot-plug capable NIC (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'nic_hot_unplug': {
        'description': ['Hot-unplug capable NIC (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_scsi_hot_plug': {
        'description': ['Hot-plug capable SCSI drive (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_scsi_hot_unplug': {
        'description': ['Is capable of SCSI drive hot unplug (no reboot required). This works only for non-Windows virtual Machines.'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_virtio_hot_plug': {
        'description': ['Hot-plug capable Virt-IO drive (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_virtio_hot_unplug': {
        'description': ['Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs.'],
        'available': ['update'],
        'type': 'bool',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: snapshot
short_description: Create, restore, update or remove a snapshot.
description:
     - This module allows you to create or remove a snapshot.
version_added: "2.4"
options:
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    cpu_hot_plug:
        description:
        - Hot-plug capable CPU (no reboot required).
        required: false
    cpu_hot_unplug:
        description:
        - Hot-unplug capable CPU (no reboot required).
        required: false
    datacenter:
        description:
        - The datacenter in which the volumes reside.
        required: false
    description:
        description:
        - Human-readable description.
        required: false
    disc_scsi_hot_plug:
        description:
        - Hot-plug capable SCSI drive (no reboot required).
        required: false
    disc_scsi_hot_unplug:
        description:
        - Is capable of SCSI drive hot unplug (no reboot required). This works only for
            non-Windows virtual Machines.
        required: false
    disc_virtio_hot_plug:
        description:
        - Hot-plug capable Virt-IO drive (no reboot required).
        required: false
    disc_virtio_hot_unplug:
        description:
        - Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows
            VMs.
        required: false
    licence_type:
        choices:
        - UNKNOWN
        - WINDOWS
        - WINDOWS2016
        - WINDOWS2022
        - RHEL
        - LINUX
        - OTHER
        description:
        - OS type of this snapshot
        required: false
    name:
        description:
        - The name of the  resource.
        required: false
    nic_hot_plug:
        description:
        - Hot-plug capable NIC (no reboot required).
        required: false
    nic_hot_unplug:
        description:
        - Hot-unplug capable NIC (no reboot required).
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    ram_hot_plug:
        description:
        - Hot-plug capable RAM (no reboot required).
        required: false
    ram_hot_unplug:
        description:
        - Hot-unplug capable RAM (no reboot required).
        required: false
    snapshot:
        description:
        - The ID or name of an existing snapshot.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        - restore
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    volume:
        description:
        - The name or UUID of the volume.
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.1.6"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''# Create a snapshot
  - name: Create snapshot
    snapshot:
      datacenter: production DC
      volume: master
      name: boot volume image
      state: present

  ''',
    'update': '''# Update a snapshot
  - name: Update snapshot
    snapshot:
      snapshot: "boot volume image"
      description: Ansible test snapshot - RENAME
      state: update
  ''',
    'restore': '''# Restore a snapshot
  - name: Restore snapshot
    snapshot:
      datacenter: production DC
      volume: slave
      snapshot: boot volume image
      state: restore
  ''',
    'absent': '''# Remove a snapshot
  - name: Remove snapshot
    snapshot:
      snapshot: master-Snapshot-11/30/2017
      state: absent
  ''',
}

EXAMPLES = """# Create a snapshot
  - name: Create snapshot
    snapshot:
      datacenter: production DC
      volume: master
      name: boot volume image
      state: present

  
# Update a snapshot
  - name: Update snapshot
    snapshot:
      snapshot: "boot volume image"
      description: Ansible test snapshot - RENAME
      state: update
  
# Restore a snapshot
  - name: Restore snapshot
    snapshot:
      datacenter: production DC
      volume: slave
      snapshot: boot volume image
      state: restore
  
# Remove a snapshot
  - name: Remove snapshot
    snapshot:
      snapshot: master-Snapshot-11/30/2017
      state: absent
"""


class SnapshotModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def present_object(self, clients):
        """
        Creates a snapshot.

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            The snapshot instance
        """
        client = clients[0]
        datacenter = self.module.params.get('datacenter')
        volume = self.module.params.get('volume')
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        datacenter_server = ionoscloud.DataCentersApi(api_client=client)
        volume_server = ionoscloud.VolumesApi(api_client=client)
        snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

        # Locate UUID for virtual datacenter
        datacenter_list = datacenter_server.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, datacenter)

        # Locate UUID for volume
        volume_list = volume_server.datacenters_volumes_get(datacenter_id=datacenter_id, depth=1)
        volume_id = get_resource_id(self.module, volume_list, volume)

        # Locate snapshot by name/UUID
        snapshot_list = snapshot_server.snapshots_get(depth=1)
        snapshot = get_resource(self.module, snapshot_list, name)

        should_change = snapshot is None

        if self.module.check_mode:
            self.module.exit_json(changed=should_change)

        if not should_change:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                RETURNED_KEY: snapshot.to_dict()
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
                RETURNED_KEY: snapshot_response.to_dict()
            }

        except Exception as e:
            self.module.fail_json(msg="failed to create the snapshot: %s" % to_native(e))


    def restore_object(self, clients):
        """
        Restores a snapshot.

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            True if the snapshot started restoring, false otherwise
        """
        client = clients[0]
        datacenter = self.module.params.get('datacenter')
        volume = self.module.params.get('volume')
        snapshot = self.module.params.get('snapshot')
        wait = self.module.params.get('wait')

        datacenter_server = ionoscloud.DataCentersApi(api_client=client)
        volume_server = ionoscloud.VolumesApi(api_client=client)
        snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

        # Locate UUID for virtual datacenter
        datacenter_list = datacenter_server.datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, datacenter)

        # Locate UUID for volume
        volume_list = volume_server.datacenters_volumes_get(datacenter_id=datacenter_id, depth=1)
        volume_id = get_resource_id(self.module, volume_list, volume)

        # Locate UUID for snapshot
        snapshot_list = snapshot_server.snapshots_get(depth=1)
        snapshot_id = get_resource_id(self.module, snapshot_list, snapshot)

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        try:
            snapshot_response, _, headers = volume_server.datacenters_volumes_restore_snapshot_post_with_http_info(
                datacenter_id=datacenter_id, volume_id=volume_id, snapshot_id=snapshot_id,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

            return {
                'changed': True,
                'failed': False,
                'action': 'restore',
                RETURNED_KEY: snapshot_response
            }

        except Exception as e:
            self.module.fail_json(msg="failed to restore the snapshot: %s" % to_native(e))


    def update_object(self, clients):
        """
        Updates a snapshot.

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            The snapshot instance
        """
        client = clients[0]
        snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

        snapshot = self.module.params.get('snapshot')

        # Locate snapshot by name
        snapshot_list = snapshot_server.snapshots_get(depth=1)

        snapshot = get_resource(self.module, snapshot_list, snapshot)

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        cpu_hot_plug = self.module.params.get('cpu_hot_plug')
        cpu_hot_unplug = self.module.params.get('cpu_hot_unplug')
        ram_hot_plug = self.module.params.get('ram_hot_plug')
        ram_hot_unplug = self.module.params.get('ram_hot_unplug')
        nic_hot_plug = self.module.params.get('nic_hot_plug')
        nic_hot_unplug = self.module.params.get('nic_hot_unplug')
        disc_virtio_hot_plug = self.module.params.get('disc_virtio_hot_plug')
        disc_virtio_hot_unplug = self.module.params.get('disc_virtio_hot_unplug')
        disc_scsi_hot_plug = self.module.params.get('disc_scsi_hot_plug')
        disc_scsi_hot_unplug = self.module.params.get('disc_scsi_hot_unplug')
        licence_type = self.module.params.get('licence_type')
        wait_timeout = self.module.params.get('wait_timeout')

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
                RETURNED_KEY: snapshot_response.to_dict()
            }

        except Exception as e:
            self.module.fail_json(msg="failed to update the snapshot: %s" % to_native(e))


    def absent_object(self, clients):
        """
        Removes a snapshot

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            True if the snapshot was removed, false otherwise
        """
        client = clients[0]
        snapshot_server = ionoscloud.SnapshotsApi(api_client=client)
        snapshot = self.module.params.get('snapshot')

        # Locate snapshot UUID
        snapshot_list = snapshot_server.snapshots_get(depth=1)
        snapshot_id = get_resource_id(self.module, snapshot_list, snapshot)

        if not snapshot_id:
            self.module.exit_json(changed=False)

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        try:
            snapshot_server.snapshots_delete(snapshot_id)
            return {
                'action': 'delete',
                'changed': True,
                'id': snapshot_id
            }
        except Exception as e:
            self.module.fail_json(msg="failed to remove the snapshot: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = SnapshotModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
