#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from asyncore import read
from xxlimited import new

__metaclass__ = type

import re
import yaml
import copy

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import ApplicationLoadBalancer, ApplicationLoadBalancerProperties, \
        ApplicationLoadBalancerForwardingRule, \
        ApplicationLoadBalancerForwardingRuleProperties, ApplicationLoadBalancerHttpRule, \
        ApplicationLoadBalancerHttpRuleCondition
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
    import ionoscloud_certificate_manager
    from ionoscloud_certificate_manager import __version__ as certificate_manager_sdk_version
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
CERTIFICATE_MANAGER_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, certificate_manager_sdk_version)
DOC_DIRECTORY = 'applicationloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Application Loadbalancer forwarding rule'

OPTIONS = {
    'name': {
        'description': ['The name of the Application Load Balancer forwarding rule.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'algorithm': {
        'description': ['Balancing algorithm.'],
        'available': ['present', 'update'],
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
    'client_timeout': {
        'description': ['The maximum time in milliseconds to wait for the client to acknowledge or send data; default is 50,000 (50 seconds).'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'http_rules': {
        'description': [
          'An array of items in the collection. The original order of rules is perserved during processing, except for '
          'Forward-type rules are processed after the rules with other action defined. The relative order of Forward-type '
          'rules is also preserved during the processing.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'server_certificates': {
        'description': ['An array of items in the collection.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'new_server_certificates': {
        'description': [
            'An array of dict with information used to uploade new certificates and add them to the forwarding rule.'
            "A dict should contain 'certificate_file', 'private_key', 'certificate_chain_file'(optional), 'certificate_name' as keys."
            'File paths should be absolute.'
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'datacenter_id': {
        'description': ['The ID of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'application_load_balancer_id': {
        'description': ['The ID of the Application Loadbalancer.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'forwarding_rule_id': {
        'description': ['The ID of the Application Loadbalancer forwarding rule.'],
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
module: application_load_balancer_rule
short_description: Create or destroy a Ionos Cloud Application Loadbalancer Flowlog rule.
description:
     - This is a simple module that supports creating or removing Application Loadbalancer Flowlog rules.
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
  - name: Create Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }}"
      protocol: "HTTP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      client_timeout: 50
      http_rules:
        - name: "Ansible HTTP Rule"
          type : static
          response_message: "<>"
          content_type: "application/json"
          conditions:
            - type: "HEADER"
              condition: "STARTS_WITH"
              value: "Friday"

      wait: true
    register: alb_forwarding_rule_response
  ''',
  'update' : '''
  - name: Update Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      forwarding_rule_id: "{{ alb_forwarding_rule_response.forwarding_rule.id }}"
      name: "{{ name }} - UPDATED"
      protocol: "HTTP"
      wait: true
      state: update
    register: alb_forwarding_rule_update_response
  ''',
  'absent' : '''
  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      forwarding_rule_id: "{{ alb_forwarding_rule_response.forwarding_rule.id }}"
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


def _update_alb_forwarding_rule(module, client, alb_server, datacenter_id, application_load_balancer_id,
                                forwarding_rule_id,
                                forwarding_rule_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = alb_server.datacenters_applicationloadbalancers_forwardingrules_patch_with_http_info(datacenter_id,
                                                                                                    application_load_balancer_id,
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


def get_http_rule(http_rule):
    http_rule_object = ApplicationLoadBalancerHttpRule()
    if 'name' in http_rule:
        http_rule_object.name = http_rule['name']
    if 'type' in http_rule:
        http_rule_object.type = http_rule['type']
    if 'target_group' in http_rule:
        http_rule_object.target_group = http_rule['target_group']
    if 'drop_query' in http_rule:
        http_rule_object.drop_query = http_rule['drop_query']
    if 'location' in http_rule:
        http_rule_object.location = http_rule['location']
    if 'status_code' in http_rule:
        http_rule_object.status_code = http_rule['status_code']
    if 'response_message' in http_rule:
        http_rule_object.response_message = http_rule['response_message']
    if 'content_type' in http_rule:
        http_rule_object.content_type = http_rule['content_type']
    if 'conditions' in http_rule:
        for condition in http_rule['conditions']:
            http_rule_object.conditions = []
            condition_object = ApplicationLoadBalancerHttpRuleCondition()
            if 'type' in condition:
                condition_object.type = condition['type']
            if 'condition' in condition:
                condition_object.condition = condition['condition']
            if 'negate' in condition:
                condition_object.negate = condition['negate']
            if 'key' in condition:
                condition_object.key = condition['key']
            if 'value' in condition:
                condition_object.value = condition['value']
            http_rule_object.conditions.append(condition_object)
    return http_rule_object


def create_certificate(certificate_manager_client, certificate_input):
    certificate_file = certificate_input.get('certificate_file')
    private_key_file = certificate_input.get('private_key')
    certificate_chain_file = certificate_input.get('certificate_chain_file')

    if not certificate_file and not private_key_file:
        return None

    return ionoscloud_certificate_manager.CertificateApi(certificate_manager_client).add_certificate(
        ionoscloud_certificate_manager.CertificatePatchDto(
            properties=ionoscloud_certificate_manager.CertificatePostPropertiesDto(
                name=certificate_input.get('certificate_name'),
                certificate=open(certificate_file, mode='r').read(),
                certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None,
                private_key=open(private_key_file, mode='r').read(),
            )
        )
    )


def create_new_certificates(new_server_certificates, certificate_manager_client):
    new_certificates = []

    if not new_server_certificates:
        return None

    for certificate_input in new_server_certificates:
        new_certificate = create_certificate(certificate_manager_client, certificate_input)

        if new_certificate:
            new_certificates.append(new_certificate.id)

    return new_certificates if len(new_certificates) > 0 else None


def get_server_certificates(module, certificate_manager_client):
    existing_certificates = module.params.get('server_certificates')
    new_certificates = create_new_certificates(module.params.get('new_server_certificates'), certificate_manager_client)

    if new_certificates is None:
        return existing_certificates
    else:
        return new_certificates


def create_alb_forwarding_rule(module, client, certificate_manager_client):
    """
    Creates a Application Load Balancer Forwarding Rule

    This will create a new Application Load Balancer Forwarding Rule in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Application Load Balancer Forwarding Rule ID if a new Application Load Balancer Forwarding Rule was created.
    """
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    client_timeout = module.params.get('client_timeout')
    server_certificates = get_server_certificates(module, certificate_manager_client)
    http_rules = module.params.get('http_rules')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    http_rules_list = []
    if http_rules:
        for rule in http_rules:
            http_rules_list.append(get_http_rule(rule))

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    alb_forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
        datacenter_id=datacenter_id,
        application_load_balancer_id=application_load_balancer_id,
        depth=2,
    )

    existing_forwarding_rule = get_resource(module, alb_forwarding_rules, name)

    if existing_forwarding_rule:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'forwarding_rule': existing_forwarding_rule.to_dict()
        }

    alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(
        name=name, protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        client_timeout=client_timeout,
        server_certificates=server_certificates,
        http_rules=http_rules_list,
    )
    alb_forwarding_rule = ApplicationLoadBalancerForwardingRule(properties=alb_forwarding_rule_properties)

    try:
        response, _, headers = alb_server.datacenters_applicationloadbalancers_forwardingrules_post_with_http_info(
            datacenter_id, application_load_balancer_id, alb_forwarding_rule,
        )

        if wait:
            client.wait_for_completion(request_id=_get_request_id(headers['Location']), timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Application Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'forwarding_rule': response.to_dict()
    }


def update_alb_forwarding_rule(module, client, certificate_manager_client):
    """
    Updates a Application Load Balancer Forwarding Rule.

    This will update a Application Load Balancer Forwarding Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Application Load Balancer Forwarding Rule was updated, false otherwise
    """
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    client_timeout = module.params.get('client_timeout')
    server_certificates = get_server_certificates(module, certificate_manager_client)
    http_rules = module.params.get('http_rules')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')
    forwarding_rule_id = module.params.get('forwarding_rule_id')

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    forwarding_rule_response = None

    http_rules_list = []
    if http_rules:
        for rule in http_rules:
            http_rules_list.append(get_http_rule(rule))

    alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(
        name=name,
        protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        client_timeout=client_timeout,
        server_certificates=server_certificates,
        http_rules=http_rules_list,
    )

    forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
        datacenter_id=datacenter_id,
        application_load_balancer_id=application_load_balancer_id,
        depth=2,
    )
    existing_alb_fw_id_by_name = get_resource_id(module, forwarding_rules, name)

    if forwarding_rule_id is not None and existing_alb_fw_id_by_name is not None and existing_alb_fw_id_by_name != forwarding_rule_id:
            module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, name))

    forwarding_rule_id = forwarding_rule_id if forwarding_rule_id else existing_alb_fw_id_by_name

    if forwarding_rule_id:
        forwarding_rule_response = _update_alb_forwarding_rule(
            module, client, alb_server, datacenter_id,
            application_load_balancer_id, forwarding_rule_id,
            alb_forwarding_rule_properties,
        )
    else:
        module.fail_json(msg="failed to update the Application Load Balancer Forwarding Rule: The resource does not exist")

    return {
        'changed': True,
        'action': 'update',
        'failed': False,
        'forwarding_rule': forwarding_rule_response.to_dict()
    }


def remove_alb_forwarding_rule(module, client):
    """
    Removes a Application Load Balancer Forwarding Rule.

    This will remove a Application Load Balancer Forwarding Rule.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Application Load Balancer Forwarding Rule was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')
    forwarding_rule_id = module.params.get('forwarding_rule_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)


    forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
        datacenter_id=datacenter_id,
        application_load_balancer_id=application_load_balancer_id,
        depth=2,
    )
    existing_alb_fw_id_by_name = get_resource_id(module, forwarding_rules, name)

    forwarding_rule_id = forwarding_rule_id if forwarding_rule_id else existing_alb_fw_id_by_name

    try:
        _, _, headers = alb_server.datacenters_applicationloadbalancers_forwardingrules_delete_with_http_info(
            datacenter_id, application_load_balancer_id, forwarding_rule_id,
        )

        if wait:
            client.wait_for_completion(request_id=_get_request_id(headers['Location']), timeout=wait_timeout)

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Application Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': True,
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

    certificate_manager_api_client = ionoscloud_certificate_manager.ApiClient(get_sdk_config(module, ionoscloud_certificate_manager))
    api_client = ApiClient(get_sdk_config(module, ionoscloud))

    api_client.user_agent = USER_AGENT
    certificate_manager_api_client.user_agent = CERTIFICATE_MANAGER_USER_AGENT

    check_required_arguments(module, state, OBJECT_NAME)

    if state in ['absent', 'update'] and not module.params.get('name') and not module.params.get('forwarding_rule_id'):
        module.fail_json(msg='either name or forwarding_rule_id parameter is required for {object_name} state absent'.format(object_name=OBJECT_NAME))

    if state == 'absent':
        try:
            module.exit_json(**remove_alb_forwarding_rule(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to delete the Application Load Balancer: %s' % to_native(e))
    elif state == 'present':
        try:
            module.exit_json(**create_alb_forwarding_rule(module, api_client, certificate_manager_api_client))
        except Exception as e:
            module.fail_json(msg='failed to set Application Load Balancer Forwarding Rule state: %s' % to_native(e))
    elif state == 'update':
        try:
            module.exit_json(**update_alb_forwarding_rule(module, api_client, certificate_manager_api_client))
        except Exception as e:
            module.fail_json(
                msg='failed to update the Application Load Balancer Forwarding Rule: %s' % to_native(e))


if __name__ == '__main__':
    main()
