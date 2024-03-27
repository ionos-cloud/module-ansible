from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options_with_depth


HAS_SDK = True
try:
    import ionoscloud_vm_autoscaling
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-vm-autoscaling/%s' % (
    __version__, ionoscloud_vm_autoscaling.__version__)
DOC_DIRECTORY = 'vm-autoscaling'
STATES = ['info']
OBJECT_NAME = 'VM Autoscaling Group Actions'
RETURNED_KEY = 'result'

OPTIONS = {
    'vm_autoscaling_group': {
        'description': ['The ID or name of an existing VM Autoscaling Group.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options_with_depth(STATES),
}

DOCUMENTATION = """
module: vm_autoscaling_action_info
short_description: List VM Autoscaling Group Actions
description:
     - This is a simple module that supports listing existing VM Autoscaling Group Actions
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
    depth:
        default: 1
        description:
        - The depth used when retrieving the items.
        required: false
    filters:
        description:
        - 'Filter that can be used to list only objects which have a certain set of propeties.
            Filters should be a dict with a key containing keys and value pair in the
            following format: ''properties.name'': ''server_name'''
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
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
    vm_autoscaling_group:
        description:
        - The ID or name of an existing VM Autoscaling Group.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud-vm-autoscaling >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
name: List VM Autoscaling Group Actions
ionoscloudsdk.ionoscloud.vm_autoscaling_action_info:
  vm_autoscaling_group: ''
register: vm_autoscaling_actions_response
"""


def get_objects(module, client):
    groups_api = ionoscloud_vm_autoscaling.AutoScalingGroupsApi(client)
    group_id = get_resource_id(
        module,
        groups_api.groups_get(depth=1),
        module.params.get('vm_autoscaling_group'),
    )
    return groups_api.groups_actions_get(group_id, depth=module.params.get('depth'))


if __name__ == '__main__':
    default_main_info(
        ionoscloud_vm_autoscaling, 'ionoscloud_vm_autoscaling', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )