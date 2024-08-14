#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, Group, GroupProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id, get_users,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Group'
RETURNED_KEY = 'group'

OPTIONS = {
    'name': {
        'description': ['The name of the resource.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'group': {
        'description': ['The ID or name of the group.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'create_datacenter': {
        'description': ['Create data center privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_snapshot': {
        'description': ['Create snapshot privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'reserve_ip': {
        'description': ['Reserve IP block privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_activity_log': {
        'description': ['Activity log access privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_pcc': {
        'description': ['User privilege to create a cross connect.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    's3_privilege': {
        'description': ['S3 privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_backup_unit': {
        'description': ['Create backup unit privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_internet_access': {
        'description': ['Create internet access privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_k8s_cluster': {
        'description': ['Create Kubernetes cluster privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_flow_log': {
        'description': ['Create Flow Logs privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_and_manage_monitoring': {
        'description': ['Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS).'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_and_manage_certificates': {
        'description': ['Privilege for a group to access and manage certificates.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'manage_dbaas': {
        'description': ['Privilege for a group to manage DBaaS related functionality.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'users': {
        'description': [
            'A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: group
short_description: Create, update or remove a group.
description:
     - This module allows you to create, update or remove a group.
version_added: "2.0"
options:
    access_activity_log:
        description:
        - Activity log access privilege.
        required: false
    access_and_manage_certificates:
        description:
        - Privilege for a group to access and manage certificates.
        required: false
    access_and_manage_monitoring:
        description:
        - Privilege for a group to access and manage monitoring related functionality
            (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service
            (MaaS).
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
    create_backup_unit:
        description:
        - Create backup unit privilege.
        required: false
    create_datacenter:
        description:
        - Create data center privilege.
        required: false
    create_flow_log:
        description:
        - Create Flow Logs privilege.
        required: false
    create_internet_access:
        description:
        - Create internet access privilege.
        required: false
    create_k8s_cluster:
        description:
        - Create Kubernetes cluster privilege.
        required: false
    create_pcc:
        description:
        - User privilege to create a cross connect.
        required: false
    create_snapshot:
        description:
        - Create snapshot privilege.
        required: false
    group:
        description:
        - The ID or name of the group.
        required: false
    manage_dbaas:
        description:
        - Privilege for a group to manage DBaaS related functionality.
        required: false
    name:
        description:
        - The name of the resource.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    reserve_ip:
        description:
        - Reserve IP block privilege.
        required: false
    s3_privilege:
        description:
        - S3 privilege.
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
    users:
        description:
        - A list of (non-administrator) user IDs or emails to associate with the group.
            Set to empty list ([]) to remove all users from the group.
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
  'present' : '''
name: Create group
ionoscloudsdk.ionoscloud.group:
  name: 'AnsibleAutoTestUM'
  create_datacenter: true
  create_snapshot: true
  reserve_ip: true
  access_activity_log: true
  create_pcc: true
  s3_privilege: true
  create_backup_unit: true
  create_internet_access: true
  create_k8s_cluster: true
  create_flow_log: true
  access_and_manage_monitoring: true
  access_and_manage_certificates: true
  manage_dbaas: true
register: group_response
''',
  'update' : '''
name: Add user1 to group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  users:
  - ''
  state: update
''',
  'absent' : '''
name: Delete group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  state: absent
''',
}

EXAMPLES = """
name: Create group
ionoscloudsdk.ionoscloud.group:
  name: 'AnsibleAutoTestUM'
  create_datacenter: true
  create_snapshot: true
  reserve_ip: true
  access_activity_log: true
  create_pcc: true
  s3_privilege: true
  create_backup_unit: true
  create_internet_access: true
  create_k8s_cluster: true
  create_flow_log: true
  access_and_manage_monitoring: true
  access_and_manage_certificates: true
  manage_dbaas: true
register: group_response


name: Add user1 to group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  users:
  - ''
  state: update


name: Delete group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  state: absent
"""


class GroupModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('create_datacenter') is not None
            and existing_object.properties.create_data_center != self.module.params.get('create_datacenter')
            or self.module.params.get('create_snapshot') is not None
            and existing_object.properties.create_snapshot != self.module.params.get('create_snapshot')
            or self.module.params.get('reserve_ip') is not None
            and existing_object.properties.reserve_ip != self.module.params.get('reserve_ip')
            or self.module.params.get('access_activity_log') is not None
            and existing_object.properties.access_activity_log != self.module.params.get('access_activity_log')
            or self.module.params.get('create_pcc') is not None
            and existing_object.properties.create_pcc != self.module.params.get('create_pcc')
            or self.module.params.get('s3_privilege') is not None
            and existing_object.properties.s3_privilege != self.module.params.get('s3_privilege')
            or self.module.params.get('create_backup_unit') is not None
            and existing_object.properties.create_backup_unit != self.module.params.get('create_backup_unit')
            or self.module.params.get('create_internet_access') is not None
            and existing_object.properties.create_internet_access != self.module.params.get('create_internet_access')
            or self.module.params.get('create_k8s_cluster') is not None
            and existing_object.properties.create_k8s_cluster != self.module.params.get('create_k8s_cluster')
            or self.module.params.get('create_flow_log') is not None
            and existing_object.properties.create_flow_log != self.module.params.get('create_flow_log')
            or self.module.params.get('access_and_manage_monitoring') is not None
            and existing_object.properties.access_and_manage_monitoring != self.module.params.get('access_and_manage_monitoring')
            or self.module.params.get('access_and_manage_certificates') is not None
            and existing_object.properties.access_and_manage_certificates != self.module.params.get('access_and_manage_certificates')
            or self.module.params.get('manage_dbaas') is not None
            and existing_object.properties.manage_dbaas != self.module.params.get('manage_dbaas')
            or self.module.params.get('users') is not None
        )


    def _get_object_list(self, clients):
        return ionoscloud.UserManagementApi(clients[0]).um_groups_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('group')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        create_datacenter = self.module.params.get('create_datacenter')
        create_snapshot = self.module.params.get('create_snapshot')
        reserve_ip = self.module.params.get('reserve_ip')
        access_activity_log = self.module.params.get('access_activity_log')
        create_pcc = self.module.params.get('create_pcc')
        s3_privilege = self.module.params.get('s3_privilege')
        create_backup_unit = self.module.params.get('create_backup_unit')
        create_internet_access = self.module.params.get('create_internet_access')
        create_k8s_cluster = self.module.params.get('create_k8s_cluster')
        create_flow_log = self.module.params.get('create_flow_log')
        access_and_manage_monitoring = self.module.params.get('access_and_manage_monitoring')
        access_and_manage_certificates = self.module.params.get('access_and_manage_certificates')
        manage_dbaas = self.module.params.get('manage_dbaas')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            create_datacenter = existing_object.properties.create_data_center if create_datacenter is None else create_datacenter
            create_snapshot = existing_object.properties.create_snapshot if create_snapshot is None else create_snapshot
            reserve_ip = existing_object.properties.reserve_ip if reserve_ip is None else reserve_ip
            access_activity_log = existing_object.properties.access_activity_log if access_activity_log is None else access_activity_log
            create_pcc = existing_object.properties.create_pcc if create_pcc is None else create_pcc
            s3_privilege = existing_object.properties.s3_privilege if s3_privilege is None else s3_privilege
            create_backup_unit = existing_object.properties.create_backup_unit if create_backup_unit is None else create_backup_unit
            create_internet_access = existing_object.properties.create_internet_access if create_internet_access is None else create_internet_access
            create_k8s_cluster = existing_object.properties.create_k8s_cluster if create_k8s_cluster is None else create_k8s_cluster
            create_flow_log = existing_object.properties.create_flow_log if create_flow_log is None else create_flow_log
            access_and_manage_monitoring = existing_object.properties.access_and_manage_monitoring if access_and_manage_monitoring is None else access_and_manage_monitoring
            access_and_manage_certificates = existing_object.properties.access_and_manage_certificates if access_and_manage_certificates is None else access_and_manage_certificates
            manage_dbaas = existing_object.properties.manage_dbaas if manage_dbaas is None else manage_dbaas

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        um_api = ionoscloud.UserManagementApi(client)

        group = Group(properties=GroupProperties(
            name=name,
            create_data_center=create_datacenter or False,
            create_snapshot=create_snapshot or False,
            reserve_ip=reserve_ip or False,
            access_activity_log=access_activity_log or False,
            create_pcc=create_pcc or False,
            s3_privilege=s3_privilege or False,
            create_backup_unit=create_backup_unit or False,
            create_internet_access=create_internet_access or False,
            create_k8s_cluster=create_k8s_cluster or False,
            create_flow_log=create_flow_log or False,
            access_and_manage_monitoring=access_and_manage_monitoring or False,
            access_and_manage_certificates=access_and_manage_certificates or False,
            manage_dbaas=manage_dbaas or False,
        ))

        try:
            group_response, _, headers = um_api.um_groups_post_with_http_info(group)

            if wait or self.module.params.get('users') is not None:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            
            if self.module.params.get('users') is not None:
                old_group_user_ids = []
                for u in um_api.um_groups_users_get(existing_object.id, depth=1).items:
                    old_group_user_ids.append(u.id)

                all_users = get_users(um_api, ionoscloud.Users(items=[]))
                new_group_user_ids = []

                for u in self.module.params.get('users'):
                    user_id = get_resource_id(self.module, all_users, u, [['id'], ['properties', 'email']])
                    if user_id is None:
                        self.module.fail_json(msg="User '{}' not found!".format(u))
                    new_group_user_ids.append(user_id)

                for user_id in old_group_user_ids:
                    if user_id not in new_group_user_ids:
                        um_api.um_groups_users_delete(
                            group_id=existing_object.id,
                            user_id=user_id
                        )

                for user_id in new_group_user_ids:
                    if user_id not in old_group_user_ids:
                        _, _, headers = um_api.um_groups_users_post_with_http_info(
                            group_id=existing_object.id,
                            user=User(id=user_id)
                        )

                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                # update group_response to contain changed user list
                group_response = um_api.um_groups_find_by_id(group_response.id, depth=2)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new group: %s" % to_native(e))
        return group_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        create_datacenter = self.module.params.get('create_datacenter')
        create_snapshot = self.module.params.get('create_snapshot')
        reserve_ip = self.module.params.get('reserve_ip')
        access_activity_log = self.module.params.get('access_activity_log')
        create_pcc = self.module.params.get('create_pcc')
        s3_privilege = self.module.params.get('s3_privilege')
        create_backup_unit = self.module.params.get('create_backup_unit')
        create_internet_access = self.module.params.get('create_internet_access')
        create_k8s_cluster = self.module.params.get('create_k8s_cluster')
        create_flow_log = self.module.params.get('create_flow_log')
        access_and_manage_monitoring = self.module.params.get('access_and_manage_monitoring')
        access_and_manage_certificates = self.module.params.get('access_and_manage_certificates')
        manage_dbaas = self.module.params.get('manage_dbaas')

        name = existing_object.properties.name if name is None else name
        create_datacenter = existing_object.properties.create_data_center if create_datacenter is None else create_datacenter
        create_snapshot = existing_object.properties.create_snapshot if create_snapshot is None else create_snapshot
        reserve_ip = existing_object.properties.reserve_ip if reserve_ip is None else reserve_ip
        access_activity_log = existing_object.properties.access_activity_log if access_activity_log is None else access_activity_log
        create_pcc = existing_object.properties.create_pcc if create_pcc is None else create_pcc
        s3_privilege = existing_object.properties.s3_privilege if s3_privilege is None else s3_privilege
        create_backup_unit = existing_object.properties.create_backup_unit if create_backup_unit is None else create_backup_unit
        create_internet_access = existing_object.properties.create_internet_access if create_internet_access is None else create_internet_access
        create_k8s_cluster = existing_object.properties.create_k8s_cluster if create_k8s_cluster is None else create_k8s_cluster
        create_flow_log = existing_object.properties.create_flow_log if create_flow_log is None else create_flow_log
        access_and_manage_monitoring = existing_object.properties.access_and_manage_monitoring if access_and_manage_monitoring is None else access_and_manage_monitoring
        access_and_manage_certificates = existing_object.properties.access_and_manage_certificates if access_and_manage_certificates is None else access_and_manage_certificates
        manage_dbaas = existing_object.properties.manage_dbaas if manage_dbaas is None else manage_dbaas

        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        um_api = ionoscloud.UserManagementApi(client)

        group_properties = GroupProperties(
            name=name,
            create_data_center=create_datacenter,
            create_snapshot=create_snapshot,
            reserve_ip=reserve_ip,
            access_activity_log=access_activity_log,
            create_pcc=create_pcc,
            s3_privilege=s3_privilege,
            create_backup_unit=create_backup_unit,
            create_internet_access=create_internet_access,
            create_k8s_cluster=create_k8s_cluster,
            create_flow_log=create_flow_log,
            access_and_manage_monitoring=access_and_manage_monitoring,
            access_and_manage_certificates=access_and_manage_certificates,
            manage_dbaas=manage_dbaas,
        )

        group = Group(properties=group_properties)

        try:
            group_response, _, headers = um_api.um_groups_put_with_http_info(
                existing_object.id, group,
            )
            if wait or self.module.params.get('users') is not None:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            
            if self.module.params.get('users') is not None:
                old_group_user_ids = []
                for u in um_api.um_groups_users_get(existing_object.id, depth=1).items:
                    old_group_user_ids.append(u.id)

                all_users = get_users(um_api, ionoscloud.Users(items=[]))
                new_group_user_ids = []

                for u in self.module.params.get('users'):
                    user_id = get_resource_id(self.module, all_users, u, [['id'], ['properties', 'email']])
                    if user_id is None:
                        self.module.fail_json(msg="User '{}' not found!".format(u))
                    new_group_user_ids.append(user_id)

                for user_id in old_group_user_ids:
                    if user_id not in new_group_user_ids:
                        um_api.um_groups_users_delete(
                            group_id=existing_object.id,
                            user_id=user_id
                        )

                for user_id in new_group_user_ids:
                    if user_id not in old_group_user_ids:
                        _, _, headers = um_api.um_groups_users_post_with_http_info(
                            group_id=existing_object.id,
                            user=User(id=user_id)
                        )

                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                # update group_response to contain changed user list
                group_response = um_api.um_groups_find_by_id(group_response.id, depth=2)

            return group_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the group: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        um_api = ionoscloud.UserManagementApi(client)

        try:
            _, _, headers = um_api.um_groups_delete_with_http_info(existing_object.id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the group: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = GroupModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
