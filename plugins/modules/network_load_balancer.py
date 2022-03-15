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
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties
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
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Network Loadbalancer'

OPTIONS = {
    'name': {
        'description': ['The name of the Network Loadbalancer forwarding rule.'],
        'available': STATES,
        'required': ['present', 'update'],
        'type': 'str',
    },
    'listener_lan': {
        'description': ['ID of the listening LAN (inbound).'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'ips': {
        'description': [
            'Collection of the Network Load Balancer IP addresses. (Inbound and outbound) '
            'IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'target_lan': {
        'description': ['ID of the balanced private target LAN (outbound).'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'lb_private_ips': {
        'description': [
            'Collection of private IP addresses with subnet mask of the Network Load Balancer. '
            'IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'datacenter_id': {
        'description': ['The ID of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'network_load_balancer_id': {
        'description': ['The ID of the Network Loadbalancer.'],
        'available': ['update', 'absent'],
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
module: network_load_balancer
short_description: Create or destroy a Ionos Cloud NetworkLoadbalancer.
description:
     - This is a simple module that supports creating or removing NetworkLoadbalancers.
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
  - name: Create Network Load Balancer
    network_load_balancer:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
    register: nlb_response
  ''',
  'update' : '''
  - name: Update Network Load Balancer
    network_load_balancer:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
      state: update
    register: nlb_response_update
  ''',
  'absent' : '''
  - name: Remove Network Load Balancer
    network_load_balancer:
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      wait: true
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


def _update_nlb(module, client, nlb_server, datacenter_id, network_load_balancer_id, nlb_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nlb_server.datacenters_networkloadbalancers_patch_with_http_info(datacenter_id, network_load_balancer_id,
                                                                                nlb_properties)
    (nlb_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return nlb_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nlb(module, client):
    """
    Creates a Network Load Balancer

    This will create a new Network Load Balancer in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Network Load Balancer ID if a new Network Load Balancer was created.
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=2)
    nlb_response = None

    for nlb in nlb_list.items:
        if name == nlb.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'network_load_balancer': nlb.to_dict()
            }

    nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips, target_lan=target_lan,
                                                   lb_private_ips=lb_private_ips)
    network_load_balancer = NetworkLoadBalancer(properties=nlb_properties)

    try:
        response = nlb_server.datacenters_networkloadbalancers_post_with_http_info(datacenter_id, network_load_balancer)
        (nlb_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Network Load Balancer: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'network_load_balancer': nlb_response.to_dict()
    }


def update_nlb(module, client):
    """
    Updates a Network Load Balancer.

    This will update a Network Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer was updated, false otherwise
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_response = None
    changed = False

    if network_load_balancer_id:
        nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                       target_lan=target_lan,
                                                       lb_private_ips=lb_private_ips)
        nlb_response = _update_nlb(module, client, nlb_server, datacenter_id, network_load_balancer_id,
                                   nlb_properties)
        changed = True

    else:
        nlb_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=2)
        for nlb in nlb_list.items:
            if name == nlb.properties.name:
                nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                               target_lan=target_lan,
                                                               lb_private_ips=lb_private_ips)
                nlb_response = _update_nlb(module, client, nlb_server, datacenter_id, nlb.id,
                                           nlb_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Network Load Balancer: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'network_load_balancer': nlb_response.to_dict()
    }


def remove_nlb(module, client):
    """
    Removes a Network Load Balancer.

    This will remove a Network Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False

    try:

        network_load_balancer_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=5)
        if network_load_balancer_id:
            network_load_balancer = _get_resource(network_load_balancer_list, network_load_balancer_id)
        else:
            network_load_balancer = _get_resource(network_load_balancer_list, name)

        if not network_load_balancer:
            module.exit_json(changed=False)

        response = nlb_server.datacenters_networkloadbalancers_delete_with_http_info(datacenter_id, network_load_balancer)
        (nlb_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Network Load Balancer: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': network_load_balancer_id
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

        if state == 'absent' and not module.params.get('name') and not module.params.get('network_load_balancer_id'):
            module.fail_json(msg='either name or network_load_balancer_id parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME))

        try:
            if state == 'absent':
                module.exit_json(**remove_nlb(module, api_client))
            elif state == 'present':
                module.exit_json(**create_nlb(module, api_client))
            elif state == 'update':
                module.exit_json(**update_nlb(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
