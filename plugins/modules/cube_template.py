#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import yaml

__metaclass__ = type

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
DOC_DIRECTORY = 'compute-engine'
STATES = ['present']

OPTIONS = {
    'template_id': {
        'description': ['The ID of the template.'],
        'available': STATES,
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
short_description: Retrieve one or more Cube templates.
description:
     - This is a simple module that supports retrieving one or more Cube templates
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 5.0.0"
author:
    - "Matt Baldwin (baldwin@stackpointcloud.com)"
    - "Ethan Devenport (@edevenport)"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
    - name: List templates
      cube_template:
        state: present
      register: template_list

    - name: Debug - Show Templates List
      debug:
        msg: "{{  template_list.template }}"

    - name: Get template by template id
      cube_template:
        template_id: "{{ template_list.template['items'][0]['id'] }}"
      register: template_response

    - name: Debug - Show Template
      debug:
        msg: "{{ template_response.template }}"
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def get_template(module, client):
    """
    List templates or find template by UUID

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The list of templates.
    """

    template_id = module.params.get('template_id')
    template_server = ionoscloud.TemplatesApi(client)
    template_response = None

    try:
        if template_id:
            template_response = template_server.templates_find_by_id(template_id)

        else:
            template_response = template_server.templates_get(depth=2)

    except ApiException as e:
        module.fail_json(msg="failed to get the template list: %s" % to_native(e))

    return {
        'changed': False,
        'failed': False,
        'template': template_response.to_dict()
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


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT

        for option_name, option in OPTIONS.items():
            if 'present' in option.get('required', []) and not module.params.get(option_name):
                module.fail_json(msg='% parameter is required for retrieving Cube templates'.format(option_name))
        try:
            (template_dict_array) = get_template(module, api_client)
            module.exit_json(**template_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to get template: %s' % to_native(e))


if __name__ == '__main__':
    main()
