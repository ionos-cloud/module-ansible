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
    from ionoscloud.models import NatGatewayRule, NatGatewayRuleProperties
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
DOC_DIRECTORY = 'natgateway'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'NAT Gateway rule'

OPTIONS = {
    'name': {
        'description': ['The name of the NAT Gateway rule.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'type': {
        'description': ['Type of the NAT Gateway rule.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ["Protocol of the NAT Gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set."],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'source_subnet': {
        'description': [
            'Source subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this '
            'translation rule applies to based on the packets source IP address.',
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'public_ip': {
        'description': [
            'Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing '
            'packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource.',
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'target_subnet': {
        'description': [
            'Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets '
            'this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address.',
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'target_port_range': {
        'description': [
            'Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation '
            'rule applies to based on destination port. If none is provided, rule will match any port.',
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'datacenter_id': {
        'description': ['The ID of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway_id': {
        'description': ['The ID of the NAT Gateway.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway_rule_id': {
        'description': ['The ID of the NAT Gateway rule.'],
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
module: nat_gateway_rule
short_description: Create or destroy a Ionos Cloud NATGateway rule.
description:
     - This is a simple module that supports creating or removing NATGateway rules.
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
  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      name: "{{ name }}"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: "{{ ipblock_response.ipblock.properties.ips[0] }}"
      wait: true
    register: nat_gateway_rule_response
  ''',
  'update' : '''
  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
      public_ip: "{{ ipblock_response.ipblock.properties.ips[1] }}"
      name: "{{ name }} - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  ''',
  'absent' : '''
  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
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



def _update_nat_gateway_rule(module, client, nat_gateway_server, datacenter_id, nat_gateway_id, nat_gateway_rule_id,
                             nat_gateway_rule_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    response = nat_gateway_server.datacenters_natgateways_rules_patch_with_http_info(datacenter_id, nat_gateway_id,
                                                                                     nat_gateway_rule_id,
                                                                                     nat_gateway_rule_properties)
    (nat_gateway_rule_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return nat_gateway_rule_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nat_gateway_rule(module, client):
    """
    Creates a NAT Gateway Rule

    This will create a new NAT Gateway Rule in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The NAT Gateway Rule ID if a new NAT Gateway Rule was created.
    """
    name = module.params.get('name')
    type = module.params.get('type')
    protocol = module.params.get('protocol')
    source_subnet = module.params.get('source_subnet')
    public_ip = module.params.get('public_ip')
    target_subnet = module.params.get('target_subnet')
    target_port_range = module.params.get('target_port_range')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    nat_gateway_rules = nat_gateway_server.datacenters_natgateways_rules_get(datacenter_id=datacenter_id,
                                                                             nat_gateway_id=nat_gateway_id, depth=2)

    for rule in nat_gateway_rules.items:
        if name == rule.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'nat_gateway_rule': rule.to_dict()
            }

    nat_gateway_rule_properties = NatGatewayRuleProperties(name=name, type=type, protocol=protocol,
                                                           source_subnet=source_subnet, public_ip=public_ip,
                                                           target_subnet=target_subnet,
                                                           target_port_range=target_port_range)
    nat_gateway_rule = NatGatewayRule(properties=nat_gateway_rule_properties)

    try:
        response = nat_gateway_server.datacenters_natgateways_rules_post_with_http_info(datacenter_id, nat_gateway_id,
                                                                                        nat_gateway_rule)
        (nat_gateway_rule_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'nat_gateway_rule': nat_gateway_rule_response.to_dict()
        }

    except ApiException as e:
        module.fail_json(msg="failed to create the new NAT Gateway Rule: %s" % to_native(e))


def update_nat_gateway_rule(module, client):
    """
    Updates a NAT Gateway Rule.

    This will update a NAT Gateway Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway Rule was updated, false otherwise
    """
    name = module.params.get('name')
    type = module.params.get('type')
    protocol = module.params.get('protocol')
    source_subnet = module.params.get('source_subnet')
    public_ip = module.params.get('public_ip')
    target_subnet = module.params.get('target_subnet')
    target_port_range = module.params.get('target_port_range')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')
    nat_gateway_rule_id = module.params.get('nat_gateway_rule_id')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False
    nat_gateway_rule_response = None

    if nat_gateway_rule_id:
        nat_gateway_rule_properties = NatGatewayRuleProperties(name=name, type=type, protocol=protocol,
                                                               source_subnet=source_subnet, public_ip=public_ip,
                                                               target_subnet=target_subnet,
                                                               target_port_range=target_port_range)
        nat_gateway_rule_response = _update_nat_gateway_rule(module, client, nat_gateway_server, datacenter_id,
                                                             nat_gateway_id, nat_gateway_rule_id,
                                                             nat_gateway_rule_properties)
        changed = True

    else:
        nat_gateway_rules = nat_gateway_server.datacenters_natgateways_rules_get(datacenter_id=datacenter_id,
                                                                                 nat_gateway_id=nat_gateway_id, depth=2)
        for rule in nat_gateway_rules.items:
            if name == rule.properties.name:
                nat_gateway_rule_properties = NatGatewayRuleProperties(name=name, type=type, protocol=protocol,
                                                                       source_subnet=source_subnet, public_ip=public_ip,
                                                                       target_subnet=target_subnet,
                                                                       target_port_range=target_port_range)
                nat_gateway_rule_response = _update_nat_gateway_rule(module, client, nat_gateway_server, datacenter_id,
                                                                     nat_gateway_id, rule.id,
                                                                     nat_gateway_rule_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the NAT Gateway Rule: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'nat_gateway_rule': nat_gateway_rule_response.to_dict()
    }


def remove_nat_gateway_rule(module, client):
    """
    Removes a NAT Gateway Rule.

    This will remove a NAT Gateway Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway Rule was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')
    nat_gateway_rule_id = module.params.get('nat_gateway_rule_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False

    try:
        nat_gateway_rule_list = nat_gateway_server.datacenters_natgateways_rules_get(datacenter_id=datacenter_id, nat_gateway_id=nat_gateway_id, depth=5)
        if nat_gateway_rule_id:
            nat_gateway_rule = _get_resource(nat_gateway_rule_list, nat_gateway_rule_id)
        else:
            nat_gateway_rule = _get_resource(nat_gateway_rule_list, name)

        if not nat_gateway_rule:
            module.exit_json(changed=False)

        response = nat_gateway_server.datacenters_natgateways_rules_delete_with_http_info(datacenter_id,
                                                                                          nat_gateway_id,
                                                                                          nat_gateway_rule)
        (nat_gateway_rule_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the NAT Gateway Rule: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': nat_gateway_rule_id
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

        if state in ['absent', 'update'] and not module.params.get('name') and not module.params.get('nat_gateway_rule_id'):
            module.fail_json(
                msg='either name or nat_gateway_rule_id parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME),
            )

        try:
            if state == 'present':
                module.exit_json(**create_nat_gateway_rule(module, api_client))
            elif state == 'update':
                module.exit_json(**update_nat_gateway_rule(module, api_client))
            elif state == 'absent':
                module.exit_json(**remove_nat_gateway_rule(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
