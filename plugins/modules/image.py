from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import re

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Image, Images, ImageProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None



def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def delete_image(module, client):
    image_id = module.params.get('image_id')
    wait = module.params.get('wait')
    changed = False

    image_server = ionoscloud.ImagesApi(api_client=client)

    images_list = image_server.images_get(depth=5)
    image = _get_resource(images_list, image_id)

    if not image:
        module.exit_json(changed=False)


    try:
        response = image_server.images_delete_with_http_info(image_id=image_id)
        (image_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to delete the image: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': image_id
    }


def update_image(module, client):
    image_id = module.params.get('image_id')
    name = module.params.get('name')
    description = module.params.get('description')
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
    cloud_init = module.params.get('cloud_init')
    wait = module.params.get('wait')

    image_server = ionoscloud.ImagesApi(api_client=client)
    image_response = None

    if module.check_mode:
        module.exit_json(changed=True)
    try:

        image_properties = ImageProperties(name=name, description=description, cpu_hot_plug=cpu_hot_plug,
                                           cpu_hot_unplug=cpu_hot_unplug, ram_hot_plug=ram_hot_plug, ram_hot_unplug=ram_hot_unplug,
                                           nic_hot_plug=nic_hot_plug, nic_hot_unplug=nic_hot_unplug, disc_virtio_hot_plug=disc_virtio_hot_plug,
                                           disc_virtio_hot_unplug=disc_virtio_hot_unplug, disc_scsi_hot_plug=disc_scsi_hot_plug,
                                           disc_scsi_hot_unplug=disc_scsi_hot_unplug, licence_type=licence_type, cloud_init=cloud_init)

        image_response, _, headers = image_server.images_patch_with_http_info(image_id=image_id, image=image_properties)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to update the image: %s" % to_native(e))
        changed = False

    return {
        'changed': changed,
        'failed': False,
        'action': 'update',
        'image': image_response.to_dict()
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            image_id=dict(type='str'),
            name=dict(type='str'),
            description=dict(type='str'),
            cpu_hot_plug=dict(type='bool'),
            cpu_hot_unplug=dict(type='bool'),
            ram_hot_plug=dict(type='bool'),
            ram_hot_unplug=dict(type='bool'),
            nic_hot_plug=dict(type='bool'),
            nic_hot_unplug=dict(type='bool'),
            disc_scsi_hot_plug=dict(type='str'),
            disc_scsi_hot_unplug=dict(type='bool'),
            disc_virtio_hot_plug=dict(type='bool'),
            disc_virtio_hot_unplug=dict(type='bool'),
            licence_type=dict(type='str'),
            cloud_init=dict(type='str'),
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
            state=dict(type='str'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(
            msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')
    if not state:
        module.fail_json(msg='state parameter is required')

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
            if not module.params.get('image_id'):
                module.fail_json(
                    msg='image_id parameter is required for deleting an image.')
            try:
                (changed) = delete_image(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(
                    msg='failed to set image state: %s' % to_native(e))

        elif state == 'update':
            error_message = "%s parameter is required for updating an image."
            if not module.params.get('image_id'):
                module.fail_json(msg=error_message % 'image_id')
            if not module.params.get('licence_type'):
                module.fail_json(msg=error_message % 'licence_type')

            try:
                (changed) = update_image(module, api_client)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(
                    msg='failed to set image state: %s' % to_native(e))


if __name__ == '__main__':
    main()
