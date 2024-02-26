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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


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
OBJECT_NAME = 'Zone'
RETURNED_KEY = 'zone'
REPO_URL = "https://github.com/ionos-cloud/module-ansible"

OPTIONS = {
    'enabled': {
        'description': ['Users can activate and deactivate zones.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'description': {
        'description': ['The hosted zone is used for...'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'name': {
        'description': ['The zone name'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'zone': {
        'description': ['The ID or name of an existing Zone.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: dns_zone
short_description: Allows operations with Ionos Cloud DNS Zones.
description:
     - This is a module that supports creating, updating or destroying DNS Zones
version_added: "2.0"
options:
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
    description:
        description:
        - The hosted zone is used for...
        required: false
    enabled:
        description:
        - Users can activate and deactivate zones.
        required: false
    name:
        description:
        - The zone name
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
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
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dns >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Zone
    dns_zone:
      name: example.com
      description: zone_description
      enabled: true
    register: zone_response
  ''',
    'update': '''- name: Update zone
    dns_zone:
      zone: example.com
      description: zone_description_update
      enabled: false
      state: update
    register: updated_zone_response
  ''',
    'absent': '''- name: Delete zone
    dns_zone:
      zone: example.com
      wait: true
      state: absent
  ''',
}

EXAMPLES = """- name: Create Zone
    dns_zone:
      name: example.com
      description: zone_description
      enabled: true
    register: zone_response
  
- name: Update zone
    dns_zone:
      zone: example.com
      description: zone_description_update
      enabled: false
      state: update
    register: updated_zone_response
  
- name: Delete zone
    dns_zone:
      zone: example.com
      wait: true
      state: absent
"""


class DnsZoneModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dns]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'zone_name']]


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('description') is not None
            and existing_object.properties.description != self.module.params.get('description')
            or self.module.params.get('enabled') is not None
            and existing_object.properties.enabled != self.module.params.get('enabled')
            or self.module.params.get('name') is not None
            and existing_object.properties.zone_name != self.module.params.get('name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_dns.ZonesApi(clients[0]).zones_get()


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('zone')


    def _create_object(self, existing_object, clients):
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        enabled = self.module.params.get('enabled')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            description = existing_object.properties.description if description is None else description
            enabled = existing_object.properties.enabled if enabled is None else enabled

        zones_api = ionoscloud_dns.ZonesApi(clients[0])
        zone = ionoscloud_dns.ZoneEnsure(
            properties=ionoscloud_dns.Zone(
                zone_name=name,
                description=description,
                enabled=enabled,
            ),
        )

        try:
            zone = zones_api.zones_put(str(uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_URL, REPO_URL), str(uuid.uuid4()))), zone)
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to create the new DNS Zone: %s" % to_native(e))
        return zone


    def _update_object(self, existing_object, clients):
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        enabled = self.module.params.get('enabled')
        if existing_object is not None:
            name = existing_object.properties.zone_name if name is None else name
            description = existing_object.properties.description if description is None else description
            enabled = existing_object.properties.enabled if enabled is None else enabled

        zone = ionoscloud_dns.ZoneEnsure(properties=ionoscloud_dns.Zone(
            zone_name=name,
            description=description,
            enabled=enabled,
        ))

        try:
            zone = ionoscloud_dns.ZonesApi(clients[0]).zones_put(zone_id=existing_object.id, zone_ensure=zone)

            return zone
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to update the DNS Zone: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        zones_api = ionoscloud_dns.ZonesApi(clients[0])

        try:
            zones_api.zones_delete(existing_object.id)
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to remove the DNS Zone: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = DnsZoneModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dns is required for this module, run `pip install ionoscloud_dns`')
    ionos_module.main()
