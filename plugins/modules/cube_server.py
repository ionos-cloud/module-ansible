#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Server, ServerProperties, Volume, VolumeProperties, AttachedVolumes, ServerEntities
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _update_cube_server(module, client, cube_server_server, datacenter_id, cube_server_id, cube_server_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = cube_server_server.datacenters_servers_patch_with_http_info(datacenter_id, cube_server_id,
                                                                               cube_server_properties)
    (cube_server_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return cube_server_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_cube_server(module, client):
    """
    Creates a Cube Server

    This will create a new Cube Server in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Cube Server ID if a new Cube Server was created.
    """
    datacenter_id = module.params.get('datacenter_id')
    template_uuid = module.params.get('template_uuid')
    name = module.params.get('name')
    cores = module.params.get('cores')
    ram = module.params.get('ram')
    availability_zone = module.params.get('availability_zone')
    vm_state = module.params.get('vm_state')
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')
    cpu_family = module.params.get('cpu_family')
    volume_size = module.params.get('volume_size')
    volume_type = module.params.get('volume_type')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    cube_servers_server = ionoscloud.ServersApi(client)

    volume_properties = VolumeProperties(size=volume_size, type=volume_type, image="91e7519f-92af-11eb-b68e-9ad3ea4b1420", image_password="aaabbbcccddd")
    volume = Volume(properties=volume_properties)
    attached_volumes = AttachedVolumes(items=[volume])
    server_entities = ServerEntities(volumes=attached_volumes)

    cube_server_properties = ServerProperties(template_uuid=template_uuid, name=name, cores=cores, ram=ram,
                                              availability_zone=availability_zone, vm_state=vm_state,
                                              boot_cdrom=boot_cdrom, boot_volume=boot_volume,
                                              cpu_family=cpu_family, type="CUBE")
    cube_server = Server(properties=cube_server_properties, entities=server_entities)

    try:
        response = cube_servers_server.datacenters_servers_post_with_http_info(datacenter_id, cube_server)
        (cube_server_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'cube_server': cube_server_response.to_dict()
        }

    except ApiException as e:
        module.fail_json(msg="failed to create the new Cube Server: %s" % to_native(e))


def update_cube_server(module, client):
    """
    Updates a Cube Server.

    This will update a Cube Server.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Cube Server was updated, false otherwise
    """
    datacenter_id = module.params.get('datacenter_id')
    cube_server_id = module.params.get('cube_server_id')
    template_uuid = module.params.get('template_uuid')
    name = module.params.get('name')
    cores = module.params.get('cores')
    ram = module.params.get('ram')
    availability_zone = module.params.get('availability_zone')
    vm_state = module.params.get('vm_state')
    boot_cdrom = module.params.get('boot_cdrom')
    boot_volume = module.params.get('boot_volume')
    cpu_family = module.params.get('cpu_family')

    cube_server_server = ionoscloud.ServersApi(client)
    changed = False
    cube_server_response = None

    if cube_server_id:
        cube_server_properties = ServerProperties(template_uuid=template_uuid, name=name, cores=cores, ram=ram,
                                                  availability_zone=availability_zone, vm_state=vm_state,
                                                  boot_cdrom=boot_cdrom, boot_volume=boot_volume,
                                                  cpu_family=cpu_family)
        cube_server_response = _update_cube_server(module, client, cube_server_server, datacenter_id, cube_server_id,
                                                   cube_server_properties)
        changed = True

    else:
        cube_servers = cube_server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
        for server in cube_servers.items:
            if name == server.properties.name:
                cube_server_properties = ServerProperties(template_uuid=template_uuid, name=name, cores=cores, ram=ram,
                                                  availability_zone=availability_zone, vm_state=vm_state,
                                                  boot_cdrom=boot_cdrom, boot_volume=boot_volume,
                                                  cpu_family=cpu_family)
                cube_server_response = _update_cube_server(module, client, cube_server_server, datacenter_id, server.id,
                                                           cube_server_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Cube Server: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'cube_server': cube_server_response.to_dict()
    }


def remove_cube_server(module, client):
    """
    Removes a Cube Server.

    This will remove a Cube Server.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Cube Server was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    cube_server_id = module.params.get('cube_server_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    cube_server_server = ionoscloud.ServersApi(client)
    changed = False

    try:
        if cube_server_id:
            response = cube_server_server.datacenters_servers_delete_with_http_info(datacenter_id, cube_server_id)
            (cube_server_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            cube_servers = cube_server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
            for n in cube_servers.items:
                if name == n.properties.name:
                    cube_server_id = n.id
                    response = cube_server_server.datacenters_servers_delete_with_http_info(datacenter_id,
                                                                                                cube_server_id)
                    (cube_server_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Cube Server: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': cube_server_id
    }


def suspend_cube_server(module, client):
    """
    Suspends a Cube Server.

    This will suspend a Cube Server.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Cube Server was suspended, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    cube_server_id = module.params.get('cube_server_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    cube_server_server = ionoscloud.ServersApi(client)
    changed = False

    try:
        if cube_server_id:
            response = cube_server_server.datacenters_servers_suspend_post_with_http_info(datacenter_id, cube_server_id)
            (cube_server_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            cube_servers = cube_server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
            for n in cube_servers.items:
                if name == n.properties.name:
                    cube_server_id = n.id
                    response = cube_server_server.datacenters_servers_suspend_post_with_http_info(datacenter_id,
                                                                                                cube_server_id)
                    (cube_server_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to suspend the Cube Server: %s" % to_native(e))

    return {
        'action': 'suspend',
        'changed': changed,
        'id': cube_server_id
    }


def resume_cube_server(module, client):
    """
    Resumes a Cube Server.

    This will resume a Cube Server.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Cube Server was resumed, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    cube_server_id = module.params.get('cube_server_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    cube_server_server = ionoscloud.ServersApi(client)
    changed = False

    try:
        if cube_server_id:
            response = cube_server_server.datacenters_servers_resume_post_with_http_info(datacenter_id, cube_server_id)
            (cube_server_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            cube_servers = cube_server_server.datacenters_servers_get(datacenter_id=datacenter_id, depth=2)
            for n in cube_servers.items:
                if name == n.properties.name:
                    cube_server_id = n.id
                    response = cube_server_server.datacenters_servers_resume_post_with_http_info(datacenter_id,
                                                                                                cube_server_id)
                    (cube_server_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to resume the Cube Server: %s" % to_native(e))

    return {
        'action': 'resume',
        'changed': changed,
        'id': cube_server_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            datacenter_id=dict(type='str'),
            cube_server_id=dict(type='str'),
            template_uuid=dict(type='str'),
            name=dict(type='str'),
            cores=dict(type='str'),
            ram=dict(type='str'),
            availability_zone=dict(type='str'),
            vm_state=dict(type='str'),
            boot_cdrom=dict(type='str'),
            boot_volume=dict(type='str'),
            cpu_family=dict(type='str'),
            volume_size=dict(type='str'),
            volume_type=dict(type='str'),
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
    state = module.params.get('state')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a deleting a Cube Server')
            if not (module.params.get('name') or module.params.get('cube_server_id')):
                module.fail_json(msg='name parameter or cube_server_id parameter are required deleting a Cube Server.')
            try:
                (result) = remove_cube_server(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set Cube Server state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Cube Server')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a new Cube Server')

            try:
                (cube_server_dict) = create_cube_server(module, api_client)
                module.exit_json(**cube_server_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Cube Server state: %s' % to_native(e))

        elif state == 'update':
            if not (module.params.get('name') or module.params.get('cube_server_id')):
                module.fail_json(
                    msg='name parameter or cube_server_id parameter are required for updating a Cube Server.')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a Cube Server.')
            try:
                (cube_server_dict_array) = update_cube_server(module, api_client)
                module.exit_json(**cube_server_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set Cube Server state: %s' % to_native(e))

        elif state == 'suspend':
            if not module.params.get('name'):
                if not (module.params.get('name') or module.params.get('cube_server_id')):
                    module.fail_json(
                        msg='name parameter or cube_server_id parameter are required for suspending a Cube Server.')
                if not module.params.get('datacenter_id'):
                    module.fail_json(msg='datacenter_id parameter is required for suspending a Cube Server.')
            try:
                (cube_server_dict) = suspend_cube_server(module, api_client)
                module.exit_json(**cube_server_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Cube Server state: %s' % to_native(e))

        elif state == 'resume':
            if not (module.params.get('name') or module.params.get('cube_server_id')):
                module.fail_json(
                    msg='name parameter or cube_server_id parameter are required for resuming a Cube Server.')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for resuming a Cube Server.')
            try:
                (cube_server_dict_array) = resume_cube_server(module, api_client)
                module.exit_json(**cube_server_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set Cube Server state: %s' % to_native(e))


if __name__ == '__main__':
    main()
