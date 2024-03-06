from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_container_registry
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-container-registry/%s'% (
    __version__, ionoscloud_container_registry.__version__,
)
DOC_DIRECTORY = 'container-registry'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Registry'
RETURNED_KEY = 'registry'

OPTIONS = {
    'garbage_collection_schedule': {
        'description': [
            'Dict containing "time" (the time of the day when to perform the garbage_collection) '
            'and "days" (the days when to perform the garbage_collection).',
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'location': {
        'description': ['The location of your registry'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'features': {
        'description': ["Optional registry features. Format: 'vulnerability_scanning' key having a dict for value containing the 'enabled' key with a boolean value Note: Vulnerability scanning for images is enabled by default. This is a paid add-on, please make sure you specify if you do not want it enabled"],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'name': {
        'description': ['The name of your registry.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'registry': {
        'description': ['The ID or name of an existing Registry.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "name", "note": "" },
    { "name": "location", "note": "" },
    { "name": "features", "note": "changing features.vulnerability_scanning.enabled from true to false will trigger a resource replacement" },
]

DOCUMENTATION = """
module: registry
short_description: Allows operations with Ionos Cloud Registries.
description:
     - This is a module that supports creating, updating or destroying Registries
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
    features:
        description:
        - 'Optional registry features. Format: ''vulnerability_scanning'' key having a
            dict for value containing the ''enabled'' key with a boolean value Note: Vulnerability
            scanning for images is enabled by default. This is a paid add-on, please make
            sure you specify if you do not want it enabled'
        required: false
    garbage_collection_schedule:
        description:
        - Dict containing "time" (the time of the day when to perform the garbage_collection)
            and "days" (the days when to perform the garbage_collection).
        required: false
    location:
        description:
        - The location of your registry
        required: false
    name:
        description:
        - The name of your registry.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    registry:
        description:
        - The ID or name of an existing Registry.
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
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-container-registry >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''name: Create Registry
ionoscloudsdk.ionoscloud.registry:
  name: 'ansibletest123-'
  location: de/fra
  garbage_collection_schedule:
    days:
    - Wednesday
    time: 04:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  wait: true
register: registry_response
''',
    'update': '''name: Update Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  garbage_collection_schedule:
    days:
    - Wednesday
    - Sunday
    time: 06:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  allow_replace: false
  state: update
register: updated_registry_response
''',
    'absent': '''name: Delete Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  wait: true
  state: absent
''',
}

EXAMPLES = """name: Create Registry
ionoscloudsdk.ionoscloud.registry:
  name: 'ansibletest123-'
  location: de/fra
  garbage_collection_schedule:
    days:
    - Wednesday
    time: 04:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  wait: true
register: registry_response

name: Update Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  garbage_collection_schedule:
    days:
    - Wednesday
    - Sunday
    time: 06:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  allow_replace: false
  state: update
register: updated_registry_response

name: Delete Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  wait: true
  state: absent
"""


class RegistryModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_container_registry]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        features = self.module.params.get('features')
        return (
            self.module.params.get('location') is not None
            and existing_object.properties.location != self.module.params.get('location')
            or self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or features is not None
            and existing_object.properties.features.vulnerability_scanning.enabled == True
            and features.get('vulnerability_scanning', {}).get('enabled') == False
        )


    def _should_update_object(self, existing_object, clients):
        gc_schedule = self.module.params.get('garbage_collection_schedule')
        features = self.module.params.get('features')
        return (
            gc_schedule is not None
            and (
                gc_schedule.get('days') is not None
                and sorted(existing_object.properties.garbage_collection_schedule.days) != sorted(gc_schedule.get('days'))
                or gc_schedule.get('time') is not None
                and existing_object.properties.garbage_collection_schedule.time != gc_schedule.get('time')
            )
            or features.get('enabled') is not None
            and existing_object.properties.features.vulnerability_scanning.enabled == False
            and features.get('vulnerability_scanning', {}).get('enabled') == True
        )


    def _get_object_list(self, clients):
        return ionoscloud_container_registry.RegistriesApi(clients[0]).registries_get()


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('registry')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))
        gc_schedule = self.module.params.get('garbage_collection_schedule')
        features = self.module.params.get('features')
        vulnerability_scanning_feature = None
        if gc_schedule:
            gc_schedule = ionoscloud_container_registry.WeeklySchedule(
                days=gc_schedule.get('days'),
                time=gc_schedule.get('time'),
            )
        if features:
            vulnerability_scanning_feature = ionoscloud_container_registry.FeatureVulnerabilityScanning(
                enabled=features.get('vulnerability_scanning').get('enabled'),
            )
        name = self.module.params.get('name')
        location = self.module.params.get('location')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            location = existing_object.properties.location if location is None else location
            gc_schedule = existing_object.properties.garbage_collection_schedule if gc_schedule is None else gc_schedule

        registries_api = ionoscloud_container_registry.RegistriesApi(client)

        registry_properties = ionoscloud_container_registry.PostRegistryProperties(
            name=name,
            location=location,
            garbage_collection_schedule=gc_schedule,
            features=ionoscloud_container_registry.RegistryFeatures(
                vulnerability_scanning=vulnerability_scanning_feature,
            ),
        )

        registry = ionoscloud_container_registry.PostRegistryInput(properties=registry_properties)

        try:
            registry = registries_api.registries_post(registry)

            if wait:
                client.wait_for(
                    fn_request=lambda: registries_api.registries_find_by_id(registry.id).metadata.state,
                    fn_check=lambda r: r == 'Running',
                    scaleup=10000,
                    timeout=wait_timeout,
                )
            registry = registries_api.registries_find_by_id(registry.id)
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to create the new Registry: %s" % to_native(e))
        return registry


    def _update_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))
        gc_schedule = self.module.params.get('garbage_collection_schedule')
        features = self.module.params.get('features')
        vulnerability_scanning_feature = None
        if gc_schedule:
            gc_schedule = ionoscloud_container_registry.WeeklySchedule(
                days=gc_schedule.get('days'),
                time=gc_schedule.get('time'),
            )
        if features:
            vulnerability_scanning_feature = ionoscloud_container_registry.FeatureVulnerabilityScanning(
                enabled=features.get('vulnerability_scanning').get('enabled'),
            )

        registries_api = ionoscloud_container_registry.RegistriesApi(client)

        registry_properties = ionoscloud_container_registry.PatchRegistryInput(
            garbage_collection_schedule=gc_schedule,
            features=ionoscloud_container_registry.RegistryFeatures(
                vulnerability_scanning=vulnerability_scanning_feature,
            ),
        )

        try:
            registry = registries_api.registries_patch(
                registry_id=existing_object.id,
                patch_registry_input=registry_properties,
            )

            if wait:
                client.wait_for(
                    fn_request=lambda: registries_api.registries_find_by_id(registry.id).metadata.state,
                    fn_check=lambda r: r == 'Running',
                    scaleup=10000,
                    timeout=wait_timeout,
                )
            registry = registries_api.registries_find_by_id(existing_object.id)

            return registry
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to update the Registry: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        registries_api = ionoscloud_container_registry.RegistriesApi(client)
        names_api = ionoscloud_container_registry.NamesApi(client)

        try:
            registries_api.registries_delete(existing_object.id)

            if self.module.params.get('wait'):
                try:
                    client.wait_for(
                        fn_request=lambda: names_api.names_check_usage(existing_object.properties.name),
                        fn_check=lambda _: False,
                        scaleup=10000,
                    )
                except ionoscloud_container_registry.ApiException as e:
                    if e.status != 404:
                        raise e
        except ionoscloud_container_registry.ApiException as e:
            self.module.fail_json(msg="failed to remove the Registry: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = RegistryModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_container_registry is required for this module, run `pip install ionoscloud_container_registry`')
    ionos_module.main()
