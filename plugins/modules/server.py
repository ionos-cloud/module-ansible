#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import copy
import re
import traceback
import yaml

from uuid import (uuid4, UUID)

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import (Volume, VolumeProperties, Server, ServerProperties, Datacenter,
                                   DatacenterProperties, Nic, NicProperties, Lan, LanProperties, LanPropertiesPost,
                                   LanPost, ServerEntities, Nics, Volumes, AttachedVolumes)
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.six.moves import xrange
from ansible.module_utils._text import to_native

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['running', 'stopped', 'resume', 'suspend', 'absent', 'present', 'update']
OBJECT_NAME = 'Server'

AVAILABILITY_ZONES = [
    'AUTO',
    'ZONE_1',
    'ZONE_2',
    'ZONE_3',
]

OPTIONS = {
    'name': {
        'description': ['The name of the virtual machine.'],
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
    'volume_availability_zone': {
        'description': ['The storage availability zone assigned to the volume.'],
        'available': ['present'],
        'choices': AVAILABILITY_ZONES,
        'type': 'str',
        'version_added': '2.3',
    },
    'datacenter': {
        'description': ['The datacenter to provision this virtual machine.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'cores': {
        'description': ['The number of CPU cores to allocate to the virtual machine.'],
        'available': ['present', 'update'],
        'default': 2,
        'type': 'int',
    },
    'ram': {
        'description': ['The amount of memory to allocate to the virtual machine.'],
        'available': ['present', 'update'],
        'default': 2048,
        'type': 'int',
    },
    'cpu_family': {
        'description': ['The amount of memory to allocate to the virtual machine.'],
        'available': ['present'],
        'choices': ['AMD_OPTERON', 'INTEL_XEON', 'INTEL_SKYLAKE'],
        'default': 'AMD_OPTERON',
        'type': 'str',
        'version_added': '2.2',
    },
    'availability_zone': {
        'description': ['The availability zone assigned to the server.'],
        'available': ['present'],
        'choices': AVAILABILITY_ZONES,
        'default': 'AUTO',
        'type': 'str',
        'version_added': '2.3',
    },
    'volume_size': {
        'description': ['The size in GB of the boot volume.'],
        'available': ['present'],
        'default': 10,
        'type': 'int',
    },
    'bus': {
        'description': ['The bus type for the volume.'],
        'available': ['present'],
        'choices': ['IDE', 'VIRTIO'],
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
        'choices': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'],
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
        'choices': ['HDD', 'SSD', 'SSD Standard', 'SSD Premium', 'DAS'],
        'default': 'HDD',
        'type': 'str',
    },
    'nic_ips': {
        'description': ['The list of IPS for the NIC.'],
        'available': ['present'],
        'type': 'list',
        'elements': 'str',
    },
    'template_uuid': {
        'description': ['The template used when crating a CUBE server.'],
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
    'type': {
        'description': ['The type of the virtual machine.'],
        'available': ['present'],
        'choices': ['ENTERPRISE', 'CUBE'],
        'default': 'ENTERPRISE',
        'type': 'str',
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
module: server
short_description: Create, update, destroy, start, stop, and reboot a Ionos virtual machine.
description:
     - Create, update, destroy, update, start, stop, and reboot a Ionos virtual machine.
       When the virtual machine is created it can optionally wait for it to be 'running' before returning.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionos-cloud >= 5.2.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Provisioning example. This will create three servers and enumerate their names.
    - server:
        datacenter: Tardis One
        name: web%02d.stackpointcloud.com
        cores: 4
        ram: 2048
        volume_size: 50
        cpu_family: INTEL_XEON
        image: ubuntu:latest
        location: us/las
        count: 3
        assign_public_ip: true
  ''',
  'update' : '''# Update Virtual machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - web001.stackpointcloud.com
        - web002.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update
  # Rename virtual machine
    - server:
        datacenter: Tardis One
        instance_ids: web001.stackpointcloud.com
        name: web101.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update
''',
  'absent' : '''# Removing Virtual machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: absent
  ''',
  'running' : '''# Starting Virtual Machines.
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: running
  ''',
  'stopped' : '''# Stopping Virtual Machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: stopped
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
        identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
        resource_identity = []

        for identity_path in identity_paths:
            current = resource
            for el in identity_path:
                current = getattr(current, el)
            resource_identity.append(current)

        return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


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


def _create_machine(module, client, datacenter, name):
    cores = module.params.get('cores')
    ram = module.params.get('ram')
    cpu_family = module.params.get('cpu_family')
    volume_size = module.params.get('volume_size')
    disk_type = module.params.get('disk_type')
    availability_zone = module.params.get('availability_zone')
    volume_availability_zone = module.params.get('volume_availability_zone')
    image_password = module.params.get('image_password')
    ssh_keys = module.params.get('ssh_keys')
    user_data = module.params.get('user_data')
    bus = module.params.get('bus')
    lan = module.params.get('lan')
    nat = module.params.get('nat')
    image = module.params.get('image')
    assign_public_ip = module.boolean(module.params.get('assign_public_ip'))
    nic_ips = module.params.get('nic_ips')
    template_uuid = module.params.get('template_uuid')
    type = module.params.get('type')
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    server_server = ionoscloud.ServersApi(api_client=client)
    lan_server = ionoscloud.LANsApi(api_client=client)

    nics = []

    if assign_public_ip:
        lans_list = lan_server.datacenters_lans_get(datacenter_id=datacenter, depth=2).items
        public_lan = _get_lan_by_id_or_properties(lans_list, public=True)

        public_ip_lan_id = public_lan.id if public_lan is not None else None

        if public_ip_lan_id is None:
            lan_properties = LanPropertiesPost(name='public', public=True)
            lan_post = LanPost(properties=lan_properties)

            response = lan_server.datacenters_lans_post_with_http_info(datacenter_id=datacenter, lan=lan_post)
            (lan_response, _, headers) = response
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            public_ip_lan_id = lan_response.id

        nic = Nic(properties=NicProperties(name=str(uuid4()).replace('-', '')[:10],
                                           lan=int(public_ip_lan_id)))
        if nic_ips:
            nic.properties.ips = nic_ips
        nics.append(nic)

    if lan is not None:
        lans_list = lan_server.datacenters_lans_get(datacenter_id=datacenter, depth=2).items
        matching_lan = get_resource(module, lans_list, lan)

        if (not any(n.properties.lan == int(matching_lan.id) for n in nics)) or len(nics) < 1:
            nic = Nic(properties=NicProperties(name=str(uuid4()).replace('-', '')[:10],
                                               lan=int(int(matching_lan.id))))
            if nic_ips:
                nic.properties.ips = nic_ips
            nics.append(nic)


    if type == 'CUBE':
        server_properties = ServerProperties(template_uuid=template_uuid, name=name,
                                             availability_zone=availability_zone,
                                             boot_cdrom=boot_cdrom, boot_volume=boot_volume,
                                             cpu_family=cpu_family, type=type)

        volume_properties = VolumeProperties(type=disk_type, image_password=image_password)

    else:
        server_properties = ServerProperties(name=name, cores=cores, ram=ram, availability_zone=availability_zone,
                                             cpu_family=cpu_family)
        volume_properties = VolumeProperties(name=str(uuid4()).replace('-', '')[:10],
                                             type=disk_type,
                                             size=volume_size,
                                             availability_zone=volume_availability_zone,
                                             image_password=image_password,
                                             ssh_keys=ssh_keys,
                                             user_data=user_data,
                                             bus=bus)

    if image:
        if uuid_match.match(image):
            volume_properties.image = image
        else:
            volume_properties.image_alias = image

    volume = Volume(properties=volume_properties)
    server_entities = ServerEntities(volumes=Volumes(items=[volume]), nics=Nics(items=nics))

    server = Server(properties=server_properties, entities=server_entities)

    try:
        response = server_server.datacenters_servers_post_with_http_info(datacenter_id=datacenter, server=server)
        (server_response, _, headers) = response
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        if type == 'CUBE':
            client.wait_for(
                fn_request=lambda: server_server.datacenters_servers_find_by_id(datacenter_id=datacenter,
                                                                                server_id=server_response.id, depth=5),
                fn_check=lambda r: (r.entities.volumes is not None) and (r.entities.volumes.items is not None) and (
                        len(r.entities.volumes.items) > 0), scaleup=10000)
        else:
            client.wait_for(
                fn_request=lambda: server_server.datacenters_servers_find_by_id(datacenter_id=datacenter,
                                                                                server_id=server_response.id, depth=5),
                fn_check=lambda r: (r.entities.volumes is not None) and (r.entities.volumes.items is not None) and (
                        len(r.entities.volumes.items) > 0)
                                   and (r.entities.nics is not None) and (r.entities.nics.items is not None) and (
                                           len(r.entities.nics.items) == len(nics)), scaleup=10000)


        server = server_server.datacenters_servers_find_by_id(datacenter_id=datacenter,
                                                              server_id=server_response.id, depth=2)

    except Exception as e:
        module.fail_json(msg="failed to create the new server: %s" % to_native(e))
    else:
        if len(server.entities.nics.items) > 0:
            server.nic = server.entities.nics.items[0]
    return server


def _startstop_machine(module, client, datacenter_id, server_id, current_state):
    state = module.params.get('state')
    server_server = ionoscloud.ServersApi(api_client=client)
    server = None
    changed = False
    try:
        if state == 'running':
            if current_state != 'AVAILABLE':
                response = server_server.datacenters_servers_start_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = server_server.datacenters_servers_find_by_id(datacenter_id, server_id)
                if server_response.metadata.state == 'AVAILABLE':
                    changed = True
                    server = server_response
        else:
            if current_state != 'INACTIVE':
                response = server_server.datacenters_servers_stop_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = server_server.datacenters_servers_find_by_id(datacenter_id, server_id)
                if server_response.metadata.state == 'INACTIVE':
                    changed = True
                    server = server_response

    except Exception as e:
        module.fail_json(
            msg="failed to start or stop the virtual machine %s at %s: %s" % (server_id, datacenter_id, to_native(e)))

    return changed, server

def _resume_suspend_machine(module, client, datacenter_id, server_id, current_state):
    state = module.params.get('state')
    server_server = ionoscloud.ServersApi(api_client=client)
    server = None
    changed = False
    try:
        if state == 'resume':
            if current_state != 'RUNNING':
                response = server_server.datacenters_servers_resume_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = server_server.datacenters_servers_find_by_id(datacenter_id, server_id)
                if server_response.properties.vm_state == 'RUNNING':
                    changed = True
                    server = server_response

        else:
            if current_state != 'SUSPENDED':
                response = server_server.datacenters_servers_stop_post_with_http_info(datacenter_id, server_id)
                (_, _, headers) = response
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id)

                server_response = server_server.datacenters_servers_find_by_id(datacenter_id, server_id)
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
    datacenter_server = ionoscloud.DataCentersApi(api_client=client)

    datacenter_properties = DatacenterProperties(name=datacenter, location=location)
    datacenter = Datacenter(properties=datacenter_properties)

    try:
        response = datacenter_server.datacenters_post_with_http_info(datacenter=datacenter)
        (datacenter_response, _, headers) = response
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return datacenter_response

    except ApiException as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def create_virtual_machine(module, client):
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
    lan = module.params.get('lan')
    wait_timeout = module.params.get('wait_timeout')
    datacenter_found = False

    virtual_machines = []

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)
    nic_server = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = datacenter_server.datacenters_get(depth=2)
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

    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=3)
    for name in names:
        # Fail server creation if a server with this name and int combination already exists.
        if get_resource_id(module, server_list, name) is not None:
            module.fail_json(msg="Server with name %s already exists" % name, exception=traceback.format_exc())

    changed = False
    # Prefetch a list of servers for later comparison.
    for name in names:
        create_response = _create_machine(module, client, str(datacenter_id), name)
        changed = True

        virtual_machines.append(create_response)

    return {
        'changed': changed,
        'failed': False,
        'machines': [v.to_dict() for v in virtual_machines],
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
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')
    type = module.params.get('type')
    instance_ids = module.params.get('instance_ids')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)

    if name is None:
        if not isinstance(instance_ids, list) or len(instance_ids) < 1:
            module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')
    else:
        if isinstance(instance_ids, list) and len(instance_ids) > 1:
            module.fail_json(msg='when renaming, instance_ids can only have one id at most')

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    cores = module.params.get('cores')
    ram = module.params.get('ram')
    cpu_family = module.params.get('cpu_family')
    availability_zone = module.params.get('availability_zone')

    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)

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

        if type == 'CUBE':
            server_properties = ServerProperties(name=name if name is not None else instance.properties.name,
                                                 boot_cdrom=boot_cdrom, boot_volume=boot_volume)
        else:
            server_properties = ServerProperties(name=name if name is not None else instance.properties.name,
                                                 cores=cores, ram=ram, availability_zone=availability_zone,
                                                 cpu_family=cpu_family)

        new_server = Server(properties=server_properties)
        try:
            server_response = server_server.datacenters_servers_put(datacenter_id=datacenter_id, server_id=instance.id,
                                                                    server=new_server)

        except Exception as e:
            module.fail_json(msg="failed to update the server: %s" % to_native(e), exception=traceback.format_exc())
        else:
            updated_servers.append(server_response)

    return {
        'failed': False,
        'changed': True,
        'machines': [s.to_dict() for s in updated_servers],
        'action': 'update'
    }


def remove_virtual_machine(module, client):
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
    remove_boot_volume = module.params.get('remove_boot_volume')
    changed = False

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)

    server_id = None

    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    # Prefetch server list for later comparison.
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    for instance in instance_ids:
        # Locate UUID for server if referenced by name.
        server_id = get_resource_id(module, server_list, instance)
        if server_id:
            if module.check_mode:
                module.exit_json(changed=True)

            # Remove the server's boot volume
            if remove_boot_volume:
                _remove_boot_volume(module, client, datacenter_id, server_id)

            # Remove the server
            try:
                server_server.datacenters_servers_delete(datacenter_id, server_id)
            except Exception as e:
                module.fail_json(msg="failed to terminate the virtual server: %s" % to_native(e),
                                 exception=traceback.format_exc())
            else:
                changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': server_id
    }


