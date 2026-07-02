from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from functools import partial

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id, get_paginated,
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
OBJECT_NAME = 'Postgres Cluster (v2)'
RETURNED_KEY = 'postgres_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur. A dict with keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and `day_of_the_week` (e.g. "Sunday").'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'dict',
    },
    'postgres_version': {
        'description': ['The PostgreSQL version for the cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster (one primary and n-1 secondary).'],
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
        'description': ['The amount of memory per instance in gigabytes (GB).'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_size': {
        'description': ['The amount of storage per instance in gigabytes (GB).'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'connection': {
        'description': [
            'Connection information of the PostgreSQL cluster. A dict with keys '
            '`datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` '
            '(IP and netmask of the cluster\'s primary instance, e.g. 192.168.1.101/24).',
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'dict',
    },
    'replication_mode': {
        'description': ['Defines the replication mode across instances. - `ASYNCHRONOUS`: Propagates updates to other instances without waiting for confirmation. Offers higher performance but may result in temporary data inconsistencies during replication delays. - `STRICTLY_SYNCHRONOUS`: Only supported for clusters with at least 3 instances. Requires all instances to acknowledge the update before it is committed, guaranteeing strong consistency at the cost of potential performance impact in high-latency environments.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'choices_docs': ['ASYNCHRONOUS', 'STRICTLY_SYNCHRONOUS'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of your PostgreSQL cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'db_username': {
        'description': ['The username of the master database user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`).'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The password for the master database user. Must meet the following requirements: - At least 8 characters long. - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
        'no_log': True,
    },
    'db_database': {
        'description': ['The name of the initial database to be created. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
    },
    'connection_pooler': {
        'description': ['Defines how database connections are managed and reused. Default value is DISABLED. DISABLED: No connection pooling is used. Each request opens a new connection, which is closed immediately after use. It ensures isolation but may impact performance due to frequent connection setup and teardown. TRANSACTION: Connections are pooled and reused for the duration of a transaction. Once the transaction completes, the connection is returned to the pool. This mode balances efficiency with transactional integrity. SESSION: Connections are retained for the entire session and reused across multiple transactions. Offers the highest performance by minimizing connection overhead, but may tie up resources longer.'],
        'available': ['present', 'update'],
        'choices_docs': ['DISABLED', 'TRANSACTION', 'SESSION'],
        'type': 'str',
    },
    'backup_location': {
        'description': ['The Object Storage location where the backup will be created. The BackupLocations provides a list of supported locations.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'backup_retention_days': {
        'description': ['Configures how many days cluster backups are retained.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'logs_enabled': {
        'description': ['Allows or disallows the collection and reporting of logs for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; log collection will not be enabled until the observability service is activated.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'metrics_enabled': {
        'description': ['Allows or disallows the collection and reporting of metrics for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; metric collection will not be enabled until the observability service is activated.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'backup_id': {
        'description': ['The ID of the backup to initialize the cluster from when creating (restore from an existing backup).'],
        'available': ['present'],
        'type': 'str',
    },
    'recovery_target_time': {
        'description': ['Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation, or for an in-place restore when state is `restore`.'],
        'available': ['present', 'restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'postgres_cluster': {
        'description': ['The ID or name of an existing Postgres Cluster.'],
        'available': ['update', 'absent', 'restore'],
        'required': ['update', 'absent', 'restore'],
        'type': 'str',
    },
    'location': {
        'description': ['The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/txl". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    {"name": "connection", "note": ""},
    {"name": "backup_location", "note": ""},
]

DOCUMENTATION = """
module: postgres_cluster_v2
short_description: Allows operations with IONOS CLOUD Postgres Clusters (DBaaS PostgreSQL v2 API).
description:
     - This module supports creating, updating, restoring or destroying Postgres Clusters using
       the DBaaS PostgreSQL v2 API. The cluster region is selected through the I(location) option;
       I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).
version_added: "2.0"
options:
    location:
        description:
        - 'The location (region) in which the cluster will be created. Different service
            endpoints are used based on location, possible options are: "de/fra", "de/txl",
            "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not
            set, the endpoint will be the one corresponding to "de/txl". The api_url, if
            set, overrides this.'
        required: false
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
        - The ID of the backup to initialize the cluster from when creating (restore from
            an existing backup).
        required: false
    backup_location:
        description:
        - The Object Storage location where the backup will be created. The BackupLocations
            provides a list of supported locations.
        required: false
    backup_retention_days:
        description:
        - Configures how many days cluster backups are retained.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    connection:
        description:
        - Connection information of the PostgreSQL cluster. A dict with keys `datacenter`
            (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask
            of the cluster's primary instance, e.g. 192.168.1.101/24).
        required: false
    connection_pooler:
        choices:
        - DISABLED
        - TRANSACTION
        - SESSION
        description:
        - 'Defines how database connections are managed and reused. Default value is DISABLED.
            DISABLED: No connection pooling is used. Each request opens a new connection,
            which is closed immediately after use. It ensures isolation but may impact
            performance due to frequent connection setup and teardown. TRANSACTION: Connections
            are pooled and reused for the duration of a transaction. Once the transaction
            completes, the connection is returned to the pool. This mode balances efficiency
            with transactional integrity. SESSION: Connections are retained for the entire
            session and reused across multiple transactions. Offers the highest performance
            by minimizing connection overhead, but may tie up resources longer.'
        required: false
    cores:
        description:
        - The number of CPU cores per instance.
        required: false
    db_database:
        description:
        - The name of the initial database to be created. Must be 63 characters or less
            and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores
            (`_`).
        required: false
    db_password:
        description:
        - 'The password for the master database user. Must meet the following requirements:
            - At least 8 characters long. - Contains at least one lowercase letter. -
            Contains at least one uppercase letter. - Contains at least one digit (0-9).
            - Contains at least one special character from the set: @$!%*?&'
        no_log: true
        required: false
    db_username:
        description:
        - The username of the master database user. Must be 16 characters or less and
            must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores
            (`_`).
        no_log: true
        required: false
    instances:
        description:
        - The total number of instances in the cluster (one primary and n-1 secondary).
        required: false
    logs_enabled:
        description:
        - Allows or disallows the collection and reporting of logs for this cluster's
            observability. If the observability service is not activated on the contract,
            this setting is accepted but has no effect; log collection will not be enabled
            until the observability service is activated.
        required: false
    maintenance_window:
        description:
        - A weekly 4 hour-long window, during which maintenance might occur. A dict with
            keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and
            `day_of_the_week` (e.g. "Sunday").
        required: false
    metrics_enabled:
        description:
        - Allows or disallows the collection and reporting of metrics for this cluster's
            observability. If the observability service is not activated on the contract,
            this setting is accepted but has no effect; metric collection will not be
            enabled until the observability service is activated.
        required: false
    name:
        description:
        - The name of your PostgreSQL cluster. Must be 63 characters or less and must
            begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`),
            underscores (`_`), dots (`.`), and alphanumerics between.
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
        - The PostgreSQL version for the cluster.
        required: false
    ram:
        description:
        - The amount of memory per instance in gigabytes (GB).
        required: false
    recovery_target_time:
        description:
        - Recovery target time (ISO 8601). Used to replay backups up to the specified
            time on creation, or for an in-place restore when state is `restore`.
        required: false
    replication_mode:
        choices:
        - ASYNCHRONOUS
        - STRICTLY_SYNCHRONOUS
        description:
        - 'Defines the replication mode across instances. - `ASYNCHRONOUS`: Propagates
            updates to other instances without waiting for confirmation. Offers higher
            performance but may result in temporary data inconsistencies during replication
            delays. - `STRICTLY_SYNCHRONOUS`: Only supported for clusters with at least
            3 instances. Requires all instances to acknowledge the update before it is
            committed, guaranteeing strong consistency at the cost of potential performance
            impact in high-latency environments.'
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
        - The amount of storage per instance in gigabytes (GB).
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
    - "python >= 3.8"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dbaas-postgres >= 3.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_version: '16'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  replication_mode: ASYNCHRONOUS
  maintenance_window: ''
  backup_location: ''
  backup_retention_days: 7
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  wait: true
  wait_timeout: ''
register: cluster_response
''',
    'update': '''
name: Update Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  storage_size: 20
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response
''',
    'restore': '''
name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  postgres_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  state: restore
  wait: true
''',
    'absent': '''
name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  state: absent
  wait: false
''',
}

EXAMPLES = """
name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_version: '16'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  replication_mode: ASYNCHRONOUS
  maintenance_window: ''
  backup_location: ''
  backup_retention_days: 7
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  wait: true
  wait_timeout: ''
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  storage_size: 20
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  postgres_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  state: restore
  wait: true


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  state: absent
  wait: false
"""


class PostgresClusterV2Module(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_postgres, ionoscloud]
        self.user_agents = [USER_AGENT, USER_AGENT_CLOUDAPI]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'name']]

    def _wait_until_available(self, clusters_api, dbaas_client, cluster_id):
        """Wait until the cluster reaches AVAILABLE, honouring wait_timeout and failing fast on FAILED."""
        def check_state(cluster):
            if cluster.metadata.state == 'FAILED':
                raise Exception(
                    'Postgres Cluster {} entered FAILED state: {}'.format(
                        cluster_id, getattr(cluster.metadata, 'status_message', None)))
            return cluster.metadata.state == 'AVAILABLE'

        dbaas_client.wait_for(
            fn_request=lambda: clusters_api.clusters_find_by_id(cluster_id),
            fn_check=check_state,
            timeout=self.module.params.get('wait_timeout'),
        )

    def get_maintenance_window(self):
        maintenance_window = self.module.params.get('maintenance_window')
        if not maintenance_window:
            return None
        return ionoscloud_dbaas_postgres.MaintenanceWindow(
            time=maintenance_window.get('time'),
            day_of_the_week=maintenance_window.get('day_of_the_week'),
        )

    def _resolve_connection(self, clients):
        cloudapi_client = clients[1]
        connection = self.module.params.get('connection')
        if not connection:
            return None

        datacenter_id = get_resource_id(
            self.module,
            get_paginated(ionoscloud.DataCentersApi(cloudapi_client).datacenters_get, depth=2),
            connection.get('datacenter'),
        )
        if datacenter_id is None:
            self.module.fail_json(msg='Datacenter {} not found.'.format(connection.get('datacenter')))

        lan_id = get_resource_id(
            self.module,
            get_paginated(partial(ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get, datacenter_id), depth=1),
            connection.get('lan'),
        )
        if lan_id is None:
            self.module.fail_json(msg='LAN {} not found.'.format(connection.get('lan')))

        return ionoscloud_dbaas_postgres.PostgresClusterConnection(
            datacenter_id=datacenter_id,
            lan_id=str(lan_id),
            primary_instance_address=connection.get('primary_instance_address'),
        )

    def _build_full_cluster(self, existing_object, restore_from_backup=None):
        """Build a complete Cluster object for a PUT (Ensure), merging params over the existing cluster."""
        params = self.module.params
        existing = existing_object.properties

        def pick(param_key, existing_value):
            value = params.get(param_key)
            return value if value is not None else existing_value

        existing_instances = existing.instances
        instances = ionoscloud_dbaas_postgres.InstanceConfiguration(
            count=pick('instances', existing_instances.count if existing_instances else None),
            cores=pick('cores', existing_instances.cores if existing_instances else None),
            ram=pick('ram', existing_instances.ram if existing_instances else None),
            storage_size=pick('storage_size', existing_instances.storage_size if existing_instances else None),
        )

        backup = existing.backup
        if params.get('backup_retention_days') is not None and existing.backup is not None:
            backup = ionoscloud_dbaas_postgres.ClusterBackup(
                location=existing.backup.location,
                retention_days=params.get('backup_retention_days'),
            )

        # credentials are re-sent from the module params on every full-replace PUT, matching the
        # Terraform provider (buildClusterUpdateProperties always sets props.Credentials). The
        # writeOnly password can't be read back from the API, so it must be supplied again by the
        # caller — this is why db_username/db_password/db_database are required on update/restore.
        # Omitting credentials here would risk wiping/blanking the master user on the PUT.
        return ionoscloud_dbaas_postgres.Cluster(
            name=pick('name', existing.name),
            description=existing.description,
            version=pick('postgres_version', existing.version),
            instances=instances,
            connection=existing.connection,
            maintenance_window=self.get_maintenance_window() or existing.maintenance_window,
            replication_mode=pick('replication_mode', existing.replication_mode),
            credentials=ionoscloud_dbaas_postgres.PostgresUser(
                username=params.get('db_username'),
                password=params.get('db_password'),
                database=params.get('db_database'),
            ),
            connection_pooler=pick('connection_pooler', existing.connection_pooler),
            logs_enabled=pick('logs_enabled', existing.logs_enabled),
            metrics_enabled=pick('metrics_enabled', existing.metrics_enabled),
            backup=backup,
            restore_from_backup=restore_from_backup,
        )

    def _should_replace_object(self, existing_object, clients):
        params = self.module.params
        datacenter_id = lan_id = primary_instance_address = None
        if params.get('connection'):
            resolved = self._resolve_connection(clients)
            datacenter_id = resolved.datacenter_id
            lan_id = resolved.lan_id
            primary_instance_address = resolved.primary_instance_address

        return (
            params.get('backup_location') is not None
            and (
                existing_object.properties.backup is None
                or existing_object.properties.backup.location != params.get('backup_location')
            )
            or params.get('connection') is not None
            and (
                existing_object.properties.connection is None
                or existing_object.properties.connection.datacenter_id != datacenter_id
                or existing_object.properties.connection.lan_id != lan_id
                or existing_object.properties.connection.primary_instance_address != primary_instance_address
            )
        )

    def _should_update_object(self, existing_object, clients):
        params = self.module.params
        existing = existing_object.properties
        instances = existing.instances
        maintenance_window = params.get('maintenance_window')

        return (
            params.get('name') is not None
            and existing.name != params.get('name')
            or maintenance_window is not None
            and (
                existing.maintenance_window is None
                or existing.maintenance_window.day_of_the_week != maintenance_window.get('day_of_the_week')
                or existing.maintenance_window.time != maintenance_window.get('time')
            )
            or params.get('postgres_version') is not None
            and existing.version != params.get('postgres_version')
            or params.get('instances') is not None
            and (instances is None or instances.count != params.get('instances'))
            or params.get('cores') is not None
            and (instances is None or instances.cores != params.get('cores'))
            or params.get('ram') is not None
            and (instances is None or instances.ram != params.get('ram'))
            or params.get('storage_size') is not None
            and (instances is None or instances.storage_size != params.get('storage_size'))
            or params.get('replication_mode') is not None
            and existing.replication_mode != params.get('replication_mode')
            or params.get('connection_pooler') is not None
            and existing.connection_pooler != params.get('connection_pooler')
            or params.get('logs_enabled') is not None
            and existing.logs_enabled != params.get('logs_enabled')
            or params.get('metrics_enabled') is not None
            and existing.metrics_enabled != params.get('metrics_enabled')
            or params.get('backup_retention_days') is not None
            and existing.backup is not None
            and existing.backup.retention_days != params.get('backup_retention_days')
        )

    def _get_object_list(self, clients):
        return get_paginated(ionoscloud_dbaas_postgres.ClustersApi(clients[0]).clusters_get, depth=None)

    def _get_object_name(self):
        return self.module.params.get('name')

    def _get_object_identifier(self):
        return self.module.params.get('postgres_cluster')

    def _create_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
        params = self.module.params

        if params.get('recovery_target_time') and not params.get('backup_id'):
            self.module.fail_json(
                msg='recovery_target_time on create requires backup_id; point-in-time replay restores from an existing backup.')

        connection = self._resolve_connection(clients)
        if connection is None and existing_object is not None:
            connection = existing_object.properties.connection

        maintenance_window = self.get_maintenance_window()
        if maintenance_window is None and existing_object is not None:
            maintenance_window = existing_object.properties.maintenance_window

        restore_from_backup = None
        if params.get('backup_id'):
            restore_from_backup = ionoscloud_dbaas_postgres.ClusterRestoreFromBackup(
                ionoscloud_dbaas_postgres.PostgresRestoreClusterFromBackup(
                    source_backup_id=params.get('backup_id'),
                    recovery_target_datetime=params.get('recovery_target_time'),
                )
            )

        properties = ionoscloud_dbaas_postgres.ClusterCreateProperties(
            name=params.get('name'),
            version=params.get('postgres_version'),
            instances=ionoscloud_dbaas_postgres.InstanceConfiguration(
                count=params.get('instances'),
                cores=params.get('cores'),
                ram=params.get('ram'),
                storage_size=params.get('storage_size'),
            ),
            connection=connection,
            maintenance_window=maintenance_window,
            replication_mode=params.get('replication_mode'),
            credentials=ionoscloud_dbaas_postgres.PostgresUser(
                username=params.get('db_username'),
                password=params.get('db_password'),
                database=params.get('db_database'),
            ),
            connection_pooler=params.get('connection_pooler'),
            backup=ionoscloud_dbaas_postgres.ClusterBackup(
                location=params.get('backup_location'),
                retention_days=params.get('backup_retention_days'),
            ),
            logs_enabled=params.get('logs_enabled'),
            metrics_enabled=params.get('metrics_enabled'),
            restore_from_backup=restore_from_backup,
        )
        cluster_create = ionoscloud_dbaas_postgres.ClusterCreate(properties=properties)

        try:
            postgres_cluster = clusters_api.clusters_post(cluster_create)
            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, postgres_cluster.id)
        except Exception as e:
            self.module.fail_json(msg="failed to create the new Postgres Cluster: %s" % to_native(e))
        return postgres_cluster

    def _update_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
        self._wait_until_available(clusters_api, dbaas_client, existing_object.id)

        cluster_ensure = ionoscloud_dbaas_postgres.ClusterEnsure(
            id=existing_object.id,
            properties=self._build_full_cluster(existing_object),
        )

        try:
            postgres_cluster = clusters_api.clusters_put(existing_object.id, cluster_ensure)
            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, existing_object.id)
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
                        timeout=self.module.params.get('wait_timeout'),
                    )
                except ionoscloud_dbaas_postgres.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))

    def restore_object(self, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

        postgres_cluster_id = get_resource_id(
            self.module,
            get_paginated(clusters_api.clusters_get, depth=None),
            self.module.params.get('postgres_cluster'),
            [['id'], ['properties', 'name']],
        )
        if postgres_cluster_id is None:
            self.module.fail_json(
                msg='Postgres Cluster {} not found.'.format(self.module.params.get('postgres_cluster')))

        existing_object = clusters_api.clusters_find_by_id(postgres_cluster_id)
        self._wait_until_available(clusters_api, dbaas_client, postgres_cluster_id)

        restore_from_backup = ionoscloud_dbaas_postgres.ClusterRestoreFromBackup(
            ionoscloud_dbaas_postgres.PostgresInPlaceRestoreClusterFromBackup(
                recovery_target_datetime=self.module.params.get('recovery_target_time'),
            )
        )
        cluster_ensure = ionoscloud_dbaas_postgres.ClusterEnsure(
            id=postgres_cluster_id,
            properties=self._build_full_cluster(existing_object, restore_from_backup=restore_from_backup),
        )

        try:
            clusters_api.clusters_put(postgres_cluster_id, cluster_ensure)

            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, postgres_cluster_id)

            return {
                'action': 'restore',
                'changed': True,
                'id': postgres_cluster_id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to restore the Postgres cluster: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = PostgresClusterV2Module()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud ionoscloud_dbaas_postgres`')
    ionos_module.main()
