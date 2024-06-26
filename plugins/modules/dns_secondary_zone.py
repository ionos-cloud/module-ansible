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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, get_resource
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
STATES = ['present', 'absent', 'update', 'transfer']
OBJECT_NAME = 'Secondary Zone'
RETURNED_KEY = 'secondary_zone'
REPO_URL = "https://github.com/ionos-cloud/module-ansible"

OPTIONS = {
    'name': {
        'description': ['The zone name'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'description': {
        'description': ['The hosted zone is used for...'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'primary_ips': {
        'description': ['Indicates IP addresses of primary nameservers for a secondary zone. Accepts IPv4 and IPv6 addresses'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'secondary_zone': {
        'description': ['The ID or name of an existing Secondary Zone.'],
        'available': ['update', 'absent', 'transfer'],
        'required': ['update', 'absent', 'transfer'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: dns_secondary_zone
short_description: Allows operations with Ionos Cloud DNS Secondary Zones.
description:
     - This is a module that supports creating, updating or destroying DNS Secondary Zones
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
    primary_ips:
        description:
        - Indicates IP addresses of primary nameservers for a secondary zone. Accepts
            IPv4 and IPv6 addresses
        required: false
    secondary_zone:
        description:
        - The ID or name of an existing Secondary Zone.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        - transfer
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
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dns >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Secondary Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  name: 'test.example.test.ansible.com'
  description: 'test_description'
  primary_ips: ''
register: zone_response
''',
    'update': '''
name: Update Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  description: 'zone_description_updated'
  primary_ips: ''
  allow_replace: false
  state: update
register: updated_zone_response
''',
    'transfer': '''
name: Transfer Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  wait: false
  state: transfer
''',
    'absent': '''
name: Delete Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  wait: true
  state: absent
''',
}

EXAMPLES = """
name: Create Secondary Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  name: 'test.example.test.ansible.com'
  description: 'test_description'
  primary_ips: ''
register: zone_response


name: Update Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  description: 'zone_description_updated'
  primary_ips: ''
  allow_replace: false
  state: update
register: updated_zone_response


name: Transfer Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  wait: false
  state: transfer


name: Delete Zone
ionoscloudsdk.ionoscloud.dns_secondary_zone:
  secondary_zone: ''
  wait: true
  state: absent
"""


class DnsSecondaryZoneModule(CommonIonosModule):
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
            or self.module.params.get('primary_ips') is not None
            and sorted(existing_object.properties.primary_ips) != sorted(self.module.params.get('primary_ips'))
            or self.module.params.get('name') is not None
            and existing_object.properties.zone_name != self.module.params.get('name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_dns.SecondaryZonesApi(clients[0]).secondaryzones_get()


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('secondary_zone')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        primary_ips = self.module.params.get('primary_ips')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            description = existing_object.properties.description if description is None else description
            primary_ips = existing_object.properties.primary_ips if primary_ips is None else primary_ips

        secondary_zones_api = ionoscloud_dns.SecondaryZonesApi(client)
        secondary_zone = ionoscloud_dns.SecondaryZoneEnsure(
            properties=ionoscloud_dns.SecondaryZone(
                zone_name=name,
                description=description,
                primary_ips=primary_ips,
            ),
        )

        try:
            secondary_zone = secondary_zones_api.secondaryzones_put(
                str(uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_URL, REPO_URL), str(uuid.uuid4()))),
                secondary_zone,
            )
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to create the new DNS Secondary Zone: %s" % to_native(e))
        return secondary_zone


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        primary_ips = self.module.params.get('primary_ips')
        if existing_object is not None:
            name = existing_object.properties.zone_name if name is None else name
            description = existing_object.properties.description if description is None else description
            primary_ips = existing_object.properties.primary_ips if primary_ips is None else primary_ips

        secondary_zones_api = ionoscloud_dns.SecondaryZonesApi(client)
        secondary_zone = ionoscloud_dns.SecondaryZoneEnsure(
            properties=ionoscloud_dns.SecondaryZone(
                zone_name=name,
                description=description,
                primary_ips=primary_ips,
            ),
        )

        try:
            zone = secondary_zones_api.secondaryzones_put(existing_object.id, secondary_zone)

            return zone
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to update the DNS Secondary Zone: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        try:
            ionoscloud_dns.SecondaryZonesApi(clients[0]).secondaryzones_delete(existing_object.id)
        except ionoscloud_dns.ApiException as e:
            self.module.fail_json(msg="failed to remove the DNS Secondary Zone: %s" % to_native(e))


    def transfer_object(self, clients):
        client = clients[0]
        existing_object = get_resource(
            self.module, self._get_object_list(clients),
            self._get_object_identifier(), self.object_identity_paths,
        )
        ionoscloud_dns.SecondaryZonesApi(client).secondaryzones_axfr_put(existing_object.id)

        if self.module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: ionoscloud_dns.SecondaryZonesApi(client).secondaryzones_axfr_get(existing_object.id).items,
                fn_check=lambda r: all([ip.status == 'Ok' for ip in r]),
                scaleup=10000,
                timeout=int(self.module.params.get('wait_timeout')),
            )
        return {
            'action': 'transfer',
            'changed': True,
            'id': existing_object.id,
        }

if __name__ == '__main__':
    ionos_module = DnsSecondaryZoneModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dns is required for this module, run `pip install ionoscloud_dns`')
    ionos_module.main()
