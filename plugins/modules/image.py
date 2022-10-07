from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Image, Images, ImageProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['absent', 'update']
OBJECT_NAME = 'Image'


OPTIONS = {
    'image_id': {
        'description': ['The ID of the image.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'name': {
        'description': ['The name of the image.'],
        'available': STATES,
        'type': 'str',
    },
    'description': {
        'description': ['The description of the image.'],
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
    'licence_type': {
        'description': ['OS type for this image.'],
        'available': ['update'],
        'required': ['update'],
        'type': 'str',
    },
    'cloud_init': {
        'description': ['Cloud init compatibility.'],
        'available': ['update'],
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
module: image
short_description: Update or destroy a Ionos Cloud Image.
description:
     - This is a simple module that supports updating or removing Images. This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'update' : '''# Update an image
  - name: Update image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      name: "CentOS-8.3.2011-x86_64-boot-renamed.iso"
      description: "An image used for testing the Ansible Module"
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
      licence_type: "LINUX"
      cloud_init: V1
      state: update
  ''',
  'absent' : '''# Destroy an image
  - name: Delete image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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
        'image': image_response.to_dict()
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


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

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
                module.exit_json(**delete_image(module, api_client))
            elif state == 'update':
                module.exit_json(**update_image(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
