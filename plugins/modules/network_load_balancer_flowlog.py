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
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties, FlowLog, FlowLogProperties
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


def _update_nlb_flowlog(module, client, nlb_server, datacenter_id, network_load_balancer_id, flowlog_id,
                        flowlog_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nlb_server.datacenters_networkloadbalancers_flowlogs_patch_with_http_info(datacenter_id,
                                                                                         network_load_balancer_id,
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


def create_nlb_flowlog(module, client):
    """
    Creates a Network Load Balancer Flowlog

    This will create a new Network Load Balancer Flowlog in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Network Load Balancer Flowlog ID if a new Network Load Balancer Flowlog was created.
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_flowlogs = nlb_server.datacenters_networkloadbalancers_flowlogs_get(datacenter_id=datacenter_id,
                                                                            network_load_balancer_id=network_load_balancer_id,
                                                                            depth=2)
    nlb_flowlog_response = None

    for flowlog in nlb_flowlogs.items:
        if name == flowlog.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'flowlog': flowlog.to_dict()
            }

    nlb_flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
    nlb_flowlog = FlowLog(properties=nlb_flowlog_properties)

    try:
        response = nlb_server.datacenters_networkloadbalancers_flowlogs_post_with_http_info(datacenter_id,
                                                                                            network_load_balancer_id,
                                                                                            nlb_flowlog)
        (nlb_flowlog_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Network Load Balancer Flowlog: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'flowlog': nlb_flowlog_response.to_dict()
    }


def update_nlb_flowlog(module, client):
    """
    Updates a Network Load Balancer Flowlog.

    This will update a Network Load Balancer Flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer Flowlog was updated, false otherwise
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    flowlog_id = module.params.get('flowlog_id')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False
    flowlog_response = None

    if flowlog_id:
        flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
        flowlog_response = _update_nlb_flowlog(module, client, nlb_server, datacenter_id,
                                               network_load_balancer_id, flowlog_id,
                                               flowlog_properties)
        changed = True

    else:
        flowlogs = nlb_server.datacenters_networkloadbalancers_flowlogs_get(datacenter_id=datacenter_id,
                                                                            network_load_balancer_id=network_load_balancer_id,
                                                                            depth=2)
        for f in flowlogs.items:
            if name == f.properties.name:
                flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
                flowlog_response = _update_nlb_flowlog(module, client, nlb_server, datacenter_id,
                                                       network_load_balancer_id, f.id,
                                                       flowlog_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Network Load Balancer Flowlog: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'flowlog': flowlog_response.to_dict()
    }


def remove_nlb_flowlog(module, client):
    """
    Removes a Network Load Balancer Flowlog.

    This will remove a Network Load Balancer Flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer Flowlog was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')
    flowlog_id = module.params.get('flowlog_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False

    try:
        network_load_balancer_flowlog_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=5)
        if flowlog_id:
            network_load_balancer_flowlog = _get_resource(network_load_balancer_flowlog_list,
                                                          flowlog_id)
        else:
            network_load_balancer_flowlog = _get_resource(network_load_balancer_flowlog_list, name)

        if not network_load_balancer_flowlog:
            module.exit_json(changed=False)

        response = nlb_server.datacenters_networkloadbalancers_flowlogs_delete_with_http_info(datacenter_id,
                                                                                              network_load_balancer_id,
                                                                                              network_load_balancer_flowlog)
        (flowlog_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Network Load Balancer Flowlog: %s" % to_native(e))

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
            network_load_balancer_id=dict(type='str'),
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
            if not (module.params.get('name') or module.params.get('network_load_balancer_id')):
                module.fail_json(
                    msg='name parameter or network_load_balancer_id parameter are required deleting a Network Load Balancer Flowlog.')
            try:
                (result) = remove_nlb_flowlog(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set Network Load Balancer state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Network Load Balancer Flowlog')
            if not module.params.get('action'):
                module.fail_json(msg='action parameter is required for a new Network Load Balancer Flowlog')
            if not module.params.get('direction'):
                module.fail_json(msg='direction parameter is required for a new Network Load Balancer Flowlog')
            if not module.params.get('bucket'):
                module.fail_json(msg='bucket parameter is required for a new Network Load Balancer Flowlog')
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for a new Network Load Balancer Flowlog')
            if not module.params.get('network_load_balancer_id'):
                module.fail_json(
                    msg='network_load_balancer_id parameter is required for a new Network Load Balancer Flowlog')

            try:
                (nlb_flowlog_dict) = create_nlb_flowlog(module, api_client)
                module.exit_json(**nlb_flowlog_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Network Load Balancer Flowlog state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a Network Load Balancer Flowlog')
            if not module.params.get('network_load_balancer_id'):
                module.fail_json(
                    msg='network_load_balancer_id parameter is required for updating a Network Load Balancer Flowlog')
            if not module.params.get('flowlog_id'):
                module.fail_json(msg='flowlog_id parameter is required for updating a Network Load Balancer Flowlog')
            try:
                (nlb_dict) = update_nlb_flowlog(module, api_client)
                module.exit_json(**nlb_dict)
            except Exception as e:
                module.fail_json(msg='failed to update the Network Load Balancer Flowlog: %s' % to_native(e))


if __name__ == '__main__':
    main()
