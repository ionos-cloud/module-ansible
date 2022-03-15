#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import User, UserProperties, Group, GroupProperties
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
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Group'

OPTIONS = {
    'name': {
        'description': ['The name of the group.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'create_datacenter': {
        'description': ['Boolean value indicating if the group is allowed to create virtual data centers.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_snapshot': {
        'description': ['Boolean value indicating if the group is allowed to create snapshots.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'reserve_ip': {
        'description': ['Boolean value indicating if the group is allowed to reserve IP addresses.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_activity_log': {
        'description': ['Boolean value indicating if the group is allowed to access the activity log.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_pcc': {
        'description': ['Boolean value indicating if the group is allowed to create PCCs.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    's3_privilege': {
        'description': ['Boolean value indicating if the group has S3 privilege.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_backup_unit': {
        'description': ['Boolean value indicating if the group is allowed to create backup units.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_internet_access': {
        'description': ['Boolean value indicating if the group is allowed to create internet access.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_k8s_cluster': {
        'description': ['Boolean value indicating if the group is allowed to create k8s clusters.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'create_flow_log': {
        'description': ['Boolean value indicating if the group is allowed to create flowlogs.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_and_manage_monitoring': {
        'description': [
            'Privilege for a group to access and manage monitoring related functionality (access metrics, '
            'CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS).',
        ],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'access_and_manage_certificates': {
        'description': ['Privilege for a group to access and manage certificates.'],
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
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
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
module: group
short_description: Create, update or remove a group.
description:
     - This module allows you to create, update or remove a group.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a group
  - name: Create group
    group:
      name: guests
      create_datacenter: true
      create_snapshot: true
      reserve_ip: false
      access_activity_log: false
      state: present
  ''',
  'update' : '''# Update a group
  - name: Update group
    group:
      name: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  ''',
  'absent' : '''# Remove a group
  - name: Remove group
    group:
      name: guests
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_group(module, client):
    """
    Creates a group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The group instance
    """
    name = module.params.get('name')
    create_datacenter = module.params.get('create_datacenter')
    create_snapshot = module.params.get('create_snapshot')
    reserve_ip = module.params.get('reserve_ip')
    access_activity_log = module.params.get('access_activity_log')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    create_pcc = module.params.get('create_pcc')
    s3_privilege = module.params.get('s3_privilege')
    create_backup_unit = module.params.get('create_backup_unit')
    create_internet_access = module.params.get('create_internet_access')
    create_k8s_cluster = module.params.get('create_k8s_cluster')
    create_flow_log = module.params.get('create_flow_log')
    access_and_manage_monitoring = module.params.get('access_and_manage_monitoring')
    access_and_manage_certificates = module.params.get('access_and_manage_certificates')

    user_management_server = ionoscloud.UserManagementApi(client)

    group = None
    groups = user_management_server.um_groups_get(depth=2)
    for g in groups.items:
        if name == g.properties.name:
            group = g
            break

    should_change = group is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'group': group.to_dict()
        }

    try:
        group_properties = GroupProperties(name=name,
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
                                           access_and_manage_certificates=access_and_manage_certificates or False)

        group = Group(properties=group_properties)
        response = user_management_server.um_groups_post_with_http_info(group)
        (group_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'group': group_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the group: %s" % to_native(e))


def update_group(module, client):
    """
    Updates a group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The group instance
    """
    name = module.params.get('name')
    create_datacenter = module.params.get('create_datacenter')
    create_snapshot = module.params.get('create_snapshot')
    reserve_ip = module.params.get('reserve_ip')
    access_activity_log = module.params.get('access_activity_log')
    create_pcc = module.params.get('create_pcc')
    s3_privilege = module.params.get('s3_privilege')
    create_backup_unit = module.params.get('create_backup_unit')
    create_internet_access = module.params.get('create_internet_access')
    create_k8s_cluster = module.params.get('create_k8s_cluster')
    create_flow_log = module.params.get('create_flow_log')
    access_and_manage_monitoring = module.params.get('access_and_manage_monitoring')
    access_and_manage_certificates = module.params.get('access_and_manage_certificates')
    
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    user_management_server = ionoscloud.UserManagementApi(client)

    try:
        group = None
        group_id = None
        groups = user_management_server.um_groups_get(depth=2)
        for g in groups.items:
            if name == g.properties.name:
                group = g
                group_id = g.id
                break

        if group:
            if module.check_mode:
                module.exit_json(changed=True)

            if create_datacenter is None:
                create_datacenter = group.properties.create_data_center
            if create_snapshot is None:
                create_snapshot = group.properties.create_snapshot
            if reserve_ip is None:
                reserve_ip = group.properties.reserve_ip
            if access_activity_log is None:
                access_activity_log = group.properties.access_activity_log
            if create_pcc is None:
                create_pcc = group.properties.create_pcc
            if s3_privilege is None:
                s3_privilege = group.properties.s3_privilege
            if create_backup_unit is None:
                create_backup_unit = group.properties.create_backup_unit
            if create_internet_access is None:
                create_internet_access = group.properties.create_internet_access
            if create_k8s_cluster is None:
                create_k8s_cluster = group.properties.create_k8s_cluster
            if create_flow_log is None:
                create_flow_log = group.properties.create_flow_log
            if access_and_manage_monitoring is None:
                access_and_manage_monitoring = group.properties.access_and_manage_monitoring
            if access_and_manage_certificates is None:
                access_and_manage_certificates = group.properties.access_and_manage_certificates

            group_properties = GroupProperties(name=name,
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
                                               access_and_manage_certificates=access_and_manage_certificates)

            group = Group(properties=group_properties)

            response = user_management_server.um_groups_put_with_http_info(group_id=group_id, group=group)
            (group_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            if module.params.get('users') is not None:

                group = user_management_server.um_groups_find_by_id(group_id=group_response.id, depth=2)
                old_gu = []
                for u in group.entities.users.items:
                    old_gu.append(u.id)

                all_users = user_management_server.um_users_get(depth=2)
                new_gu = []

                for u in module.params.get('users'):
                    user_id = _get_user_id(all_users, u)
                    new_gu.append(user_id)

                for user_id in old_gu:
                    if user_id not in new_gu:
                        user_management_server.um_groups_users_delete(
                            group_id=group.id,
                            user_id=user_id
                        )

                for user_id in new_gu:
                    if user_id not in old_gu:
                        response = user_management_server.um_groups_users_post_with_http_info(
                            group_id=group.id,
                            user=User(id=user_id)
                        )
                        (user_response, _, headers) = response
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                'group': group_response.to_dict()
            }
        else:
            module.fail_json(msg='Group \'%s\' not found.' % str(name))

    except Exception as e:
        module.fail_json(msg="failed to update the group: %s" % to_native(e))


def delete_group(module, client):
    """
    Removes a group

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the group was removed, false otherwise
    """
    name = module.params.get('name')

    # Locate UUID for the group
    group_list = client.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, name, module, "Group")

    if not group_id:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        client.um_groups_delete(group_id=group_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': group_id
        }

    except Exception as e:
        module.fail_json(msg="failed to remove the group: %s" % to_native(e))


def _get_user_id(resource_list, identity):
    """
    Return the UUID of a user regardless of whether the email or UUID is passed.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.email, resource.id):
            return resource.id
    return None


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


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
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

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
        api_instance = ionoscloud.UserManagementApi(api_client)

        try:
            if state == 'absent':
                module.exit_json(**delete_group(module, api_instance))
            elif state == 'present':
                module.exit_json(**create_group(module, api_client))
            elif state == 'update':
                module.exit_json(**update_group(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
