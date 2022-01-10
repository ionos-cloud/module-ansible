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
    from ionoscloud.models import FlowLog, FlowLogProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _update_nat_gateway_flowlog(module, client, nat_gateway_server, datacenter_id, nat_gateway_id, flowlog_id,
                                flowlog_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nat_gateway_server.datacenters_natgateways_flowlogs_patch_with_http_info(datacenter_id, nat_gateway_id,
                                                                                        flowlog_id,
                                                                                        flowlog_properties)
    (flowlog_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return flowlog_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nat_gateway_flowlog(module, client):
    """
    Creates a NAT Gateway Flowlog

    This will create a new NAT Gateway Flowlog in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The NAT Gateway Flowlog ID if a new NAT Gateway Flowlog was created.
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    nat_gateway_flowlogs = nat_gateway_server.datacenters_natgateways_flowlogs_get(datacenter_id=datacenter_id,
                                                                                   nat_gateway_id=nat_gateway_id,
                                                                                   depth=2)
    nat_gateway_flowlog_response = None

    for flowlog in nat_gateway_flowlogs.items:
        if name == flowlog.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'flowlog': flowlog.to_dict()
            }

    nat_gateway_flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
    nat_gateway_flowlog = FlowLog(properties=nat_gateway_flowlog_properties)

    try:
        response = nat_gateway_server.datacenters_natgateways_flowlogs_post_with_http_info(datacenter_id,
                                                                                           nat_gateway_id,
                                                                                           nat_gateway_flowlog)
        (nat_gateway_flowlog_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new NAT Gateway Flowlog: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'flowlog': nat_gateway_flowlog_response.to_dict()
    }


def update_nat_gateway_flowlog(module, client):
    """
    Updates a NAT Gateway Flowlog.

    This will update a NAT Gateway Flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway Flowlog was updated, false otherwise
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')
    flowlog_id = module.params.get('flowlog_id')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False
    flowlog_response = None

    if flowlog_id:
        flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
        flowlog_response = _update_nat_gateway_flowlog(module, client, nat_gateway_server, datacenter_id,
                                                       nat_gateway_id, flowlog_id,
                                                       flowlog_properties)
        changed = True

    else:
        flowlogs = nat_gateway_server.datacenters_natgateways_flowlogs_get(datacenter_id=datacenter_id,
                                                                           nat_gateway_id=nat_gateway_id, depth=2)
        for f in flowlogs.items:
            if name == f.properties.name:
                flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
                flowlog_response = _update_nat_gateway_flowlog(module, client, nat_gateway_server, datacenter_id,
                                                               nat_gateway_id, f.id,
                                                               flowlog_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the NAT Gateway Flowlog: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'flowlog': flowlog_response.to_dict()
    }


def remove_nat_gateway_flowlog(module, client):
    """
    Removes a NAT Gateway Flowlog.

    This will remove a NAT Gateway Flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the NAT Gateway Flowlog was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    nat_gateway_id = module.params.get('nat_gateway_id')
    flowlog_id = module.params.get('flowlog_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nat_gateway_server = ionoscloud.NATGatewaysApi(client)
    changed = False

    try:
        if flowlog_id:
            response = nat_gateway_server.datacenters_natgateways_flowlogs_delete_with_http_info(datacenter_id, nat_gateway_id, flowlog_id)
            (flowlog_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            flowlogs = nat_gateway_server.datacenters_natgateways_flowlogs_get(datacenter_id=datacenter_id, nat_gateway_id=nat_gateway_id, depth=2)
            for f in flowlogs.items:
                if name == f.properties.name:
                    flowlog_id = f.id
                    response = nat_gateway_server.datacenters_natgateways_flowlogs_delete_with_http_info(datacenter_id, nat_gateway_id, flowlog_id)
                    (flowlog_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the NAT Gateway Flowlog: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': flowlog_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            action=dict(type='str'),
            direction=dict(type='str'),
            bucket=dict(type='str'),
            datacenter_id=dict(type='str'),
            server_id=dict(type='str'),
            flowlog_id=dict(type='str'),
            nat_gateway_id=dict(type='str'),
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
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

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
            if not (module.params.get('name') or module.params.get('nat_gateway_id')):
                module.fail_json(
                    msg='name parameter or nat_gateway_id parameter are required deleting a NAT Gateway Flowlog.')
            try:
                (result) = remove_nat_gateway_flowlog(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new NAT Gateway Flowlog')
            if not module.params.get('action'):
                module.fail_json(msg='action parameter is required for a new NAT Gateway Flowlog')
            if not module.params.get('direction'):
                module.fail_json(msg='direction parameter is required for a new NAT Gateway Flowlog')
            if not module.params.get('bucket'):
                module.fail_json(msg='bucket parameter is required for a new NAT Gateway Flowlog')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a new NAT Gateway Flowlog')
            if not module.params.get('nat_gateway_id'):
                module.fail_json(msg='nat_gateway_id parameter is required for a new NAT Gateway Flowlog')

            try:
                (nat_gateway_flowlog_dict) = create_nat_gateway_flowlog(module, api_client)
                module.exit_json(**nat_gateway_flowlog_dict)
            except Exception as e:
                module.fail_json(msg='failed to set NAT Gateway Flowlog state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a NAT Gateway Flowlog')
            if not module.params.get('nat_gateway_id'):
                module.fail_json(msg='nat_gateway_id parameter is required for updating a NAT Gateway Flowlog')
            if not module.params.get('flowlog_id'):
                module.fail_json(msg='flowlog_id parameter is required for updating a NAT Gateway Flowlog')
            try:
                (nat_gateway_dict_array) = update_nat_gateway_flowlog(module, api_client)
                module.exit_json(**nat_gateway_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update the NAT Gateway Flowlog: %s' % to_native(e))


if __name__ == '__main__':
    main()
