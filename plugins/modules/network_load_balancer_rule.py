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
        'required': ['present'],
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
    'forwarding_rule_id': {
        'description': ['The ID of the Network Loadbalancer forwarding rule.'],
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
       This module has a dependency on ionos-cloud >= 6.0.0
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
      forwarding_rule_id: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
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
      forwarding_rule_id: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def _update_nlb_forwarding_rule(module, client, nlb_server, datacenter_id, network_load_balancer_id, forwarding_rule_id,
                                forwarding_rule_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nlb_server.datacenters_networkloadbalancers_forwardingrules_patch_with_http_info(datacenter_id,
                                                                                                network_load_balancer_id,
                                                                                                forwarding_rule_id,
                                                                                                forwarding_rule_properties)
    (forwarding_rule_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return forwarding_rule_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nlb_forwarding_rule(module, client):
    """
    Creates a Network Load Balancer Forwarding Rule

    This will create a new Network Load Balancer Forwarding Rule in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Network Load Balancer Forwarding Rule ID if a new Network Load Balancer Forwarding Rule was created.
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    health_check = module.params.get('health_check')
    targets = module.params.get('targets')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_forwarding_rules = nlb_server.datacenters_networkloadbalancers_forwardingrules_get(datacenter_id=datacenter_id,
                                                                                           network_load_balancer_id=network_load_balancer_id,
                                                                                           depth=2)
    nlb_forwarding_rule_response = None

    for forwarding_rule in nlb_forwarding_rules.items:
        if name == forwarding_rule.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'forwarding_rule': forwarding_rule.to_dict()
            }

    nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(name=name, algorithm=algorithm,
                                                                                 protocol=protocol,
                                                                                 listener_ip=listener_ip,
                                                                                 listener_port=listener_port,
                                                                                 health_check=health_check,
                                                                                 targets=targets)
    nlb_forwarding_rule = NetworkLoadBalancerForwardingRule(properties=nlb_forwarding_rule_properties)

    try:
        response = nlb_server.datacenters_networkloadbalancers_forwardingrules_post_with_http_info(datacenter_id,
                                                                                                   network_load_balancer_id,
                                                                                                   nlb_forwarding_rule)
        (nlb_forwarding_rule_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Network Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'forwarding_rule': nlb_forwarding_rule_response.to_dict()
    }


def update_nlb_forwarding_rule(module, client):
    """
    Updates a Network Load Balancer Forwarding Rule.

    This will update a Network Load Balancer Forwarding Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer Forwarding Rule was updated, false otherwise
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    health_check = module.params.get('health_check')
    targets = module.params.get('targets')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    forwarding_rule_id = module.params.get('forwarding_rule_id')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False
    forwarding_rule_response = None

    if forwarding_rule_id:
        nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(name=name, algorithm=algorithm,
                                                                                     protocol=protocol,
                                                                                     listener_ip=listener_ip,
                                                                                     listener_port=listener_port,
                                                                                     health_check=health_check,
                                                                                     targets=targets)
        forwarding_rule_response = _update_nlb_forwarding_rule(module, client, nlb_server, datacenter_id,
                                                               network_load_balancer_id, forwarding_rule_id,
                                                               nlb_forwarding_rule_properties)
        changed = True

    else:
        forwarding_rules = nlb_server.datacenters_networkloadbalancers_forwardingrules_get(datacenter_id=datacenter_id,
                                                                                           network_load_balancer_id=network_load_balancer_id,
                                                                                           depth=2)
        for rule in forwarding_rules.items:
            if name == rule.properties.name:
                nlb_forwarding_rule_properties = NetworkLoadBalancerForwardingRuleProperties(name=name,
                                                                                             algorithm=algorithm,
                                                                                             protocol=protocol,
                                                                                             listener_ip=listener_ip,
                                                                                             listener_port=listener_port,
                                                                                             health_check=health_check,
                                                                                             targets=targets)
                forwarding_rule_response = _update_nlb_forwarding_rule(module, client, nlb_server, datacenter_id,
                                                                       network_load_balancer_id, rule.id,
                                                                       nlb_forwarding_rule_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Network Load Balancer Forwarding Rule: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'forwarding_rule': forwarding_rule_response.to_dict()
    }


def remove_nlb_forwarding_rule(module, client):
    """
    Removes a Network Load Balancer Forwarding Rule.

    This will remove a Network Load Balancer Forwarding Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer Forwarding Rule was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    forwarding_rule_id = module.params.get('forwarding_rule_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False

    try:
        network_load_balancer_rule_list = nlb_server.datacenters_networkloadbalancers_forwardingrules_get(datacenter_id=datacenter_id, network_load_balancer_id=network_load_balancer_id, depth=5)
        if forwarding_rule_id:
            network_load_balancer_rule = _get_resource(network_load_balancer_rule_list, forwarding_rule_id)
        else:
            network_load_balancer_rule = _get_resource(network_load_balancer_rule_list, name)

        if not network_load_balancer_rule:
            module.exit_json(changed=False)

        response = nlb_server.datacenters_networkloadbalancers_forwardingrules_delete_with_http_info(datacenter_id,
                                                                                                     network_load_balancer_id,
                                                                                                     network_load_balancer_rule)
        (forwarding_rule_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True


    except Exception as e:
        module.fail_json(
            msg="failed to delete the Network Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': forwarding_rule_id
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

        if state in ['absent', 'update'] and not module.params.get('name') and not module.params.get('forwarding_rule_id'):
            module.fail_json(msg='either name or forwarding_rule_id parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME))

        try:
            if state == 'absent':
                module.exit_json(**remove_nlb_forwarding_rule(module, api_client))
            elif state == 'present':
                module.exit_json(**create_nlb_forwarding_rule(module, api_client))
            elif state == 'update':
                module.exit_json(**update_nlb_forwarding_rule(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
