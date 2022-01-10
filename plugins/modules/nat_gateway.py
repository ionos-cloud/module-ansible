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
    from ionoscloud.models import NatGateway, NatGatewayProperties, NatGatewayLanProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def _update_nat_gateway(module, client, nat_gateway_server, datacenter_id, nat_gateway_id, nat_gateway_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nat_gateway_server.datacenters_natgateways_patch_with_http_info(datacenter_id, nat_gateway_id,
                                                                               nat_gateway_properties)
    (nat_gateway_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return nat_gateway_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nat_gateway(module, client):
    """
    Creates a NAT Gateway

    This will create a new NAT Gateway in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The NAT Gateway ID if a new NAT Gateway was created.
    """
    name = module.params.get('name')
    public_ips = module.params.get('public_ips')
    datacenter_id = module.params.get('datacenter_id')
    lans = module.params.get('lans')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    nat_gateways = nat_gateway_server.datacenters_natgateways_get(datacenter_id=datacenter_id, depth=2)
    nat_gateway_response = None

    for nat_gateway in nat_gateways.items:
        if name == nat_gateway.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'nat_gateway': nat_gateway.to_dict()
            }

    nat_gateway_lans = []
    if lans:
        for lan in lans:
            nat_gateway_lans.append(NatGatewayLanProperties(id=lan['id'], gateway_ips=lan['gateway_ips']))

    nat_gateway_properties = NatGatewayProperties(name=name, public_ips=public_ips, lans=nat_gateway_lans)
    nat_gateway = NatGateway(properties=nat_gateway_properties)

    try:
        response = nat_gateway_server.datacenters_natgateways_post_with_http_info(datacenter_id, nat_gateway)
        (nat_gateway_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new NAT Gateway: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'nat_gateway': nat_gateway_response.to_dict()
    }


def update_nat_gateway(module, client):
    """
    Updates a NAT Gateway.

    This will update a NAT Gateway.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway was updated, false otherwise
    """
    name = module.params.get('name')
    public_ips = module.params.get('public_ips')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')
    lans = module.params.get('lans')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False
    nat_gateway_response = None

    if nat_gateway_id:
        nat_gateway_properties = NatGatewayProperties(name=name, public_ips=public_ips, lans=lans)
        nat_gateway_response = _update_nat_gateway(module, client, nat_gateway_server, datacenter_id, nat_gateway_id,
                                                   nat_gateway_properties)
        changed = True

    else:
        nat_gateways = nat_gateway_server.datacenters_natgateways_get(datacenter_id=datacenter_id, depth=2)
        for n in nat_gateways.items:
            if name == n.properties.name:
                nat_gateway_properties = NatGatewayProperties(name=name, public_ips=public_ips, lans=lans)
                nat_gateway_response = _update_nat_gateway(module, client, nat_gateway_server, datacenter_id, n.id,
                                                           nat_gateway_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the nat gateway: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'nat_gateway': nat_gateway_response.to_dict()
    }


def remove_nat_gateway(module, client):
    """
    Removes a NAT Gateway.

    This will remove a NAT Gateway.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False

    try:
        nat_gateway_list = nat_gateway_server.datacenters_natgateways_get(datacenter_id=datacenter_id, depth=5)
        if nat_gateway_id:
            nat_gateway = _get_resource(nat_gateway_list, nat_gateway_id)
        else:
            nat_gateway = _get_resource(nat_gateway_list, name)

        if not nat_gateway:
            module.exit_json(changed=False)

        response = nat_gateway_server.datacenters_natgateways_delete_with_http_info(datacenter_id, nat_gateway_id)
        (nat_gateway_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the NAT Gateway: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': nat_gateway_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            datacenter_id=dict(type='str'),
            nat_gateway_id=dict(type='str'),
            public_ips=dict(type='list', default=None),
            lans=dict(type='list', default=None),
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
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
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

    state = module.params.get('state')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    configuration = ionoscloud.Configuration(**conf)

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a deleting a NAT Gateway')
            if not (module.params.get('name') or module.params.get('nat_gateway_id')):
                module.fail_json(msg='name parameter or nat_gateway_id parameter are required deleting a NAT Gateway.')
            try:
                (result) = remove_nat_gateway(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new NAT Gateway')
            if not module.params.get('public_ips'):
                module.fail_json(msg='public_ips parameter is required for a new NAT Gateway')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a new NAT Gateway')

            try:
                (nat_gateway_dict) = create_nat_gateway(module, api_client)
                module.exit_json(**nat_gateway_dict)
            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway state: %s' % to_native(e))

        elif state == 'update':
            if not (module.params.get('name') or module.params.get('nat_gateway_id')):
                module.fail_json(
                    msg='name parameter or nat_gateway_id parameter are required for updating a NAT Gateway.')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a NAT Gateway.')
            try:
                (nat_gateway_dict_array) = update_nat_gateway(module, api_client)
                module.exit_json(**nat_gateway_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update the NAT Gateway: %s' % to_native(e))


if __name__ == '__main__':
    main()
