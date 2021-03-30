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
    from ionoscloud.models import FlowLog, FlowLogProperties, FlowLogPut
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _update_flowlog(module, client, nic_flowlog_server, datacenter_id, server_id, nic_id, flowlog_id, flowlog_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nic_flowlog_server.datacenters_servers_nics_flowlogs_patch_with_http_info(datacenter_id, server_id, nic_id, flowlog_id, flowlog_properties)
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


def create_flowlog(module, client):
    """
    Creates a Flowlog

    This will create a new Flowlog in the specified location.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The flowlog ID if a new flowlog was created.
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    server_id = module.params.get('server_id')
    nic_id = module.params.get('nic_id')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nic_flowlog_server = ionoscloud.FlowLogsApi(client)
    flowlogs = nic_flowlog_server.datacenters_servers_nics_flowlogs_get(datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, depth=2)

    for flowlog in flowlogs.items:
        if name == flowlog.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'flowlog': flowlog.to_dict()
            }

    flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
    flowlog = FlowLog(properties=flowlog_properties)

    try:
        response = nic_flowlog_server.datacenters_servers_nics_flowlogs_post_with_http_info(datacenter_id, server_id, nic_id, flowlog)
        (flowlog_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return{
            'changed': True,
            'failed': False,
            'action': 'create',
            'flowlog': flowlog_response.to_dict()
        }

    except ApiException as e:
        module.fail_json(msg="failed to create the new flowlog: %s" % to_native(e))


def update_flowlog(module, client):
    """
    Updates a Flowlog.

    This will update a flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the flowlog was updated, false otherwise
    """
    name = module.params.get('name')
    action = module.params.get('action')
    direction = module.params.get('direction')
    bucket = module.params.get('bucket')
    datacenter_id = module.params.get('datacenter_id')
    server_id = module.params.get('server_id')
    nic_id = module.params.get('nic_id')
    flowlog_id = module.params.get('flowlog_id')

    nic_flowlog_server = ionoscloud.FlowLogsApi(client)
    changed = False
    flowlog_response = None

    if flowlog_id:
        flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
        flowlog_response = _update_flowlog(module, client, nic_flowlog_server, datacenter_id, server_id, nic_id, flowlog_id, flowlog_properties)
        changed = True

    else:
        flowlogs = nic_flowlog_server.datacenters_servers_nics_flowlogs_get(datacenter_id=datacenter_id, nic_id=nic_id, server_id=server_id, depth=2)
        for f in flowlogs.items:
            if name == f.properties.name:
                flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
                flowlog_response = _update_flowlog(module, client, nic_flowlog_server, datacenter_id, server_id, nic_id, f.id, flowlog_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the flowlog: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'flowlog': flowlog_response.to_dict()
    }


def remove_flowlog(module, client):
    """
    Removes a Flowlog.

    This will remove a flowlog.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the flowlog was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    server_id = module.params.get('server_id')
    nic_id = module.params.get('nic_id')
    flowlog_id = module.params.get('flowlog_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nic_flowlog_server = ionoscloud.FlowLogsApi(client)
    changed = False

    try:

        if flowlog_id:
            response = nic_flowlog_server.datacenters_servers_nics_flowlogs_delete_with_http_info(datacenter_id, server_id, nic_id, flowlog_id)
            (flowlog_id_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            flowlogs = nic_flowlog_server.datacenters_servers_nics_flowlogs_get(datacenter_id=datacenter_id,
                                                                                nic_id=nic_id, server_id=server_id,
                                                                                depth=2)
            for f in flowlogs.items:
                if name == f.properties.name:
                    flowlog_id = f.id
                    response = nic_flowlog_server.datacenters_servers_nics_flowlogs_delete_with_http_info(datacenter_id, server_id, nic_id, flowlog_id)
                    (flowlog_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the flowlog: %s" % to_native(e))

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
            nic_id=dict(type='str'),
            flowlog_id=dict(type='str'),
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
            if not (module.params.get('name') or module.params.get('flowlog_id')):
                module.fail_json(msg='name parameter or flowlog_id parameter are required deleting a flowlog.')
            try:
                (result) = remove_flowlog(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set flowlog state: %s' % to_native(e))

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new flowlog')
            if not module.params.get('action'):
                module.fail_json(msg='action parameter is required for a new flowlog')
            if not module.params.get('direction'):
                module.fail_json(msg='direction parameter is required for a new flowlog')
            if not module.params.get('bucket'):
                module.fail_json(msg='bucket parameter is required for a new flowlog')

            try:
                (flowlog_dict_array) = create_flowlog(module, api_client)
                module.exit_json(**flowlog_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set flowlog state: %s' % to_native(e))

        elif state == 'update':
            try:
                (flowlog_dict_array) = update_flowlog(module, api_client)
                module.exit_json(**flowlog_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update the flowlog: %s' % to_native(e))


if __name__ == '__main__':
    main()
