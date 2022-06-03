#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import yaml
import copy

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import TargetGroup, TargetGroupPut, TargetGroupTarget, TargetGroupProperties, TargetGroups, \
        TargetGroupHealthCheck, TargetGroupHttpHealthCheck
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
DOC_DIRECTORY = 'applicationloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Target Group'


OPTIONS = {
    'name': {
        'description': ['The name of the Target Group.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'algorithm': {
        'description': ['Balancing algorithm.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['Balancing protocol.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'health_check': {
        'description': ['Health check properties for target group.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'http_health_check': {
        'description': ['HTTP health check properties for target group.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'targets': {
        'description': ['An array of items in the collection.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'target_group_id': {
        'description': ['The ID of the Target Group.'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'required': STATES,
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'required': STATES,
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
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
module: target_hroup
short_description: Create or destroy a Ionos Cloud Target Group.
description:
     - This is a simple module that supports creating or removing Target Groups.
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
  'present' : '''
  - name: Create Target Group
    target_group:
      name: "{{ name }}"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      targets:
        - ip: "22.231.2.2"
          port: 8080
          weight: 123
          health_check_enabled: true
          maintenance_enabled: false
      health_check:
        check_timeout: 2000
        check_interval: 1000
        retries: 3
      http_health_check:
        path: "./"
        method: "GET"
        match_type: "STATUS_CODE"
        response: 200
        regex: false
        negate: false
      wait: true
    register: target_group_response
  ''',
  'update' : '''
  - name: Update Target Group
    target_group:
      name: "{{ name }} - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      state: update
    register: target_group_response_update
  ''',
  'absent' : '''
  - name: Remove Target Group
    target_group:
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      wait_timeout: 2000
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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


def _update_target_group(module, client, target_group_server, target_group_id, target_group_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = target_group_server.targetgroups_patch_with_http_info(target_group_id, target_group_properties)
    (target_group_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return target_group_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))

def get_target(target):
    target_object = TargetGroupTarget()
    if target['ip']:
        target_object.ip = target['ip']
    if target['port']:
        target_object.port = target['port']
    if target['weight']:
        target_object.weight = target['weight']
    if target['health_check_enabled']:
        target_object.health_check_enabled = target['health_check_enabled']
    if target['maintenance_enabled']:
        target_object.maintenance_enabled = target['maintenance_enabled']
    return target_object


def get_http_health_check(http_health_check):
    http_health_check_object = TargetGroupHttpHealthCheck()
    if http_health_check['path']:
        http_health_check_object.path = http_health_check['path']
    if http_health_check['method']:
        http_health_check_object.method = http_health_check['method']
    if http_health_check['match_type']:
        http_health_check_object.match_type = http_health_check['match_type']
    if http_health_check['response']:
        http_health_check_object.response = http_health_check['response']
    if http_health_check['regex']:
        http_health_check_object.regex = http_health_check['regex']
    if http_health_check['negate']:
        http_health_check_object.negate = http_health_check['negate']
    http_health_check = http_health_check_object
    return http_health_check


def get_health_check(health_check):
    health_check_object = TargetGroupHealthCheck()
    if health_check['check_timeout']:
        health_check_object.check_timeout = health_check['check_timeout']
    if health_check['check_interval']:
        health_check_object.check_interval = health_check['check_interval']
    if health_check['retries']:
        health_check_object.retries = health_check['retries']
    return health_check_object


def create_target_group(module, client):
    """
    Creates a Target Group

    This will create a new Target Group in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Target Group ID if a new Target Group was created.
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    target_group_server = ionoscloud.TargetGroupsApi(client)
    target_groups = target_group_server.targetgroups_get(depth=5)
    target_group_response = None

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)

    target_list = []
    if targets and len(targets) > 0:
        for t in targets:
            target = get_target(t)
            target_list.append(target)

    existing_target_group = get_resource(module, target_groups, name)

    if existing_target_group:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'target_group': existing_target_group.to_dict()
        }

    target_group_properties = TargetGroupProperties(
        name=name, algorithm=algorithm, protocol=protocol,
        targets=target_list, health_check=health_check,
        http_health_check=http_health_check,
    )
    target_group = TargetGroup(properties=target_group_properties)

    try:
        response = target_group_server.targetgroups_post_with_http_info(target_group)
        (target_group_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Target Group: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'target_group': target_group_response.to_dict()
    }


def update_target_group(module, client):
    """
    Updates a Target Group.

    This will update a Target Group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Target Group was updated, false otherwise
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    target_group_id = module.params.get('target_group_id')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    target_group_server = ionoscloud.TargetGroupsApi(client)
    target_group_response = None

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)

    target_list = []
    if targets and len(targets) > 0:
        for t in targets:
            target = get_target(t)
            target_list.append(target)

    target_groups = target_group_server.targetgroups_get(depth=2)
    existing_target_group_id_by_name = get_resource_id(module, target_groups, name)

    if target_group_id is not None and existing_target_group_id_by_name is not None and existing_target_group_id_by_name != target_group_id:
            module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, name))

    target_group_id = target_group_id if target_group_id else existing_target_group_id_by_name

    target_group_properties = TargetGroupProperties(
        name=name, algorithm=algorithm, protocol=protocol,
        targets=targets, health_check=health_check,
        http_health_check=http_health_check,
    )

    if target_group_id:
        target_group_response = _update_target_group(
            module, client, target_group_server,
            target_group_id,
            target_group_properties,
        )
    else:
        module.fail_json(msg="failed to update the Target Group: The resource does not exist")

    return {
        'changed': True,
        'action': 'update',
        'failed': False,
        'target_group': target_group_response.to_dict()
    }


def remove_target_group(module, client):
    """
    Removes a Target Group.

    This will remove a Target Group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Target Group was deleted, false otherwise
    """
    name = module.params.get('name')
    target_group_id = module.params.get('target_group_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    target_group_server = ionoscloud.TargetGroupsApi(client)

    target_groups = target_group_server.targetgroups_get(depth=2)
    existing_target_group_id_by_name = get_resource_id(module, target_groups, name)

    target_group_id = target_group_id if target_group_id else existing_target_group_id_by_name

    try:
        _, _, headers = target_group_server.target_groups_delete_with_http_info(target_group_id)
        if wait:
            client.wait_for_completion(request_id=_get_request_id(headers['Location']), timeout=wait_timeout)
    except Exception as e:
        module.fail_json(msg="failed to delete the Target Group: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': True,
        'id': target_group_id
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

        if state in ['absent', 'update'] and not module.params.get('name') and not module.params.get('target_group_id'):
            module.fail_json(msg='either name or target_group_id parameter is required for {object_name} state absent'.format(object_name=OBJECT_NAME))

        if state == 'absent':
            try:
                module.exit_json(**remove_target_group(module, api_client))
            except Exception as e:
                module.fail_json(msg='failed to set Target Group state: %s' % to_native(e))
        elif state == 'present':
            try:
                module.exit_json(**create_target_group(module, api_client))
            except Exception as e:
                module.fail_json(msg='failed to set Target Group state: %s' % to_native(e))
        elif state == 'update':
            try:
                module.exit_json(**update_target_group(module, api_client))
            except Exception as e:
                module.fail_json(msg='failed to update the Target Group: %s' % to_native(e))


if __name__ == '__main__':
    main()
