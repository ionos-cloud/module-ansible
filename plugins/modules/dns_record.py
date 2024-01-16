from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import uuid

HAS_SDK = True
try:
    import ionoscloud_dns
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dns/%s'% (
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
    **get_default_options_with_replace(STATES),
}

DOCUMENTATION = """
module: dns_record
short_description: Allows operations with Ionos Cloud DNS Records.
description:
     - This is a module that supports creating, updating or destroying DNS Records
version_added: "2.0"
options:
    allow_replace:
        default: false
        description:
        - Boolean indicating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    content:
        description:
        - The conted of the Record.
        required: false
    enabled:
        description:
        - When true - the record is visible for lookup.
        required: false
    name:
        description:
        - The Record name.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    priority:
        description:
        - Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and
            URI record types and ignored for all other types.
        required: false
    record:
        description:
        - The ID or name of an existing Record.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    ttl:
        description:
        - Time to live for the record, recommended 3600.
        required: false
    type:
        description:
        - Holds supported DNS resource record types. In the DNS context a record is a
            DNS resource record.
        options:
        - A
        - AAAA
        - CNAME
        - ALIAS
        - MX
        - NS
        - SRV
        - TXT
        - CAA
        - SSHFP
        - TLSA
        - SMIMEA
        - DS
        - HTTPS
        - SVCB
        - OPENPGPKEY
        - CERT
        - URI
        - RP
        - LOC
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
    zone:
        description:
        - The ID or name of an existing Zone.
        required: true
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dns >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

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

EXAMPLES = """- name: Create record
    dns_record:
      zone: example.com
      name: record_name
      type: MX
      content: record_content
      ttl: 3600
      priority: 10
      enabled: true
    register: record_response
  
- name: Update record
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
  
- name: Delete record
    dns_record:
      zone: example.com
      record: record_name2
      wait: true
      state: absent
"""


class DnsRecordModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dns]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('type') is not None
            and existing_object.properties.type != self.module.params.get('type')
            or self.module.params.get('content') is not None
            and existing_object.properties.content != self.module.params.get('content')
            or self.module.params.get('ttl') is not None
            and existing_object.properties.ttl != self.module.params.get('ttl')
            or self.module.params.get('priority') is not None
            and self.module.params.get('type', existing_object.properties.type) in ['MX', 'SRV', 'URI']
            and existing_object.properties.priority != self.module.params.get('priority')
            or self.module.params.get('enabled') is not None
            and existing_object.properties.enabled != self.module.params.get('enabled')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        zone_id = get_resource_id(
            self.module, ionoscloud_dns.ZonesApi(client).zones_get(),
            self.module.params.get('zone'),
            identity_paths=[['id'], ['properties', 'zone_name']],
        )

        return ionoscloud_dns.RecordsApi(client).zones_records_get(zone_id)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('record')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        record_type = self.module.params.get('type')
        content = self.module.params.get('content')
        ttl = self.module.params.get('ttl')
        priority = self.module.params.get('priority')
        enabled = self.module.params.get('enabled')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            record_type = existing_object.properties.type if record_type is None else record_type
            content = existing_object.properties.content if content is None else content
            ttl = existing_object.properties.ttl if ttl is None else ttl
            priority = existing_object.properties.priority if priority is None else priority
            enabled = existing_object.properties.enabled if enabled is None else enabled

        zone_id = get_resource_id(
            self.module, ionoscloud_dns.ZonesApi(client).zones_get(),
            self.module.params.get('zone'),
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
            self.module.fail_json(msg="failed to create the new DNS Record: %s" % to_native(e))
        return record


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        record_type = self.module.params.get('type')
        content = self.module.params.get('content')
        ttl = self.module.params.get('ttl')
        priority = self.module.params.get('priority')
        enabled = self.module.params.get('enabled')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            record_type = existing_object.properties.type if record_type is None else record_type
            content = existing_object.properties.content if content is None else content
            ttl = existing_object.properties.ttl if ttl is None else ttl
            priority = existing_object.properties.priority if priority is None else priority
            enabled = existing_object.properties.enabled if enabled is None else enabled

        zone_id = get_resource_id(
            self.module, ionoscloud_dns.ZonesApi(client).zones_get(),
            self.module.params.get('zone'),
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
            self.module.fail_json(msg="failed to update the DNS Record: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        zone_id = get_resource_id(
            self.module, ionoscloud_dns.ZonesApi(client).zones_get(),
            self.module.params.get('zone'),
            identity_paths=[['id'], ['properties', 'zone_name']],
        )
        try:
            ionoscloud_dns.RecordsApi(client).zones_records_delete(zone_id, existing_object.id)
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to remove the DNS Record: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = DnsRecordModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dns is required for this module, run `pip install ionoscloud_dns`')
    ionos_module.main()
