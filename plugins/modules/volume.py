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
module: volume
short_description: Create, update or destroy a volume.
description:
     - Allows you to create, update or remove a volume from a Ionos datacenter.
version_added: "2.0"
options:
  datacenter:
    description:
      - The datacenter in which to create the volumes.
    required: true
  name:
    description:
      - The name of the volumes. You can enumerate the names using auto_increment.
    required: true
  size:
    description:
      - The size of the volume.
    required: false
    default: 10
  bus:
    description:
      - The bus type.
    required: false
    default: VIRTIO
    choices: [ "IDE", "VIRTIO"]
  image:
    description:
      - The image alias or ID for the volume. This can also be a snapshot image ID.
    required: true
  image_password:
    description:
      - Password set for the administrative user.
    required: false
    version_added: "2.2"
  ssh_keys:
    description:
      - Public SSH keys allowing access to the virtual machine.
    required: false
    version_added: "2.2"
  disk_type:
    description:
      - The disk type of the volume.
    required: false
    default: HDD
    choices: [ "HDD", "SSD" ]
  licence_type:
    description:
      - The licence type for the volume. This is used when the image is non-standard.
    required: false
    default: UNKNOWN
    choices: ["LINUX", "WINDOWS", "UNKNOWN" , "OTHER", "WINDOWS2016"]
  availability_zone:
    description:
      - The storage availability zone assigned to the volume.
    required: false
    default: None
    choices: [ "AUTO", "ZONE_1", "ZONE_2", "ZONE_3" ]
    version_added: "2.3"
  count:
    description:
      - The number of volumes you wish to create.
    required: false
    default: 1
  auto_increment:
    description:
      - Whether or not to increment a single number in the name for created virtual machines.
    default: yes
    choices: ["yes", "no"]
  instance_ids:
    description:
      - list of instance ids, currently only used when state='absent' to remove instances.
    required: false
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
    default: "present"
    choices: ["present", "absent", "update"]

requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLES = '''

# Create Multiple Volumes

- volume:
    datacenter: Tardis One
    name: vol%02d
    count: 5
    auto_increment: yes
    wait_timeout: 500
    state: present

# Update Volumes

- volume:
    datacenter: Tardis One
    instance_ids:
      - 'vol01'
      - 'vol02'
    size: 50
    bus: IDE
    wait_timeout: 500
    state: update

# Remove Volumes

- volume:
    datacenter: Tardis One
    instance_ids:
      - 'vol01'
      - 'vol02'
    wait_timeout: 500
    state: absent

'''

import re
import traceback

from uuid import UUID

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Volume, VolumeProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.six.moves import xrange
from ansible.module_utils._text import to_native

DISK_TYPES = ['HDD',
              'SSD']

BUS_TYPES = ['VIRTIO',
             'IDE']

AVAILABILITY_ZONES = ['AUTO',
                      'ZONE_1',
                      'ZONE_2',
                      'ZONE_3']

