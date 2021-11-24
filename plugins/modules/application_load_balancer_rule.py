#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import ApplicationLoadBalancer, ApplicationLoadBalancerProperties, \
        ApplicationLoadBalancerForwardingRule, \
        ApplicationLoadBalancerForwardingRuleProperties, ApplicationLoadBalancerHttpRule, \
        ApplicationLoadBalancerHttpRuleCondition, ApplicationLoadBalancerForwardingRuleHealthCheck
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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


def get_health_check(health_check):
    health_check_object = ApplicationLoadBalancerForwardingRuleHealthCheck()
    if health_check['client_timeout']:
        health_check_object.client_timeout = health_check['client_timeout']
    return health_check_object


def create_alb_forwarding_rule(module, client):
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
    health_check = module.params.get('health_check')
    server_certificates = module.params.get('server_certificates')
    http_rules = module.params.get('http_rules')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    http_rules_list = []
    if http_rules:
        for rule in http_rules:
            http_rules_list.append(get_http_rule(rule))

    if health_check:
        health_check = get_health_check(health_check)

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    alb_forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
        datacenter_id=datacenter_id,
        application_load_balancer_id=application_load_balancer_id,
        depth=2)
    alb_forwarding_rule_response = None

    for forwarding_rule in alb_forwarding_rules.items:
        if name == forwarding_rule.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'forwarding_rule': forwarding_rule.to_dict()
            }

    alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(name=name, protocol=protocol,
                                                                                     listener_ip=listener_ip,
                                                                                     listener_port=listener_port,
                                                                                     health_check=health_check,
                                                                                     server_certificates=server_certificates,
                                                                                     http_rules=http_rules_list)
    alb_forwarding_rule = ApplicationLoadBalancerForwardingRule(properties=alb_forwarding_rule_properties)

    try:
        response = alb_server.datacenters_applicationloadbalancers_forwardingrules_post_with_http_info(datacenter_id,
                                                                                                       application_load_balancer_id,
                                                                                                       alb_forwarding_rule)
        (alb_forwarding_rule_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Application Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'forwarding_rule': alb_forwarding_rule_response.to_dict()
    }


