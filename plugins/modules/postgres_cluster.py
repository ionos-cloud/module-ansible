from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource, get_resource_id, get_paginated,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT_CLOUDAPI = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-postgres/%s' % (
    __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Postgres Cluster'
RETURNED_KEY = 'postgres_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'postgres_version': {
        'description': ['The PostgreSQL version of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster (one master and n-1 standbys).'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'cores': {
        'description': ['The number of CPU cores per instance.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'ram': {
        'description': ['The amount of memory per instance in megabytes. Has to be a multiple of 1024.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_size': {
        'description': ['The amount of storage per instance in megabytes.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_type': {
        'description': ['The storage type used in your cluster. (Value "SSD" is deprecated. Use the equivalent "SSD Premium" instead)'],
        'available': ['present'],
        'choices_docs': ['HDD', 'SSD', 'SSD Standard', 'SSD Premium'],
        'required': ['present'],
        'type': 'str',
    },
    'connections': {
        'description': ['Array of datacenters to connect to your cluster.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'location': {
        'description': ['The physical location where the cluster will be created. This will be where all of your instances live. Property cannot be modified after datacenter creation.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'display_name': {
        'description': ['The friendly name of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'db_username': {
        'description': ['The username for the initial PostgreSQL user. Some system usernames are restricted (e.g. "postgres", "admin", "standby").'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The password for the initial postgres user.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'synchronization_mode': {
        'description': ['Represents different modes of replication.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'backup_location': {
        'description': ['The S3 location where the backups will be stored.'],
        'available': ['present'],
        'type': 'str',
    },
    'backup_id': {
        'description': ['The ID of the backup to be used.'],
        'available': ['present', 'restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'recovery_target_time': {
        'description': ['Recovery target time.'],
        'available': ['present', 'restore'],
        'type': 'str',
    },
    'postgres_cluster': {
        'description': ['The ID or name of an existing Postgres Cluster.'],
        'available': ['update', 'absent', 'restore'],
        'required': ['update', 'absent', 'restore'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "connections", "note": "" },
    { "name": "backup_location", "note": "" },
    { "name": "location", "note": "" },
    { "name": "synchronization_mode", "note": "" },
    { "name": "storage_type", "note": "" },
]

DOCUMENTATION = """
module: postgres_cluster
short_description: Allows operations with Ionos Cloud Postgres Clusters.
description:
     - This is a module that supports creating, updating, restoring or destroying Postgres Clusters
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
    backup_id:
        description:
        - The ID of the backup to be used.
        required: false
    backup_location:
        description:
        - The S3 location where the backups will be stored.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    connections:
        description:
        - Array of datacenters to connect to your cluster.
        elements: dict
        required: false
    cores:
        description:
        - The number of CPU cores per instance.
        required: false
    db_password:
        description:
        - The password for the initial postgres user.
        no_log: true
        required: false
    db_username:
        description:
        - The username for the initial PostgreSQL user. Some system usernames are restricted
            (e.g. "postgres", "admin", "standby").
        no_log: true
        required: false
    display_name:
        description:
        - The friendly name of your cluster.
        required: false
    instances:
        description:
        - The total number of instances in the cluster (one master and n-1 standbys).
        required: false
    location:
        description:
        - The physical location where the cluster will be created. This will be where
            all of your instances live. Property cannot be modified after datacenter creation.
        required: false
    maintenance_window:
        description:
        - A weekly 4 hour-long window, during which maintenance might occur.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    postgres_cluster:
        description:
        - The ID or name of an existing Postgres Cluster.
        required: false
    postgres_version:
        description:
        - The PostgreSQL version of your cluster.
        required: false
    ram:
        description:
        - The amount of memory per instance in megabytes. Has to be a multiple of 1024.
        required: false
    recovery_target_time:
        description:
        - Recovery target time.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        - restore
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    storage_size:
        description:
        - The amount of storage per instance in megabytes.
        required: false
    storage_type:
        choices:
        - HDD
        - SSD
        - SSD Standard
        - SSD Premium
        description:
        - The storage type used in your cluster. (Value "SSD" is deprecated. Use the equivalent
            "SSD Premium" instead)
        required: false
    synchronization_mode:
        description:
        - Represents different modes of replication.
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
    - "ionoscloud-dbaas-postgres >= 1.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_version: 12
  instances: 1
  cores: 1
  ram: 2048
  storage_size: 20480
  storage_type: SSD Premium
  location: de/fra
  backup_location: eu-central-2
  connections:
  - cidr: 192.168.1.106/24
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS'
    lan: test_lan1
  display_name: backuptest-04
  synchronization_mode: ASYNCHRONOUS
  db_username: clusteruser
  db_password: 7357cluster
  wait: true
register: cluster_response
''',
    'update': '''
name: Update Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 4096
  storage_size: 30480
  state: update
  wait: true
register: updated_cluster_response
''',
    'absent': '''
name: Delete Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_cluster: ''
  state: absent
  wait: false
''',
}

EXAMPLES = """
name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_version: 12
  instances: 1
  cores: 1
  ram: 2048
  storage_size: 20480
  storage_type: SSD Premium
  location: de/fra
  backup_location: eu-central-2
  connections:
  - cidr: 192.168.1.106/24
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS'
    lan: test_lan1
  display_name: backuptest-04
  synchronization_mode: ASYNCHRONOUS
  db_username: clusteruser
  db_password: 7357cluster
  wait: true
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 4096
  storage_size: 30480
  state: update
  wait: true
register: updated_cluster_response


name: Delete Cluster
ionoscloudsdk.ionoscloud.postgres_cluster:
  postgres_cluster: ''
  state: absent
  wait: false
"""

class PostgresClusterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_postgres, ionoscloud]
        self.user_agents = [USER_AGENT, USER_AGENT_CLOUDAPI]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'display_name']]


    def _should_replace_object(self, existing_object, clients):
        cloudapi_client = clients[1]
        datacenter_id = lan_id = cidr = None
        if self.module.params.get('connections'):
            connection = self.module.params.get('connections')[0]
            datacenter_list = get_paginated(ionoscloud.DataCentersApi(cloudapi_client).datacenters_get)
            datacenter_id = get_resource_id(self.module, datacenter_list, connection['datacenter'])

            if datacenter_id is None:
                self.module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
            
            lan_id = get_resource_id(
                self.module,
                ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1),
                connection['lan'],
            )
            if lan_id is None:
                self.module.fail_json('LAN {} not found.'.format(connection['lan']))
            cidr = connection['cidr']

        return (
            self.module.params.get('backup_location') is not None
            and existing_object.properties.backup_location != self.module.params.get('backup_location')
            or self.module.params.get('location') is not None
            and existing_object.properties.location != self.module.params.get('location')
            or self.module.params.get('synchronization_mode') is not None
            and existing_object.properties.synchronization_mode != self.module.params.get('synchronization_mode')
            or self.module.params.get('storage_type') is not None
            and existing_object.properties.storage_type != self.module.params.get('storage_type')
            or self.module.params.get('connections') is not None
            and (
                existing_object.properties.connections[0].datacenter_id != datacenter_id
                or existing_object.properties.connections[0].lan_id != lan_id
                or existing_object.properties.connections[0].cidr != cidr
            )
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('display_name') is not None
            and existing_object.properties.display_name != self.module.params.get('display_name')
                    or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            ) or self.module.params.get('postgres_version') is not None
            and existing_object.properties.postgres_version != self.module.params.get('postgres_version')
            or self.module.params.get('instances') is not None
            and existing_object.properties.instances != self.module.params.get('instances')
            or self.module.params.get('cores') is not None
            and existing_object.properties.cores != self.module.params.get('cores')
            or self.module.params.get('ram') is not None
            and existing_object.properties.ram != self.module.params.get('ram')
        )


    def _get_object_list(self, clients):
        return ionoscloud_dbaas_postgres.ClustersApi(clients[0]).clusters_get()


    def _get_object_name(self):
        return self.module.params.get('display_name')


    def _get_object_identifier(self):
        return self.module.params.get('postgres_cluster')


    def _create_object(self, existing_object, clients):
        dbaas_client = clients[0]
        cloudapi_client = clients[1]
        maintenance_window = self.module.params.get('maintenance_window')
        if maintenance_window:
            maintenance_window = dict(self.module.params.get('maintenance_window'))
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
        backup_location=self.module.params.get('backup_location')
        if existing_object is not None:
            backup_location = existing_object.properties.backup_location if backup_location is None else backup_location
            maintenance_window = existing_object.properties.maintenance_window if maintenance_window is None else maintenance_window

        if self.module.params.get('connections'):
            connection = self.module.params.get('connections')[0]

            datacenter_id = get_resource_id(self.module, get_paginated(ionoscloud.DataCentersApi(cloudapi_client).datacenters_get, depth=2), connection['datacenter'])

            if datacenter_id is None:
                self.module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
            
            lan_id = get_resource_id(self.module, ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

            if lan_id is None:
                self.module.fail_json('LAN {} not found.'.format(connection['lan']))

            connections = [
                ionoscloud_dbaas_postgres.Connection(datacenter_id=datacenter_id, lan_id=lan_id, cidr=connection['cidr']),
            ]
        else:
            connections = existing_object.properties.connections if existing_object is not None else None

        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

        postgres_cluster_properties = ionoscloud_dbaas_postgres.CreateClusterProperties(
            postgres_version=self.module.params.get('postgres_version'),
            instances=self.module.params.get('instances'),
            cores=self.module.params.get('cores'),
            ram=self.module.params.get('ram'),
            storage_size=self.module.params.get('storage_size'),
            storage_type=self.module.params.get('storage_type'),
            connections=connections,
            location=self.module.params.get('location'),
            backup_location=backup_location,
            display_name=self.module.params.get('display_name'),
            maintenance_window=maintenance_window,
            credentials=ionoscloud_dbaas_postgres.DBUser(
                username=self.module.params.get('db_username'),
                password=self.module.params.get('db_password'),
            ),
            synchronization_mode=self.module.params.get('synchronization_mode'),
            from_backup=ionoscloud_dbaas_postgres.CreateRestoreRequest(
                backup_id=self.module.params.get('backup_id'),
                recovery_target_time=self.module.params.get('recovery_target_time'),
            ),
        )

        postgres_cluster = ionoscloud_dbaas_postgres.CreateClusterRequest(properties=postgres_cluster_properties)

        try:
            postgres_cluster = clusters_api.clusters_post(postgres_cluster)
            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                )
        except Exception as e:
            self.module.fail_json(msg="failed to create the new Postgres Cluster: %s" % to_native(e))
        return postgres_cluster


    def _update_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
        dbaas_client.wait_for(
            fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
            fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
            scaleup=10000,
        )

        maintenance_window = self.module.params.get('maintenance_window')
        if maintenance_window:
            maintenance_window = dict(self.module.params.get('maintenance_window'))
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        display_name=self.module.params.get('display_name')

        postgres_cluster_properties = ionoscloud_dbaas_postgres.PatchClusterProperties(
            postgres_version=self.module.params.get('postgres_version'),
            instances=self.module.params.get('instances'),
            cores=self.module.params.get('cores'),
            ram=self.module.params.get('ram'),
            storage_size=self.module.params.get('storage_size'),
            display_name=display_name,
            maintenance_window=maintenance_window,
        )
        postgres_cluster = ionoscloud_dbaas_postgres.PatchClusterRequest(properties=postgres_cluster_properties)

        try:
            postgres_cluster = clusters_api.clusters_patch(
                cluster_id=existing_object.id,
                patch_cluster_request=postgres_cluster,
            )

            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                )

        except Exception as e:
            self.module.fail_json(msg="failed to update the Postgres Cluster: %s" % to_native(e))
        return postgres_cluster


    def _remove_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

        try:
            if existing_object.metadata.state != 'DESTROYING':
                clusters_api.clusters_delete(existing_object.id)

            if self.module.params.get('wait'):
                try:
                    dbaas_client.wait_for(
                        fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
                        fn_check=lambda _: False,
                        scaleup=10000,
                    )
                except ionoscloud_dbaas_postgres.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))


    def restore_object(self, clients):
        dbaas_client = clients[0]
        postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

        postgres_cluster_id = get_resource_id(
            self.module,
            postgres_cluster_server.clusters_get(),
            self.module.params.get('postgres_cluster'),
            [['id'], ['properties', 'display_name']],
        )

        restore_request = ionoscloud_dbaas_postgres.CreateRestoreRequest(
            backup_id=self.module.params.get('backup_id'),
            recovery_target_time=self.module.params.get('recovery_target_time'),
        )

        try:
            ionoscloud_dbaas_postgres.RestoresApi(dbaas_client).cluster_restore_post(postgres_cluster_id, restore_request)

            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                )

            return {
                'action': 'restore',
                'changed': True,
                'id': postgres_cluster_id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to restore the Postgres cluster: %s" % to_native(e))
            return {
                'action': 'restore',
                'changed': False,
                'id': postgres_cluster_id,
            }


if __name__ == '__main__':
    ionos_module = PostgresClusterModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud ionoscloud_dbaas_postgres`')
    ionos_module.main()
