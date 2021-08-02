#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

HAS_SDK = True

try:
    import ionoscloudautoscaling
    from ionoscloudautoscaling import __version__ as sdk_version
    from ionoscloudautoscaling.models import Template, TemplateProperties, TemplateNic, TemplateVolume
    from ionoscloudautoscaling.rest import ApiException
    from ionoscloudautoscaling import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)

LOCATIONS = ['us/las',
             'us/ewr',
             'de/fra',
             'de/fkb',
             'de/txl',
             'gb/lhr'
             ]


def _remove_template(module, template_server, template):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        template_server.autoscaling_templates_delete_with_http_info(template_id=template)
    except Exception as e:
        module.fail_json(msg="failed to remove the template: %s" % to_native(e))


def get_nic(nic):
    nic_object = TemplateNic()
    if 'lan' in nic:
        nic_object.lan = nic['lan']
    if 'name' in nic:
        nic_object.name = nic['name']
    return nic_object


def get_volume(volume):
    volume_object = TemplateVolume()
    if 'image' in volume:
        volume_object.image = volume['image']
    if 'image_password' in volume:
        volume_object.image_password = volume['image_password']
    if 'size' in volume:
        volume_object.size = volume['size']
    if 'name' in volume:
        volume_object.name = volume['name']
    if 'ssh_keys' in volume:
        volume_object.ssh_keys = volume['ssh_keys']
    if 'type' in volume:
        volume_object.type = volume['type']
    if 'user_data' in volume:
        volume_object.user_data = volume['user_data']
    return volume_object


def create_template(module, client):
    """
    Creates a Autoscaling Template

    This will create a new Autoscaling Template in the specified location.

    module : AnsibleModule object
    client: authenticated ionoscloudautoscaling object.

    Returns:
        The template ID if a new template was created.
    """
    name = module.params.get('name')
    location = module.params.get('location')
    availability_zone = module.params.get('availability_zone')
    cores = module.params.get('cores')
    cpu_family = module.params.get('cpu_family')
    ram = module.params.get('ram')
    nics_list = module.params.get('nics')
    volumes_list = module.params.get('volumes')

    nics = []
    for nic in nics_list:
        nics.append(get_nic(nic))

    volumes = []
    for volume in volumes_list:
        volumes.append(get_volume(volume))

    template_server = ionoscloudautoscaling.TemplatesApi(client)
    templates = template_server.autoscaling_templates_get(depth=2)

    for dc in templates.items:
        if name == dc.properties.name and location == dc.properties.location:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'template': dc.to_dict()
            }

    template_properties = TemplateProperties(availability_zone=availability_zone, cores=cores, cpu_family=cpu_family, location=location,
                                             name=name, nics=nics, ram=ram, volumes=volumes)
    template = Template(properties=template_properties)

    try:
        response = template_server.autoscaling_templates_post_with_http_info(template=template)
        (template_response, _, _) = response

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'template': template_response.to_dict()
        }

        return results

    except ApiException as e:
        module.fail_json(msg="failed to create the new template: %s" % to_native(e))


def remove_template(module, client):
    """
    Removes a Autoscaling Template.

    This will remove a template.

    module : AnsibleModule object
    client: authenticated ionoscloudautoscaling object.

    Returns:
        True if the template was deleted, false otherwise
    """
    name = module.params.get('name')
    template_id = module.params.get('template_id')
    template_server = ionoscloudautoscaling.TemplatesApi(client)
    changed = False

    if template_id:
        _remove_template(module, template_server, template_id)
        changed = True

    else:
        templates = template_server.autoscaling_templates_get(depth=2)
        for d in templates.items:
            vdc = template_server.autoscaling_templates_find_by_id(d.id)
            if name == vdc.properties.name:
                template_id = d.id
                _remove_template(module, template_server, template_id)
                changed = True

    return {
        'action': 'delete',
        'changed': changed,
        'id': template_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            location=dict(type='str', choices=LOCATIONS, default='us/las'),
            template_id=dict(type='str'),
            availability_zone=dict(type='str'),
            cores=dict(type='int'),
            cpu_family=dict(type='str'),
            nics=dict(type='list', elements='dict'),
            ram=dict(type='int'),
            volumes=dict(type='list', elements='dict'),
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
        module.fail_json(msg='ionoscloudautoscaling is required for this module, run `pip install ionoscloudautoscaling`')

    username = module.params.get('username')
    password = module.params.get('password')
    state = module.params.get('state')
    user_agent = 'ionoscloudautoscaling-python/%s Ansible/%s' % (sdk_version, __version__)

    configuration = ionoscloudautoscaling.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not module.params.get('name') and not module.params.get('template_id'):
                module.fail_json(msg='name parameter or template_id parameter are required deleting a virtual template.')

            try:
                (result) = remove_template(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set template state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new template')
            if not module.params.get('location'):
                module.fail_json(msg='location parameter is required for a new template')

            if module.check_mode:
                module.exit_json(changed=True)

            try:
                (template_dict_array) = create_template(module, api_client)
                module.exit_json(**template_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set template state: %s' % to_native(e))


if __name__ == '__main__':
    main()
