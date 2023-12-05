import re
import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_sdk_config, check_required_arguments, apply_filters, default_main_info,
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

OPTIONS = {**get_info_default_options(STATES)}


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
    return ionoscloud.DataCentersApi(client).datacenters_get(depth=module.params.get('depth'))


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
