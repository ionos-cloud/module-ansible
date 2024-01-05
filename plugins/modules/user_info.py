HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options_with_depth


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['info']
OBJECT_NAME = 'Users'
RETURNED_KEY = 'users'

OPTIONS = {
    'group': {
        'description': ['The name or ID of the group.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options_with_depth(STATES),
}

DOCUMENTATION = """
module: nic_info
short_description: List Ionos Cloud Users.
description:
     - This is a simple module that supports listing Users.
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
    group:
        description:
        - The name or ID of the group.
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
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all Users of a group
      user_info:
        group: "AnsibleIonosGroup"
      register: user_list_response

    - name: Get all Users
      user_info:
      register: all_user_list_response
    """


def list_users(depth, users_get_method, extra_args):
    all_users = ionoscloud.Users(items=[])
    offset = 0
    limit = 100

    users = users_get_method(**extra_args, depth=depth, limit=limit, offset=offset)
    all_users.items += users.items
    while(users.links.next is not None):
        offset += limit
        users = users_get_method(**extra_args, depth=depth, limit=limit, offset=offset)
        all_users.items += users.items

    return all_users


def get_objects(module, client):
    group = module.params.get('group')
    um_api = ionoscloud.UserManagementApi(api_client=client)

    if group:
        # Locate UUID for Group
        group_list = um_api.um_groups_get(depth=1)
        group_id = get_resource_id(module, group_list, group)

        users = list_users(
            module.params.get('depth'),
            users_get_method=um_api.um_groups_users_get,
            extra_args={'group_id': group_id},
        )
    else:
        users = list_users(
            module.params.get('depth'),
            users_get_method=um_api.um_users_get,
            extra_args={},
        )
    return users


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
