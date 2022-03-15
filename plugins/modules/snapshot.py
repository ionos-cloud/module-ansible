#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import copy
import re
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Snapshot, SnapshotProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Snapshot'

LICENCE_TYPES = ['LINUX', 'WINDOWS', 'UNKNOWN', 'OTHER', 'WINDOWS2016']
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
        'description': ['The name of the snapshot.'],
        'available': STATES,
        'required': ['restore', 'update', 'absent'],
        'type': 'str',
    },
    'description': {
        'description': ['The description of the snapshot.'],
        'available': ['present'],
        'type': 'str',
    },
    'licence_type': {
        'description': ['The license type used'],
        'choices': ['LINUX', 'WINDOWS', 'UNKNOWN', 'OTHER', 'WINDOWS2016'],
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
        'description': ['Hot-plug capable RAM (no reboot required)'],
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
        'description': ['Hot-unplug capable NIC (no reboot required)'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_scsi_hot_plug': {
        'description': ['Hot-plug capable SCSI drive (no reboot required).'],
        'available': ['update'],
        'type': 'bool',
    },
    'disc_scsi_hot_unplug': {
        'description': ['Hot-unplug capable SCSI drive (no reboot required). Not supported with Windows VMs.'],
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
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}

def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

DOCUMENTATION = '''
---
module: snapshot
short_description: Create, restore, update or remove a snapshot.
description:
     - This module allows you to create or remove a snapshot.
version_added: "2.4"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a snapshot
  - name: Create snapshot
    snapshot:
      datacenter: production DC
      volume: master
      name: boot volume image
      state: present

  ''',
  'update' : '''# Update a snapshot
  - name: Update snapshot
    snapshot:
      name: "boot volume image"
      description: Ansible test snapshot - RENAME
      state: update
  ''',
  'restore' : '''# Restore a snapshot
  - name: Restore snapshot
    snapshot:
      datacenter: production DC
      volume: slave
      name: boot volume image
      state: restore
  ''',
  'absent' : '''# Remove a snapshot
  - name: Remove snapshot
    snapshot:
      name: master-Snapshot-11/30/2017
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    volume_server = ionoscloud.VolumesApi(api_client=client)
    snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

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

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    volume_server = ionoscloud.VolumesApi(api_client=client)
    snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

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
    snapshot_server = ionoscloud.SnapshotsApi(api_client=client)

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

    snapshot_server = ionoscloud.SnapshotsApi(api_client=client)
    name = module.params.get('name')

    # Locate UUID for snapshot
    snapshot_list = snapshot_server.snapshots_get(depth=2)
    snapshot = _get_resource(snapshot_list, name)

    if not snapshot:
        module.exit_json(changed=False)

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


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
      arguments[option_name] = {
        'type': option['type'],
      }
      for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
        if option.get(key) is not None:
          arguments[option_name][key] = option.get(key)

      if option.get('env_fallback'):
        arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

      if len(option.get('required', [])) == len(STATES):
        arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'absent':
                module.exit_json(**delete_snapshot(module, api_client))
            elif state == 'present':
                module.exit_json(**create_snapshot(module, api_client))
            elif state == 'restore':
                module.exit_json(**restore_snapshot(module, api_client))
            elif state == 'update':
                module.exit_json(**update_snapshot(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
