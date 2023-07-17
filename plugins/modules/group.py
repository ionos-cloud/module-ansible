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
        'description': ['Boolean value indicating if the group is allowed to create virtual data centers.'],
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
        'description': ['Create pcc privilege.'],
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
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different'
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
    - "ionoscloud >= 6.0.2"
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
      group: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  ''',
  'absent' : '''# Remove a group
  - name: Remove group
    group:
      group: guests
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('create_datacenter') is not None
        and existing_object.properties.create_data_center != module.params.get('create_datacenter')
        or module.params.get('create_snapshot') is not None
        and existing_object.properties.create_snapshot != module.params.get('create_snapshot')
        or module.params.get('reserve_ip') is not None
        and existing_object.properties.reserve_ip != module.params.get('reserve_ip')
        or module.params.get('access_activity_log') is not None
        and existing_object.properties.access_activity_log != module.params.get('access_activity_log')
        or module.params.get('create_pcc') is not None
        and existing_object.properties.create_pcc != module.params.get('create_pcc')
        or module.params.get('s3_privilege') is not None
        and existing_object.properties.s3_privilege != module.params.get('s3_privilege')
        or module.params.get('create_backup_unit') is not None
        and existing_object.properties.create_backup_unit != module.params.get('create_backup_unit')
        or module.params.get('create_internet_access') is not None
        and existing_object.properties.create_internet_access != module.params.get('create_internet_access')
        or module.params.get('create_k8s_cluster') is not None
        and existing_object.properties.create_k8s_cluster != module.params.get('create_k8s_cluster')
        or module.params.get('create_flow_log') is not None
        and existing_object.properties.create_flow_log != module.params.get('create_flow_log')
        or module.params.get('access_and_manage_monitoring') is not None
        and existing_object.properties.access_and_manage_monitoring != module.params.get('access_and_manage_monitoring')
        or module.params.get('access_and_manage_certificates') is not None
        and existing_object.properties.access_and_manage_certificates != module.params.get('access_and_manage_certificates')
        or module.params.get('manage_dbaas') is not None
        and existing_object.properties.manage_dbaas != module.params.get('manage_dbaas')
        or module.params.get('users') is not None
    )


def _get_object_list(module, client):
    return ionoscloud.UserManagementApi(client).um_groups_get(depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('group')


def _create_object(module, client, existing_object=None):
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
    manage_dbaas = module.params.get('manage_dbaas')

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

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

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

        if wait or module.params.get('users') is not None:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        
        if module.params.get('users') is not None:
            old_group_user_ids = []
            for u in um_api.um_groups_users_get(existing_object.id, depth=1).items:
                old_group_user_ids.append(u.id)

            all_users = get_users(um_api)
            new_group_user_ids = []

            for u in module.params.get('users'):
                user_id = get_resource_id(module, all_users, u, [['id'], ['properties', 'email']])
                if user_id is None:
                    module.fail_json(msg="User '{}' not found!".format(u))
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
        module.fail_json(msg="failed to create the new group: %s" % to_native(e))
    return group_response


def _update_object(module, client, existing_object):
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
    manage_dbaas = module.params.get('manage_dbaas')

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

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

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
        if wait or module.params.get('users') is not None:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        
        if module.params.get('users') is not None:
            old_group_user_ids = []
            for u in um_api.um_groups_users_get(existing_object.id, depth=1).items:
                old_group_user_ids.append(u.id)

            all_users = get_users(um_api)
            new_group_user_ids = []

            for u in module.params.get('users'):
                user_id = get_resource_id(module, all_users, u, [['id'], ['properties', 'email']])
                if user_id is None:
                    module.fail_json(msg="User '{}' not found!".format(u))
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
        module.fail_json(msg="failed to update the group: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    um_api = ionoscloud.UserManagementApi(client)

    try:
        _, _, headers = um_api.um_groups_delete_with_http_info(existing_object.id)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the group: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

    existing_object = get_resource(module, object_list, _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(module, object_list, object_name)

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
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
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

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

        try:
            if state == 'absent':
                module.exit_json(**remove_object(module, api_client))
            elif state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()
