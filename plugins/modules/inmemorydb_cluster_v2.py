from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from functools import partial

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_inmemorydb
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
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-in-memory-db/%s' % (
    __version__, ionoscloud_dbaas_inmemorydb.__version__)
DOC_DIRECTORY = 'dbaas-in-memory-db'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'In-Memory DB Cluster (v2)'
RETURNED_KEY = 'inmemorydb_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur. A dict with keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and `day_of_the_week` (e.g. "Sunday").'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'dict',
    },
    'version': {
        'description': ['The In-Memory DB version of the cluster. Use the inmemorydb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster. A value of 1 creates a standalone instance; values 2-5 create a replicated setup with one primary and n-1 passive secondaries.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'cores': {
        'description': ['The number of dedicated CPU cores per instance.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'ram': {
        'description': ['The amount of memory per instance in gigabytes (GB). RAM cannot be downgraded because storage size is automatically derived from RAM.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'connection': {
        'description': [
            'Connection information of the In-Memory DB cluster. A dict with keys '
            '`datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` '
            '(IP and netmask of the cluster\'s primary instance in CIDR notation, e.g. 192.168.1.101/24).',
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'dict',
    },
    'eviction_policy': {
        'description': ['The key eviction policy applied when the memory limit is reached.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'choices_docs': ['noeviction', 'allkeys-lru', 'allkeys-lfu', 'allkeys-random', 'volatile-lru', 'volatile-lfu', 'volatile-random', 'volatile-ttl'],
        'type': 'str',
    },
    'persistence_mode': {
        'description': ['Specifies how and whether data is persisted to disk. `None` disables persistence; `AOF` logs every write operation; `RDB` takes periodic point-in-time snapshots; `RDB_AOF` combines both.'],
        'available': ['present', 'update'],
        'choices_docs': ['None', 'AOF', 'RDB', 'RDB_AOF'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of your In-Memory DB cluster. Must be 2-63 characters and must begin and end with an alphanumeric character (`[A-Za-z0-9]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'db_username': {
        'description': ['The username for the initial In-Memory DB user. Must be 2-16 characters and may only contain alphanumeric characters (`[A-Za-z0-9]`) and underscores (`_`). Restricted usernames (for example, admin, standby) are not allowed. Required when creating a cluster; on update and restore it may be omitted to keep the existing user unchanged. Supply db_username and db_password_hash together to (re)set the user or rotate its password; because the API never returns the hash for comparison, providing them always triggers an update (reported as changed).'],
        'available': ['present', 'update', 'restore'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password_hash': {
        'description': ['The pre-hashed password for the initial In-Memory DB user. The hex-encoded hash of the password; must be exactly 64 lowercase hexadecimal characters (the standard output of SHA-256). Note: base64-encoded SHA-256 hashes (44 characters) are not accepted. The plaintext password is never sent to nor returned by the API. Required when creating a cluster; on update and restore it may be omitted to leave the current password unchanged. Supplying it (together with db_username) always (re)sets the password and reports the task as changed, since the API never returns the hash for comparison; omit it for idempotent runs.'],
        'available': ['present', 'update', 'restore'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password_algorithm': {
        'description': ['The hashing algorithm used to produce db_password_hash.'],
        'available': ['present', 'update', 'restore'],
        'choices_docs': ['SHA-256'],
        'default': 'SHA-256',
        'type': 'str',
        'no_log': False,
    },
    'snapshot_location': {
        'description': ['The Object Storage location where snapshots will be stored. For added data safety, use a different location than the cluster. The inmemorydb_snapshot_location_v2_info module provides a list of supported locations. Changing this forces the cluster to be re-created.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'snapshot_retention_days': {
        'description': ['The number of days snapshots are retained before being automatically deleted. Reducing this value causes the platform to purge any existing snapshots that fall outside the new retention window.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'snapshot_hours': {
        'description': ['Hours of the day (UTC) at which snapshots are scheduled to be taken. Each value must be between 0 and 23. At least one hour must be specified.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
        'elements': 'int',
    },
    'description': {
        'description': ['A human-readable description for the cluster.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'logs_enabled': {
        'description': ['Activates or deactivates log collection and reporting for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'metrics_enabled': {
        'description': ['Activates or deactivates metrics collection and reporting for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'source_snapshot_id': {
        'description': ['The ID of the snapshot to initialize the cluster from when creating (restore from an existing snapshot).'],
        'available': ['present'],
        'type': 'str',
    },
    'recovery_target_time': {
        'description': ['Recovery target time (ISO 8601). Restores the cluster from the most recent snapshot taken at or before that time. Optional on create (used together with source_snapshot_id); required for an in-place restore when state is `restore`. In-Memory DB does not provide continuous point-in-time recovery; the nearest preceding snapshot is used.'],
        'available': ['present', 'restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'inmemorydb_cluster': {
        'description': ['The ID or name of an existing In-Memory DB Cluster.'],
        'available': ['update', 'absent', 'restore'],
        'required': ['update', 'absent', 'restore'],
        'type': 'str',
    },
    'location': {
        'description': ['The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/fra". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    {"name": "connection", "note": ""},
    {"name": "snapshot_location", "note": ""},
]

DOCUMENTATION = """
module: inmemorydb_cluster_v2
short_description: Allows operations with IONOS CLOUD In-Memory DB Clusters (DBaaS In-Memory DB v2 API).
description:
     - This module supports creating, updating, restoring or destroying In-Memory DB Clusters using
       the DBaaS In-Memory DB v2 API. The cluster region is selected through the I(location) option;
       I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).
version_added: "2.0"
options:
    location:
        description:
        - 'The location (region) in which the cluster will be created. Different service
            endpoints are used based on location, possible options are: "de/fra", "de/txl",
            "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not
            set, the endpoint will be the one corresponding to "de/fra". The api_url, if
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
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    connection:
        description:
        - Connection information of the In-Memory DB cluster. A dict with keys `datacenter`
            (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask
            of the cluster's primary instance in CIDR notation, e.g. 192.168.1.101/24).
        required: false
    cores:
        description:
        - The number of dedicated CPU cores per instance.
        required: false
    db_password_algorithm:
        choices:
        - SHA-256
        default: SHA-256
        description:
        - The hashing algorithm used to produce db_password_hash.
        no_log: false
        required: false
    db_password_hash:
        description:
        - 'The pre-hashed password for the initial In-Memory DB user. The hex-encoded
            hash of the password; must be exactly 64 lowercase hexadecimal characters
            (the standard output of SHA-256). Note: base64-encoded SHA-256 hashes (44
            characters) are not accepted. The plaintext password is never sent to nor
            returned by the API. Required when creating a cluster; on update and restore
            it may be omitted to leave the current password unchanged. Supplying it (together
            with db_username) always (re)sets the password and reports the task as changed,
            since the API never returns the hash for comparison; omit it for idempotent
            runs.'
        no_log: true
        required: false
    db_username:
        description:
        - The username for the initial In-Memory DB user. Must be 2-16 characters and
            may only contain alphanumeric characters (`[A-Za-z0-9]`) and underscores (`_`).
            Restricted usernames (for example, admin, standby) are not allowed. Required
            when creating a cluster; on update and restore it may be omitted to keep the
            existing user unchanged. Supply db_username and db_password_hash together
            to (re)set the user or rotate its password; because the API never returns
            the hash for comparison, providing them always triggers an update (reported
            as changed).
        no_log: true
        required: false
    description:
        description:
        - A human-readable description for the cluster.
        required: false
    eviction_policy:
        choices:
        - noeviction
        - allkeys-lru
        - allkeys-lfu
        - allkeys-random
        - volatile-lru
        - volatile-lfu
        - volatile-random
        - volatile-ttl
        description:
        - The key eviction policy applied when the memory limit is reached.
        required: false
    inmemorydb_cluster:
        description:
        - The ID or name of an existing In-Memory DB Cluster.
        required: false
    instances:
        description:
        - The total number of instances in the cluster. A value of 1 creates a standalone
            instance; values 2-5 create a replicated setup with one primary and n-1 passive
            secondaries.
        required: false
    logs_enabled:
        description:
        - Activates or deactivates log collection and reporting for this cluster's observability.
            If the observability service is not activated on the contract, this setting
            is accepted but has no effect until the service is activated.
        required: false
    maintenance_window:
        description:
        - A weekly 4 hour-long window, during which maintenance might occur. A dict with
            keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and `day_of_the_week`
            (e.g. "Sunday").
        required: false
    metrics_enabled:
        description:
        - Activates or deactivates metrics collection and reporting for this cluster's
            observability. If the observability service is not activated on the contract,
            this setting is accepted but has no effect until the service is activated.
        required: false
    name:
        description:
        - The name of your In-Memory DB cluster. Must be 2-63 characters and must begin
            and end with an alphanumeric character (`[A-Za-z0-9]`) with dashes (`-`), underscores
            (`_`), dots (`.`), and alphanumerics between.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    persistence_mode:
        choices:
        - None
        - AOF
        - RDB
        - RDB_AOF
        description:
        - 'Specifies how and whether data is persisted to disk. `None` disables persistence;
            `AOF` logs every write operation; `RDB` takes periodic point-in-time snapshots;
            `RDB_AOF` combines both.'
        required: false
    ram:
        description:
        - The amount of memory per instance in gigabytes (GB). RAM cannot be downgraded
            because storage size is automatically derived from RAM.
        required: false
    recovery_target_time:
        description:
        - Recovery target time (ISO 8601). Restores the cluster from the most recent snapshot
            taken at or before that time. Optional on create (used together with source_snapshot_id);
            required for an in-place restore when state is `restore`. In-Memory DB does
            not provide continuous point-in-time recovery; the nearest preceding snapshot
            is used.
        required: false
    snapshot_hours:
        description:
        - Hours of the day (UTC) at which snapshots are scheduled to be taken. Each value
            must be between 0 and 23. At least one hour must be specified.
        elements: int
        required: false
    snapshot_location:
        description:
        - The Object Storage location where snapshots will be stored. For added data safety,
            use a different location than the cluster. The inmemorydb_snapshot_location_v2_info
            module provides a list of supported locations. Changing this forces the cluster
            to be re-created.
        required: false
    snapshot_retention_days:
        description:
        - The number of days snapshots are retained before being automatically deleted.
            Reducing this value causes the platform to purge any existing snapshots that
            fall outside the new retention window.
        required: false
    source_snapshot_id:
        description:
        - The ID of the snapshot to initialize the cluster from when creating (restore
            from an existing snapshot).
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
    version:
        description:
        - The In-Memory DB version of the cluster. Use the inmemorydb_version_v2_info module
            (GET /versions) to retrieve the list of supported versions. To upgrade, provide
            a version listed in `can_upgrade_to` for the current version; downgrades are
            not supported.
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
    - "ionoscloud-dbaas-inmemorydb >= 1.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  version: '9.0'
  instances: 1
  cores: 1
  ram: 4
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - InMemoryDB v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  eviction_policy: noeviction
  persistence_mode: RDB
  maintenance_window: ''
  snapshot_location: ''
  snapshot_retention_days: 7
  snapshot_hours:
    - 2
  db_username: clusteruser
  db_password_hash: ''
  wait: true
  wait_timeout: ''
register: cluster_response
''',
    'update': '''
name: Update Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  db_username: clusteruser
  db_password_hash: ''
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response
''',
    'restore': '''
name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  inmemorydb_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  db_username: clusteruser
  db_password_hash: ''
  state: restore
  wait: true
''',
    'absent': '''
name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  state: absent
  wait: false
''',
}

EXAMPLES = """
name: Create Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  version: '9.0'
  instances: 1
  cores: 1
  ram: 4
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - InMemoryDB v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  eviction_policy: noeviction
  persistence_mode: RDB
  maintenance_window: ''
  snapshot_location: ''
  snapshot_retention_days: 7
  snapshot_hours:
    - 2
  db_username: clusteruser
  db_password_hash: ''
  wait: true
  wait_timeout: ''
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  db_username: clusteruser
  db_password_hash: ''
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  inmemorydb_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  db_username: clusteruser
  db_password_hash: ''
  state: restore
  wait: true


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  state: absent
  wait: false
"""


class InMemoryDBClusterV2Module(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_inmemorydb, ionoscloud]
        self.user_agents = [USER_AGENT, USER_AGENT_CLOUDAPI]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'name']]

    def _wait_until_available(self, clusters_api, dbaas_client, cluster_id):
        """Wait until the cluster reaches AVAILABLE, honouring wait_timeout and failing fast on FAILED."""
        def check_state(cluster):
            if cluster.metadata.state == 'FAILED':
                raise Exception(
                    'In-Memory DB Cluster {} entered FAILED state: {}'.format(
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
        return ionoscloud_dbaas_inmemorydb.MaintenanceWindow(
            time=maintenance_window.get('time'),
            day_of_the_week=maintenance_window.get('day_of_the_week'),
        )

    def get_credentials(self):
        """Build the credentials (User) from the module params.

        Returns None when neither db_username nor db_password_hash is supplied, which drops the
        credentials field from the PUT body (Cluster.to_dict) and leaves the existing user unchanged.
        The two must be supplied together (the API rejects a partial credentials block); supplying
        both (re)sets the user on the PUT.
        """
        params = self.module.params
        username = params.get('db_username')
        password_hash = params.get('db_password_hash')
        if username is None and password_hash is None:
            return None
        if username is None or password_hash is None:
            self.module.fail_json(msg='db_username and db_password_hash must be supplied together.')
        return ionoscloud_dbaas_inmemorydb.User(
            username=username,
            password=ionoscloud_dbaas_inmemorydb.HashedPassword(
                algorithm=params.get('db_password_algorithm'),
                hash=password_hash,
            ),
        )

    def get_snapshot_config(self, existing_snapshot=None):
        """Build a SnapshotConfiguration; snapshot_location is immutable so it is preserved from the existing cluster on update."""
        params = self.module.params
        location = params.get('snapshot_location')
        if location is None and existing_snapshot is not None:
            location = existing_snapshot.location

        retention_days = params.get('snapshot_retention_days')
        if retention_days is None and existing_snapshot is not None:
            retention_days = existing_snapshot.retention_days

        snapshot_hours = params.get('snapshot_hours')
        if snapshot_hours is None and existing_snapshot is not None:
            snapshot_hours = existing_snapshot.snapshot_hours

        return ionoscloud_dbaas_inmemorydb.SnapshotConfiguration(
            location=location,
            retention_days=retention_days,
            snapshot_hours=snapshot_hours,
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

        return ionoscloud_dbaas_inmemorydb.ClusterConnection(
            datacenter_id=datacenter_id,
            lan_id=str(lan_id),
            primary_instance_address=connection.get('primary_instance_address'),
        )

    def _build_full_cluster(self, existing_object, restore_from_snapshot=None):
        """Build a complete Cluster object for a PUT (Ensure), merging params over the existing cluster."""
        params = self.module.params
        existing = existing_object.properties

        def pick(param_key, existing_value):
            value = params.get(param_key)
            return value if value is not None else existing_value

        existing_instances = existing.instances
        instances = ionoscloud_dbaas_inmemorydb.InstanceConfiguration(
            count=pick('instances', existing_instances.count if existing_instances else None),
            cores=pick('cores', existing_instances.cores if existing_instances else None),
            ram=pick('ram', existing_instances.ram if existing_instances else None),
        )

        # credentials are sent only when db_username/db_password_hash are supplied. get_credentials()
        # returns None otherwise, which drops the credentials field from the PUT so the existing user
        # is left unchanged. Supply both to (re)set the user.
        return ionoscloud_dbaas_inmemorydb.Cluster(
            name=pick('name', existing.name),
            description=pick('description', existing.description),
            version=pick('version', existing.version),
            instances=instances,
            connection=existing.connection,
            persistence_mode=pick('persistence_mode', existing.persistence_mode),
            eviction_policy=pick('eviction_policy', existing.eviction_policy),
            snapshot=self.get_snapshot_config(existing.snapshot),
            maintenance_window=self.get_maintenance_window() or existing.maintenance_window,
            credentials=self.get_credentials(),
            logs_enabled=pick('logs_enabled', existing.logs_enabled),
            metrics_enabled=pick('metrics_enabled', existing.metrics_enabled),
            restore_from_snapshot=restore_from_snapshot,
        )

    def _should_replace_object(self, existing_object, clients):
        params = self.module.params
        existing = existing_object.properties
        datacenter_id = lan_id = primary_instance_address = None
        if params.get('connection'):
            resolved = self._resolve_connection(clients)
            datacenter_id = resolved.datacenter_id
            lan_id = resolved.lan_id
            primary_instance_address = resolved.primary_instance_address

        return (
            params.get('snapshot_location') is not None
            and (
                existing.snapshot is None
                or existing.snapshot.location != params.get('snapshot_location')
            )
            or params.get('connection') is not None
            and (
                existing.connection is None
                or existing.connection.datacenter_id != datacenter_id
                or existing.connection.lan_id != lan_id
                or existing.connection.primary_instance_address != primary_instance_address
            )
        )

    def _should_update_object(self, existing_object, clients):
        params = self.module.params
        existing = existing_object.properties
        instances = existing.instances
        maintenance_window = params.get('maintenance_window')
        snapshot = existing.snapshot

        # Supplying credentials (re)sets the user/password. The API never returns the password hash,
        # so it can't be compared against the desired value; when the caller provides credentials
        # (db_username and db_password_hash — the API requires the pair) we treat it as an intentional
        # (re)set and trigger the PUT (reported as changed). Omit them for idempotent runs — the
        # existing user is then left unchanged.
        if self.get_credentials() is not None:
            return True

        return (
            params.get('name') is not None
            and existing.name != params.get('name')
            or params.get('description') is not None
            and existing.description != params.get('description')
            or maintenance_window is not None
            and (
                existing.maintenance_window is None
                or existing.maintenance_window.day_of_the_week != maintenance_window.get('day_of_the_week')
                or existing.maintenance_window.time != maintenance_window.get('time')
            )
            or params.get('version') is not None
            and existing.version != params.get('version')
            or params.get('instances') is not None
            and (instances is None or instances.count != params.get('instances'))
            or params.get('cores') is not None
            and (instances is None or instances.cores != params.get('cores'))
            or params.get('ram') is not None
            and (instances is None or instances.ram != params.get('ram'))
            or params.get('eviction_policy') is not None
            and existing.eviction_policy != params.get('eviction_policy')
            or params.get('persistence_mode') is not None
            and existing.persistence_mode != params.get('persistence_mode')
            or params.get('logs_enabled') is not None
            and existing.logs_enabled != params.get('logs_enabled')
            or params.get('metrics_enabled') is not None
            and existing.metrics_enabled != params.get('metrics_enabled')
            or params.get('snapshot_retention_days') is not None
            and snapshot is not None
            and snapshot.retention_days != params.get('snapshot_retention_days')
            or params.get('snapshot_hours') is not None
            and snapshot is not None
            and sorted(snapshot.snapshot_hours or []) != sorted(params.get('snapshot_hours'))
        )

    def _get_object_list(self, clients):
        return get_paginated(ionoscloud_dbaas_inmemorydb.ClustersApi(clients[0]).clusters_get, depth=None)

    def _get_object_name(self):
        return self.module.params.get('name')

    def _get_object_identifier(self):
        return self.module.params.get('inmemorydb_cluster')

    def _create_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_inmemorydb.ClustersApi(dbaas_client)
        params = self.module.params

        if params.get('recovery_target_time') and not params.get('source_snapshot_id'):
            self.module.fail_json(
                msg='recovery_target_time on create requires source_snapshot_id; point-in-time recovery restores from an existing snapshot.')

        credentials = self.get_credentials()
        if credentials is None:
            self.module.fail_json(
                msg='db_username and db_password_hash are required to create the In-Memory DB Cluster '
                    '(this also applies when a change to an immutable property triggers a re-create).')

        connection = self._resolve_connection(clients)
        if connection is None and existing_object is not None:
            connection = existing_object.properties.connection

        maintenance_window = self.get_maintenance_window()
        if maintenance_window is None and existing_object is not None:
            maintenance_window = existing_object.properties.maintenance_window

        restore_from_snapshot = None
        if params.get('source_snapshot_id'):
            restore_from_snapshot = ionoscloud_dbaas_inmemorydb.ClusterRestoreFromSnapshot(
                ionoscloud_dbaas_inmemorydb.RestoreClusterFromSnapshot(
                    source_snapshot_id=params.get('source_snapshot_id'),
                    recovery_target_datetime=params.get('recovery_target_time'),
                )
            )

        properties = ionoscloud_dbaas_inmemorydb.ClusterCreateProperties(
            name=params.get('name'),
            description=params.get('description'),
            version=params.get('version'),
            instances=ionoscloud_dbaas_inmemorydb.InstanceConfiguration(
                count=params.get('instances'),
                cores=params.get('cores'),
                ram=params.get('ram'),
            ),
            connection=connection,
            persistence_mode=params.get('persistence_mode'),
            eviction_policy=params.get('eviction_policy'),
            snapshot=self.get_snapshot_config(),
            maintenance_window=maintenance_window,
            credentials=credentials,
            logs_enabled=params.get('logs_enabled'),
            metrics_enabled=params.get('metrics_enabled'),
            restore_from_snapshot=restore_from_snapshot,
        )
        cluster_create = ionoscloud_dbaas_inmemorydb.ClusterCreate(properties=properties)

        try:
            inmemorydb_cluster = clusters_api.clusters_post(cluster_create)
            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, inmemorydb_cluster.id)
        except Exception as e:
            self.module.fail_json(msg="failed to create the new In-Memory DB Cluster: %s" % to_native(e))
        return inmemorydb_cluster

    def _update_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_inmemorydb.ClustersApi(dbaas_client)
        self._wait_until_available(clusters_api, dbaas_client, existing_object.id)

        cluster_ensure = ionoscloud_dbaas_inmemorydb.ClusterEnsure(
            id=existing_object.id,
            properties=self._build_full_cluster(existing_object),
        )

        try:
            inmemorydb_cluster = clusters_api.clusters_put(existing_object.id, cluster_ensure)
            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, existing_object.id)
        except Exception as e:
            self.module.fail_json(msg="failed to update the In-Memory DB Cluster: %s" % to_native(e))
        return inmemorydb_cluster

    def _remove_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_inmemorydb.ClustersApi(dbaas_client)

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
                except ionoscloud_dbaas_inmemorydb.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the In-Memory DB cluster: %s" % to_native(e))

    def restore_object(self, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_inmemorydb.ClustersApi(dbaas_client)

        inmemorydb_cluster_id = get_resource_id(
            self.module,
            get_paginated(clusters_api.clusters_get, depth=None),
            self.module.params.get('inmemorydb_cluster'),
            [['id'], ['properties', 'name']],
        )
        if inmemorydb_cluster_id is None:
            self.module.fail_json(
                msg='In-Memory DB Cluster {} not found.'.format(self.module.params.get('inmemorydb_cluster')))

        existing_object = clusters_api.clusters_find_by_id(inmemorydb_cluster_id)
        self._wait_until_available(clusters_api, dbaas_client, inmemorydb_cluster_id)

        restore_from_snapshot = ionoscloud_dbaas_inmemorydb.ClusterRestoreFromSnapshot(
            ionoscloud_dbaas_inmemorydb.InPlaceRestoreClusterFromSnapshot(
                recovery_target_datetime=self.module.params.get('recovery_target_time'),
            )
        )
        cluster_ensure = ionoscloud_dbaas_inmemorydb.ClusterEnsure(
            id=inmemorydb_cluster_id,
            properties=self._build_full_cluster(existing_object, restore_from_snapshot=restore_from_snapshot),
        )

        try:
            clusters_api.clusters_put(inmemorydb_cluster_id, cluster_ensure)

            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, inmemorydb_cluster_id)

            return {
                'action': 'restore',
                'changed': True,
                'id': inmemorydb_cluster_id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to restore the In-Memory DB cluster: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = InMemoryDBClusterV2Module()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dbaas_inmemorydb are required for this module, run `pip install ionoscloud ionoscloud_dbaas_inmemorydb`')
    ionos_module.main()