def update_alb_forwarding_rule(module, client):
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
    health_check = module.params.get('health_check')
    server_certificates = module.params.get('server_certificates')
    http_rules = module.params.get('http_rules')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')
    forwarding_rule_id = module.params.get('forwarding_rule_id')

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    changed = False
    forwarding_rule_response = None

    if health_check:
        health_check = get_health_check(health_check)

    http_rules_list = []
    if http_rules:
        for rule in http_rules:
            http_rules_list.append(get_http_rule(rule))

    if forwarding_rule_id:
        alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(name=name, protocol=protocol,
                                                                                         listener_ip=listener_ip,
                                                                                         listener_port=listener_port,
                                                                                         health_check=health_check,
                                                                                         server_certificates=server_certificates,
                                                                                         http_rules=http_rules_list)
        forwarding_rule_response = _update_alb_forwarding_rule(module, client, alb_server, datacenter_id,
                                                               application_load_balancer_id, forwarding_rule_id,
                                                               alb_forwarding_rule_properties)
        changed = True

    else:
        forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
            datacenter_id=datacenter_id,
            application_load_balancer_id=application_load_balancer_id,
            depth=2)
        for rule in forwarding_rules.items:
            if name == rule.properties.name:
                alb_forwarding_rule_properties = ApplicationLoadBalancerForwardingRuleProperties(name=name,
                                                                                                 protocol=protocol,
                                                                                                 listener_ip=listener_ip,
                                                                                                 listener_port=listener_port,
                                                                                                 health_check=health_check,
                                                                                                 server_certificates=server_certificates,
                                                                                                 http_rules=http_rules_list)
                forwarding_rule_response = _update_alb_forwarding_rule(module, client, alb_server, datacenter_id,
                                                                       application_load_balancer_id, rule.id,
                                                                       alb_forwarding_rule_properties)
                changed = True

    if not changed:
        module.fail_json(
            msg="failed to update the Application Load Balancer Forwarding Rule: The resource does not exist")

    return {
        'changed': changed,
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
    changed = False

    try:
        if forwarding_rule_id:
            response = alb_server.datacenters_applicationloadbalancers_forwardingrules_delete_with_http_info(
                datacenter_id,
                application_load_balancer_id,
                forwarding_rule_id)
            (forwarding_rule_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            forwarding_rules = alb_server.datacenters_applicationloadbalancers_forwardingrules_get(
                datacenter_id=datacenter_id,
                application_load_balancer_id=application_load_balancer_id,
                depth=2)
            for rule in forwarding_rules.items:
                if name == rule.properties.name:
                    forwarding_rule_id = rule.id
                    response = alb_server.datacenters_applicationloadbalancers_forwardingrules_delete_with_http_info(
                        datacenter_id,
                        application_load_balancer_id,
                        forwarding_rule_id)
                    (forwarding_rule_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Application Load Balancer Forwarding Rule: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': forwarding_rule_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            algorithm=dict(type='str'),
            protocol=dict(type='str'),
            listener_ip=dict(type='str'),
            listener_port=dict(type='str'),
            health_check=dict(type='dict',
                              client_timeout=dict(type='str'),
                              connect_timeout=dict(type='str'),
                              target_timeout=dict(type='str'),
                              retries=dict(type='str')
                              ),
            http_rules=dict(type='list'),
            server_certificates=dict(type='list'),
            datacenter_id=dict(type='str'),
            forwarding_rule_id=dict(type='str'),
            application_load_balancer_id=dict(type='str'),
            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    state = module.params.get('state')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not module.params.get('datacenter_id'):
                module.fail_json(
                    msg='datacenter_id parameter is required for deleting a Application Load Balancer Forwarding Rule')
            if not module.params.get('application_load_balancer_id'):
                module.fail_json(
                    msg='application_load_balancer_id parameter is required for deleting a Application Load Balancer Forwarding Rule')
            if not (module.params.get('name') or module.params.get('forwarding_rule_id')):
                module.fail_json(
                    msg='name parameter or forwarding_rule_id parameter are required for deleting a Application Load Balancer Forwarding Rule.')
            try:
                (result) = remove_alb_forwarding_rule(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to delete the Application Load Balancer: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Application Load Balancer Forwarding Rule')
            if not module.params.get('protocol'):
                module.fail_json(
                    msg='protocol parameter is required for a new Application Load Balancer Forwarding Rule')
            if not module.params.get('listener_ip'):
                module.fail_json(
                    msg='listener_ip parameter is required for a new Application Load Balancer Forwarding Rule')
            if not module.params.get('listener_port'):
                module.fail_json(
                    msg='listener_port parameter is required for a new Application Load Balancer Forwarding Rule')
            if not module.params.get('datacenter_id'):
                module.fail_json(
                    msg='datacenter_id parameter is required for a new Application Load Balancer Forwarding Rule')
            if not module.params.get('application_load_balancer_id'):
                module.fail_json(
                    msg='application_load_balancer_id parameter is required for a new Application Load Balancer Forwarding Rule')

            try:
                (alb_forwarding_rule_dict) = create_alb_forwarding_rule(module, api_client)
                module.exit_json(**alb_forwarding_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Application Load Balancer Forwarding Rule state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(
                    msg='datacenter_id parameter is required for updating a Application Load Balancer Forwarding Rule')
            if not module.params.get('application_load_balancer_id'):
                module.fail_json(
                    msg='application_load_balancer_id parameter is required for updating a Application Load Balancer Forwarding Rule')
            if not (module.params.get('name') or module.params.get('forwarding_rule_id')):
                module.fail_json(
                    msg='name parameter or forwarding_rule_id parameter are required deleting a Application Load Balancer Forwarding Rule.')
            try:
                (alb_dict) = update_alb_forwarding_rule(module, api_client)
                module.exit_json(**alb_dict)
            except Exception as e:
                module.fail_json(
                    msg='failed to update the Application Load Balancer Forwarding Rule: %s' % to_native(e))


if __name__ == '__main__':
    main()
