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
RETURNED_KEY = 'target_group'


OPTIONS = {
    'name': {
        'description': ['The target group name.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'algorithm': {
        'description': ['The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['The forwarding protocol. Only the value \'HTTP\' is allowed.'],
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
        'description': ['Array of items in the collection.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'target_group': {
        'description': ['The ID or name of the Target Group.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))

def get_target(target):
    target_object = TargetGroupTarget()
    if target.get('ip'):
        target_object.ip = target['ip']
    if target.get('port'):
        target_object.port = target['port']
    if target.get('weight'):
        target_object.weight = target['weight']
    if target.get('health_check_enabled'):
        target_object.health_check_enabled = target['health_check_enabled']
    if target.get('maintenance_enabled'):
        target_object.maintenance_enabled = target['maintenance_enabled']
    return target_object


def get_http_health_check(http_health_check):
    http_health_check_object = TargetGroupHttpHealthCheck()
    if http_health_check.get('path'):
        http_health_check_object.path = http_health_check['path']
    if http_health_check.get('method'):
        http_health_check_object.method = http_health_check['method']
    if http_health_check.get('match_type'):
        http_health_check_object.match_type = http_health_check['match_type']
    if http_health_check.get('response'):
        http_health_check_object.response = http_health_check['response']
    if http_health_check.get('regex'):
        http_health_check_object.regex = http_health_check['regex']
    if http_health_check.get('negate'):
        http_health_check_object.negate = http_health_check['negate']
    http_health_check = http_health_check_object
    return http_health_check


def get_health_check(health_check):
    health_check_object = TargetGroupHealthCheck()
    if health_check.get('check_timeout'):
        health_check_object.check_timeout = health_check['check_timeout']
    if health_check.get('check_interval'):
        health_check_object.check_interval = health_check['check_interval']
    if health_check.get('retries'):
        health_check_object.retries = health_check['retries']
    return health_check_object


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')
    new_health_check = get_health_check(health_check) if health_check else None
    new_http_health_check = get_http_health_check(http_health_check) if http_health_check else None

    def sort_func(el):
        return el['ip'], el['port']

    if module.params.get('targets'):
        existing_targets = sorted(map(
            lambda x: {
                'ip': x.ip,
                'port': x.port,
                'weight': x.weight,
                'health_check_enabled': x.health_check_enabled,
                'maintenance_enabled': x.maintenance_enabled,
            },
            existing_object.properties.targets
        ), key=sort_func)
        new_targets = sorted(module.params.get('targets'), key=sort_func)

    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('algorithm') is not None
        and existing_object.properties.algorithm != module.params.get('algorithm')
        or module.params.get('protocol') is not None
        and existing_object.properties.protocol != module.params.get('protocol')
        or module.params.get('health_check') is not None
        and (
            existing_object.properties.health_check.check_timeout != new_health_check.check_timeout
            or existing_object.properties.health_check.check_interval != new_health_check.check_interval
            or existing_object.properties.health_check.retries != new_health_check.retries
        )
        or module.params.get('http_health_check') is not None
        and (
            existing_object.properties.http_health_check.path != new_http_health_check.path
            or existing_object.properties.http_health_check.method != new_http_health_check.method
            or existing_object.properties.http_health_check.match_type != new_http_health_check.match_type
            or existing_object.properties.http_health_check.response != new_http_health_check.response
            or existing_object.properties.http_health_check.regex != new_http_health_check.regex
            or existing_object.properties.http_health_check.negate != new_http_health_check.negate
        )
        or module.params.get('targets') is not None
        and new_targets != existing_targets
    )


def _get_object_list(module, client):
    return ionoscloud.TargetGroupsApi(client).targetgroups_get(depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('target_group')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)

    if targets:
        targets = list(map(lambda x: get_target(x), targets))

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        algorithm = existing_object.properties.algorithm if algorithm is None else algorithm
        protocol = existing_object.properties.protocol if protocol is None else protocol
        targets = existing_object.properties.targets if targets is None else targets
        health_check = existing_object.properties.health_check if health_check is None else health_check
        http_health_check = existing_object.properties.http_health_check if http_health_check is None else http_health_check

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    target_groups_api = ionoscloud.TargetGroupsApi(client)
    
    target_group = TargetGroup(properties=TargetGroupProperties(
        name=name, algorithm=algorithm, protocol=protocol,
        targets=targets, health_check=health_check,
        http_health_check=http_health_check,
    ))

    try:
        response, _, headers = target_groups_api.targetgroups_post_with_http_info(target_group)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to create the new Target Group: %s" % to_native(e))
    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)


    if targets:
        targets = list(map(lambda x: get_target(x), targets))


    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    target_groups_api = ionoscloud.TargetGroupsApi(client)
    
    target_group_properties = TargetGroupProperties(
        name=name, algorithm=algorithm, protocol=protocol,
        targets=targets, health_check=health_check,
        http_health_check=http_health_check,
    )

    try:
        response, _, headers = target_groups_api.targetgroups_patch_with_http_info(
            existing_object.id, target_group_properties,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the Target Group: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    target_groups_api = ionoscloud.TargetGroupsApi(client)

    try:
        _, _, headers = target_groups_api.target_groups_delete_with_http_info(existing_object.id)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the Target Group: %s" % to_native(e))


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
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))



if __name__ == '__main__':
    main()
