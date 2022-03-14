#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import copy
import yaml

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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'natgateway'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Flowlog'

OPTIONS = {
    'name': {
        'description': ['The name of the flowlog.'],
        'available': STATES,
        'required': ['present'],
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
    'datacenter_id': {
        'description': ['The ID of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nat_gateway_id': {
        'description': ['The ID of the NAT Gateway.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'flowlog_id': {
        'description': ['The ID of the Flowlog.'],
        'available': ['absent', 'update'],
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
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'required': STATES,
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'required': STATES,
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
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
module: nat_gateway_flowlog
short_description: Create or destroy a Ionos Cloud NATGateway Flowlog.
description:
     - This is a simple module that supports creating or removing NATGateway Flowlogs.
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
  'present' : '''
  - name: Create NAT Gateway Flowlog
    nat_gateway_flowlog:
      name: "{{ name }}"
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      wait: true
    register: nat_gateway_flowlog_response
  ''',
  'update' : '''
  - name: Update NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      flowlog_id: "{{ nat_gateway_flowlog_response.flowlog.id }}"
      name: "{{ name }}"
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: nat_gateway_flowlog_update_response
  ''',
  'absent' : '''
  - name: Delete NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      flowlog_id: "{{ nat_gateway_flowlog_response.flowlog.id }}"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


uuid_match = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


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
        nat_gateway_flowlog_list = nat_gateway_server.datacenters_natgateways_flowlogs_get(datacenter_id=datacenter_id, nat_gateway_id=nat_gateway_id, depth=5)
        if flowlog_id:
            flowlog_id = _get_resource(nat_gateway_flowlog_list, flowlog_id)
        else:
            flowlog_id = _get_resource(nat_gateway_flowlog_list, name)

        if not flowlog_id:
            module.exit_json(changed=False)

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
    api_url = module.params.get('api_url')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
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

        if state == 'absent' and not module.params.get('name') and not module.params.get('flowlog_id'):
            module.fail_json(msg='either name or flowlog_id parameter is required for {object_name} state absent'.format(object_name=OBJECT_NAME))

        try:
            if state == 'absent':
                module.exit_json(**remove_nat_gateway_flowlog(module, api_client))
            elif state == 'present':
                module.exit_json(**create_nat_gateway_flowlog(module, api_client))
            elif state == 'update':
                module.exit_json(**update_nat_gateway_flowlog(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
