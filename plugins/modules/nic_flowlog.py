#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import re
import yaml

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


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Flowflog'

OPTIONS = {
    'name': {
        'description': ['The name of the Flowlog.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'flowlog_id': {
        'description': ['The ID of the Flowlog.'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'datacenter_id': {
        'description': ['The ID of the virtual datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'server_id': {
        'description': ['The ID of the Server.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nic_id': {
        'description': ['The ID of the NIC.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'action': {
        'description': ['Specifies the traffic action pattern.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'direction': {
        'description': ['Specifies the traffic direction pattern.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'bucket': {
        'description': ['S3 bucket name of an existing IONOS Cloud S3 bucket.'],
        'available': ['present', 'update'],
        'required': ['present'],
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
module: datacenter
short_description: Create or destroy a Ionos Cloud NIC Flowlog.
description:
     - This is a simple module that supports creating or removing NIC Flowlogs.
       This module has a dependency on ionos-cloud >= 6.0.0
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
  'present' : '''- name: Create a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
  register: flowlog_response
  ''',
  'update' : '''- name: Update a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
  register: flowlog_update_response
  ''',
  'absent' : '''- name: Delete a nic flowlog
  nic_flowlog:
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
    name: "{{ name }}"
    state: absent
    wait: true
  register: flowlog_delete_response
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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
        nic_flowlog_list = nic_flowlog_server.datacenters_servers_nics_flowlogs_get(datacenter_id=datacenter_id, nic_id=nic_id, server_id=server_id, depth=5)
        if flowlog_id:
            nic_flowlog = _get_resource(nic_flowlog_list, flowlog_id)
        else:
            nic_flowlog = _get_resource(nic_flowlog_list, name)

        if not nic_flowlog:
            module.exit_json(changed=False)

        response = nic_flowlog_server.datacenters_servers_nics_flowlogs_delete_with_http_info(datacenter_id, server_id, nic_id, nic_flowlog)
        (flowlog_id_response, _, headers) = response

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
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'absent':
                module.exit_json(**remove_flowlog(module, api_client))
            if state == 'present':
                module.exit_json(**create_flowlog(module, api_client))
            elif state == 'update':
                module.exit_json(**update_flowlog(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
