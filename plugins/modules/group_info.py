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
OBJECT_NAME = 'Groups'
RETURNED_KEY = 'groups'

OPTIONS = {
    'user': {
        'description': ['The ID or name of the user.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options_with_depth(STATES),
}


DOCUMENTATION = """
module: group_info
short_description: List Ionos Cloud groups.
description:
     - This is a simple module that supports listing group.
version_added: "2.0"
options:
    qw;oeifghwo[gjwpgjpowefpokj]
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all groups
      group_info:
      register: group_list_response
    - name: Get all groups for a user
      group_info:
        user: <USER_EMAIL>
      register: group_list_response
"""

def get_users(client):
    all_users = ionoscloud.Users(items=[])
    offset = 0
    limit = 100

    users = client.um_users_get(depth=2, limit=limit, offset=offset)
    all_users.items += users.items
    while(users.links.next is not None):
        offset += limit
        users = client.um_users_get(depth=2, limit=limit, offset=offset)
        all_users.items += users.items

    return all_users


def get_objects(module, client):
    um_api = ionoscloud.UserManagementApi(api_client=client)
    user = module.params.get('user')

    if user:
        # Locate UUID for User
        user_list = get_users(client)
        user_id = get_resource_id(module, user_list, user)
        groups = um_api.um_users_groups_get(user_id, depth=module.params.get('depth'))

    else:
        groups = um_api.um_groups_get(depth=module.params.get('depth'))
    
    return groups


if __name__ == '__main__':
    default_main_info(
        ionoscloud, 'ionoscloud', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
