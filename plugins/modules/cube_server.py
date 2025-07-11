#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import re
import traceback

from uuid import uuid4

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import (Volume, VolumeProperties, Server, ServerProperties, Datacenter,
                                   DatacenterProperties, Nic, NicProperties, LanPropertiesPost,
                                   LanPost, ServerEntities, Nics, Volumes)
    from ionoscloud.rest import ApiException
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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['resume', 'suspend', 'absent', 'present', 'update']
OBJECT_NAME = 'CUBE Server'
RETURNED_KEY = 'server'

OPTIONS = {
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    'assign_public_ip': {
        'description': ['This will assign the machine to the public LAN. If no LAN exists with public Internet access it is created.'],
        'available': ['present'],
        'choices': [True, False],
        'default': False,
        'type': 'bool',
    },
    'image': {
        'description': ['The image alias or ID for creating the virtual machine.'],
        'required': ['present'],
        'available': ['present'],
        'type': 'str',
    },
    'image_password': {
        'description': ['Password set for the administrative user.'],
        'available': ['present'],
        'version_added': '2.2',
        'no_log': True,
        'type': 'str',
    },
    'ssh_keys': {
        'description': ['Public SSH keys allowing access to the virtual machine.'],
        'available': ['present'],
        'version_added': '2.2',
        'default': [],
        'type': 'list',
    },
    'user_data': {
        'description': ['The cloud-init configuration for the volume as base64 encoded string.'],
        'available': ['present'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The datacenter to provision this virtual machine.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'availability_zone': {
        'description': ['The availability zone in which the server should be provisioned.'],
        'available': ['present'],
        'choices_docs': ['AUTO', 'ZONE_1', 'ZONE_2'],
        'type': 'str',
        'version_added': '2.3',
    },
    'bus': {
        'description': ['The bus type for the volume.'],
        'available': ['present'],
        'choices_docs': ['IDE', 'VIRTIO'],
        'default': 'VIRTIO',
        'type': 'str',
    },
    'instance_ids': {
        'description': ["list of instance ids. Should only contain one ID if renaming in update state"],
        'available': ['running', 'stopped', 'resume', 'suspend', 'absent', 'update'],
        'default': [],
        'type': 'list',
    },
    'count': {
        'description': ['The number of virtual machines to create.'],
        'available': ['present'],
        'default': 1,
        'type': 'int',
    },
    'location': {
        'description': ['The datacenter location. Use only if you want to create the Datacenter or else this value is ignored.'],
        'available': ['present'],
        'choices_docs': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'],
        'default': 'us/las',
        'type': 'str',
    },
    'lan': {
        'description': ['The ID or name of the LAN you wish to add the servers to (can be a string or a number).'],
        'available': ['present'],
        'type': 'str',
    },
    'nat': {
        'description': ['Boolean value indicating if the private IP address has outbound access to the public Internet.'],
        'available': ['present'],
        'choices': [True, False],
        'default': False,
        'type': 'bool',
        'version_added': '2.3',
    },
    'remove_boot_volume': {
        'description': ["Remove the bootVolume of the virtual machine you're destroying."],
        'available': ['present'],
        'choices': [True, False],
        'default': True,
        'type': 'bool',
    },
    'disk_type': {
        'description': ['The disk type for the volume.'],
        'available': ['present'],
        'choices_docs': ['HDD', 'SSD', 'SSD Standard', 'SSD Premium', 'DAS'],
        'default': 'DAS',
        'type': 'str',
    },
    'nic_ips': {
        'description': ['The list of IPS for the NIC.'],
        'available': ['present'],
        'type': 'list',
        'elements': 'str',
    },
    'template_uuid': {
        'description': ['The ID of the template for creating a CUBE server; the available templates for CUBE servers can be found on the templates resource.'],
        'available': ['present'],
        'type': 'str',
    },
    'boot_volume': {
        'description': ['The volume used for boot.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'boot_cdrom': {
        'description': ['The CDROM used for boot.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "template_uuid", "note": "" },
    { "name": "availability_zone", "note": "" },
]

DOCUMENTATION = '''
---
module: cube_server
short_description: Create, update, destroy, resume, suspend, and reboot a Ionos CUBE virtual machine.
description:
     - Create, update, destroy, update, resume, suspend, and reboot a Ionos CUBE virtual machine.
       When the virtual machine is created it can optionally wait for it to be 'running' before returning.
version_added: "2.0"
options:
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    assign_public_ip:
        choices:
        - true
        - false
        default: false
        description:
        - This will assign the machine to the public LAN. If no LAN exists with public
            Internet access it is created.
        required: false
    availability_zone:
        choices:
        - AUTO
        - ZONE_1
        - ZONE_2
        description:
        - The availability zone in which the server should be provisioned.
        required: false
        version_added: '2.3'
    boot_cdrom:
        description:
        - The CDROM used for boot.
        required: false
    boot_volume:
        description:
        - The volume used for boot.
        required: false
    bus:
        choices:
        - IDE
        - VIRTIO
        default: VIRTIO
        description:
        - The bus type for the volume.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    count:
        default: 1
        description:
        - The number of virtual machines to create.
        required: false
    datacenter:
        description:
        - The datacenter to provision this virtual machine.
        required: true
    disk_type:
        choices:
        - HDD
        - SSD
        - SSD Standard
        - SSD Premium
        - DAS
        default: DAS
        description:
        - The disk type for the volume.
        required: false
    image:
        description:
        - The image alias or ID for creating the virtual machine.
        required: false
    image_password:
        description:
        - Password set for the administrative user.
        no_log: true
        required: false
        version_added: '2.2'
    instance_ids:
        default: []
        description:
        - list of instance ids. Should only contain one ID if renaming in update state
        required: false
    lan:
        description:
        - The ID or name of the LAN you wish to add the servers to (can be a string or
            a number).
        required: false
    location:
        choices:
        - us/las
        - us/ewr
        - de/fra
        - de/fkb
        - de/txl
        - gb/lhr
        default: us/las
        description:
        - The datacenter location. Use only if you want to create the Datacenter or else
            this value is ignored.
        required: false
    name:
        description:
        - The name of the  resource.
        required: false
    nat:
        choices:
        - true
        - false
        default: false
        description:
        - Boolean value indicating if the private IP address has outbound access to the
            public Internet.
        required: false
        version_added: '2.3'
    nic_ips:
        description:
        - The list of IPS for the NIC.
        elements: str
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    remove_boot_volume:
        choices:
        - true
        - false
        default: true
        description:
        - Remove the bootVolume of the virtual machine you're destroying.
        required: false
    ssh_keys:
        default: []
        description:
        - Public SSH keys allowing access to the virtual machine.
        required: false
        version_added: '2.2'
    state:
        choices:
        - resume
        - suspend
        - absent
        - present
        - update
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    template_uuid:
        description:
        - The ID of the template for creating a CUBE server; the available templates for
            CUBE servers can be found on the templates resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    user_data:
        description:
        - The cloud-init configuration for the volume as base64 encoded string.
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
    - "ionos-cloud >= 5.2.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
name: Provision a server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute 01'
  disk_type: DAS
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  location: de/txl
  count: 1
  assign_public_ip: true
  remove_boot_volume: true
  template_uuid: '72e73b81-8551-4e74-b398-fc63b39994af'
  availability_zone: AUTO
  wait: true
  wait_timeout: '500'
  state: present
register: server_cube
''',
  'update' : '''
name: Update server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute - UPDATED'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  wait: true
  wait_timeout: '500'
  state: update
''',
  'absent' : '''
name: Remove server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  remove_boot_volume: true
  wait_timeout: '500'
  state: absent
''',
  'resume' : '''
name: Resume server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  wait_timeout: '500'
  state: resume
''',
  'suspend' : '''
name: Suspend server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  wait_timeout: '500'
  state: suspend
''',
}

EXAMPLES = """
name: Provision a server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute 01'
  disk_type: DAS
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  location: de/txl
  count: 1
  assign_public_ip: true
  remove_boot_volume: true
  template_uuid: '72e73b81-8551-4e74-b398-fc63b39994af'
  availability_zone: AUTO
  wait: true
  wait_timeout: '500'
  state: present
register: server_cube


name: Update server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute - UPDATED'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  wait: true
  wait_timeout: '500'
  state: update


name: Remove server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  remove_boot_volume: true
  wait_timeout: '500'
  state: absent


name: Resume server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  wait_timeout: '500'
  state: resume


name: Suspend server
ionoscloudsdk.ionoscloud.cube_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute - UPDATED'
  wait_timeout: '500'
  state: suspend
"""

uuid_match = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_lan_by_id_or_properties(networks, id=None, **kwargs):
    matched_lan = None
    query = kwargs.items()

    if id is not None or len(query) > 0:
        for elan in networks:
            dict_lan_properties = elan.properties.__dict__

            if id is not None and str(elan.id) == str(id):
                matched_lan = elan
                break

            if all(dict_lan_properties.get('_' + pn, None) == pv for pn, pv in query):
                matched_lan = elan
                break

    return matched_lan


def _should_replace_object(module, existing_object):
    return (
        module.params.get('template_uuid') is not None
        and existing_object.properties.template_uuid != module.params.get('template_uuid')
        or module.params.get('availability_zone') is not None
        and existing_object.properties.availability_zone != module.params.get('availability_zone')
    )


def _should_update_object(module, existing_object, new_object_name):
    existing_boot_volume_id = existing_boot_cdrom_id = None
    if existing_object.properties.boot_volume:
        existing_boot_volume_id = existing_object.properties.boot_volume.id
    if existing_object.properties.boot_cdrom:
        existing_boot_cdrom_id = existing_object.properties.boot_cdrom.id
    return (
        new_object_name is not None
        and existing_object.properties.name != new_object_name
        or module.params.get('boot_cdrom') is not None
        and existing_boot_cdrom_id != module.params.get('boot_cdrom')
        or module.params.get('boot_volume') is not None
        and existing_boot_volume_id != module.params.get('boot_volume')
    )


def update_replace_object(module, client, datacenter_id, existing_object, new_object_name):
    if _should_replace_object(module, existing_object):
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
    disk_type = module.params.get('disk_type')
    availability_zone = module.params.get('availability_zone')
    image_password = module.params.get('image_password')
    ssh_keys = module.params.get('ssh_keys')
    user_data = module.params.get('user_data')
    bus = module.params.get('bus')
    lan = module.params.get('lan')
    image = module.params.get('image')
    assign_public_ip = module.boolean(module.params.get('assign_public_ip'))
    nic_ips = module.params.get('nic_ips')
    template_uuid = module.params.get('template_uuid')
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')

    if existing_object is not None:
        template_uuid = existing_object.properties.template_uuid if template_uuid is None else template_uuid
        boot_cdrom = existing_object.properties.boot_cdrom if boot_cdrom is None else boot_cdrom
        boot_volume = existing_object.properties.boot_volume if boot_volume is None else boot_volume
        availability_zone = existing_object.properties.availability_zone if availability_zone is None else availability_zone

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    servers_api = ionoscloud.ServersApi(api_client=client)
    lans_api = ionoscloud.LANsApi(api_client=client)

    nics = []

    if assign_public_ip:
        lans_list = lans_api.datacenters_lans_get(datacenter_id=datacenter_id, depth=1).items
        public_lan = _get_lan_by_id_or_properties(lans_list, public=True)

        public_ip_lan_id = public_lan.id if public_lan is not None else None

        if public_ip_lan_id is None:
            lan_properties = LanPropertiesPost(name='public', public=True)
            lan_post = LanPost(properties=lan_properties)

            lan_response, _, headers = lans_api.datacenters_lans_post_with_http_info(datacenter_id, lan_post)
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            public_ip_lan_id = lan_response.id

        nic = Nic(properties=NicProperties(name=str(uuid4()).replace('-', '')[:10], lan=int(public_ip_lan_id)))
        if nic_ips:
            nic.properties.ips = nic_ips
        nics.append(nic)

    if lan is not None:
        lans_list = lans_api.datacenters_lans_get(datacenter_id=datacenter_id, depth=1)
        matching_lan = get_resource(module, lans_list, lan)

        if (not any(n.properties.lan == int(matching_lan.id) for n in nics)) or len(nics) < 1:
            nic = Nic(properties=NicProperties(
                name=str(uuid4()).replace('-', '')[:10],
                lan=int(int(matching_lan.id)),
            ))
            if nic_ips:
                nic.properties.ips = nic_ips
            nics.append(nic)

    server_properties = ServerProperties(
        template_uuid=template_uuid, name=name,
        availability_zone=availability_zone,
        boot_cdrom=boot_cdrom, boot_volume=boot_volume, type='CUBE',
    )

    volume_properties = VolumeProperties(
        name=str(uuid4()).replace('-', '')[:10],
        type=disk_type, image_password=image_password,
        ssh_keys=ssh_keys, user_data=user_data, bus=bus,
    )

    if image:
        if uuid_match.match(image):
            volume_properties.image = image
        else:
            volume_properties.image_alias = image

    volume = Volume(properties=volume_properties)
    server_entities = ServerEntities(volumes=Volumes(items=[volume]), nics=Nics(items=nics))

    server = Server(properties=server_properties, entities=server_entities)

    try:
        server_response, _, headers = servers_api.datacenters_servers_post_with_http_info(datacenter_id, server)
        
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            client.wait_for(
                fn_request=lambda: servers_api.datacenters_servers_find_by_id(
                    datacenter_id=datacenter_id, server_id=server_response.id, depth=1,
                ),
                fn_check=lambda r: (r.entities.volumes is not None)
                        and (r.entities.volumes.items is not None) 
                        and (len(r.entities.volumes.items) > 0),
                    scaleup=10000,
                )

        # Depth 2 needed for nested nic and volume properties
        server = servers_api.datacenters_servers_find_by_id(
            datacenter_id=datacenter_id, server_id=server_response.id, depth=2,
        )

    except Exception as e:
        module.fail_json(msg="failed to create the new server: %s" % to_native(e))
    else:
        if len(server.entities.nics.items) > 0:
            server.nic = server.entities.nics.items[0]
    return server


def _resume_server(module, client, datacenter_id, server_id, current_state):
    state = module.params.get('state')
    servers_api = ionoscloud.ServersApi(api_client=client)
    server = None
    changed = False
    try:
        if state == 'resume':
            if current_state != 'RUNNING':
                response = servers_api.datacenters_servers_resume_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = servers_api.datacenters_servers_find_by_id(datacenter_id, server_id)
                if server_response.properties.vm_state == 'RUNNING':
                    changed = True
                    server = server_response

        else:
            if current_state != 'SUSPENDED':
                response = servers_api.datacenters_servers_suspend_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = servers_api.datacenters_servers_find_by_id(datacenter_id, server_id)
                if server_response.properties.vm_state == 'SUSPENDED':
                    changed = True
                    server = server_response

    except Exception as e:
        module.fail_json(
            msg="failed to resume or suspend the virtual machine %s at %s: %s" % (server_id, datacenter_id, to_native(e)))

    return changed, server


def _create_datacenter(module, client):
    datacenter = module.params.get('datacenter')
    location = module.params.get('location')
    wait_timeout = module.params.get('wait_timeout')
    datacenters_api = ionoscloud.DataCentersApi(api_client=client)

    datacenter_properties = DatacenterProperties(name=datacenter, location=location)
    datacenter = Datacenter(properties=datacenter_properties)

    try:
        response = datacenters_api.datacenters_post_with_http_info(datacenter=datacenter)
        (datacenter_response, _, headers) = response
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return datacenter_response

    except ApiException as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def _remove_boot_volume(module, client, datacenter_id, server_id):
    """
    Remove the boot volume from the server
    """
    servers_api = ionoscloud.ServersApi(api_client=client)
    try:
        server = servers_api.datacenters_servers_find_by_id(datacenter_id, server_id, depth=1)
        
        if server.properties.boot_volume:
            volume = servers_api.datacenters_servers_volumes_find_by_id(datacenter_id, server_id, server.properties.boot_volume.id)
            if volume.properties.type != 'DAS':
                servers_api.datacenters_servers_volumes_delete(datacenter_id, server_id, volume.id)
    except Exception as e:
        module.fail_json(msg="failed to remove the server's boot volume: %s" % to_native(e),
                         exception=traceback.format_exc())


def _update_object(module, client, datacenter_id, new_object_name, existing_object):
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')

    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    servers_api = ionoscloud.ServersApi(api_client=client)

    new_server_properties = ServerProperties(
        name=new_object_name if new_object_name is not None else existing_object.properties.name,
        boot_cdrom=boot_cdrom, boot_volume=boot_volume,
    )
    try:
        server_response, _, headers = servers_api.datacenters_servers_patch_with_http_info(
            datacenter_id=datacenter_id, server_id=existing_object.id, server=new_server_properties,
        )

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        return server_response
    except Exception as e:
        module.fail_json(msg="failed to update the server: %s" % to_native(e), exception=traceback.format_exc())


def _remove_object(module, client, datacenter_id, existing_object):
    if module.check_mode:
        module.exit_json(changed=True)

    wait_timeout = module.params.get('wait_timeout')
    wait = module.params.get('wait')

    servers_api = ionoscloud.ServersApi(api_client=client)

    # Remove the server's boot volume
    if module.params.get('remove_boot_volume'):
        _remove_boot_volume(module, client, datacenter_id, existing_object.id)

    # Remove the server
    try:
        _, _, headers = servers_api.datacenters_servers_delete_with_http_info(datacenter_id, existing_object.id)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except Exception as e:
        module.fail_json(
            msg="failed to terminate the virtual server: %s" % to_native(e), exception=traceback.format_exc(),
        )


def create_server(module, client):
    """
    Create new virtual machine

    module : AnsibleModule object
    client: authenticated ionos-cloud object

    Returns:
        True if a new virtual machine was created, false otherwise
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    count = module.params.get('count')
    datacenter_found = False

    virtual_machines = []

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = get_paginated(datacenters_api.datacenters_get, depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if datacenter_id:
        datacenter_found = True

    if not datacenter_found:
        datacenter_response = _create_datacenter(module, client)
        datacenter_id = datacenter_response.id

    if count > 1:
        numbers = set()
        count_offset = 1

        try:
            name % 0
        except TypeError as e:
            if (hasattr(e, 'message') and e.message.startswith('not all') or to_native(e).startswith('not all')):
                name = '%s%%d' % name
            else:
                module.fail_json(msg=e, exception=traceback.format_exc())

        number_range = xrange(count_offset, count_offset + count + len(numbers))

        available_numbers = list(set(number_range).difference(numbers))
        names = []
        numbers_to_use = available_numbers[:count]
        for number in numbers_to_use:
            names.append(name % number)
    else:
        names = [name]

    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    changed = False
    for name in names:
        existing_server = get_resource(module, server_list, name)
        if existing_server is not None:
            update_replace = update_replace_object(module, client, datacenter_id, existing_server, name)
            create_response = update_replace[RETURNED_KEY]
            if update_replace['changed']:
                changed = True
        else:
            create_response =_create_object(module, client, datacenter_id, name).to_dict()
            changed = True

        virtual_machines.append(create_response)

    return {
        'changed': changed,
        'failed': False,
        'machines': virtual_machines,
        'action': 'create'
    }


def update_server(module, client):
    """
    Update servers.

    This will update one or more servers.

    module : AnsibleModule object
    client: authenticated ionos-cloud object.

    Returns:
        dict of updated servers
    """
    datacenter = module.params.get('datacenter')
    name = module.params.get('name')
    instance_ids = module.params.get('instance_ids')

    changed = False

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)

    if not isinstance(instance_ids, list) or len(instance_ids) < 1:
        module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')

    if name and isinstance(instance_ids, list) and len(instance_ids) > 1:
        module.fail_json(msg='when renaming, instance_ids can only have one id at most')

    # Locate UUID for datacenter if referenced by name.
    datacenters_api = ionoscloud.DataCentersApi(client)

    datacenter_list = get_paginated(datacenters_api.datacenters_get)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)

    # Fail early if one of the ids provided doesn't match any server
    checked_instances = []
    for instance in instance_ids:
        server = get_resource(module, server_list, instance)
        if server is None:
            module.fail_json(msg='Server \'%s\' not found.' % str(instance))
        checked_instances.append(server)

    updated_servers = []
    for instance in checked_instances:
        existing_server_by_name = None if name is None else get_resource_id(module, server_list, name)
        if existing_server_by_name is not None:
            module.fail_json(msg='A server with name \'%s\' already exists.' % str(name))

        if module.check_mode:
            module.exit_json(changed=True)
        update_replace = update_replace_object(module, client, datacenter_id, instance, name)
        server_response = update_replace[RETURNED_KEY]
        if update_replace['changed']:
            changed = True
        updated_servers.append(server_response)

    return {
        'failed': False,
        'changed': changed,
        'machines': updated_servers,
        'action': 'update'
    }


def remove_server(module, client):
    """
    Removes a virtual machine.

    This will remove the virtual machine along with the bootVolume.

    module : AnsibleModule object
    client: authenticated ionos-cloud object.

    Not yet supported: handle deletion of attached data disks.

    Returns:
        True if a new virtual server was deleted, false otherwise
    """
    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')
    changed = False

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)

    server_id = None

    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = get_paginated(datacenter_server.datacenters_get, depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    # Prefetch server list for later comparison.
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    for instance in instance_ids:
        # Locate UUID for server if referenced by name.
        server = get_resource(module, server_list, instance)
        if server:
            _remove_object(module, client, datacenter_id, server)
            changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': server_id
    }


def resume_server(module, client, state):
    """
    Reusmes or Suspend a CUBE virtual machine.

    module : AnsibleModule object
    client: authenticated ionos-cloud object.

    Returns:
        True when the servers process the action successfully, false otherwise.
    """
    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')

    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = get_paginated(datacenters_api.datacenters_get, depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    # Prefetch server list for later comparison.
    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    matched_instances = []
    for instance in instance_ids:
        # Locate UUID of server if referenced by name.
        server = get_resource(module, server_list, instance)
        if server:
            if module.check_mode:
                module.exit_json(changed=True)

            state = server.properties.vm_state
            changed, server = _resume_server(module, client, datacenter_id, server.id, state)
            if changed:
                matched_instances.append(server)

    if len(matched_instances) == 0:
        changed = False
    else:
        changed = True

    return {
        'action': state,
        'changed': changed,
        'failed': False,
        'machines': [m.to_dict() for m in matched_instances]
    }


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    if (
        module.params.get('lan') is not None 
        and not (isinstance(module.params.get('lan'), str) or isinstance(module.params.get('lan'), int))
    ):
        module.fail_json(msg='lan should either be a string or a number')

    state = module.params.get('state')
    check_required_arguments(module, state, OBJECT_NAME, OPTIONS)

    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        try:
            if state == 'absent':
                module.exit_json(**remove_server(module, api_client))
            elif state in ('resume', 'suspend'):
                module.exit_json(**resume_server(module, api_client, state))
            elif state == 'present':
                if module.check_mode:
                    module.exit_json(changed=True)
                module.exit_json(**create_server(module, api_client))
            elif state == 'update':
                module.exit_json(**update_server(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
