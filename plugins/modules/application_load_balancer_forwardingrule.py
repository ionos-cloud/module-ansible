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
    import ionoscloud_cert_manager
    from ionoscloud_cert_manager import __version__ as certificate_manager_sdk_version
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
OBJECT_NAME = 'Application Load Balancer Forwarding Rule'
RETURNED_KEY = 'forwarding_rule'

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
        'description': ['The balancing protocol.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'listener_ip': {
        'description': ['The listening (inbound) IP.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'listener_port': {
        'description': ['The listening (inbound) port number; the valid range is 1 to 65535.'],
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
        'description': ['An array of items in the collection. The original order of rules is preserved during processing, except that rules of the \'FORWARD\' type are processed after the rules with other defined actions. The relative order of the \'FORWARD\' type rules is also preserved during the processing.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'server_certificates': {
        'description': ['Array of items in the collection.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'new_server_certificates': {
        'description': [
            'An array of dict with information used to uploade new certificates and add them to the forwarding rule.'
            "A dict should contain 'certificate_file', 'private_key_file', 'certificate_chain_file'(optional), 'certificate_name' as keys."
            'File paths should be absolute.'
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'application_load_balancer': {
        'description': ['The ID or name of the Application Loadbalancer.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'forwarding_rule': {
        'description': ['The ID or name of the Application Loadbalancer forwarding rule.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'allow_replace': {
        'description': [
            'Boolean indicating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
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
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      name: RuleName
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
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      protocol: "HTTP"
      wait: true
      state: update
    register: alb_forwarding_rule_update_response
  ''',
  'absent' : '''
  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: "RuleName - UPDATED"
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


def get_http_rule_object(http_rule):
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
    private_key_file = certificate_input.get('private_key_file')
    certificate_chain_file = certificate_input.get('certificate_chain_file')

    if not certificate_file and not private_key_file:
        return None

    return ionoscloud_cert_manager.CertificatesApi(certificate_manager_client).certificates_post(
        ionoscloud_cert_manager.CertificatePostDto(
            properties=ionoscloud_cert_manager.CertificatePostPropertiesDto(
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
        return []

    for certificate_input in new_server_certificates:
        new_certificate = create_certificate(certificate_manager_client, certificate_input)

        if new_certificate:
            new_certificates.append(new_certificate.id)

    return new_certificates


def get_server_certificates(module, certificate_manager_client):
    existing_certificates = module.params.get('server_certificates') if module.params.get('server_certificates') else []
    new_certificates = create_new_certificates(module.params.get('new_server_certificates'), certificate_manager_client)

    return new_certificates +  existing_certificates


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('protocol') is not None
        and existing_object.properties.protocol != module.params.get('protocol')
        or module.params.get('listener_ip') is not None
        and existing_object.properties.listener_ip != module.params.get('listener_ip')
        or module.params.get('listener_port') is not None
        and existing_object.properties.listener_port != module.params.get('listener_port')
        or module.params.get('client_timeout') is not None
        and existing_object.properties.client_timeout != module.params.get('client_timeout')
        or module.params.get('new_server_certificates') is not None
        or module.params.get('http_rules') is not None
        or module.params.get('server_certificates') is not None
        and sorted(existing_object.properties.server_certificates) != sorted(module.params.get('server_certificates'))
    )


def _get_object_list(module, client):
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    application_load_balancer_id = get_resource_id(
        module, 
        ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
            datacenter_id, depth=1,
        ),
        module.params.get('application_load_balancer'),
    )

    return ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_forwardingrules_get(
        datacenter_id, application_load_balancer_id, depth=1,
    )


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('forwarding_rule')


def _create_object(module, client, certificate_manager_client, existing_object=None):
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    client_timeout = module.params.get('client_timeout')
    server_certificates = get_server_certificates(module, certificate_manager_client)
    http_rules = module.params.get('http_rules')
    http_rules = list(map(lambda x: get_http_rule_object(x), http_rules)) if http_rules else None
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    application_load_balancer_id = get_resource_id(
        module, 
        ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
            datacenter_id, depth=1,
        ),
        module.params.get('application_load_balancer'),
    )

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        protocol = existing_object.properties.protocol if protocol is None else protocol
        listener_ip = existing_object.properties.listener_ip if listener_ip is None else listener_ip
        listener_port = existing_object.properties.listener_port if listener_port is None else listener_port
        client_timeout = existing_object.properties.client_timeout if client_timeout is None else client_timeout
        server_certificates = existing_object.properties.server_certificates if server_certificates is None else server_certificates
        http_rules = existing_object.properties.http_rules if http_rules is None else http_rules

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
    
    alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(
        name=name, protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        client_timeout=client_timeout,
        server_certificates=server_certificates,
        http_rules=http_rules,
    )
    alb_forwarding_rule = ApplicationLoadBalancerForwardingRule(properties=alb_forwarding_rule_properties)

    try:
        response, _, headers = albs_api.datacenters_applicationloadbalancers_forwardingrules_post_with_http_info(
            datacenter_id, application_load_balancer_id, alb_forwarding_rule,
        )
        if module.params.get('wait'):
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=int(module.params.get('wait_timeout')))
    except ApiException as e:
        module.fail_json(msg="failed to create the new Application Loadbalancer Rule: %s" % to_native(e))
    return response


def _update_object(module, client, certificate_manager_client, existing_object):
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    listener_ip = module.params.get('listener_ip')
    listener_port = module.params.get('listener_port')
    client_timeout = module.params.get('client_timeout')
    server_certificates = get_server_certificates(module, certificate_manager_client)
    http_rules = module.params.get('http_rules')
    http_rules = list(map(lambda x: get_http_rule_object(x), http_rules)) if http_rules else None
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    application_load_balancer_id = get_resource_id(
        module, 
        ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
            datacenter_id, depth=1,
        ),
        module.params.get('application_load_balancer'),
    )

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
    
    alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(
        name=name, protocol=protocol,
        listener_ip=listener_ip,
        listener_port=listener_port,
        client_timeout=client_timeout,
        server_certificates=server_certificates,
        http_rules=http_rules,
    )

    try:
        response, _, headers = albs_api.datacenters_applicationloadbalancers_forwardingrules_patch_with_http_info(
            datacenter_id, application_load_balancer_id, existing_object.id, alb_forwarding_rule_properties,
        )

        if module.params.get('wait'):
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=module.params.get('wait_timeout'))

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the Application Loadbalancer Rule: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    datacenter_id = get_resource_id(
        module, 
        ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )
    application_load_balancer_id = get_resource_id(
        module, 
        ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
            datacenter_id, depth=1,
        ),
        module.params.get('application_load_balancer'),
    )

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)

    try:
        _, _, headers = albs_api.datacenters_applicationloadbalancers_forwardingrules_delete_with_http_info(
            datacenter_id, application_load_balancer_id, existing_object.id,
        )
        if module.params.get('wait'):
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=module.params.get('wait_timeout'))
    except ApiException as e:
        module.fail_json(msg="failed to remove the Application Loadbalancer Rule: %s" % to_native(e))


def update_replace_object(module, client, certificate_manager_api_client, existing_object):
    if _should_replace_object(module, existing_object):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

        new_object = _create_object(module, client, certificate_manager_api_client, existing_object).to_dict()
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
            RETURNED_KEY: _update_object(module, client, certificate_manager_api_client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, client, certificate_manager_api_client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, client, certificate_manager_api_client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client, certificate_manager_api_client).to_dict()
    }


def update_object(module, client, certificate_manager_api_client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

    existing_object = get_resource(module, object_list, _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)
        return

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

    return update_replace_object(module, client, certificate_manager_api_client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)
        return

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

    certificate_manager_api_client = ionoscloud_cert_manager.ApiClient(get_sdk_config(module, ionoscloud_cert_manager))
    api_client = ApiClient(get_sdk_config(module, ionoscloud))

    api_client.user_agent = USER_AGENT
    certificate_manager_api_client.user_agent = CERTIFICATE_MANAGER_USER_AGENT

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'absent':
            module.exit_json(**remove_object(module, api_client))
        elif state == 'present':
            module.exit_json(**create_object(module, api_client, certificate_manager_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, api_client, certificate_manager_api_client))
    except Exception as e:
        module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
