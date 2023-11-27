import re
import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_sdk_config, check_required_arguments, apply_filters,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import (
    get_default_options, get_info_default_options,
)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['info']
OBJECT_NAME = 'Datacenters'
RETURNED_KEY = 'datacenters'

OPTIONS = {**get_default_options(STATES), **get_info_default_options(STATES)}


def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES)
    del val['available']
    del val['type']
    return val


DOCUMENTATION = '''
---
module: datacenter_info
short_description: List Ionos Cloud Datacenters.
description:
     - This is a simple module that supports listing Datacenter.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLES = '''
    - name: Get all Datacenter
      datacenter_info:
      register: datacenter_list_response
'''

def get_objects(module, client):
    datacenters = ionoscloud.DataCentersApi(client).datacenters_get(depth=module.params.get('depth'))
    try:
        results = list(map(lambda x: x.to_dict(), apply_filters(module, datacenters.items)))
        return {
            'changed': False,
            RETURNED_KEY: results
        }

    except Exception as e:
        module.fail_json(msg='failed to list the {object_name}: {error}'.format(
            object_name=OBJECT_NAME, error=to_native(e),
        ))


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, OBJECT_NAME, OPTIONS)

        try:
            module.exit_json(**get_objects(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()