def _remove_boot_volume(module, client, datacenter_id, server_id):
    """
    Remove the boot volume from the server
    """
    server_server = ionoscloud.ServersApi(api_client=client)
    try:
        server = server_server.datacenters_servers_find_by_id(datacenter_id, server_id, depth=2)
        volume = server.properties.boot_volume
        if volume:
            server_server.datacenters_servers_volumes_delete(datacenter_id, server_id, volume.id)
    except Exception as e:
        module.fail_json(msg="failed to remove the server's boot volume: %s" % to_native(e),
                         exception=traceback.format_exc())


def startstop_machine(module, client, state):
    """
    Starts or Stops a virtual machine.

    module : AnsibleModule object
    client: authenticated ionos-cloud object.

    Returns:
        True when the servers process the action successfully, false otherwise.
    """
    if not isinstance(module.params.get('instance_ids'), list) or len(module.params.get('instance_ids')) < 1:
        module.fail_json(msg='instance_ids should be a list of virtual machine ids or names, aborting')

    datacenter = module.params.get('datacenter')
    instance_ids = module.params.get('instance_ids')

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    # Prefetch server list for later comparison.
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    matched_instances = []
    for instance in instance_ids:
        # Locate UUID of server if referenced by name.
        server = get_resource(module, server_list, instance)
        if server:
            if module.check_mode:
                module.exit_json(changed=True)

            server_state = server.metadata.state
            changed, server = _startstop_machine(module, client, datacenter_id, server.id, server_state)
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

