#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import yaml

__metaclass__ = type


import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import GroupShare, GroupShareProperties
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
OBJECT_NAME = 'Share'

OPTIONS = {
    'edit_privilege': {
        'description': ['Boolean value indicating that the group has permission to edit privileges on the resource.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'share_privilege': {
        'description': ['Boolean value indicating that the group has permission to share the resource.'],
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
module: share
short_description: Add, update or remove shares.
description:
     - This module allows you to add, update or remove resource shares.
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
  'present' : '''# Create shares
  - name: Create share
    share:
      group: Demo
      edit_privilege: true
      share_privilege: true
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
      state: present
  ''',
  'update' : '''# Update shares
  - name: Update shares
    share:
      group: Demo
      edit_privilege: false
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      state: update
  ''',
  'absent' : '''# Remove shares
  - name: Remove shares
    share:
      group: Demo
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
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


def create_shares(module, client):
    """
    Create shares.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The share instance
    """
    user_management_server = ionoscloud.UserManagementApi(api_client=client)
    group = module.params.get('group')

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2).items
    for share in share_list:
        if share.id in resource_ids:
            resource_ids.remove(share.id)

    should_change = True

    if not resource_ids:
        should_change = False

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'shares': [s.to_dict() for s in share_list],
        }

    try:
        for uuid in resource_ids:
            share_properties = GroupShareProperties(edit_privilege=edit_privilege or False,
                                                    share_privilege=share_privilege or False)
            share = GroupShare(properties=share_properties)
            response = user_management_server.um_groups_shares_post_with_http_info(group_id=group_id, resource_id=uuid,
                                                                                   resource=share)
            (share_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2).items

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'shares': [s.to_dict() for s in share_list]
        }

    except Exception as e:
        module.fail_json(msg="failed to create the shares: %s" % to_native(e))


def update_shares(module, client):
    """
    Update shares.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The share instances
    """
    group = module.params.get('group')
    user_management_server = ionoscloud.UserManagementApi(api_client=client)

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    edit_privilege = module.params.get('edit_privilege')
    share_privilege = module.params.get('share_privilege')
    resource_ids = module.params.get('resource_ids')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        share_list = user_management_server.um_groups_shares_get(group_id=group_id, depth=2)
        existing = dict()
        for share in share_list.items:
            existing[share.id] = share

        responses = []

        for uuid in resource_ids:
            if uuid in existing.keys():
                share = existing[uuid]
                if edit_privilege is None:
                    edit_privilege = share.properties.edit_privilege
                if share_privilege is None:
                    share_privilege = share.properties.share_privilege

                share_properties = GroupShareProperties(edit_privilege=edit_privilege or False,
                                                        share_privilege=share_privilege or False)
                share = GroupShare(properties=share_properties)

                response = user_management_server.um_groups_shares_put_with_http_info(group_id=group_id,
                                                                                      resource_id=uuid, resource=share)
                (share_response, _, headers) = response
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
        module.fail_json(msg="failed to update the shares: %s" % to_native(e))


def delete_shares(module, client):
    """
    Remove shares

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the share was removed, false otherwise
    """
    group = module.params.get('group')
    user_management_server = ionoscloud.UserManagementApi(api_client=client)

    # Locate UUID for the group
    group_list = user_management_server.um_groups_get(depth=2)
    group_id = _get_resource_id(group_list, group, module, "Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:

        for uuid in module.params.get('resource_ids'):
            user_management_server.um_groups_shares_delete(group_id=group_id, resource_id=uuid)

        return {
            'action': 'delete',
            'changed': True,
            'id': group_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the shares: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': group_id
        }


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


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

        try:
            if state == 'absent':
                module.exit_json(**delete_shares(module, api_client))
            elif state == 'present':
                module.exit_json(**create_shares(module, api_client))
            elif state == 'update':
                module.exit_json(**update_shares(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
