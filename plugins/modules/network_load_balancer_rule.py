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
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties, NetworkLoadBalancerForwardingRule, \
        NetworkLoadBalancerForwardingRuleProperties
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
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Network Loadbalancer forwarding rule'
RETURNED_KEY = 'forwarding_rule'

OPTIONS = {
    'name': {
        'description': ['The name of the Network Loadbalancer forwarding rule.'],
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
    'listener_ip': {
        'description': ['Listening (inbound) IP.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'listener_port': {
        'description': ['Listening (inbound) port number; valid range is 1 to 65535.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'health_check': {
        'description': ['Health check properties for Network Load Balancer forwarding rule.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'targets': {
        'description': ['Array of targets.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'datacenter_id': {
        'description': ['The ID of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'network_load_balancer_id': {
        'description': ['The ID of the Network Loadbalancer.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'forwarding_rule': {
        'description': ['The ID or name of the Network Loadbalancer forwarding rule.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
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
module: network_load_balancer_rule
short_description: Create or destroy a Ionos Cloud NetworkLoadbalancer Flowlog rule.
description:
     - This is a simple module that supports creating or removing NATGateway Flowlog rules.
       This module has a dependency on ionoscloud >= 6.0.2
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
  'present' : '''
  - name: Create Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      name: "{{ name }}"
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      targets:
        - ip: "22.231.2.2"
          port: "8080"
          weight: "123"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      wait: true
    register: nlb_forwarding_rule_response
  ''',
  'update' : '''
  - name: Update Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      forwarding_rule: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
      name: "{{ name }} - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      wait: true
      state: update
    register: nlb_forwarding_rule_update_response
  ''',
  'absent' : '''
  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      forwarding_rule: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
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


def _get_health_check(health_check_param):
    health_check = None
    if health_check_param:
        health_check = ionoscloud.models.NetworkLoadBalancerForwardingRuleHealthCheck()
        if 'client_timeout' in health_check_param:
            health_check.client_timeout = health_check_param.get('client_timeout')
        if 'connect_timeout' in health_check_param:
            health_check.connect_timeout = health_check_param.get('connect_timeout')
        if 'target_timeout' in health_check_param:
            health_check.target_timeout = health_check_param.get('target_timeout')
        if 'retries' in health_check_param:
            health_check.retries = health_check_param.get('retries')

    return health_check


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    new_health_check = _get_health_check(module.params.get('health_check'))

    def sort_func(el):
        return el['ip'], el['weigth']

    if module.params.get('targets'):
        new_targets = sorted(map(
            lambda x: { 'ip': x.ip, 'port': x.port, 'weight': x.weight },
            existing_object.properties.targets
        ), key=sort_func)
        existing_targets = sorted(module.params.get('targets'), key=sort_func)

    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('algorithm') is not None
        and existing_object.properties.algorithm != module.params.get('algorithm')
        or module.params.get('protocol') is not None
        and existing_object.properties.protocol != module.params.get('protocol')
        or module.params.get('listener_ip') is not None
        and existing_object.properties.listener_ip != module.params.get('listener_ip')
        or module.params.get('listener_port') is not None
        and existing_object.properties.listener_port != module.params.get('listener_port')
        or module.params.get('target_subnet') is not None
        and existing_object.properties.target_subnet != module.params.get('target_subnet')
        or module.params.get('target_port_range') is not None
        and existing_object.properties.target_port_range != module.params.get('target_port_range')
        or module.params.get('targets') is not None
        and new_targets != existing_targets
        or module.params.get('health_check') is not None
        and (
            existing_object.properties.health_check.client_timeout != new_health_check.client_timeout
            or existing_object.properties.health_check.connect_timeout != new_health_check.connect_timeout
            or existing_object.properties.health_check.target_timeout != new_health_check.target_timeout
            or existing_object.properties.health_check.retries != new_health_check.retries
        )
    )


def _get_object_list(module, client):
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    return ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_forwardingrules_get(
        datacenter_id, network_load_balancer_id, depth=1,
    )


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('forwarding_rule')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    health_check_param = _get_health_check(module.params.get('health_check'))
    targets = module.params.get('targets')

    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        algorithm = existing_object.properties.algorithm if algorithm is None else algorithm
        protocol = existing_object.properties.protocol if protocol is None else protocol
        listener_ip = existing_object.properties.listener_ip if listener_ip is None else listener_ip
        listener_port = existing_object.properties.listener_port if listener_port is None else listener_port
        health_check_param = existing_object.properties.health_check if health_check_param is None else health_check_param
        targets = existing_object.properties.targets if targets is None else targets

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)
    
    nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(
        name=name, algorithm=algorithm,
        protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        health_check=health_check_param,
        targets=targets,
    )
    nlb_forwarding_rule = NetworkLoadBalancerForwardingRule(properties=nlb_forwarding_rule_properties)

    try:
        response, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_post_with_http_info(
            datacenter_id, network_load_balancer_id, nlb_forwarding_rule,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to create the new Network Loadbalancer Rule: %s" % to_native(e))
    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    health_check = _get_health_check(module.params.get('health_check'))
    targets = module.params.get('targets')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)

    nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(
        name=name, algorithm=algorithm,
        protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        health_check=health_check,
        targets=targets,
    )

    try:
        response, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_patch_with_http_info(
            datacenter_id, network_load_balancer_id, existing_object.id, nlb_forwarding_rule_properties,
        )

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the Network Loadbalancer Rule: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlbs_api = ionoscloud.NetworkLoadBalancersApi(client)

    try:
        _, _, headers = nlbs_api.datacenters_networkloadbalancers_forwardingrules_delete_with_http_info(
            datacenter_id, network_load_balancer_id, existing_object.id,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the Network Loadbalancer Rule: %s" % to_native(e))


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
