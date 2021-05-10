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
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties, NetworkLoadBalancerForwardingRule, \
        NetworkLoadBalancerForwardingRuleProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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
        if forwarding_rule_id:
            response = nlb_server.datacenters_networkloadbalancers_forwardingrules_delete_with_http_info(datacenter_id,
                                                                                                         network_load_balancer_id,
                                                                                                         forwarding_rule_id)
            (forwarding_rule_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            forwarding_rules = nlb_server.datacenters_networkloadbalancers_forwardingrules_get(
                                                            datacenter_id=datacenter_id,
                                                            network_load_balancer_id=network_load_balancer_id,
                                                            depth=2)
            for rule in forwarding_rules.items:
                if name == rule.properties.name:
                    forwarding_rule_id = rule.id
                    response = nlb_server.datacenters_networkloadbalancers_forwardingrules_delete_with_http_info(
                                                            datacenter_id,
                                                            network_load_balancer_id,
                                                            forwarding_rule_id)
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
                              check_timeout=dict(type='str'),
                              connect_timeout=dict(type='str'),
                              target_timeout=dict(type='str'),
                              retries=dict(type='str')
                              ),
            targets=dict(type='list', elements='dict'),
            datacenter_id=dict(type='str'),
            forwarding_rule_id=dict(type='str'),
            network_load_balancer_id=dict(type='str'),
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
                    msg='datacenter_id parameter is required for deleting a Network Load Balancer Forwarding Rule')
            if not module.params.get('network_load_balancer_id'):
                module.fail_json(
                    msg='network_load_balancer_id parameter is required for deleting a Network Load Balancer Forwarding Rule')
            if not (module.params.get('name') or module.params.get('forwarding_rule_id')):
                module.fail_json(
                    msg='name parameter or forwarding_rule_id parameter are required for deleting a Network Load Balancer Forwarding Rule.')
            try:
                (result) = remove_nlb_forwarding_rule(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to delete the Network Load Balancer: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('algorithm'):
                module.fail_json(msg='algorithm parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('protocol'):
                module.fail_json(msg='protocol parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('listener_ip'):
                module.fail_json(
                    msg='listener_ip parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('listener_port'):
                module.fail_json(
                    msg='listener_port parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('targets'):
                module.fail_json(msg='targets parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('datacenter_id'):
                module.fail_json(
                    msg='datacenter_id parameter is required for a new Network Load Balancer Forwarding Rule')
            if not module.params.get('network_load_balancer_id'):
                module.fail_json(
                    msg='network_load_balancer_id parameter is required for a new Network Load Balancer Forwarding Rule')

            try:
                (nlb_forwarding_rule_dict) = create_nlb_forwarding_rule(module, api_client)
                module.exit_json(**nlb_forwarding_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Network Load Balancer Forwarding Rule state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(
                    msg='datacenter_id parameter is required for updating a Network Load Balancer Forwarding Rule')
            if not module.params.get('network_load_balancer_id'):
                module.fail_json(
                    msg='network_load_balancer_id parameter is required for updating a Network Load Balancer Forwarding Rule')
            if not (module.params.get('name') or module.params.get('forwarding_rule_id')):
                module.fail_json(
                    msg='name parameter or forwarding_rule_id parameter are required deleting a Network Load Balancer Forwarding Rule.')
            try:
                (nlb_dict) = update_nlb_forwarding_rule(module, api_client)
                module.exit_json(**nlb_dict)
            except Exception as e:
                module.fail_json(msg='failed to update the Network Load Balancer Forwarding Rule: %s' % to_native(e))


if __name__ == '__main__':
    main()
