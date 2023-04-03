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
    from ionoscloud.models import ApplicationLoadBalancer, ApplicationLoadBalancerProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError as e:
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
DOC_DIRECTORY = 'applicationloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Application Loadbalancer'
RETURNED_KEY = 'application_load_balancer'

OPTIONS = {
    'name': {
        'description': ['The name of the Application Load Balancer.'],
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
            'Collection of the Application Load Balancer IP addresses. (Inbound and outbound) '
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
            'Collection of private IP addresses with subnet mask of the Application Load Balancer. '
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
    'application_load_balancer': {
        'description': ['The ID or name of the Application Loadbalancer.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different'
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
module: application_load_balancer
short_description: Create or destroy a Ionos Cloud Application Loadbalancer.
description:
     - This is a simple module that supports creating or removing Application Loadbalancers.
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
  - name: Create Application Load Balancer
    application_load_balancer:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
    register: alb_response
  ''',
  'update' : '''
  - name: Update Application Load Balancer
    application_load_balancer:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
      state: update
    register: alb_response_update
  ''',
  'absent' : '''
  - name: Remove Application Load Balancer
    application_load_balancer:
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      wait: true
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def _should_replace_object(module, existing_object):
    return False


def _should_update_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('ips') is not None
        and sorted(existing_object.properties.ips) != sorted(module.params.get('ips'))
        or module.params.get('lb_private_ips') is not None
        and sorted(existing_object.properties.lb_private_ips) != sorted(module.params.get('lb_private_ips'))
        or module.params.get('listener_lan') is not None
        and existing_object.properties.listener_lan != module.params.get('listener_lan')
        or module.params.get('target_lan') is not None
        and existing_object.properties.target_lan != module.params.get('target_lan')
    )


def _get_object_list(module, client):
    return ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
        module.params.get('datacenter_id'), depth=1,
    )


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('application_load_balancer')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')
    datacenter_id = module.params.get('datacenter_id')
    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        ips = existing_object.properties.ips if ips is None else ips
        listener_lan = existing_object.properties.listener_lan if listener_lan is None else listener_lan
        target_lan = existing_object.properties.target_lan if target_lan is None else target_lan
        lb_private_ips = existing_object.properties.lb_private_ips if lb_private_ips is None else lb_private_ips

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
    
    application_load_balancer = ApplicationLoadBalancer(properties=ApplicationLoadBalancerProperties(
        name=name, listener_lan=listener_lan, ips=ips,
        target_lan=target_lan, lb_private_ips=lb_private_ips,
    ))

    try:
        response, _, headers = albs_api.datacenters_applicationloadbalancers_post_with_http_info(
            datacenter_id, application_load_balancer,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to create the new Application Loadbalancer: %s" % to_native(e))
    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')
    datacenter_id = module.params.get('datacenter_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
    
    alb_properties = ApplicationLoadBalancerProperties(
        name=name, listener_lan=listener_lan, ips=ips,
        target_lan=target_lan, lb_private_ips=lb_private_ips,
    )

    try:
        response, _, headers = albs_api.datacenters_applicationloadbalancers_patch_with_http_info(
            datacenter_id, existing_object.id, alb_properties,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the Application Loadbalancer: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    datacenter_id = module.params.get('datacenter_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    albs_api = ionoscloud.ApplicationLoadBalancersApi(client)

    try:
        _, _, headers = albs_api.datacenters_applicationloadbalancers_delete_with_http_info(
            datacenter_id, existing_object.id,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the Application Loadbalancer: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

    existing_object = get_resource(module, object_list, _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(module, object_list, object_name)

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
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
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

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
                module.exit_json(**remove_object(module, api_client))
            elif state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))

if __name__ == '__main__':
    main()
