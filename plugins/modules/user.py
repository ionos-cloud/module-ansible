#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, UserPropertiesPost, UserPropertiesPut, UserPost, UserPut
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_users, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options

import re


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'User'
RETURNED_KEY = 'user'

OPTIONS = {
    'firstname': {
        'description': ['The first name of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'lastname': {
        'description': ['The last name of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'email': {
        'description': ['The email address of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'user': {
        'description': ['The ID or name of the user.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'user_password': {
        'description': ['A password for the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'administrator': {
        'description': ['Indicates if the user has admin rights.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'force_sec_auth': {
        'description': ['Indicates if secure authentication should be forced on the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'groups': {
        'description': ['A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'sec_auth_active': {
        'description': ['Indicates if secure authentication is active for the user.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: user
short_description: Create, update or remove a user.
description:
     - This module allows you to create, update or remove a user.
version_added: "2.0"
options:
    administrator:
        description:
        - Indicates if the user has admin rights.
        required: false
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
    email:
        description:
        - The email address of the user.
        required: false
    firstname:
        description:
        - The first name of the user.
        required: false
    force_sec_auth:
        description:
        - Indicates if secure authentication should be forced on the user.
        required: false
    groups:
        description:
        - A list of group IDs or names where the user (non-administrator) is to be added.
            Set to empty list ([]) to remove the user from all groups.
        required: false
    lastname:
        description:
        - The last name of the user.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    sec_auth_active:
        description:
        - Indicates if secure authentication is active for the user.
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
    user:
        description:
        - The ID or name of the user.
        required: false
    user_password:
        description:
        - A password for the user.
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
name: Create user
ionoscloudsdk.ionoscloud.user:
  firstname: John
  lastname: Doe
  email: ''
  administrator: false
  user_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  force_sec_auth: false
  state: present
''',
    'update': '''
name: Add user to first group
ionoscloudsdk.ionoscloud.user:
  user: ''
  groups:
  - 'AnsibleAutoTestUM 1'
  state: update
''',
    'absent': '''
name: Delete user
ionoscloudsdk.ionoscloud.user:
  user: ''
  state: absent
''',
}

EXAMPLES = """
name: Create user
ionoscloudsdk.ionoscloud.user:
  firstname: John
  lastname: Doe
  email: ''
  administrator: false
  user_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  force_sec_auth: false
  state: present


name: Add user to first group
ionoscloudsdk.ionoscloud.user:
  user: ''
  groups:
  - 'AnsibleAutoTestUM 1'
  state: update


name: Delete user
ionoscloudsdk.ionoscloud.user:
  user: ''
  state: absent
"""


class UserModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'email']]


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('lastname') is not None
            and existing_object.properties.lastname != self.module.params.get('lastname')
            or self.module.params.get('firstname') is not None
            and existing_object.properties.firstname != self.module.params.get('firstname')
            or self.module.params.get('email') is not None
            and existing_object.properties.email != self.module.params.get('email')
            or self.module.params.get('administrator') is not None
            and existing_object.properties.administrator != self.module.params.get('administrator')
            or self.module.params.get('force_sec_auth') is not None
            and existing_object.properties.force_sec_auth != self.module.params.get('force_sec_auth')
            or self.module.params.get('user_password') is not None
            or self.module.params.get('groups') is not None
        )


    def _get_object_list(self, clients):
        query_params = {}
        if self.module.params.get('email') is not None:
            query_params = {
                'filter.email': self.module.params.get('email')
            }
        elif self.module.params.get('user') and not None and re.match(r"[^@]+@[^@]+\.[^@]+", self.module.params.get('user')):
            query_params = {
                'filter.email': self.module.params.get('user')
            }

        return get_users(ionoscloud.UserManagementApi(clients[0]), ionoscloud.Users(items=[]), query_params=query_params)


    def _get_object_name(self):
        return self.module.params.get('email')


    def _get_object_identifier(self):
        return self.module.params.get('user')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        firstname = self.module.params.get('firstname')
        lastname = self.module.params.get('lastname')
        email = self.module.params.get('email')
        user_password = self.module.params.get('user_password')
        administrator = self.module.params.get('administrator')
        force_sec_auth = self.module.params.get('force_sec_auth')

        if existing_object is not None:
            firstname = existing_object.properties.firstname if firstname is None else firstname
            lastname = existing_object.properties.lastname if lastname is None else lastname
            email = existing_object.properties.email if email is None else email
            user_password = existing_object.properties.user_password if user_password is None else user_password
            administrator = existing_object.properties.administrator if administrator is None else administrator
            force_sec_auth = existing_object.properties.force_sec_auth if force_sec_auth is None else force_sec_auth

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        um_api = ionoscloud.UserManagementApi(client)

        user = UserPost(properties=UserPropertiesPost(
            firstname=firstname, lastname=lastname, email=email,
            administrator=administrator or False,
            force_sec_auth=force_sec_auth or False,
            password=user_password,
        ))

        try:
            user_response, _, headers = um_api.um_users_post_with_http_info(user)

            if wait or self.module.params.get('groups') is not None:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            
            if self.module.params.get('groups') is not None:
                # Get IDs of current groups of the user
                old_user_group_ids = []
                for g in um_api.um_users_groups_get(user_response.id).items:
                    old_user_group_ids.append(g.id)

                all_groups = um_api.um_groups_get(depth=2)
                # Get IDs of groups that user needs to have at the end of update
                new_user_group_ids = []
                for g in self.module.params.get('groups'):
                    group_id = get_resource_id(self.module, all_groups, g)
                    new_user_group_ids.append(group_id)

                # Delete groups user not supposed to be in at end of update
                for group_id in old_user_group_ids:
                    if group_id not in new_user_group_ids:
                        um_api.um_groups_users_delete(
                            group_id=group_id,
                            user_id=user_response.id
                        )

                # Post groups that weren't assigned to the user before
                for group_id in new_user_group_ids:
                    if group_id not in old_user_group_ids:
                        response = um_api.um_groups_users_post_with_http_info(
                            group_id=group_id,
                            user=User(id=user_response.id)
                        )
                        (user_response, _, headers) = response
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                # update to reflect new group changes
                user_response = um_api.um_users_find_by_id(user_response.id, depth=2)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new user: %s" % to_native(e))
        return user_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        firstname = self.module.params.get('firstname')
        lastname = self.module.params.get('lastname')
        email = self.module.params.get('email')
        administrator = self.module.params.get('administrator')
        force_sec_auth = self.module.params.get('force_sec_auth')
        user_password = self.module.params.get('user_password')

        email = existing_object.properties.email if email is None else email
        firstname = existing_object.properties.firstname if firstname is None else firstname
        lastname = existing_object.properties.lastname if lastname is None else lastname
        administrator = existing_object.properties.administrator if administrator is None else administrator
        force_sec_auth = existing_object.properties.force_sec_auth if force_sec_auth is None else force_sec_auth

        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        um_api = ionoscloud.UserManagementApi(client)

        user_properties = UserPropertiesPut(
            firstname=firstname,
            lastname=lastname,
            email=email,
            administrator=administrator or False,
            force_sec_auth=force_sec_auth or False,
        )
        if user_password:
            user_properties.password = user_password
        
        new_user = UserPut(properties=user_properties)

        try:
            user_response, _, headers = um_api.um_users_put_with_http_info(
                existing_object.id, new_user,
            )

            if wait or self.module.params.get('groups') is not None:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            
            if self.module.params.get('groups') is not None:
                # Get IDs of current groups of the user
                old_user_group_ids = []
                for g in um_api.um_users_groups_get(user_response.id).items:
                    old_user_group_ids.append(g.id)

                all_groups = um_api.um_groups_get(depth=2)
                # Get IDs of groups that user needs to have at the end of update
                new_user_group_ids = []
                for g in self.module.params.get('groups'):
                    group_id = get_resource_id(self.module, all_groups, g)
                    new_user_group_ids.append(group_id)

                # Delete groups user not supposed to be in at end of update
                for group_id in old_user_group_ids:
                    if group_id not in new_user_group_ids:
                        um_api.um_groups_users_delete(
                            group_id=group_id,
                            user_id=user_response.id
                        )

                # Post groups that weren't assigned to the user before
                for group_id in new_user_group_ids:
                    if group_id not in old_user_group_ids:
                        response = um_api.um_groups_users_post_with_http_info(
                            group_id=group_id,
                            user=User(id=user_response.id)
                        )
                        (user_response, _, headers) = response
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                # update to reflect new group changes
                user_response = um_api.um_users_find_by_id(user_response.id, depth=2)

            return user_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the user: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        um_api = ionoscloud.UserManagementApi(client)

        try:
            _, _, headers = um_api.um_users_delete_with_http_info(existing_object.id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the user: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = UserModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
