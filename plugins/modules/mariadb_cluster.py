from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_mariadb
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id,
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
OBJECT_NAME = 'MariaDB Cluster'
RETURNED_KEY = 'mariadb_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'mariadb_version': {
        'description': ['The MariaDB version of your cluster.'],
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
    'connections': {
        'description': ['Array of datacenters to connect to your cluster.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'display_name': {
        'description': ['The friendly name of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'db_username': {
        'description': ['The username for the initial MariaDB user. Some system usernames are restricted (e.g. "mariadb", "admin", "standby").'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The password for a MariaDB user.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'mariadb_cluster': {
        'description': ['The ID or name of an existing MariaDB Cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "maintenance_window", "note": "" },
    { "name": "mariadb_version", "note": "" },
    { "name": "instances", "note": "" },
    { "name": "cores", "note": "" },
    { "name": "ram", "note": "" },
    { "name": "storage_size", "note": "" },
    { "name": "connections", "note": "" },
    { "name": "display_name", "note": "" },
    { "name": "db_username", "note": "" },
    { "name": "db_password", "note": "" },
]

DOCUMENTATION = """
module: mariadb_cluster
short_description: Allows operations with Ionos Cloud MariaDB Clusters.
description:
     - This is a module that supports creating, updating or destroying MariaDB Clusters
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
        - The password for a MariaDB user.
        no_log: true
        required: false
    db_username:
        description:
        - The username for the initial MariaDB user. Some system usernames are restricted
            (e.g. "mariadb", "admin", "standby").
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
    maintenance_window:
        description:
        - A weekly 4 hour-long window, during which maintenance might occur.
        required: false
    mariadb_cluster:
        description:
        - The ID or name of an existing MariaDB Cluster.
        required: false
    mariadb_version:
        description:
        - The MariaDB version of your cluster.
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
        - The amount of memory per instance in megabytes. Has to be a multiple of 1024.
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
    - "ionoscloud-dbaas-mariadb >= 1.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create MariaDB Cluster
    mariadb_cluster:
      mariadb_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  ''',
    'update': '''- name: Update MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      mariadb_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  ''',
    'absent': '''- name: Delete MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      state: absent
  ''',
}

EXAMPLES = """- name: Create MariaDB Cluster
    mariadb_cluster:
      mariadb_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
- name: Update MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      mariadb_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  
- name: Delete MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      state: absent
"""

class MariaDBClusterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_mariadb, ionoscloud]
        self.user_agents = [USER_AGENT, USER_AGENT_CLOUDAPI]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'display_name']]


    def _should_replace_object(self, existing_object, clients):
        cloudapi_client = clients[1]
        datacenter_id = lan_id = cidr = None
        if self.module.params.get('connections'):
            connection = self.module.params.get('connections')[0]
            datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
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
            self.module.params.get('connections') is not None
            and (
                existing_object.properties.connections[0].datacenter_id != datacenter_id
                or existing_object.properties.connections[0].lan_id != lan_id
                or existing_object.properties.connections[0].cidr != cidr
            )
            or self.module.params.get('display_name') is not None
            and existing_object.properties.display_name != self.module.params.get('display_name')
                    or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            ) or self.module.params.get('mariadb_version') is not None
            and existing_object.properties.mariadb_version != self.module.params.get('mariadb_version')
            or self.module.params.get('instances') is not None
            and existing_object.properties.instances != self.module.params.get('instances')
            or self.module.params.get('cores') is not None
            and existing_object.properties.cores != self.module.params.get('cores')
            or self.module.params.get('ram') is not None
            and existing_object.properties.ram != self.module.params.get('ram')
        )


    def _should_update_object(self, existing_object, clients):
        return False

    def _get_object_list(self, clients):
        return ionoscloud_dbaas_mariadb.ClustersApi(clients[0]).clusters_get()


    def _get_object_name(self):
        return self.module.params.get('display_name')


    def _get_object_identifier(self):
        return self.module.params.get('mariadb_cluster')


    def _create_object(self, existing_object, clients):
        dbaas_client = clients[0]
        cloudapi_client = clients[1]
        maintenance_window = self.module.params.get('maintenance_window')
        if maintenance_window:
            maintenance_window = dict(self.module.params.get('maintenance_window'))
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
        if existing_object is not None:
            maintenance_window = existing_object.properties.maintenance_window if maintenance_window is None else maintenance_window

        connection = self.module.params.get('connections')[0]

        datacenter_id = get_resource_id(self.module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=2), connection['datacenter'])

        if datacenter_id is None:
            self.module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
        
        lan_id = get_resource_id(self.module, ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

        if lan_id is None:
            self.module.fail_json('LAN {} not found.'.format(connection['lan']))

        connections = [
            ionoscloud_dbaas_mariadb.Connection(datacenter_id=datacenter_id, lan_id=lan_id, cidr=connection['cidr']),
        ]

        clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(dbaas_client)

        mariadb_cluster_properties = ionoscloud_dbaas_mariadb.CreateClusterProperties(
            mariadb_version=self.module.params.get('mariadb_version'),
            instances=self.module.params.get('instances'),
            cores=self.module.params.get('cores'),
            ram=self.module.params.get('ram'),
            storage_size=self.module.params.get('storage_size'),
            connections=connections,
            display_name=self.module.params.get('display_name'),
            maintenance_window=maintenance_window,
            credentials=ionoscloud_dbaas_mariadb.DBUser(
                username=self.module.params.get('db_username'),
                password=self.module.params.get('db_password'),
            ),
        )

        mariadb_cluster = ionoscloud_dbaas_mariadb.CreateClusterRequest(properties=mariadb_cluster_properties)

        try:
            mariadb_cluster = clusters_api.clusters_post(mariadb_cluster)
            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(mariadb_cluster.id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                )
        except Exception as e:
            self.module.fail_json(msg="failed to create the new MariaDB Cluster: %s" % to_native(e))
        return mariadb_cluster


    def _update_object(self, existing_object, clients):
        pass


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
                        scaleup=10000,
                    )
                except ionoscloud_dbaas_mariadb.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the MariaDB cluster: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = MariaDBClusterModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dbaas_mariadb are required for this module, run `pip install ionoscloud ionoscloud_dbaas_mariadb`')
    ionos_module.main()