def resume_suspend_machine(module, client, state):
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

    datacenter_server = ionoscloud.DataCentersApi(api_client=client)
    server_server = ionoscloud.ServersApi(api_client=client)

    # Locate UUID for datacenter if referenced by name.
    datacenter_list = datacenter_server.datacenters_get(depth=2)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)
    if not datacenter_id:
        module.fail_json(msg='Virtual data center \'%s\' not found.' % str(datacenter))

    # Prefetch server list for later comparison.
    server_list = server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
    matched_instances = []
    for instance in instance_ids:
        # Locate UUID of server if referenced by name.
        server = get_resource(module, server_list, instance)
        if server:
            if module.check_mode:
                module.exit_json(changed=True)

            state = server.properties.vm_state
            changed, server = _resume_suspend_machine(module, client, datacenter_id, server.id, state)
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


def get_sdk_config(module):
    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    token = module.params.get('token')

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

    return ionoscloud.Configuration(**conf)


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

    if (
        module.params.get('lan') is not None 
        and not (isinstance(module.params.get('lan'), str) or isinstance(module.params.get('lan'), int))
    ):
        module.fail_json(msg='lan should either be a string or a number')

    state = module.params.get('state')
    check_required_arguments(module, state, OBJECT_NAME)

    with ApiClient(get_sdk_config(module)) as api_client:
        api_client.user_agent = USER_AGENT

        try:
            if state == 'absent':
                module.exit_json(**remove_virtual_machine(module, api_client))
            elif state in ('running', 'stopped'):
                module.exit_json(**startstop_machine(module, api_client, state))
            elif state in ('resume', 'suspend'):
                module.exit_json(**resume_suspend_machine(module, api_client, state))
            elif state == 'present':
                if module.check_mode:
                    module.exit_json(changed=True)
                module.exit_json(**create_virtual_machine(module, api_client))
            elif state == 'update':
                module.exit_json(**update_server(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
