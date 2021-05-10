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
    from ionoscloud.models import NatGatewayRule, NatGatewayRuleProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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
        if nat_gateway_rule_id:
            response = nat_gateway_server.datacenters_natgateways_rules_delete_with_http_info(datacenter_id,
                                                                                              nat_gateway_id,
                                                                                              nat_gateway_rule_id)
            (nat_gateway_rule_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            nat_gateway_rules = nat_gateway_server.datacenters_natgateways_rules_get(datacenter_id=datacenter_id,
                                                                                     nat_gateway_id=nat_gateway_id,
                                                                                     depth=2)
            for rule in nat_gateway_rules.items:
                if name == rule.properties.name:
                    nat_gateway_rule_id = rule.id
                    response = nat_gateway_server.datacenters_natgateways_rules_delete_with_http_info(datacenter_id,
                                                                                                      nat_gateway_id,
                                                                                                      nat_gateway_rule_id)
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            type=dict(type='str'),
            protocol=dict(type='str'),
            source_subnet=dict(type='str'),
            public_ip=dict(type='str'),
            target_subnet=dict(type='str'),
            datacenter_id=dict(type='str'),
            nat_gateway_id=dict(type='str'),
            nat_gateway_rule_id=dict(type='str'),
            target_port_range=dict(
                type='dict',
                start=dict(type='int'),
                end=dict(type='int')
            ),
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

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new NAT Gateway Rule')
            if not module.params.get('source_subnet'):
                module.fail_json(msg='source_subnet parameter is required for a new NAT Gateway Rule')
            if not module.params.get('public_ip'):
                module.fail_json(msg='public_ip parameter is required for a new NAT Gateway Rule')
            if not module.params.get('nat_gateway_id'):
                module.fail_json(msg='nat_gateway_id parameter is required for a new NAT Gateway Rule')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a new NAT Gateway Rule')

            try:
                (nat_gateway_rule_dict) = create_nat_gateway_rule(module, api_client)
                module.exit_json(**nat_gateway_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway Rule state: %s' % to_native(e))

        elif state == 'update':
            if not (module.params.get('name') or module.params.get('nat_gateway_id')):
                module.fail_json(
                    msg='name parameter or nat_gateway_id parameter are required for updating a NAT Gateway Rule.')
            if not module.params.get('nat_gateway_rule_id'):
                module.fail_json(msg='nat_gateway_rule_id parameter is required for updating a NAT Gateway Rule.')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a NAT Gateway Rule.')
            try:
                (nat_gateway_rule_dict) = update_nat_gateway_rule(module, api_client)
                module.exit_json(**nat_gateway_rule_dict)
            except Exception as e:
                module.fail_json(msg='failed to update the NAT Gateway: %s' % to_native(e))

        elif state == 'absent':
            if not (module.params.get('name') or module.params.get('nat_gateway_id')):
                module.fail_json(
                    msg='name parameter or nat_gateway_id parameter are required for deleting a NAT Gateway Rule.')
            if not module.params.get('nat_gateway_rule_id'):
                module.fail_json(msg='nat_gateway_rule_id parameter is required for deleting a NAT Gateway Rule.')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for deleting a NAT Gateway Rule.')

            try:
                (result) = remove_nat_gateway_rule(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway Rule state: %s' % to_native(e))


if __name__ == '__main__':
    main()
