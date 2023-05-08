#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
from tabnanny import check
import yaml
import re

HAS_SDK = True

try:
    import ionoscloud_dnsaas
    from ionoscloud_dnsaas import __version__ as sdk_version
    from ionoscloud_dnsaas.rest import ApiException
    from ionoscloud_dnsaas import ApiClient
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dnsaas/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'dnsaas'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Record'
RETURNED_KEY = 'record'

OPTIONS = {
    'zone': {
        'description': ['The ID or name of the zone.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'name': {
        'description': ['The name of the record.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'content': {
        'description': ['The content of the record.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'type': {
        'description': [
            'Holds supported DNS resource record types. In the DNS context a record is a '
            'DNS resource record. The options are: '
            "['A', 'AAAA', 'CNAME', 'ALIAS', 'MX', 'NS', 'SRV', 'TXT', 'CAA', 'SSHFP', "
            "'TLSA', 'SMIMEA', 'DS', 'HTTPS', 'SVCB', 'OPENPGPKEY', 'CERT', 'URI', 'RP', 'LOC']",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'ttl': {
        'description': ['Time to live for the record, recommended 3600.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'priority': {
        'description': [
            'Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI '
            'record types and ignored for all other types.',
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'enabled': {
        'description': ['When true - the record is visible for lookup.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'record': {
        'description': ['The ID or name of the record.'],
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
module: record
short_description: Create or destroy a Ionos Cloud DNS Record.
description:
     - This is a simple module that supports creating or removing records.
       This module has a dependency on ionoscloud-dnsaas >= 1.0.0
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud-dnsaas >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
    - name: Create Record
    record:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ record_name }}"
      type: "{{ record_type }}"
      content: "{{ record_content }}"
      enabled: "{{ record_enabled }}"
      ttl: "{{ record_ttl }}"
      priority: "{{ record_priority }}"
    register: record_response
  ''',
  'update' : '''
  - name: Update Record
    record:
      zone: "{{ zone_response.zone.id }}"
      record: "{{ record_response.record.id }}"
      name: "{{ record_name_update }}"
      type: "{{ record_type_update }}"
      content: "{{ record_content_update }}"
      enabled: "{{ record_enabled_update }}"
      ttl: "{{ record_ttl_update }}"
      priority: "{{ record_priority_update }}"
      state: update
    register: record_response_update
  ''',
  'absent' : '''# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Delete Record
    record:
      zone: "{{ zone_response.zone.id }}"
      record: "{{ record_response_update.record.id }}"
      wait: true
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


def _should_update_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('content') is not None
        and existing_object.properties.content != module.params.get('content')
        or module.params.get('type') is not None
        and existing_object.properties.type != module.params.get('type')
        or module.params.get('ttl') is not None
        and existing_object.properties.ttl != module.params.get('ttl')
        or module.params.get('priority') is not None
        and existing_object.properties.priority != module.params.get('priority')
        or module.params.get('enabled') is not None
        and existing_object.properties.enabled != module.params.get('enabled')
    )


def _get_object_list(module, client):
    zone_list = ionoscloud_dnsaas.ZonesApi(client).zones_get()
    zone_id = get_resource_id(
        module, zone_list, module.params.get('zone'),
        [['id'], ['properties', 'zone_name']],
    )
    return ionoscloud_dnsaas.RecordsApi(client).zones_records_get(zone_id)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('record')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    content = module.params.get('content')
    enabled = module.params.get('enabled')
    zone_type = module.params.get('type')
    ttl = module.params.get('ttl')
    priority = module.params.get('priority')
    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        content = existing_object.properties.content if content is None else content
        enabled = existing_object.properties.enabled if enabled is None else enabled
        zone_type = existing_object.properties.type if zone_type is None else zone_type
        ttl = existing_object.properties.ttl if ttl is None else ttl
        priority = existing_object.properties.priority if priority is None else priority
    
    zone_list = ionoscloud_dnsaas.ZonesApi(client).zones_get()
    zone_id = get_resource_id(
        module, zone_list, module.params.get('zone'),
        [['id'], ['properties', 'zone_name']],
    )

    records_api = ionoscloud_dnsaas.RecordsApi(client)

    record_properties = ionoscloud_dnsaas.RecordProperties(
        name=name, type=zone_type, enabled=enabled, ttl=ttl, priority=priority, content=content
    )
    record = ionoscloud_dnsaas.RecordCreateRequest(properties=record_properties)

    try:
        response = records_api.zones_records_post(zone_id, record)
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: records_api.zones_records_find_by_id(zone_id, response.id).metadata.state,
                fn_check=lambda r: r == 'CREATED',
                scaleup=10000,
                timeout=int(module.params.get('wait_timeout')),
            )
    except ApiException as e:
        module.fail_json(msg="failed to create the new record: %s" % to_native(e))
    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    content = module.params.get('content')
    enabled = module.params.get('enabled')
    zone_type = module.params.get('type')
    ttl = module.params.get('ttl')
    priority = module.params.get('priority')

    zone_list = ionoscloud_dnsaas.ZonesApi(client).zones_get()
    zone_id = get_resource_id(
        module, zone_list, module.params.get('zone'),
        [['id'], ['properties', 'zone_name']],
    )
    records_api = ionoscloud_dnsaas.RecordsApi(client)

    record_properties = ionoscloud_dnsaas.RecordProperties(
        name=name if name is not None else existing_object.properties.name,
        type=zone_type if zone_type is not None else existing_object.properties.type,
        content=content if content is not None else existing_object.properties.content,
        enabled=enabled if enabled is not None else existing_object.properties.enabled,
        ttl=ttl if ttl is not None else existing_object.properties.ttl,
        priority=priority if priority is not None else existing_object.properties.priority,
    )
    record = ionoscloud_dnsaas.RecordUpdateRequest(properties=record_properties)

    try:
        response = records_api.zones_records_put(zone_id, existing_object.id, record)
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: records_api.zones_records_find_by_id(zone_id, response.id).metadata.state,
                fn_check=lambda r: r == 'CREATED',
                scaleup=10000,
                timeout=int(module.params.get('wait_timeout')),
            )

        return response
    except ApiException as e:
        module.fail_json(msg="failed to update the record: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    zone_list = ionoscloud_dnsaas.ZonesApi(client).zones_get()
    zone_id = get_resource_id(
        module, zone_list, module.params.get('zone'),
        [['id'], ['properties', 'zone_name']],
    )
    records_api = ionoscloud_dnsaas.RecordsApi(client)

    try:
        records_api.zones_records_delete(zone_id, existing_object.id)
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: records_api.zones_records_get(zone_id),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == existing_object.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )
    except ApiException as e:
        module.fail_json(msg="failed to remove the record: %s" % to_native(e))


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
    module = AnsibleModule(argument_spec=get_module_arguments())

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dnsaas is required for this module, run `pip install ionoscloud_dnsaas`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud_dnsaas)) as api_client:
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
