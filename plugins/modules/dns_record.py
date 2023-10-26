import copy
from distutils.command.config import config
from operator import mod
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re
import uuid

HAS_SDK = True
try:
    import ionoscloud_dns
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DNS_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dns/%s'% (
    __version__, ionoscloud_dns.__version__,
)
DOC_DIRECTORY = 'dns'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Record'
RETURNED_KEY = 'record'
REPO_URL = "https://github.com/ionos-cloud/module-ansible"

OPTIONS = {
    'name': {
        'description': ['The Record name.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'type': {
        'description': ['Holds supported DNS resource record types. In the DNS context a record is a DNS resource record.'],
        'options': [
            'A', 'AAAA', 'CNAME', 'ALIAS', 'MX', 'NS', 'SRV', 'TXT', 'CAA', 'SSHFP', 'TLSA', 'SMIMEA',
            'DS', 'HTTPS', 'SVCB', 'OPENPGPKEY', 'CERT', 'URI', 'RP', 'LOC'
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'content': {
        'description': ['The conted of the Record.'],
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
        'description': ['Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI record types and ignored for all other types.'],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'enabled': {
        'description': ['When true - the record is visible for lookup.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'record': {
        'description': ['The ID or name of an existing Record.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'zone': {
        'description': ['The ID or name of an existing Zone.'],
        'available': STATES,
        'required': STATES,
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


IMMUTABLE_OPTIONS = [
    { "name": "name", "note": "" },
]


def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES)
    del val['available']
    del val['type']
    return val


DOCUMENTATION = '''
---
module: dns_record
short_description: Allows operations with Ionos Cloud DNS Records.
description:
     - This is a module that supports creating, updating or destroying DNS Records
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dns >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create record
    dns_record:
      zone: example.com
      name: record_name
      type: MX
      content: record_content
      ttl: 3600
      priority: 10
      enabled: true
    register: record_response
  ''',
    'update': '''- name: Update record
    dns_record:
      zone: example.com
      record: record_name2
      name: record_name2
      type: MX
      content: record_content
      ttl: 1800
      priority: 9
      enabled: true
      state: update
    register: updated_record_response
  ''',
    'absent': '''- name: Delete record
    dns_record:
      zone: example.com
      record: record_name2
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


def _should_replace_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
    )


def _should_update_object(module, existing_object):
    return (
        module.params.get('type') is not None
        and existing_object.properties.type != module.params.get('type')
        or module.params.get('content') is not None
        and existing_object.properties.content != module.params.get('content')
        or module.params.get('ttl') is not None
        and existing_object.properties.ttl != module.params.get('ttl')
        or module.params.get('priority') is not None
        and module.params.get('type', existing_object.properties.type) in ['MX', 'SRV', 'URI']
        and existing_object.properties.priority != module.params.get('priority')
        or module.params.get('enabled') is not None
        and existing_object.properties.enabled != module.params.get('enabled')
    )


def _get_object_list(module, client):
    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )

    return ionoscloud_dns.RecordsApi(client).zones_records_get(zone_id)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('record')


def _create_object(module, client, existing_object=None):
    name = module.params.get('name')
    record_type = module.params.get('type')
    content = module.params.get('content')
    ttl = module.params.get('ttl')
    priority = module.params.get('priority')
    enabled = module.params.get('enabled')

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        record_type = existing_object.properties.type if record_type is None else record_type
        content = existing_object.properties.content if content is None else content
        ttl = existing_object.properties.ttl if ttl is None else ttl
        priority = existing_object.properties.priority if priority is None else priority
        enabled = existing_object.properties.enabled if enabled is None else enabled

    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )
    record = ionoscloud_dns.RecordEnsure(
        properties=ionoscloud_dns.Record(
            name=name, type=record_type,content=content,
            ttl=ttl, priority=priority, enabled=enabled,
        ),
    )

    try:
        record = ionoscloud_dns.RecordsApi(client).zones_records_put(
            zone_id, str(uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_URL, REPO_URL), str(uuid.uuid4()))), record,
        )
    except ionoscloud_dns.ApiException as e:
        module.fail_json(msg="failed to create the new DNS Record: %s" % to_native(e))
    return record


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    record_type = module.params.get('type')
    content = module.params.get('content')
    ttl = module.params.get('ttl')
    priority = module.params.get('priority')
    enabled = module.params.get('enabled')

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        record_type = existing_object.properties.type if record_type is None else record_type
        content = existing_object.properties.content if content is None else content
        ttl = existing_object.properties.ttl if ttl is None else ttl
        priority = existing_object.properties.priority if priority is None else priority
        enabled = existing_object.properties.enabled if enabled is None else enabled

    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )
    record = ionoscloud_dns.RecordEnsure(
        properties=ionoscloud_dns.Record(
            name=name, type=record_type,content=content,
            ttl=ttl, priority=priority, enabled=enabled,
        ),
    )

    try:
        record = ionoscloud_dns.RecordsApi(client).zones_records_put(
            zone_id=zone_id, record_id=existing_object.id, record_ensure=record,
        )

        return record
    except ionoscloud_dns.ApiException as e:
        module.fail_json(msg="failed to update the DNS Record: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    zone_id = get_resource_id(
        module, ionoscloud_dns.ZonesApi(client).zones_get(),
        module.params.get('zone'),
        identity_paths=[['id'], ['properties', 'zone_name']],
    )
    try:
        ionoscloud_dns.RecordsApi(client).zones_records_delete(zone_id, existing_object.id)
    except ionoscloud_dns.ApiException as e:
        module.fail_json(msg="failed to remove the DNS Record: %s" % to_native(e))


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
    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_name(module),
    )
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

    existing_object = get_resource(
        module, object_list, _get_object_identifier(module),
    )

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
    existing_object = get_resource(
        module, _get_object_list(module, client),
        _get_object_identifier(module),
    )

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
            msg='Token or username & password are required for {object_name}'.format(
                object_name=object_name,
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
        module.fail_json(msg='ionoscloud_dns is required for this module, '
                             'run `pip install ionoscloud_dns`')


    client = ionoscloud_dns.ApiClient(get_sdk_config(module, ionoscloud_dns))
    client.user_agent = DNS_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, client))
        elif state == 'update':
            module.exit_json(**update_object(module, client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()