LICENCE_TYPES = ['LINUX',
                 'WINDOWS',
                 'UNKNOWN',
                 'OTHER',
                 'WINDOWS2016']

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def _create_volume(module, volume_server, datacenter, name, client):
    size = module.params.get('size')
    bus = module.params.get('bus')
    image = module.params.get('image')
    image_password = module.params.get('image_password')
    ssh_keys = module.params.get('ssh_keys')
    disk_type = module.params.get('disk_type')
    availability_zone = module.params.get('availability_zone')
    licence_type = module.params.get('licence_type')
    image_alias = module.params.get('image_alias')
    cpu_hot_plug = module.params.get('cpu_hot_plug')
    ram_hot_plug = module.params.get('ram_hot_plug')
    nic_hot_plug = module.params.get('nic_hot_plug')
    nic_hot_unplug = module.params.get('nic_hot_unplug')
    disc_virtio_hot_plug = module.params.get('disc_virtio_hot_plug')
    disc_virtio_hot_unplug = module.params.get('disc_virtio_hot_unplug')
    backupunit_id = module.params.get('backupunit_id')
    user_data = module.params.get('user_data')
    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        volume_properties = VolumeProperties(name=name, type=disk_type, size=size, availability_zone=availability_zone,
                                             image=image,
                                             image_password=image_password, image_alias=image_alias, ssh_keys=ssh_keys,
                                             bus=bus,
                                             licence_type=licence_type, cpu_hot_plug=cpu_hot_plug,
                                             ram_hot_plug=ram_hot_plug, nic_hot_plug=nic_hot_plug,
                                             nic_hot_unplug=nic_hot_unplug, disc_virtio_hot_plug=disc_virtio_hot_plug,
                                             disc_virtio_hot_unplug=disc_virtio_hot_unplug, backupunit_id=backupunit_id,
                                             user_data=user_data)

        volume = Volume(properties=volume_properties)

        try:
            UUID(image)
        except Exception:
            volume.properties.image_alias = image
        else:
            volume.properties.image = image
            volume.properties.licence_type = None

        response = volume_server.datacenters_volumes_post_with_http_info(datacenter_id=datacenter, volume=volume)
        (volume_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except Exception as e:
        module.fail_json(msg="failed to create the volume: %s" % to_native(e))

    return volume_response


def _update_volume(module, volume_server, api_client, datacenter, volume_id):
    size = module.params.get('size')
    bus = module.params.get('bus')
    disk_type = module.params.get('disk_type')
    availability_zone = module.params.get('availability_zone')
    licence_type = module.params.get('licence_type')
    image_alias = module.params.get('image_alias')
    cpu_hot_plug = module.params.get('cpu_hot_plug')
    ram_hot_plug = module.params.get('ram_hot_plug')
    nic_hot_plug = module.params.get('nic_hot_plug')
    nic_hot_unplug = module.params.get('nic_hot_unplug')
    disc_virtio_hot_plug = module.params.get('disc_virtio_hot_plug')
    disc_virtio_hot_unplug = module.params.get('disc_virtio_hot_unplug')

    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        volume_properties = VolumeProperties(size=size, availability_zone=availability_zone,
                                             image_alias=image_alias, bus=bus,
                                             cpu_hot_plug=cpu_hot_plug, ram_hot_plug=ram_hot_plug,
                                             nic_hot_plug=nic_hot_plug, nic_hot_unplug=nic_hot_unplug,
                                             disc_virtio_hot_plug=disc_virtio_hot_plug,
                                             disc_virtio_hot_unplug=disc_virtio_hot_unplug)
        volume = Volume(properties=volume_properties)
        response = volume_server.datacenters_volumes_put_with_http_info(
            datacenter_id=datacenter,
            volume_id=volume_id,
            volume=volume
        )
        (volume_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            api_client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except Exception as e:
        module.fail_json(msg="failed to update the volume: %s" % to_native(e))

    return volume_response


def _delete_volume(module, volume_server, datacenter, volume):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        volume_server.datacenters_volumes_delete(datacenter, volume)
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
    auto_increment = module.params.get('auto_increment')
    count = module.params.get('count')

    volume_server = ionoscloud.VolumeApi(client)
    datacenter_server = ionoscloud.DataCenterApi(client)
    servers_server = ionoscloud.ServerApi(client)

    datacenter_found = False
    volumes = []
    instance_ids = []

    datacenter_list = datacenter_server.datacenters_get(depth=2)
    for d in datacenter_list.items:
        dc = datacenter_server.datacenters_find_by_id(d.id)
        if datacenter in [dc.properties.name, dc.id]:
            datacenter = d.id
            datacenter_found = True
            break

    if not datacenter_found:
        module.fail_json(msg='datacenter could not be found.')

    if auto_increment:
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
        names = [name] * count

    changed = False

    # Prefetch a list of volumes for later comparison.
    volume_list = volume_server.datacenters_volumes_get(datacenter, depth=2)

    for name in names:
        # Skip volume creation if a volume with the same name already exists.
        if _get_instance_id(volume_list, name):
            continue

        create_response = _create_volume(module, volume_server, str(datacenter), name, client)
        volumes.append(create_response)
        instance_ids.append(create_response.id)
        _attach_volume(module, servers_server, datacenter, create_response.id)
        changed = True

    results = {
        'changed': changed,
        'failed': False,
        'volumes': [v.to_dict() for v in volumes],
        'action': 'create',
        'instance_ids': instance_ids
    }

    return results


def update_volume(module, client):
    """
    Update volumes.

    This will update one or more volumes in a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        dict of updated volumes
    """
    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')

    volume_server = ionoscloud.VolumeApi(client)
    datacenter_server = ionoscloud.DataCenterApi(client)

    datacenter_found = False
    failed = True
    changed = False
    volumes = []
    update_response = None

    datacenter_list = datacenter_server.datacenters_get(depth=2)
    for d in datacenter_list.items:
        dc = datacenter_server.datacenters_find_by_id(d.id)
        if datacenter in [dc.properties.name, dc.id]:
            datacenter = d.id
            datacenter_found = True
            break

    if not datacenter_found:
        module.fail_json(msg='datacenter could not be found.')

    for n in instance_ids:
        if (uuid_match.match(n)):
            update_response = _update_volume(module, volume_server, client, datacenter, n)
            changed = True
        else:
            volume_list = volume_server.datacenters_volumes_get(datacenter, depth=2)
            for v in volume_list.items:
                if n == v.properties.name:
                    volume_id = v.id
                    update_response = _update_volume(module, volume_server, client, datacenter, volume_id)
                    changed = True

        volumes.append(update_response)
        failed = False

    results = {
        'changed': changed,
        'failed': failed,
        'volumes': [v.to_dict() for v in volumes],
        'action': 'update',
        'instance_ids': {
            'instances': [i.id for i in volumes],
        }
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

    volume_server = ionoscloud.VolumeApi(client)
    datacenter_server = ionoscloud.DataCenterApi(client)

    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of volume ids or names, aborting')

    datacenter = module.params.get('datacenter')
    changed = False
    instance_ids = module.params.get('instance_ids')

    volume_id = None

    # Locate UUID for Datacenter
    if not (uuid_match.match(datacenter)):
        datacenter_list = datacenter_server.datacenters_get(depth=2)
        for d in datacenter_list.items:
            dc = datacenter_server.datacenters_find_by_id(d.id)
            if datacenter in [dc.properties.name, dc.id]:
                datacenter = d.id
                break

    for n in instance_ids:
        if (uuid_match.match(n)):
            _delete_volume(module, volume_server, datacenter, n)
            changed = True
        else:
            volumes = volume_server.datacenters_volumes_get(datacenter, depth=2)
            for v in volumes.items:
                if n == v.properties.name:
                    volume_id = v.id
                    _delete_volume(module, volume_server, datacenter, volume_id)
                    changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': volume_id
    }


def _attach_volume(module, server_client, datacenter, volume_id):
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
        if not (uuid_match.match(server)):
            server_list = server_client.datacenters_servers_get(datacenter_id=datacenter, depth=2)
            for s in server_list.items:
                if server == s.properties.name:
                    server = s.id
                    break

        try:
            volume = Volume(id=volume_id)
            return server_client.datacenters_servers_volumes_post(datacenter_id=datacenter, server_id=server,
                                                                  volume=volume)
        except Exception as e:
            module.fail_json(msg='failed to attach volume: %s' % to_native(e))


def _get_instance_id(instance_list, identity):
    """
    Return instance UUID by name or ID, if found.
    """
    for i in instance_list.items:
        if identity in (i.properties.name, i.id):
            return i.id
    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter=dict(type='str'),
            server=dict(type='str'),
            name=dict(type='str'),
            size=dict(type='int', default=10),
            image=dict(type='str'),
            image_alias=dict(type='str'),
            backupunit_id=dict(type='str'),
            user_data=dict(type='str'),
            image_password=dict(type='str', default=None, no_log=True),
            ssh_keys=dict(type='list', default=[]),
            cpu_hot_plug=dict(type='bool'),
            ram_hot_plug=dict(type='bool'),
            nic_hot_plug=dict(type='bool'),
            nic_hot_unplug=dict(type='bool'),
            disc_virtio_hot_plug=dict(type='bool'),
            disc_virtio_hot_unplug=dict(type='bool'),
            bus=dict(type='str', choices=BUS_TYPES, default='VIRTIO'),
            disk_type=dict(type='str', choices=DISK_TYPES, default='HDD'),
            licence_type=dict(type='str', choices=LICENCE_TYPES, default='UNKNOWN'),
            availability_zone=dict(type='str', choices=AVAILABILITY_ZONES, default=None),
            count=dict(type='int', default=1),
            auto_increment=dict(type='bool', default=True),
            instance_ids=dict(type='list', default=[]),
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
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')

    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    state = module.params.get('state')

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            if not module.params.get('datacenter'):
                module.fail_json(msg='datacenter parameter is required for creating, updating or deleting volumes.')

            try:
                (result) = delete_volume(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set volume state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('datacenter'):
                module.fail_json(msg='datacenter parameter is required for new instance')
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for new instance')

            try:
                (volume_dict_array) = create_volume(module, api_client)
                module.exit_json(**volume_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set volume state: %s' % to_native(e))

        elif state == 'update':
            try:
                (volume_dict_array) = update_volume(module, api_client)
                module.exit_json(**volume_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update volume: %s' % to_native(e))


if __name__ == '__main__':
    main()
