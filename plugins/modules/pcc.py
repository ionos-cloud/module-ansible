import copy
import re
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import PrivateCrossConnect
    from ionoscloud.models import PrivateCrossConnectProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'PCC'

OPTIONS = {
    'name': {
        'description': ['The name of the PCC.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'pcc_id': {
        'description': ['The ID of the PCC.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'description': {
        'description': ['The description of the PCC.'],
        'available': ['present', 'update'],
        'required': ['present'],
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
module: pcc
short_description: Create or destroy a Ionos Cloud Private Cross Connect
description:
     - This is a simple module that supports creating or removing Private Cross Connects.
       This module has a dependency on ionos-cloud >= 6.0.0
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create pcc
    pcc:
      name: "{{ name }}"
      description: "{{ description }}"
  ''',
  'update' : '''
  - name: Update pcc
    pcc:
      pcc_id: "49e73efd-e1ea-11ea-aaf5-5254001a8838"
      name: "{{ new_name }}"
      description: "{{ new_description }}"
      state: update
  ''',
  'absent' : '''
  - name: Remove pcc
    pcc:
      pcc_id: "2851af0b-e1ea-11ea-aaf5-5254001a8838"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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


def create_pcc(module, client):
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    pcc_properties = PrivateCrossConnectProperties(name=name, description=description)
    pcc = PrivateCrossConnect(properties=pcc_properties)

    try:
        response = pcc_server.pccs_post_with_http_info(pcc)
        (pcc_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'pcc': pcc_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the pcc: %s" % to_native(e))


def delete_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    pcc_list = pcc_server.pccs_get(depth=5)
    pcc = _get_resource(pcc_list, pcc_id)

    if not pcc:
        module.exit_json(changed=False)


    try:
        pcc_server.pccs_delete(pcc_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': pcc_id
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the pcc: %s" % to_native(e))


def update_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    pcc_properties = PrivateCrossConnectProperties(name=name, description=description)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = pcc_server.pccs_patch_with_http_info(pcc_id=pcc_id, pcc=pcc_properties)
        (pcc_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'pcc': pcc_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the pcc: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
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
            if state == 'present':
                module.exit_json(**create_pcc(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_pcc(module, api_client))
            elif state == 'update':
                module.exit_json(**update_pcc(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
