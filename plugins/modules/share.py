#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import GroupShare, GroupShareProperties
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Share'
RETURNED_KEY = 'share'

OPTIONS = {
    'edit_privilege': {
        'description': ['edit privilege on a resource'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'share_privilege': {
        'description': ['share privilege on a resource'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'group': {
        'description': ['The name or ID of the group.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'resource_ids': {
        'description': ['A list of resource IDs to add, update or remove as shares.'],
        'available': STATES,
        'required': STATES,
        'type': 'list',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: share
short_description: Add, update or remove shares.
description:
     - This module allows you to add, update or remove resource shares.
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
    edit_privilege:
        description:
        - edit privilege on a resource
        required: false
    group:
        description:
        - The name or ID of the group.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    resource_ids:
        description:
        - A list of resource IDs to add, update or remove as shares.
        required: true
    share_privilege:
        description:
        - share privilege on a resource
        required: false
    state:
        choices:
        - present
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
    'present': '''
name: Create share
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: true
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: present
register: share
''',
    'update': '''
name: Update shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: false
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: update
''',
    'absent': '''
name: Remove shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  resource_ids:
  - ''
  - ''
  state: absent
''',
}

EXAMPLES = """
name: Create share
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: true
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: present
register: share


name: Update shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: false
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: update


name: Remove shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  resource_ids:
  - ''
  - ''
  state: absent
"""


class ShareModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def present_object(self, clients):
        """
        Create shares.

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            The share instance
        """
        client = clients[0]
        user_management_server = ionoscloud.UserManagementApi(api_client=client)
        group = self.module.params.get('group')

        # Locate UUID for the group
        group_list = user_management_server.um_groups_get(depth=2)
        group_id = get_resource_id(self.module, group_list, group)

        edit_privilege = self.module.params.get('edit_privilege')
        share_privilege = self.module.params.get('share_privilege')
        resource_ids = self.module.params.get('resource_ids')

        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=1).items
        for share in share_list:
            if share.id in resource_ids:
                if (
                    edit_privilege and share.properties.edit_privilege != edit_privilege
                    or share_privilege and share.properties.share_privilege != share_privilege
                ):
                    share = GroupShare(properties=GroupShareProperties(
                        edit_privilege=edit_privilege if edit_privilege is not None else share.properties.edit_privilege,
                        share_privilege=share_privilege if share_privilege is not None else share.properties.share_privilege,
                    ))

                    _, _, headers = user_management_server.um_groups_shares_put_with_http_info(
                        group_id=group_id, resource_id=uuid, resource=share,
                    )
                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                resource_ids.remove(share.id)

        should_change = True

        if not resource_ids:
            should_change = False

        if self.module.check_mode:
            self.module.exit_json(changed=should_change)

        if not should_change:
            share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=1).items
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'shares': [s.to_dict() for s in share_list],
            }

        try:
            for uuid in resource_ids:
                share_properties = GroupShareProperties(
                    edit_privilege=edit_privilege or False, share_privilege=share_privilege or False,
                )
                share = GroupShare(properties=share_properties)
                _, _, headers = user_management_server.um_groups_shares_post_with_http_info(
                    group_id=group_id, resource_id=uuid, resource=share,
                )

                if wait:
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=1).items

            return {
                'changed': True,
                'failed': False,
                'action': 'create',
                'shares': [s.to_dict() for s in share_list]
            }

        except Exception as e:
            self.module.fail_json(msg="failed to create the shares: %s" % to_native(e))


    def update_object(self, clients):
        """
        Update shares.

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            The share instances
        """
        client = clients[0]
        group = self.module.params.get('group')
        user_management_server = ionoscloud.UserManagementApi(api_client=client)

        # Locate UUID for the group
        group_list = user_management_server.um_groups_get(depth=2)
        group_id = get_resource_id(self.module, group_list, group)

        edit_privilege = self.module.params.get('edit_privilege')
        share_privilege = self.module.params.get('share_privilege')
        resource_ids = self.module.params.get('resource_ids')

        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        try:
            share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=1)
            existing = dict()
            for share in share_list.items:
                existing[share.id] = share

            responses = []

            for uuid in resource_ids:
                if uuid in existing.keys():
                    share = existing[uuid]

                    share = GroupShare(properties=GroupShareProperties(
                        edit_privilege=edit_privilege if edit_privilege is not None else share.properties.edit_privilege,
                        share_privilege=share_privilege if share_privilege is not None else share.properties.share_privilege,
                    ))

                    _, _, headers = user_management_server.um_groups_shares_put_with_http_info(
                        group_id=group_id, resource_id=uuid, resource=share,
                    )
                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                return {
                    'changed': True,
                    'failed': False,
                    'action': 'update',
                    'share': [s.to_dict() for s in responses]
                }

        except Exception as e:
            self.module.fail_json(msg="failed to update the shares: %s" % to_native(e))


    def absent_object(self, clients):
        """
        Remove shares

        module : AnsibleModule object
        client: authenticated ionoscloud object.

        Returns:
            True if the share was removed, false otherwise
        """
        group = self.module.params.get('group')
        user_management_server = ionoscloud.UserManagementApi(api_client=clients[0])

        # Locate UUID for the group
        group_list = user_management_server.um_groups_get(depth=1)
        group_id = get_resource_id(self.module, group_list, group)

        if self.module.check_mode:
            self.module.exit_json(changed=True)

        try:

            for uuid in self.module.params.get('resource_ids'):
                user_management_server.um_groups_shares_delete(group_id=group_id, resource_id=uuid)

            return {
                'action': 'delete',
                'changed': True,
                'id': group_id
            }
        except Exception as e:
            self.module.fail_json(msg="failed to remove the shares: %s" % to_native(e))
            return {
                'action': 'delete',
                'changed': False,
                'id': group_id
            }


if __name__ == '__main__':
    ionos_module = ShareModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
