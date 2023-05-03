#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import copy
import re
import time
import yaml


HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import FirewallRule, FirewallruleProperties, Nic, NicProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False


__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (
    __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Firewall Rule'
RETURNED_KEY = 'firewall_rule'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'server': {
        'description': ['The server name or UUID.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'nic': {
        'description': ['The NIC name or UUID.'],
        'required': STATES,
        'available': STATES,
        'type': 'str',
    },
    'firewall_rule': {
        'description': ['The Firewall Rule name or UUID.'],
        'required': ['update', 'absent'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'name': {
        'description': ['The name or UUID of the firewall rule.'],
        'required': ['present'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['The protocol for the firewall rule.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'choices': ['TCP', 'UDP', 'ICMP', 'ANY'],
        'type': 'str',
    },
    'source_mac': {
        'description': ['Only traffic originating from the respective MAC address is allowed. No value allows all source MAC addresses.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'source_ip': {
        'description': ['Only traffic originating from the respective IPv4 address is allowed. No value allows all source IPs.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'target_ip': {
        'description': [
            'In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed.'
            'No value allows all target IPs.',
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'port_range_start': {
        'description': [
            'Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave value empty to allow all ports.',
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'port_range_end': {
        'description': [
            'Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave value empty to allow all ports.',
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_type': {
        'description': ['Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. No value allows all types.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'icmp_code': {
        'description': ['Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. No value allows all codes.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'ip_version': {
        'description': [
            'The IP version for this rule. If sourceIp or targetIp are specified, you can omit this '
            'value - the IP version will then be deduced from the IP address(es) used; if you specify '
            'it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp '
            'are specified, this rule allows traffic only for the specified IP version. If neither '
            'sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic.',
        ],
        'available': ['present', 'update'],
        'choices': ['IPv4', 'IPv6'],
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
module: firewall_rule
short_description: Create, update or remove a firewall rule.
description:
     - This module allows you to create, update or remove a firewall rule.
version_added: "2.2"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''# Create a firewall rule
- name: Create SSH firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow SSH
    protocol: TCP
    source_ip: 0.0.0.0
    port_range_start: 22
    port_range_end: 22
    state: present

- name: Create ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow Ping
    protocol: ICMP
    source_ip: 0.0.0.0
    icmp_type: 8
    icmp_code: 0
    state: present
  ''',
    'update': '''# Update a firewall rule
- name: Allow SSH access
  firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update
  ''',
    'absent': '''# Remove a firewall rule
- name: Remove public ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: aa6c261b9c
    name: Allow Ping
    state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


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
    matched_resources = _get_matched_resources(
        resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(
            resource_list.id, identity))
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
        or module.params.get('protocol') is not None
        and existing_object.properties.protocol != module.params.get('protocol')
        or module.params.get('source_mac') is not None
        and existing_object.properties.source_mac != module.params.get('source_mac')
        or module.params.get('source_ip') is not None
        and existing_object.properties.source_ip != module.params.get('source_ip')
        or module.params.get('target_ip') is not None
        and existing_object.properties.target_ip != module.params.get('target_ip')
        or module.params.get('port_range_start') is not None
        and existing_object.properties.port_range_start != module.params.get('port_range_start')
        or module.params.get('port_range_end') is not None
        and existing_object.properties.port_range_end != module.params.get('port_range_end')
        or module.params.get('icmp_type') is not None
        and existing_object.properties.icmp_type != module.params.get('icmp_type')
        or module.params.get('icmp_code') is not None
        and existing_object.properties.icmp_code != module.params.get('icmp_code')
        or module.params.get('ip_version') is not None
        and existing_object.properties.ip_version != module.params.get('ip_version')
    )


def _get_object_list(module, client):
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')
    nic = module.params.get('nic')
    datacenter_api = ionoscloud.DataCentersApi(api_client=client)
    server_api = ionoscloud.ServersApi(api_client=client)
    nic_api = ionoscloud.NetworkInterfacesApi(api_client=client)
    firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

    # Locate UUID for virtual datacenter
    datacenter_list = datacenter_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, datacenter)

    # Locate UUID for server
    server_list = server_api.datacenters_servers_get(
        datacenter_id=datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, server)

    # Locate UUID for NIC
    nic_list = nic_api.datacenters_servers_nics_get(
        datacenter_id=datacenter_id, server_id=server_id, depth=1)
    nic_id = get_resource_id(module, nic_list, nic)

    return firewall_rules_api.datacenters_servers_nics_firewallrules_get(datacenter_id, server_id, nic_id, depth=2)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('firewall_rule')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    protocol = module.params.get('protocol')
    source_mac = module.params.get('source_mac')
    source_ip = module.params.get('source_ip')
    target_ip = module.params.get('target_ip')
    port_range_start = module.params.get('port_range_start')
    port_range_end = module.params.get('port_range_end')
    icmp_type = module.params.get('icmp_type')
    icmp_code = module.params.get('icmp_code')
    ip_version = module.params.get('ip_version')
    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        protocol = existing_object.properties.protocol if protocol is None else protocol
        source_mac = existing_object.properties.source_mac if source_mac is None else source_mac
        source_ip = existing_object.properties.source_ip if source_ip is None else source_ip
        target_ip = existing_object.properties.target_ip if target_ip is None else target_ip
        port_range_start = existing_object.properties.port_range_start if port_range_start is None else port_range_start
        port_range_end = existing_object.properties.port_range_end if port_range_end is None else port_range_end
        icmp_type = existing_object.properties.icmp_type if icmp_type is None else icmp_type
        icmp_code = existing_object.properties.icmp_code if icmp_code is None else icmp_code
        ip_version = existing_object.properties.ip_version if ip_version is None else ip_version

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenters_api = ionoscloud.DataCentersApi(client)
    nic_api = ionoscloud.NetworkInterfacesApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
    nic_id = get_resource_id(module, nic_list, module.params.get('nic'))

    firewall_rule = FirewallRule(properties=FirewallruleProperties(
        name=name, protocol=protocol, source_mac=source_mac,
        source_ip=source_ip, ip_version=ip_version,
        target_ip=target_ip, icmp_code=icmp_code, icmp_type=icmp_type,
        port_range_start=port_range_start, port_range_end=port_range_end,
    ))


    try:
        current_nic = nic_api.datacenters_servers_nics_find_by_id(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id,
        )
        nic = Nic(properties=NicProperties(firewall_active=True, lan=current_nic.properties.lan))
        nic_api.datacenters_servers_nics_put(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, nic=nic,
        )

    except Exception as e:
        module.fail_json(msg='Unable to activate the NIC firewall.' % to_native(e))

    try:
        response, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_post_with_http_info(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, firewallrule=firewall_rule,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the firewall rule: %s" % to_native(e))

    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    source_mac = module.params.get('source_mac')
    source_ip = module.params.get('source_ip')
    target_ip = module.params.get('target_ip')
    port_range_start = module.params.get('port_range_start')
    port_range_end = module.params.get('port_range_end')
    icmp_type = module.params.get('icmp_type')
    icmp_code = module.params.get('icmp_code')
    ip_version = module.params.get('ip_version')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenters_api = ionoscloud.DataCentersApi(client)
    servers_api = ionoscloud.ServersApi(client)
    nic_api = ionoscloud.NetworkInterfacesApi(client)
    firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
    nic_id = get_resource_id(module, nic_list, module.params.get('nic'))

    firewall_rule_properties = FirewallruleProperties(
        name=name,
        source_mac=source_mac,
        source_ip=source_ip,
        target_ip=target_ip,
        ip_version=ip_version,
    )

    if port_range_start or port_range_end:
        firewall_rule_properties.port_range_start = port_range_start
        firewall_rule_properties.port_range_end = port_range_end

    if icmp_type or icmp_code:
        firewall_rule_properties.icmp_code = icmp_code
        firewall_rule_properties.icmp_type = icmp_type

    try:
        response, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_patch_with_http_info(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewallrule_id=existing_object.id,
            firewallrule=firewall_rule_properties
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the firewall rule: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenters_api = ionoscloud.DataCentersApi(client)
    servers_api = ionoscloud.ServersApi(client)
    nic_api = ionoscloud.NetworkInterfacesApi(client)
    firewall_rules_api = ionoscloud.FirewallRulesApi(api_client=client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    server_list = servers_api.datacenters_servers_get(datacenter_id=datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    nic_list = nic_api.datacenters_servers_nics_get(datacenter_id=datacenter_id, server_id=server_id, depth=1)
    nic_id = get_resource_id(module, nic_list, module.params.get('nic'))

    try:
        _, _, headers = firewall_rules_api.datacenters_servers_nics_firewallrules_delete_with_http_info(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewallrule_id=existing_object.id,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(
            msg="failed to remove the firewall rule: %s" % to_native(e))


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
    module = AnsibleModule(
        argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(
            msg='ionoscloud is required for this module, run `pip install ionoscloud`')

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
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
