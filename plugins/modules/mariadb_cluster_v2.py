from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from functools import partial

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_mariadb
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
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-mariadb/%s' % (
    __version__, ionoscloud_dbaas_mariadb.__version__)
DOC_DIRECTORY = 'dbaas-mariadb'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'MariaDB Cluster (v2)'
RETURNED_KEY = 'mariadb_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur. A dict with keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and `day_of_the_week` (e.g. "Sunday").'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'dict',
    },
    'mariadb_version': {
        'description': ['The MariaDB version of the cluster. Use the mariadb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster. A value of 1 creates a single-instance cluster; values 2 to 5 create a replicated cluster with one primary and n-1 secondary instances.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'cores': {
        'description': ['The number of CPU cores per instance. Accepted values are 1 to 62. On update, cores can be increased or decreased.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'ram': {
        'description': ['The amount of memory per instance in gigabytes (GB). Accepted values are 4 to 240. On update, RAM can be increased or decreased.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_size': {
        'description': ['The amount of storage per instance in gigabytes (GB). Accepted values are 10 to 4096. On update, storage size can only be increased; it cannot be reduced.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'connection': {
        'description': [
            'Connection information of the MariaDB cluster. A dict with keys '
            '`datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` '
            '(IP and netmask of the cluster\'s primary instance in CIDR notation, e.g. 192.168.2.101/24).',
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'dict',
    },
    'name': {
        'description': ['The name of your MariaDB cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'description': {
        'description': ['A human-readable description for the cluster.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'db_username': {
        'description': ['The username of the initial MariaDB user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`). Some usernames are reserved for platform use (for example `mariadb`, `admin`, `standby`). The credentials block is re-sent in full on every update and restore, so this option is also required for those states.'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The password for the initial MariaDB user. Must be between 10 and 256 characters long. For a strong password we recommend that it also meets the following criteria, though these are not enforced: - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?& The password is never returned by the API, so it must be supplied again on update and restore, and a change to it alone cannot be detected: a task whose only difference is a new db_password reports changed=false and sends no request.'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
        'no_log': True,
    },
    'db_database': {
        'description': ['The name of the initial database to create and grant the user access to. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).'],
        'available': ['present', 'update', 'restore'],
        'required': ['present', 'update', 'restore'],
        'type': 'str',
    },
    'backup_location': {
        'description': ['The Object Storage location where the backups are created. The mariadb_backup_location_v2_info module provides a list of supported locations. Changing this forces the cluster to be re-created.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'backup_retention_days': {
        'description': ['The number of days cluster backups are retained. Accepted values are 1 to 365. If you reduce this value, backups older than the new retention window are purged.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'logs_enabled': {
        'description': ['Activates or deactivates the collection and reporting of logs for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Log collection does not start until the observability service is active.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'metrics_enabled': {
        'description': ['Activates or deactivates the collection and reporting of metrics for this cluster\'s observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Metric collection does not start until the observability service is active.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'backup_id': {
        'description': ['The ID of the backup to initialize the cluster from when creating (restore from an existing backup).'],
        'available': ['present'],
        'type': 'str',
    },
    'recovery_target_time': {
        'description': ['Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation (together with backup_id), or for an in-place restore when state is `restore`.'],
        'available': ['present', 'restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'mariadb_cluster': {
        'description': ['The ID or name of an existing MariaDB Cluster.'],
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
module: mariadb_cluster_v2
short_description: Allows operations with IONOS CLOUD MariaDB Clusters (DBaaS MariaDB v2 API).
description:
     - This module supports creating, updating, restoring or destroying MariaDB Clusters using
       the DBaaS MariaDB v2 API. The cluster region is selected through the I(location) option;
       I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).
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
        - The ID of the backup to initialize the cluster from when creating (restore from
            an existing backup).
        required: false
    backup_location:
        description:
        - The Object Storage location where the backups are created. The mariadb_backup_location_v2_info
            module provides a list of supported locations. Changing this forces the cluster
            to be re-created.
        required: false
    backup_retention_days:
        description:
        - The number of days cluster backups are retained. Accepted values are 1 to 365.
            If you reduce this value, backups older than the new retention window are
            purged.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    connection:
        description:
        - Connection information of the MariaDB cluster. A dict with keys `datacenter`
            (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask
            of the cluster's primary instance in CIDR notation, e.g. 192.168.2.101/24).
        required: false
    cores:
        description:
        - The number of CPU cores per instance. Accepted values are 1 to 62. On update,
            cores can be increased or decreased.
        required: false
    db_database:
        description:
        - The name of the initial database to create and grant the user access to. Must
            be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`)
            and underscores (`_`).
        required: false
    db_password:
        description:
        - 'The password for the initial MariaDB user. Must be between 10 and 256 characters
            long. For a strong password we recommend that it also meets the following
            criteria, though these are not enforced: - Contains at least one lowercase
            letter. - Contains at least one uppercase letter. - Contains at least one
            digit (0-9). - Contains at least one special character from the set: @$!%*?&
            The password is never returned by the API, so it must be supplied again on
            update and restore, and a change to it alone cannot be detected: a task whose
            only difference is a new db_password reports changed=false and sends no request.'
        no_log: true
        required: false
    db_username:
        description:
        - The username of the initial MariaDB user. Must be 16 characters or less and
            must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores
            (`_`). Some usernames are reserved for platform use (for example `mariadb`,
            `admin`, `standby`). The credentials block is re-sent in full on every update
            and restore, so this option is also required for those states.
        no_log: true
        required: false
    description:
        description:
        - A human-readable description for the cluster.
        required: false
    instances:
        description:
        - The total number of instances in the cluster. A value of 1 creates a single-instance
            cluster; values 2 to 5 create a replicated cluster with one primary and n-1
            secondary instances.
        required: false
    location:
        description:
        - 'The location (region) in which the cluster will be created. Different service
            endpoints are used based on location, possible options are: "de/fra", "de/txl",
            "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not
            set, the endpoint will be the one corresponding to "de/txl". The api_url,
            if set, overrides this.'
        required: false
    logs_enabled:
        description:
        - Activates or deactivates the collection and reporting of logs for this cluster's
            observability. If the observability service is not activated on the contract,
            this setting is accepted but has no effect. Log collection does not start
            until the observability service is active.
        required: false
    maintenance_window:
        description:
        - A weekly 4 hour-long window, during which maintenance might occur. A dict with
            keys `time` (start of the maintenance window in UTC, e.g. "16:30:00") and
            `day_of_the_week` (e.g. "Sunday").
        required: false
    mariadb_cluster:
        description:
        - The ID or name of an existing MariaDB Cluster.
        required: false
    mariadb_version:
        description:
        - The MariaDB version of the cluster. Use the mariadb_version_v2_info module (GET
            /versions) to retrieve the list of supported versions. To upgrade, provide
            a version listed in `can_upgrade_to` for the current version; downgrades are
            not supported.
        required: false
    metrics_enabled:
        description:
        - Activates or deactivates the collection and reporting of metrics for this cluster's
            observability. If the observability service is not activated on the contract,
            this setting is accepted but has no effect. Metric collection does not start
            until the observability service is active.
        required: false
    name:
        description:
        - The name of your MariaDB cluster. Must be 63 characters or less and must begin
            and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`),
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
    ram:
        description:
        - The amount of memory per instance in gigabytes (GB). Accepted values are 4 to
            240. On update, RAM can be increased or decreased.
        required: false
    recovery_target_time:
        description:
        - Recovery target time (ISO 8601). Used to replay backups up to the specified
            time on creation (together with backup_id), or for an in-place restore when
            state is `restore`.
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
        - The amount of storage per instance in gigabytes (GB). Accepted values are 10
            to 4096. On update, storage size can only be increased; it cannot be reduced.
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
    - "ionoscloud-dbaas-mariadb >= 3.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_version: '11.4'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaSMariaDB - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.2.101/24
  name: 'ansible-test-v2'
  description: Ansible test MariaDB v2 cluster
  maintenance_window:
    day_of_the_week: Sunday
    time: 09:00:00
  backup_location: 'eu-central-3'
  backup_retention_days: 7
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  wait: true
  wait_timeout: '3600'
register: cluster_response
''',
    'update': '''
name: Update Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  cores: 2
  ram: 6
  storage_size: 20
  backup_retention_days: 14
  description: Updated Ansible test MariaDB v2 cluster
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: update
  wait: true
  wait_timeout: '3600'
register: updated_cluster_response
''',
    'restore': '''
name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  recovery_target_time: ''
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: restore
  wait: true
  wait_timeout: '3600'
register: restored_cluster_response
''',
    'absent': '''
name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  state: absent
  wait: false
''',
}

EXAMPLES = """
name: Create Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_version: '11.4'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaSMariaDB - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.2.101/24
  name: 'ansible-test-v2'
  description: Ansible test MariaDB v2 cluster
  maintenance_window:
    day_of_the_week: Sunday
    time: 09:00:00
  backup_location: 'eu-central-3'
  backup_retention_days: 7
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  wait: true
  wait_timeout: '3600'
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  cores: 2
  ram: 6
  storage_size: 20
  backup_retention_days: 14
  description: Updated Ansible test MariaDB v2 cluster
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: update
  wait: true
  wait_timeout: '3600'
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  recovery_target_time: ''
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: restore
  wait: true
  wait_timeout: '3600'
register: restored_cluster_response


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  state: absent
  wait: false
"""


class MariaDBClusterV2Module(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_mariadb, ionoscloud]
        self.user_agents = [USER_AGENT, USER_AGENT_CLOUDAPI]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'name']]

    def _wait_until_available(self, clusters_api, dbaas_client, cluster_id):
        """Wait until the cluster reaches AVAILABLE and return it, honouring wait_timeout and failing fast on FAILED."""
        def check_state(cluster):
            if cluster.metadata.state == 'FAILED':
                raise Exception(
                    'MariaDB Cluster {} entered FAILED state: {}'.format(
                        cluster_id, getattr(cluster.metadata, 'status_message', None)))
            return cluster.metadata.state == 'AVAILABLE'

        return dbaas_client.wait_for(
            fn_request=lambda: clusters_api.clusters_find_by_id(cluster_id),
            fn_check=check_state,
            timeout=self.module.params.get('wait_timeout'),
        )

    def get_maintenance_window(self):
        maintenance_window = self.module.params.get('maintenance_window')
        if not maintenance_window:
            return None
        return ionoscloud_dbaas_mariadb.MaintenanceWindow(
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

        return ionoscloud_dbaas_mariadb.MariadbClusterConnection(
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
        instances = ionoscloud_dbaas_mariadb.InstanceConfiguration(
            count=pick('instances', existing_instances.count if existing_instances else None),
            cores=pick('cores', existing_instances.cores if existing_instances else None),
            ram=pick('ram', existing_instances.ram if existing_instances else None),
            storage_size=pick('storage_size', existing_instances.storage_size if existing_instances else None),
        )

        # the backup location is immutable, so it is always carried over from the existing cluster;
        # only the retention window can be changed through a PUT.
        backup = existing.backup
        if backup is not None:
            backup = ionoscloud_dbaas_mariadb.ClusterBackup(
                location=backup.location,
                retention_days=pick('backup_retention_days', backup.retention_days),
            )

        # the PUT is a full replacement, so the credentials are re-sent from the module params on
        # every call. The writeOnly password can't be read back from the API, so it must be supplied
        # again by the caller — this is why db_username/db_password/db_database are required on
        # update/restore. Omitting credentials here would risk wiping the initial user on the PUT.
        return ionoscloud_dbaas_mariadb.Cluster(
            name=pick('name', existing.name),
            description=pick('description', existing.description),
            version=pick('mariadb_version', existing.version),
            instances=instances,
            connection=existing.connection,
            maintenance_window=self.get_maintenance_window() or existing.maintenance_window,
            credentials=ionoscloud_dbaas_mariadb.MariadbUser(
                username=params.get('db_username'),
                password=params.get('db_password'),
                database=params.get('db_database'),
            ),
            logs_enabled=pick('logs_enabled', existing.logs_enabled),
            metrics_enabled=pick('metrics_enabled', existing.metrics_enabled),
            backup=backup,
            restore_from_backup=restore_from_backup,
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
            params.get('backup_location') is not None
            and (
                existing.backup is None
                or existing.backup.location != params.get('backup_location')
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
            or params.get('mariadb_version') is not None
            and existing.version != params.get('mariadb_version')
            or params.get('instances') is not None
            and (instances is None or instances.count != params.get('instances'))
            or params.get('cores') is not None
            and (instances is None or instances.cores != params.get('cores'))
            or params.get('ram') is not None
            and (instances is None or instances.ram != params.get('ram'))
            or params.get('storage_size') is not None
            and (instances is None or instances.storage_size != params.get('storage_size'))
            or params.get('logs_enabled') is not None
            and existing.logs_enabled != params.get('logs_enabled')
            or params.get('metrics_enabled') is not None
            and existing.metrics_enabled != params.get('metrics_enabled')
            or params.get('backup_retention_days') is not None
            and existing.backup is not None
            and existing.backup.retention_days != params.get('backup_retention_days')
            # only the readable half of the credentials can be compared, and only when the API
            # returned it; the password is never returned, so rotating a password on its own is
            # not detected as a change.
            or existing.credentials is not None
            and (
                existing.credentials.username is not None
                and existing.credentials.username != params.get('db_username')
                or existing.credentials.database is not None
                and existing.credentials.database != params.get('db_database')
            )
        )

    def _get_object_list(self, clients):
        return get_paginated(ionoscloud_dbaas_mariadb.ClustersApi(clients[0]).clusters_get, depth=None)

    def _get_object_name(self):
        return self.module.params.get('name')

    def _get_object_identifier(self):
        return self.module.params.get('mariadb_cluster')

    def _create_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(dbaas_client)
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
            restore_from_backup = ionoscloud_dbaas_mariadb.MariadbRestoreClusterFromBackup(
                source_backup_id=params.get('backup_id'),
                recovery_target_datetime=params.get('recovery_target_time'),
            )

        properties = ionoscloud_dbaas_mariadb.ClusterCreateProperties(
            name=params.get('name'),
            description=params.get('description'),
            version=params.get('mariadb_version'),
            instances=ionoscloud_dbaas_mariadb.InstanceConfiguration(
                count=params.get('instances'),
                cores=params.get('cores'),
                ram=params.get('ram'),
                storage_size=params.get('storage_size'),
            ),
            connection=connection,
            maintenance_window=maintenance_window,
            credentials=ionoscloud_dbaas_mariadb.MariadbUser(
                username=params.get('db_username'),
                password=params.get('db_password'),
                database=params.get('db_database'),
            ),
            backup=ionoscloud_dbaas_mariadb.ClusterBackup(
                location=params.get('backup_location'),
                retention_days=params.get('backup_retention_days'),
            ),
            logs_enabled=params.get('logs_enabled'),
            metrics_enabled=params.get('metrics_enabled'),
            restore_from_backup=restore_from_backup,
        )
        cluster_create = ionoscloud_dbaas_mariadb.ClusterCreate(properties=properties)

        try:
            mariadb_cluster = clusters_api.clusters_post(cluster_create)
            if self.module.params.get('wait'):
                mariadb_cluster = self._wait_until_available(clusters_api, dbaas_client, mariadb_cluster.id)
        except Exception as e:
            self.module.fail_json(msg="failed to create the new MariaDB Cluster: %s" % to_native(e))
        return mariadb_cluster

    def _update_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(dbaas_client)
        self._wait_until_available(clusters_api, dbaas_client, existing_object.id)

        cluster_ensure = ionoscloud_dbaas_mariadb.ClusterEnsure(
            id=existing_object.id,
            properties=self._build_full_cluster(existing_object),
        )

        try:
            mariadb_cluster = clusters_api.clusters_put(existing_object.id, cluster_ensure)
            if self.module.params.get('wait'):
                mariadb_cluster = self._wait_until_available(clusters_api, dbaas_client, existing_object.id)
        except Exception as e:
            self.module.fail_json(msg="failed to update the MariaDB Cluster: %s" % to_native(e))
        return mariadb_cluster

    def _remove_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(dbaas_client)

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
                except ionoscloud_dbaas_mariadb.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the MariaDB cluster: %s" % to_native(e))

    def restore_object(self, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(dbaas_client)

        mariadb_cluster_id = get_resource_id(
            self.module,
            get_paginated(clusters_api.clusters_get, depth=None),
            self.module.params.get('mariadb_cluster'),
            [['id'], ['properties', 'name']],
        )
        if mariadb_cluster_id is None:
            self.module.fail_json(
                msg='MariaDB Cluster {} not found.'.format(self.module.params.get('mariadb_cluster')))

        existing_object = clusters_api.clusters_find_by_id(mariadb_cluster_id)
        self._wait_until_available(clusters_api, dbaas_client, mariadb_cluster_id)

        # an in-place restore carries only the recovery target: the source is inferred from the
        # cluster's own backups and a source backup ID is rejected here.
        restore_from_backup = ionoscloud_dbaas_mariadb.MariadbRestoreClusterFromBackup(
            recovery_target_datetime=self.module.params.get('recovery_target_time'),
        )
        cluster_ensure = ionoscloud_dbaas_mariadb.ClusterEnsure(
            id=mariadb_cluster_id,
            properties=self._build_full_cluster(existing_object, restore_from_backup=restore_from_backup),
        )

        try:
            clusters_api.clusters_put(mariadb_cluster_id, cluster_ensure)

            if self.module.params.get('wait'):
                self._wait_until_available(clusters_api, dbaas_client, mariadb_cluster_id)

            return {
                'action': 'restore',
                'changed': True,
                'id': mariadb_cluster_id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to restore the MariaDB cluster: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = MariaDBClusterV2Module()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dbaas_mariadb are required for this module, run `pip install ionoscloud ionoscloud_dbaas_mariadb`')
    ionos_module.main()
