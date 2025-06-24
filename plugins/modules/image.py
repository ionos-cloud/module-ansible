from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible import __version__

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import ImageProperties
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id,
    get_resource, check_required_arguments, get_sdk_config, 
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['absent', 'update']
OBJECT_NAME = 'Image'
RETURNED_KEY = 'image'


OPTIONS = {
    'image_id': {
        'description': ['The ID of the image.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'name': {
        'description': ['The resource name.'],
        'available': STATES,
        'type': 'str',
    },
    'description': {
        'description': ['Human-readable description.'],
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
    'licence_type': {
        'description': ['The OS type of this image.'],
        'available': ['update'],
        'required': ['update'],
        'type': 'str',
    },
    'cloud_init': {
        'description': ['Cloud init compatibility.'],
        'available': ['update'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: image
short_description: Update or destroy a Ionos Cloud Image.
description:
     - This is a simple module that supports updating or removing Images. This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
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
    cloud_init:
        description:
        - Cloud init compatibility.
        required: false
    cpu_hot_plug:
        description:
        - Hot-plug capable CPU (no reboot required).
        required: false
    cpu_hot_unplug:
        description:
        - Hot-unplug capable CPU (no reboot required).
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
        - Hot-unplug capable SCSI drive (no reboot required). Not supported with Windows
            VMs.
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
    image_id:
        description:
        - The ID of the image.
        required: true
    licence_type:
        description:
        - The OS type of this image.
        required: false
    name:
        description:
        - The resource name.
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
    state:
        choices:
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
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'update' : '''name: Update image
ionoscloudsdk.ionoscloud.image:
  image_id: 87fe5b95-05e4-11ee-a7cb-028794406dc9
  name: debian-11.7.0-amd64-netinst-renamed.iso
  description: An image used for testing the Ansible Module
  cpu_hot_plug: true
  cpu_hot_unplug: false
  ram_hot_plug: true
  ram_hot_unplug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  disc_scsi_hot_plug: true
  disc_scsi_hot_unplug: false
  licence_type: LINUX
  cloud_init: V1
  state: update
register: image_output
''',
  'absent' : '''name: Delete image
ionoscloudsdk.ionoscloud.image:
  image_id: 916b10ea-be31-11eb-b909-c608708a73fa
  state: absent
''',
}

EXAMPLES = """name: Update image
ionoscloudsdk.ionoscloud.image:
  image_id: 87fe5b95-05e4-11ee-a7cb-028794406dc9
  name: debian-11.7.0-amd64-netinst-renamed.iso
  description: An image used for testing the Ansible Module
  cpu_hot_plug: true
  cpu_hot_unplug: false
  ram_hot_plug: true
  ram_hot_unplug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  disc_scsi_hot_plug: true
  disc_scsi_hot_unplug: false
  licence_type: LINUX
  cloud_init: V1
  state: update
register: image_output

name: Delete image
ionoscloudsdk.ionoscloud.image:
  image_id: 916b10ea-be31-11eb-b909-c608708a73fa
  state: absent
"""

def delete_image(module, client):
    image_id = module.params.get('image_id')
    wait = module.params.get('wait')
    changed = False

    image_server = ionoscloud.ImagesApi(api_client=client)

    image = get_resource(module, image_server.images_get(depth=2), image_id)

    if not image:
        module.exit_json(changed=False)

    try:
        _, _, headers = image_server.images_delete_with_http_info(image_id=image_id)

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

        existing_image_id_by_name = get_resource_id(module, image_server.images_get(depth=2), name)

        if image_id is not None and existing_image_id_by_name is not None and existing_image_id_by_name != image_id:
            module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, name))

        image_properties = ImageProperties(
            name=name,
            description=description,
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
            licence_type=licence_type,
            cloud_init=cloud_init,
        )

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
        RETURNED_KEY: image_response.to_dict()
    }


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
                module.exit_json(**delete_image(module, api_client))
            elif state == 'update':
                module.exit_json(**update_image(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
