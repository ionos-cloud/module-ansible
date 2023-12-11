#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from asyncore import read
from xxlimited import new

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import (
        ApplicationLoadBalancerForwardingRule, ApplicationLoadBalancerForwardingRuleProperties,
        ApplicationLoadBalancerHttpRule, ApplicationLoadBalancerHttpRuleCondition,
    )
    from ionoscloud.rest import ApiException
    import ionoscloud_cert_manager
    from ionoscloud_cert_manager import __version__ as certificate_manager_sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource, get_resource_id, _get_request_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


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


OPTIONS = { **{
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
}, **get_default_options(STATES) }


DOCUMENTATION = '''
---
module: application_load_balancer_rule
short_description: Create or destroy a Ionos Cloud Application Loadbalancer Forwarding rule.
description:
     - This is a simple module that supports creating or removing Application Loadbalancer Forwarding rules.
version_added: "2.0"
options:
    algorithm:
        description:
        - Balancing algorithm.
        required: false
    allow_replace:
        default: false
        description:
        - Boolean indincating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    application_load_balancer:
        description:
        - The ID or name of the Application Loadbalancer.
        required: true
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    client_timeout:
        description:
        - The maximum time in milliseconds to wait for the client to acknowledge or send
            data; default is 50,000 (50 seconds).
        required: false
    datacenter:
        description:
        - The ID or name of the datacenter.
        required: true
    forwarding_rule:
        description:
        - The ID or name of the Application Loadbalancer forwarding rule.
        required: false
    http_rules:
        description:
        - An array of items in the collection. The original order of rules is preserved
            during processing, except that rules of the 'FORWARD' type are processed after
            the rules with other defined actions. The relative order of the 'FORWARD'
            type rules is also preserved during the processing.
        elements: dict
        required: false
    listener_ip:
        description:
        - The listening (inbound) IP.
        required: false
    listener_port:
        description:
        - The listening (inbound) port number; the valid range is 1 to 65535.
        required: false
    name:
        description:
        - The name of the Application Load Balancer forwarding rule.
        required: false
    new_server_certificates:
        description:
        - An array of dict with information used to uploade new certificates and add them
            to the forwarding rule.A dict should contain 'certificate_file', 'private_key_file',
            'certificate_chain_file'(optional), 'certificate_name' as keys.File paths
            should be absolute.
        elements: dict
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    protocol:
        description:
        - The balancing protocol.
        required: false
    server_certificates:
        description:
        - Array of items in the collection.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
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

EXAMPLES = """
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
  

  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: "RuleName - UPDATED"
      state: absent
"""


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


class ForwardingRuleModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdk = ionoscloud
        self.user_agent = USER_AGENT


    def _should_replace_object(self, existing_object):
        return False


    def _should_update_object(self, existing_object):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('protocol') is not None
            and existing_object.properties.protocol != self.module.params.get('protocol')
            or self.module.params.get('listener_ip') is not None
            and existing_object.properties.listener_ip != self.module.params.get('listener_ip')
            or self.module.params.get('listener_port') is not None
            and existing_object.properties.listener_port != self.module.params.get('listener_port')
            or self.module.params.get('client_timeout') is not None
            and existing_object.properties.client_timeout != self.module.params.get('client_timeout')
            or self.module.params.get('new_server_certificates') is not None
            or self.module.params.get('http_rules') is not None
            or self.module.params.get('server_certificates') is not None
            and sorted(existing_object.properties.server_certificates) != sorted(self.module.params.get('server_certificates'))
        )


    def _get_object_list(self, client):
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        application_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('application_load_balancer'),
        )

        return ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_forwardingrules_get(
            datacenter_id, application_load_balancer_id, depth=1,
        )


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('forwarding_rule')


    def _create_object(self, client, certificate_manager_client, existing_object=None):
        name = self.module.params.get('name')
        protocol = self.module.params.get('protocol')
        listener_ip = self.module.params.get('listener_ip')
        listener_port = self.module.params.get('listener_port')
        client_timeout = self.module.params.get('client_timeout')
        server_certificates = get_server_certificates(self.module, certificate_manager_client)
        http_rules = self.module.params.get('http_rules')
        http_rules = list(map(lambda x: get_http_rule_object(x), http_rules)) if http_rules else None
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        application_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('application_load_balancer'),
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
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Application Loadbalancer Rule: %s" % to_native(e))
        return response

    def _update_object(self, client, certificate_manager_client, existing_object):
        name = self.module.params.get('name')
        protocol = self.module.params.get('protocol')
        listener_ip = self.module.params.get('listener_ip')
        listener_port = self.module.params.get('listener_port')
        client_timeout = self.module.params.get('client_timeout')
        server_certificates = get_server_certificates(self.module, certificate_manager_client)
        http_rules = self.module.params.get('http_rules')
        http_rules = list(map(lambda x: get_http_rule_object(x), http_rules)) if http_rules else None
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        application_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('application_load_balancer'),
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

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Application Loadbalancer Rule: %s" % to_native(e))

    def _remove_object(self, client, existing_object):
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        application_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('application_load_balancer'),
        )

        albs_api = ionoscloud.ApplicationLoadBalancersApi(client)

        try:
            _, _, headers = albs_api.datacenters_applicationloadbalancers_forwardingrules_delete_with_http_info(
                datacenter_id, application_load_balancer_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Application Loadbalancer Rule: %s" % to_native(e))

    def update_replace_object(self, client, certificate_manager_api_client, existing_object):
        module = self.module
        if self._should_replace_object(existing_object):

            if not module.params.get('allow_replace'):
                module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

            new_object = self._create_object(client, certificate_manager_api_client, existing_object).to_dict()
            self._remove_object(client, existing_object)
            return {
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: new_object,
            }
        if self._should_update_object(existing_object):
            # Update
            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                self.returned_key: self._update_object(client, certificate_manager_api_client, existing_object).to_dict()
            }

        # No action
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            self.returned_key: existing_object.to_dict()
        }


    def present_object(self, client, certificate_manager_api_client):
        existing_object = get_resource(self.module, self._get_object_list(client), self._get_object_name())

        if existing_object:
            return self.update_replace_object(client, certificate_manager_api_client, existing_object)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            self.returned_key: self._create_object(client, certificate_manager_api_client).to_dict()
        }


    def update_object(self, client, certificate_manager_api_client):
        object_name = self._get_object_name()
        object_list = self._get_object_list(client)

        existing_object = get_resource(self.module, object_list, self._get_object_identifier())

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        existing_object_id_by_new_name = get_resource_id(self.module, object_list, object_name)

        if (
            existing_object.id is not None
            and existing_object_id_by_new_name is not None
            and existing_object_id_by_new_name != existing_object.id
        ):
            self.module.fail_json(
                msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                    self.object_name, object_name,
                ),
            )

        return self.update_replace_object(client, certificate_manager_api_client, existing_object)


    def absent_object(self, client):
        existing_object = get_resource(self.module, self._get_object_list(client), self._get_object_identifier())

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        self._remove_object(client, existing_object)

        return {
            'action': 'delete',
            'changed': True,
            'id': existing_object.id,
        }


if __name__ == '__main__':
    ionos_module = ForwardingRuleModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()

