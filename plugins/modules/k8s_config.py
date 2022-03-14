import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
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
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present']
OBJECT_NAME = 'K8s config'

OPTIONS = {
    'k8s_cluster_id': {
        'description': ['The ID of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'config_file': {
        'description': ['The name of the file in which to save the config.'],
        'available': STATES,
        'required': STATES,
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
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'required': STATES,
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'required': STATES,
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
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
module: datacenter
short_description: Create or destroy a Ionos Cloud Virtual Datacenter.
description:
     - This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers.
       This module has a dependency on ionos-cloud >= 6.0.0
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Get k8s config
  k8s_config:
    k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def get_config(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    config_file = module.params.get('config_file')
    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    try:
        with open(config_file, 'w') as f:
            response = k8s_server.k8s_kubeconfig_get(k8s_cluster_id=k8s_cluster_id)
            f.write(response)

    except Exception as e:
        module.fail_json(msg="failed to get the k8s cluster config: %s" % to_native(e))

    return {
        'failed': False,
        'changed': True,
        'config': response
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
    api_url = module.params.get('api_url')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
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
                module.exit_json(**get_config(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
