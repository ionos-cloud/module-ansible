#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import re
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Lan, LanProperties
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'LAN'
RETURNED_KEY = 'lan'

OPTIONS = {
    'datacenter': {
        'description': ['The datacenter name or UUID in which to operate.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'lan': {
        'description': ['The LAN name or UUID.'],
        'available': ['absent', 'update'],
        'required': ['absent', 'update'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'pcc': {
        'description': ['The unique identifier of the private Cross-Connect the LAN is connected to, if any.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'pcc': {
        'description': ['The unique identifier of the private Cross-Connect the LAN is connected to, if any.'],
        'available': ['update'],
        'type': 'str',
    },
    'ip_failover': {
        'description': ['IP failover configurations for lan'],
        'available': ['update'],
        'type': 'list',
        'elements': 'dict',
    },
    'public': {
        'description': ['This LAN faces the public Internet.'],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'ipv6_cidr': {
        'description': [
            "[The IPv6 feature is in beta phase and not ready for production usage.] For a GET request, "
            "this value is either 'null' or contains the LAN's /64 IPv6 CIDR block if this LAN is "
            "IPv6-enabled. For POST/PUT/PATCH requests, 'AUTO' will result in enabling this LAN for "
            "IPv6 and automatically assign a /64 IPv6 CIDR block to this LAN. If you choose the IPv6 "
            "CIDR block on your own, then you must provide a /64 block, which is inside the IPv6 CIDR "
            "block of the virtual datacenter and unique inside all LANs from this virtual datacenter. "
            "If you enable IPv6 on a LAN with NICs, those NICs will get an /80 IPv6 CIDR block and one "
            "IPv6 address assigned to each automatically, unless you specify them explicitly on the NICs. "
            "A virtual data center is limited to a maximum of 256 IPv6-enabled LANs.",
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'allow_replace': {
        'description': [
            'Boolean indincating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
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
module: lan
short_description: Create, update or remove a LAN.
description:
     - This module allows you to create or remove a LAN.
version_added: "2.4"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  ''',
  'update' : '''# Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  ''',
  'absent' : '''# Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
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


def _should_update_object(module, existing_object, client):
    pcc_id = get_resource_id(
        module, 
        ionoscloud.PrivateCrossConnectsApi(client).pccs_get(depth=1),
        module.params.get('pcc'),
    )

    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('public') is not None
        and existing_object.properties.public != module.params.get('public')
        or module.params.get('ipv6_cidr') is not None
        and existing_object.properties.ipv6_cidr_block != module.params.get('ipv6_cidr')
        or module.params.get('ip_failover') is not None
        and existing_object.properties.ip_failover != list(map(lambda el: {'ip': el.ip, 'nic_uuid': el.nic_uuid}, module.params.get('ip_failover')))
        or pcc_id is not None
        and existing_object.properties.pcc != pcc_id
    )


def _get_object_list(module, client):
    datacenter_list = ionoscloud.DataCentersApi(api_client=client).datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    return ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('lan')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    public = module.params.get('public')
    ipv6_cidr = module.params.get('ipv6_cidr')

    pcc_id = get_resource_id(
        module, 
        ionoscloud.PrivateCrossConnectsApi(client).pccs_get(depth=1),
        module.params.get('pcc'),
    )
    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        public = existing_object.properties.public if public is None else public
        ipv6_cidr = existing_object.properties.ipv6_cidr_block if ipv6_cidr is None else ipv6_cidr
        pcc_id = existing_object.properties.pcc if pcc_id is None else pcc_id

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenters_api = ionoscloud.DataCentersApi(client)
    lans_api = ionoscloud.LANsApi(client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    lan = Lan(properties=LanProperties(
        name=name, pcc=pcc_id, public=public,
        ipv6_cidr_block=ipv6_cidr,
    ))

    try:
        lan_response, _, headers = lans_api.datacenters_lans_post_with_http_info(datacenter_id, lan=lan)
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
    except ApiException as e:
        module.fail_json(msg="failed to create the new LAN: %s" % to_native(e))
    return lan_response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    public = module.params.get('public')
    ip_failover = module.params.get('ip_failover')
    ipv6_cidr = module.params.get('ipv6_cidr')

    pcc_id = get_resource_id(
        module, 
        ionoscloud.PrivateCrossConnectsApi(client).pccs_get(depth=1),
        module.params.get('pcc'),
    )

    datacenters_api = ionoscloud.DataCentersApi(client)
    lans_api = ionoscloud.LANsApi(client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    if ip_failover:
        for elem in ip_failover:
            elem['nicUuid'] = elem.pop('nic_uuid')

    lan_properties = LanProperties(
        name=name, ip_failover=ip_failover,
        pcc=pcc_id, public=public,
        ipv6_cidr_block=ipv6_cidr,
    )

    try:
        lan_response, _, headers = lans_api.datacenters_lans_patch_with_http_info(
            datacenter_id, existing_object.id, lan_properties,
        )
        if module.params.get('wait'):
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=module.params.get('wait_timeout'))

        return lan_response
    except ApiException as e:
        module.fail_json(msg="failed to update the LAN: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    datacenters_api = ionoscloud.DataCentersApi(client)
    lans_api = ionoscloud.LANsApi(client)

    datacenter_list = datacenters_api.datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    try:
        _, _, headers = lans_api.datacenters_lans_delete_with_http_info(datacenter_id, existing_object.id)
        if module.params.get('wait'):
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=module.params.get('wait_timeout'))
    except ApiException as e:
        module.fail_json(msg="failed to remove the LAN: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object, client):
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
        return

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
        return

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
