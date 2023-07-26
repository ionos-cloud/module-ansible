#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import copy
import re
import yaml

from uuid import uuid4

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Nic, NicProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'NIC'
RETURNED_KEY = 'nic'

OPTIONS = {
    'name': {
        'description': ['The name of the  resource.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'nic': {
        'description': ['The ID or name of an existing NIC.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
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
    'lan': {
        'description': ['The LAN ID the NIC will be on. If the LAN ID does not exist, it will be implicitly created.'],
        'required': ['present'],
        'available': ['update'],
        'type': 'str',
    },
    'dhcp': {
        'description': ['Indicates if the NIC will reserve an IP using DHCP.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'firewall_active': {
        'description': ['Activate or deactivate the firewall. By default, an active firewall without any defined rules will block all incoming network traffic except for the firewall rules that explicitly allows certain protocols, IP addresses and ports.'],
        'available': ['present', 'update'],
        'type': 'bool',
        'version_added': '2.4',
    },
    'ips': {
        'description': ['Collection of IP addresses, assigned to the NIC. Explicitly assigned public IPs need to come from reserved IP blocks. Passing value null or empty array will assign an IP address automatically.'],
        'available': ['present', 'update'],
        'type': 'list',
        'version_added': '2.4',
    },
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
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
module: nic
short_description: Create, Update or Remove a NIC.
description:
     - This module allows you to create, update or remove a NIC.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''# Create a NIC
    - name: Create NIC
      nic:
       name: NicName
       datacenter: DatacenterName
       server: ServerName
       lan: 2
       dhcp: true
       firewall_active: true
       ips:
         - 10.0.0.1
       wait: true
       wait_timeout: 600
       state: present
      register: ionos_cloud_nic
  ''',
    'update': '''# Update a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      lan: 1
      ips:
        - 158.222.103.23
        - 158.222.103.24
      dhcp: false
      state: update
  ''',
    'absent': '''# Remove a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      wait_timeout: 500
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


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
        module.params.get('ips') is not None
        and sorted(existing_object.properties.ips) != sorted(module.params.get('ips'))
        or module.params.get('dhcp') is not None
        and existing_object.properties.dhcp != module.params.get('dhcp')
        or module.params.get('lan') is not None
        and int(existing_object.properties.lan) != int(module.params.get('lan'))
        or module.params.get('firewall_active') is not None
        and existing_object.properties.firewall_active != module.params.get('firewall_active')
        or module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
    )


def _get_object_list(module, client):
    datacenter = module.params.get('datacenter')
    server = module.params.get('server')

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter = get_resource_id(module, datacenter_list, datacenter)

    # Locate UUID for Server
    server_list = servers_api.datacenters_servers_get(datacenter, depth=1)
    server = get_resource_id(module, server_list, server)

    return nics_api.datacenters_servers_nics_get(datacenter_id=datacenter, server_id=server, depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('nic')


def _create_object(module, client, existing_object=None):
    lan = module.params.get('lan')
    dhcp = module.params.get('dhcp')
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    name = module.params.get('name')
    if existing_object is not None:
        lan = existing_object.properties.lan if lan is None else lan
        dhcp = existing_object.properties.dhcp if dhcp is None else dhcp
        firewall_active = existing_object.properties.firewall_active if firewall_active is None else firewall_active
        ips = existing_object.properties.ips if ips is None else ips
        name = existing_object.properties.name if name is None else name

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    # Locate UUID for Server
    server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    nic = Nic(properties=NicProperties(
        name=name, ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active,
    ))

    try:
        nic_response, _, headers = nics_api.datacenters_servers_nics_post_with_http_info(
            datacenter_id=datacenter_id, server_id=server_id, nic=nic,
        )

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            nic_response = nics_api.datacenters_servers_nics_find_by_id(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_response.id,
            )
    except ApiException as e:
        module.fail_json(msg="failed to create the new NIC: %s" % to_native(e))
    return nic_response


def _update_object(module, client, existing_object):
    lan = module.params.get('lan')
    dhcp = module.params.get('dhcp')
    firewall_active = module.params.get('firewall_active')
    ips = module.params.get('ips')
    name = module.params.get('name')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    # Locate UUID for Server
    server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    if lan is None:
        lan = existing_object.properties.lan
    if firewall_active is None:
        firewall_active = existing_object.properties.firewall_active
    if dhcp is None:
        dhcp = existing_object.properties.dhcp

    nic_properties = NicProperties(ips=ips, dhcp=dhcp, lan=lan, firewall_active=firewall_active, name=name)

    try:
        nic_response, _, headers = nics_api.datacenters_servers_nics_patch_with_http_info(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=existing_object.id, nic=nic_properties,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            nic_response = nics_api.datacenters_servers_nics_find_by_id(
                datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_response.id,
            )

        return nic_response
    except ApiException as e:
        module.fail_json(msg="failed to update the NIC: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    datacenters_api = ionoscloud.DataCentersApi(api_client=client)
    servers_api = ionoscloud.ServersApi(api_client=client)
    nics_api = ionoscloud.NetworkInterfacesApi(api_client=client)

    # Locate UUID for Datacenter
    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    # Locate UUID for Server
    server_list = servers_api.datacenters_servers_get(datacenter_id, depth=1)
    server_id = get_resource_id(module, server_list, module.params.get('server'))

    try:
        _, _, headers = nics_api.datacenters_servers_nics_delete_with_http_info(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=existing_object.id,
        )
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to remove the NIC: %s" % to_native(e))


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
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME,
                                                                                             error=to_native(e),
                                                                                             state=state))


if __name__ == '__main__':
    main()
