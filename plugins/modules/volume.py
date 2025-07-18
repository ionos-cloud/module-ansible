#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import re
import traceback

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Volume, VolumeProperties
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import xrange
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, check_required_arguments,
    get_sdk_config, get_resource_id, get_resource, get_paginated,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Volume'
RETURNED_KEY = 'volume'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter in which to create the volumes.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'server': {
        'description': ['The server to which to attach the volume.'],
        'available': ['present'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': STATES,
        'type': 'str',
    },
    'size': {
        'description': ['The size of the volume in GB.'],
        'available': ['update', 'present'],
        'type': 'int',
    },
    'bus': {
        'description': ['The bus type for this volume; default is VIRTIO.'],
        'choices_docs': ['VIRTIO', 'IDE', 'UNKNOWN'],
        'default': 'VIRTIO',
        'available': ['present', 'update'],
        'type': 'str',
    },
    'image': {
        'description': ['Image or snapshot ID to be used as template for this volume. MSSQL Enterprise Images can be used only if the feature toggle for MSSQL Enterprise is enabled on the contract.'],
        'available': ['present'],
        'type': 'str',
    },
    'image_password': {
        'description': ['Initial password to be set for installed OS. Works with public images only. Not modifiable, forbidden in update requests. Password rules allows all characters from a-z, A-Z, 0-9.'],
        'available': ['present'],
        'type': 'str',
        'no_log': True,
        'version_added': '2.2',
    },
    'ssh_keys': {
        'description': ['Public SSH keys are set on the image as authorized keys for appropriate SSH login to the instance using the corresponding private key. This field may only be set in creation requests. When reading, it always returns null. SSH keys are only supported if a public Linux image is used for the volume creation.'],
        'available': ['present'],
        'type': 'list',
        'version_added': '2.2',
    },
    'disk_type': {
        'description': ['The disk type of the volume.'],
        'choices_docs': ['HDD', 'SSD', 'SSD Premium', 'SSD Standard', 'DAS', 'ISO'],
        'available': ['present'],
        'type': 'str',
    },
    'licence_type': {
        'description': ['OS type for this volume.'],
        'choices_docs': ['UNKNOWN', 'WINDOWS', 'WINDOWS2016', 'WINDOWS2019', 'WINDOWS2022', 'WINDOWS2025', 'RHEL', 'LINUX', 'OTHER'],
        'available': ['present'],
        'type': 'str',
    },
    'availability_zone': {
        'description': ['The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD.'],
        'choices_docs': ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3'],
        'available': ['present', 'update'],
        'type': 'str',
        'version_added': '2.3',
    },
    'count': {
        'description': ['The number of volumes you wish to create.'],
        'available': ['present'],
        'default': 1,
        'type': 'int',
    },
    'instance_ids': {
        'description': ["list of instance ids or names. Should only contain one ID if renaming in update state"],
        'available': ['absent', 'update'],
        'default': [],
        'type': 'list',
    },
    'backupunit': {
        'description': ['The ID of the backup unit that the user has access to. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either \'public image\' or \'imageAlias\' in conjunction with this property.'],
        'available': ['present'],
        'type': 'str',
    },
    'user_data': {
        'description': ['The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either \'public image\' or \'imageAlias\' that has cloud-init compatibility in conjunction with this property.'],
        'available': ['present'],
        'type': 'str',
    },
    'cpu_hot_plug': {
        'description': ['Hot-plug capable CPU (no reboot required).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'ram_hot_plug': {
        'description': ['Hot-plug capable RAM (no reboot required).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'nic_hot_plug': {
        'description': ['Hot-plug capable NIC (no reboot required).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'nic_hot_unplug': {
        'description': ['Hot-unplug capable NIC (no reboot required).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'disc_virtio_hot_plug': {
        'description': ['Hot-plug capable Virt-IO drive (no reboot required).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'disc_virtio_hot_unplug': {
        'description': ['Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "size", "note": "" },
    { "name": "disk_type", "note": "" },
    { "name": "availability_zone", "note": "" },
    { "name": "licence_type", "note": "" },
    {
        "name": "user_data",
        "note": "Might trigger replace just by being set as this parameter is retrieved from the API as the image ID, so when using an alias it will always cause a resource replacement!",
    },
    {
        "name": "image",
        "note": "Might trigger replace just by being set as this parameter is retrieved from the API as the image ID, so when using an alias it will always cause a resource replacement!",
    },
    {
        "name": "image_password",
        "note": "Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!",
    },
    {
        "name": "ssh_keys",
        "note": "Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!",
    },
    {
        "name": "backupunit",
        "note": "Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!",
    },
]

DOCUMENTATION = '''
---
module: volume
short_description: Create, update or destroy a volume.
description:
     - Allows you to create, update or remove a volume from a Ionos datacenter.
version_added: "2.0"
options:
    allow_replace:
        default: false
        description:
        - Boolean indicating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    availability_zone:
        choices:
        - AUTO
        - ZONE_1
        - ZONE_2
        - ZONE_3
        description:
        - The availability zone in which the volume should be provisioned. The storage
            volume will be provisioned on as few physical storage devices as possible,
            but this cannot be guaranteed upfront. This is uavailable for DAS (Direct
            Attached Storage), and subject to availability for SSD.
        required: false
        version_added: '2.3'
    backupunit:
        description:
        - The ID of the backup unit that the user has access to. The property is immutable
            and is only allowed to be set on creation of a new a volume. It is mandatory
            to provide either 'public image' or 'imageAlias' in conjunction with this
            property.
        required: false
    bus:
        choices:
        - VIRTIO
        - IDE
        - UNKNOWN
        default: VIRTIO
        description:
        - The bus type for this volume; default is VIRTIO.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    count:
        default: 1
        description:
        - The number of volumes you wish to create.
        required: false
    cpu_hot_plug:
        description:
        - Hot-plug capable CPU (no reboot required).
        required: false
    datacenter:
        description:
        - The datacenter in which to create the volumes.
        required: true
    disc_virtio_hot_plug:
        description:
        - Hot-plug capable Virt-IO drive (no reboot required).
        required: false
    disc_virtio_hot_unplug:
        description:
        - Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows
            VMs.
        required: false
    disk_type:
        choices:
        - HDD
        - SSD
        - SSD Premium
        - SSD Standard
        - DAS
        - ISO
        description:
        - The disk type of the volume.
        required: false
    image:
        description:
        - Image or snapshot ID to be used as template for this volume. MSSQL Enterprise
            Images can be used only if the feature toggle for MSSQL Enterprise is enabled
            on the contract.
        required: false
    image_password:
        description:
        - Initial password to be set for installed OS. Works with public images only.
            Not modifiable, forbidden in update requests. Password rules allows all characters
            from a-z, A-Z, 0-9.
        no_log: true
        required: false
        version_added: '2.2'
    instance_ids:
        default: []
        description:
        - list of instance ids or names. Should only contain one ID if renaming in update
            state
        required: false
    licence_type:
        choices:
        - UNKNOWN
        - WINDOWS
        - WINDOWS2016
        - WINDOWS2019
        - WINDOWS2022
        - WINDOWS2025
        - RHEL
        - LINUX
        - OTHER
        description:
        - OS type for this volume.
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
    server:
        description:
        - The server to which to attach the volume.
        required: false
    size:
        description:
        - The size of the volume in GB.
        required: false
    ssh_keys:
        description:
        - Public SSH keys are set on the image as authorized keys for appropriate SSH
            login to the instance using the corresponding private key. This field may
            only be set in creation requests. When reading, it always returns null. SSH
            keys are only supported if a public Linux image is used for the volume creation.
        required: false
        version_added: '2.2'
    state:
        choices:
        - present
        - absent
        - update
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
    user_data:
        description:
        - The cloud-init configuration for the volume as base64 encoded string. The property
            is immutable and is only allowed to be set on creation of a new a volume.
            It is mandatory to provide either 'public image' or 'imageAlias' that has
            cloud-init compatibility in conjunction with this property.
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
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
'''

EXAMPLE_PER_STATE = {
  'present' : '''
name: Create volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  disk_type: SSD Premium
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  count: 2
  size: 20
  availability_zone: AUTO
  cpu_hot_plug: false
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  wait_timeout: 600
  wait: true
  state: present
register: volume_create_response
''',
  'update' : '''
name: Update no change
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  disk_type: SSD Premium
  size: 20
  availability_zone: AUTO
  image: 'c638b244-eeaa-11ef-8fa7-aee9942a25aa'
  licence_type: LINUX
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  allow_replace: false
  wait_timeout: 600
  wait: true
  state: update
register: volume_create_response_nochange
''',
  'absent' : '''
name: Delete volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute modified'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: 600
  state: absent
''',
}

EXAMPLES = """
name: Create volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  disk_type: SSD Premium
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  count: 2
  size: 20
  availability_zone: AUTO
  cpu_hot_plug: false
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  wait_timeout: 600
  wait: true
  state: present
register: volume_create_response


name: Update no change
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  disk_type: SSD Premium
  size: 20
  availability_zone: AUTO
  image: 'c638b244-eeaa-11ef-8fa7-aee9942a25aa'
  licence_type: LINUX
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  allow_replace: false
  wait_timeout: 600
  wait: true
  state: update
register: volume_create_response_nochange


name: Delete volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute modified'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: 600
  state: absent
"""

uuid_match = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _should_replace_object(module, existing_object, client):
    backupunit_id = get_resource_id(
        module,
        ionoscloud.BackupUnitsApi(client).backupunits_get(depth=1), 
        module.params.get('backupunit'),
    )

    return (
        module.params.get('size') is not None
        and int(existing_object.properties.size) != int(module.params.get('size'))
        and int(existing_object.properties.size) > int(module.params.get('size'))
        or module.params.get('disk_type') is not None
        and existing_object.properties.type != module.params.get('disk_type')
        or module.params.get('availability_zone') is not None
        and existing_object.properties.availability_zone != module.params.get('availability_zone')
        and 'AUTO' != module.params.get('availability_zone')
        or module.params.get('image') is not None
        and existing_object.properties.image != module.params.get('image')
        or module.params.get('licence_type') is not None
        and existing_object.properties.licence_type != module.params.get('licence_type')
        or backupunit_id is not None
        and existing_object.properties.backupunit_id != backupunit_id
        or module.params.get('user_data') is not None
        or module.params.get('image_password') is not None
        or module.params.get('ssh_keys') is not None
    )


def _should_update_object(module, existing_object, new_object_name):
    return (
        new_object_name is not None
        and existing_object.properties.name != new_object_name
        or module.params.get('size') is not None
        and int(existing_object.properties.size) != int(module.params.get('size'))
        and int(existing_object.properties.size) < int(module.params.get('size'))
        or module.params.get('cpu_hot_plug') is not None
        and existing_object.properties.cpu_hot_plug != module.params.get('cpu_hot_plug')
        or module.params.get('ram_hot_plug') is not None
        and existing_object.properties.ram_hot_plug != module.params.get('ram_hot_plug')
        or module.params.get('nic_hot_plug') is not None
        and existing_object.properties.nic_hot_plug != module.params.get('nic_hot_plug')
        or module.params.get('nic_hot_unplug') is not None
        and existing_object.properties.nic_hot_unplug != module.params.get('nic_hot_unplug')
        or module.params.get('disc_virtio_hot_plug') is not None
        and existing_object.properties.disc_virtio_hot_plug != module.params.get('disc_virtio_hot_plug')
        or module.params.get('disc_virtio_hot_unplug') is not None
        and existing_object.properties.disc_virtio_hot_unplug != module.params.get('disc_virtio_hot_unplug')
    )


def update_replace_object(module, client, datacenter_id, existing_object, new_object_name):
    if _should_replace_object(module, existing_object, client):
        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))
    
        new_object = _create_object(module, client, datacenter_id, new_object_name, existing_object).to_dict()
        _remove_object(module, client, datacenter_id, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object, new_object_name):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, datacenter_id, new_object_name, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def _create_object(module, client, datacenter_id, name, existing_object=None):
    size = module.params.get('size')
    bus = module.params.get('bus')
    image = module.params.get('image')
    image_password = module.params.get('image_password')
    ssh_keys = module.params.get('ssh_keys')
    disk_type = module.params.get('disk_type')
    availability_zone = module.params.get('availability_zone')
    licence_type = module.params.get('licence_type')
    cpu_hot_plug = module.params.get('cpu_hot_plug')
    ram_hot_plug = module.params.get('ram_hot_plug')
    nic_hot_plug = module.params.get('nic_hot_plug')
    nic_hot_unplug = module.params.get('nic_hot_unplug')
    disc_virtio_hot_plug = module.params.get('disc_virtio_hot_plug')
    disc_virtio_hot_unplug = module.params.get('disc_virtio_hot_unplug')
    backupunit_id = get_resource_id(
        module,
        ionoscloud.BackupUnitsApi(client).backupunits_get(depth=1), 
        module.params.get('backupunit'),
    )
    user_data = module.params.get('user_data')

    if existing_object is not None:
        size = int(existing_object.properties.size) if size is None else size
        bus = existing_object.properties.bus if bus is None else bus
        image = existing_object.properties.image if image is None else image
        image_password = existing_object.properties.image_password if image_password is None else image_password
        ssh_keys = existing_object.properties.ssh_keys if ssh_keys is None else ssh_keys
        disk_type = existing_object.properties.type if disk_type is None else disk_type
        availability_zone = existing_object.properties.availability_zone if availability_zone is None else availability_zone
        cpu_hot_plug = existing_object.properties.cpu_hot_plug if cpu_hot_plug is None else cpu_hot_plug
        ram_hot_plug = existing_object.properties.ram_hot_plug if ram_hot_plug is None else ram_hot_plug
        nic_hot_plug = existing_object.properties.nic_hot_plug if nic_hot_plug is None else nic_hot_plug
        nic_hot_unplug = existing_object.properties.nic_hot_unplug if nic_hot_unplug is None else nic_hot_unplug
        disc_virtio_hot_plug = existing_object.properties.disc_virtio_hot_plug if disc_virtio_hot_plug is None else disc_virtio_hot_plug
        disc_virtio_hot_unplug = existing_object.properties.disc_virtio_hot_unplug if disc_virtio_hot_unplug is None else disc_virtio_hot_unplug
        backupunit_id = existing_object.properties.backupunit_id if backupunit_id is None else backupunit_id
        user_data = existing_object.properties.user_data if user_data is None else user_data

    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    if module.check_mode:
        module.exit_json(changed=True)
   
    volumes_api = ionoscloud.VolumesApi(client)

    try:
        volume_properties = VolumeProperties(
            name=name, type=disk_type, size=size, availability_zone=availability_zone,
            image_password=image_password, ssh_keys=ssh_keys, bus=bus,
            licence_type=licence_type, cpu_hot_plug=cpu_hot_plug,
            ram_hot_plug=ram_hot_plug, nic_hot_plug=nic_hot_plug,
            nic_hot_unplug=nic_hot_unplug, disc_virtio_hot_plug=disc_virtio_hot_plug,
            disc_virtio_hot_unplug=disc_virtio_hot_unplug, backupunit_id=backupunit_id,
            user_data=user_data,
        )
        if image:
            if uuid_match.match(image):
                volume_properties.image = image
            else:
                volume_properties.image_alias = image

        volume = Volume(properties=volume_properties)

        volume_response, _, headers = volumes_api.datacenters_volumes_post_with_http_info(datacenter_id, volume)

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return volume_response

    except Exception as e:
        module.fail_json(msg="failed to create the volume: %s" % to_native(e))


def _update_object(module, client, datacenter_id, name, existing_object):
    size = module.params.get('size')
    bus = module.params.get('bus')
    cpu_hot_plug = module.params.get('cpu_hot_plug')
    ram_hot_plug = module.params.get('ram_hot_plug')
    nic_hot_plug = module.params.get('nic_hot_plug')
    nic_hot_unplug = module.params.get('nic_hot_unplug')
    disc_virtio_hot_plug = module.params.get('disc_virtio_hot_plug')
    disc_virtio_hot_unplug = module.params.get('disc_virtio_hot_unplug')

    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    volumes_api = ionoscloud.VolumesApi(client)

    if module.check_mode:
        module.exit_json(changed=True)

    volume = Volume(properties=VolumeProperties(
        name=name if name is not None else existing_object.properties.name, size=size,
        bus=bus, cpu_hot_plug=cpu_hot_plug,
        ram_hot_plug=ram_hot_plug, nic_hot_plug=nic_hot_plug,
        nic_hot_unplug=nic_hot_unplug, disc_virtio_hot_plug=disc_virtio_hot_plug,
        disc_virtio_hot_unplug=disc_virtio_hot_unplug,
    ))

    try:
        volume_response, _, headers = volumes_api.datacenters_volumes_put_with_http_info(
            datacenter_id=datacenter_id,
            volume_id=existing_object.id,
            volume=volume,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        return volume_response

    except Exception as e:
        module.fail_json(msg="failed to update the volume: %s" % to_native(e))


def _remove_object(module, client, datacenter_id, volume):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    volumes_api = ionoscloud.VolumesApi(client)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        _, _, headers = volumes_api.datacenters_volumes_delete_with_http_info(datacenter_id, volume.id)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except Exception as e:
        module.fail_json(msg="failed to remove the volume: %s" % to_native(e))


def create_volume(module, client):
    """
    Create volumes.

    This will create one or more volumes in a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        dict of created volumes
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    count = module.params.get('count')

    volumes_api = ionoscloud.VolumesApi(client)
    datacenters_api = ionoscloud.DataCentersApi(client)
    servers_api = ionoscloud.ServersApi(client)

    datacenter_list = get_paginated(datacenters_api.datacenters_get)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter, fail_not_found=True)

    if datacenter_id is None:
        module.fail_json(msg='datacenter could not be found.')

    # Provide unique names by appending an auto incremented value at end of name
    if count > 1:
        numbers = set()
        count_offset = 1

        try:
            name % 0
        except TypeError as e:
            if (hasattr(e, 'message') and e.message.startswith('not all') or to_native(e).startswith('not all')):
                name = '%s%%d' % name
            else:
                module.fail_json(msg=e.message, exception=traceback.format_exc())

        number_range = xrange(count_offset, count_offset + count + len(numbers))
        available_numbers = list(set(number_range).difference(numbers))
        names = []
        numbers_to_use = available_numbers[:count]
        for number in numbers_to_use:
            names.append(name % number)
    else:
        names = [name]

    # Prefetch a list of volumes for later comparison.
    volume_list = volumes_api.datacenters_volumes_get(datacenter_id, depth=1)

    volumes = []
    instance_ids = []

    changed = False
    for name in names:
        existing_volume = get_resource(module, volume_list, name)

        if existing_volume is not None:
            update_replace_result = update_replace_object(module, client, datacenter_id, existing_volume, name)
            volume = update_replace_result[RETURNED_KEY]
            if update_replace_result['changed']:
                changed = True
        else:
            volume = _create_object(module, client, datacenter_id, name).to_dict()
            changed = True
        instance_ids.append(volume['id'])
        _attach_volume(module, servers_api, datacenter_id, volume['id'])
        volumes.append(volume)

    results = {
        'changed': changed,
        'failed': False,
        'volumes': volumes,
        'action': 'create',
        'instance_ids': instance_ids,
    }

    return results


def update_volume(module, client):
    """
    Update volumes.

    This will update one or more volumes in a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        updated volume
    """
    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')
    name = module.params.get('name')

    volumes_api = ionoscloud.VolumesApi(client)
    datacenters_api = ionoscloud.DataCentersApi(client)

    if name is None:
        if not isinstance(instance_ids, list) or len(instance_ids) < 1:
            module.fail_json(msg='instance_ids should be a list of volume ids or names, aborting')
    else:
        if isinstance(instance_ids, list) and len(instance_ids) > 1:
            module.fail_json(msg='when renaming, instance_ids can only have one id at most')

    changed = False

    datacenter_list = get_paginated(datacenters_api.datacenters_get)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter, fail_not_found=True)
    if datacenter_id is None:
        module.fail_json(msg='datacenter could not be found.')

    volume_list = volumes_api.datacenters_volumes_get(datacenter_id, depth=1)

    # Fail early if one of the ids provided doesn't match any volume
    checked_instances = []
    for instance in instance_ids:
        volume = get_resource(module, volume_list, instance)
        if volume is None:
            module.fail_json(msg='Volume \'%s\' not found.' % str(instance))
        checked_instances.append(volume)

    updated_volumes = []
    for instance in checked_instances:
        existing_volume_by_name = None if name is None else get_resource_id(module, volume_list, name)
        if existing_volume_by_name is not None:
            module.fail_json(msg='A volume with the name %s already exists.' % name)

        if volume is not None:
            update_replace_result = update_replace_object(module, client, datacenter_id, instance, name)
            update_response = update_replace_result[RETURNED_KEY]
            if update_replace_result['changed']:
                changed = True
            updated_volumes.append(update_response)

    results = {
        'changed': changed,
        'failed': False,
        'volume': [updated_volumes],
        'action': 'update'
    }

    return results


def delete_volume(module, client):
    """
    Remove volumes.

    This will remove one or more volumes from a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the volumes were removed, false otherwise
    """

    volumes_api = ionoscloud.VolumesApi(client)
    datacenters_api = ionoscloud.DataCentersApi(client)

    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of volume ids or names, aborting')

    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')

    # Locate UUID for Datacenter
    datacenter_list = get_paginated(datacenters_api.datacenters_get)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter, fail_not_found=True)

    volumes = volumes_api.datacenters_volumes_get(datacenter_id, depth=1)

    changed = False
    volume = None
    for n in instance_ids:
        volume = get_resource(module, volumes, n)
        if volume is not None:
            _remove_object(module, client, datacenter_id, volume)
            changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': volume.id if volume else None,
    }


def _attach_volume(module, servers_api, datacenter_id, volume_id):
    """
    Attaches a volume.

    This will attach a volume to the server.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        the volume instance being attached
    """
    server = module.params.get('server')

    # Locate UUID for Server
    if server:
        server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
        server_id = get_resource_id(module, server_list, server)

        try:
            return servers_api.datacenters_servers_volumes_post(
                datacenter_id=datacenter_id, server_id=server_id, volume=Volume(id=volume_id),
            )
        except Exception as e:
            module.fail_json(msg='failed to attach volume: %s' % to_native(e))


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME, OPTIONS)
        try:
            if state == 'absent':
                module.exit_json(**delete_volume(module, api_client))
            elif state == 'present':
                module.exit_json(**create_volume(module, api_client))
            elif state == 'update':
                module.exit_json(**update_volume(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
