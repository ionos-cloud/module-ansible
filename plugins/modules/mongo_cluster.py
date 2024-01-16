from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_mongo
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

CLOUDAPI_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dbaas-mongo/%s' % (
    __version__, ionoscloud_dbaas_mongo.__version__)
DOC_DIRECTORY = 'dbaas-mongo'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Mongo Cluster'
RETURNED_KEY = 'mongo_cluster'

OPTIONS = {
    'mongo_cluster': {
        'description': ['The ID or name of an existing Mongo Cluster.'],
        'available': ['update', 'absent', 'restore'],
        'required': ['update', 'absent', 'restore'],
        'type': 'str',
    },
    'backup_id': {
        'description': ['The ID of the backup to be used.'],
        'available': ['restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': ['A weekly window of 4 hours during which maintenance work can be performed.'],
        'available': ['update', 'present'],
        'type': 'dict',
    },
    'mongo_db_version': {
        'description': ['The MongoDB version of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster (one primary and n-1 secondaries).'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'connections': {
        'description': ['Array of datacenters to connect to your cluster.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'template_id': {
        'description': ['The unique ID of the template, which specifies the number of cores, storage size, and memory. You cannot downgrade to a smaller template or minor edition (e.g. from business to playground). To get a list of all templates to confirm the changes use the /templates endpoint.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'location': {
        'description': ['The physical location where the cluster will be created. This is the location where all your instances will be located. This property is immutable.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'display_name': {
        'description': ['The name of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "location", "note": "" },
    { "name": "mongo_db_version", "note": "" },
]

DOCUMENTATION = """
module: mongo_cluster
short_description: Allows operations with Ionos Cloud Mongo Clusters.
description:
     - This is a module that supports creating and destroying Mongo Clusters
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
    display_name:
        description:
        - The name of your cluster.
        required: false
    instances:
        description:
        - The total number of instances in the cluster (one primary and n-1 secondaries).
        required: false
    location:
        description:
        - The physical location where the cluster will be created. This is the location
            where all your instances will be located. This property is immutable.
        required: false
    maintenance_window:
        description:
        - A weekly window of 4 hours during which maintenance work can be performed.
        required: false
    mongo_cluster:
        description:
        - The ID or name of an existing Mongo Cluster.
        required: false
    mongo_db_version:
        description:
        - The MongoDB version of your cluster.
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
        - restore
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    template_id:
        description:
        - The unique ID of the template, which specifies the number of cores, storage
            size, and memory. You cannot downgrade to a smaller template or minor edition
            (e.g. from business to playground). To get a list of all templates to confirm
            the changes use the /templates endpoint.
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
    - "ionoscloud-dbaas-mongo >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Cluster
    mongo_cluster:
      mongo_db_version: 5.0
      instances: 3
      location: de/fra
      template_id: 6b78ea06-ee0e-4689-998c-fc9c46e781f6
      connections:
        - cidr_list: 
            - 192.168.1.116/24
            - 192.168.1.117/24
            - 192.168.1.118/24
          datacenter: "Datacenter - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  ''',
    'update': '''- name: Update Cluster
    mongo_cluster:
      mongo_cluster: backuptest-04
      display_name: backuptest-05
      state: update
      allow_replace: True
      wait: true
    register: cluster_response
  ''',
    'restore': '''- name: Restore Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      backup_id: 9ab6545c-b138-4a86-b6ca-0d872a2b0953
      state: restore
  ''',
    'absent': '''- name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      state: absent
  ''',
}

EXAMPLES = """- name: Create Cluster
    mongo_cluster:
      mongo_db_version: 5.0
      instances: 3
      location: de/fra
      template_id: 6b78ea06-ee0e-4689-998c-fc9c46e781f6
      connections:
        - cidr_list: 
            - 192.168.1.116/24
            - 192.168.1.117/24
            - 192.168.1.118/24
          datacenter: "Datacenter - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  
- name: Update Cluster
    mongo_cluster:
      mongo_cluster: backuptest-04
      display_name: backuptest-05
      state: update
      allow_replace: True
      wait: true
    register: cluster_response
  
- name: Restore Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      backup_id: 9ab6545c-b138-4a86-b6ca-0d872a2b0953
      state: restore
  
- name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      state: absent
"""


class MongoClusterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_mongo, ionoscloud]
        self.user_agents = [USER_AGENT, CLOUDAPI_USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['id'], ['properties', 'display_name']]


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('location') is not None
            and existing_object.properties.location != self.module.params.get('location')
            or self.module.params.get('mongo_db_version') is not None
            and existing_object.properties.mongo_db_version != self.module.params.get('mongo_db_version')
        )


    def _should_update_object(self, existing_object, clients):
        cloudapi_client = clients[1]
        datacenter_id = lan_id = cidr_list = None
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
            cidr_list = connection['cidr_list']

        return (
            self.module.params.get('display_name') is not None
            and existing_object.properties.display_name != self.module.params.get('display_name')
                    or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            )
            or self.module.params.get('template_id') is not None
            and existing_object.properties.template_id != self.module.params.get('template_id')
            or self.module.params.get('instances') is not None
            and existing_object.properties.instances != self.module.params.get('instances')
            or self.module.params.get('connections') is not None
            and (
                existing_object.properties.connections[0].datacenter_id != datacenter_id
                or existing_object.properties.connections[0].lan_id != lan_id
                or existing_object.properties.connections[0].cidr_list != cidr_list
            )
        )


    def _get_object_list(self, clients):
        return ionoscloud_dbaas_mongo.ClustersApi(clients[0]).clusters_get()


    def _get_object_name(self):
        return self.module.params.get('display_name')


    def _get_object_identifier(self):
        return self.module.params.get('mongo_cluster')


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

        datacenter_id = get_resource_id(
            self.module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=2), connection['datacenter'],
        )

        if datacenter_id is None:
            self.module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
        
        lan_id = get_resource_id(
            self.module,
            ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'],
        )

        if lan_id is None:
            self.module.fail_json('LAN {} not found.'.format(connection['lan']))

        connections = [
            ionoscloud_dbaas_mongo.Connection(
                datacenter_id=datacenter_id,
                lan_id=lan_id,
                cidr_list=connection['cidr_list'],
            ),
        ]

        mongo_cluster_properties = ionoscloud_dbaas_mongo.CreateClusterProperties(
            mongo_db_version=self.module.params.get('mongo_db_version'),
            instances=self.module.params.get('instances'),
            connections=connections,
            location=self.module.params.get('location'),
            display_name=self.module.params.get('display_name'),
            maintenance_window=maintenance_window,
            template_id=self.module.params.get('template_id'),
        )
        mongo_cluster = ionoscloud_dbaas_mongo.CreateClusterRequest(properties=mongo_cluster_properties)

        mongo_clusters_api = ionoscloud_dbaas_mongo.ClustersApi(dbaas_client)
        try:
            mongo_cluster = mongo_clusters_api.clusters_post(mongo_cluster)
            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: mongo_clusters_api.clusters_find_by_id(mongo_cluster.id),
                    fn_check=lambda cluster: cluster and cluster.metadata and cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )
        except Exception as e:
            self.module.fail_json(msg="failed to create the Mongo Cluster: %s" % to_native(e))

        return mongo_cluster


    def _update_object(self, existing_object, clients):
        dbaas_client = clients[0]
        cloudapi_client = clients[1]
        clusters_api = ionoscloud_dbaas_mongo.ClustersApi(dbaas_client)
        dbaas_client.wait_for(
            fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
            fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
            scaleup=10000,
        )
        maintenance_window = self.module.params.get('maintenance_window')
        if maintenance_window:
            maintenance_window = dict(self.module.params.get('maintenance_window'))
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        connections = None
        if self.module.params.get('connections'):
            connection = self.module.params.get('connections')[0]

            datacenter_id = get_resource_id(
                self.module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=2), connection['datacenter'],
            )

            if datacenter_id is None:
                self.module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
            
            lan_id = get_resource_id(
                self.module,
                ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'],
            )

            if lan_id is None:
                self.module.fail_json('LAN {} not found.'.format(connection['lan']))

            connections = [
                ionoscloud_dbaas_mongo.Connection(
                    datacenter_id=datacenter_id,
                    lan_id=lan_id,
                    cidr_list=connection['cidr_list'],
                ),
            ]

        mongo_cluster_properties = ionoscloud_dbaas_mongo.PatchClusterProperties(
            instances=self.module.params.get('instances'),
            display_name=self.module.params.get('display_name'),
            maintenance_window=maintenance_window,
            connections=connections,
            template_id=self.module.params.get('template_id'),
        )
        mongo_cluster = ionoscloud_dbaas_mongo.PatchClusterRequest(properties=mongo_cluster_properties)

        try:
            mongo_cluster = clusters_api.clusters_patch(
                cluster_id=existing_object.id,
                patch_cluster_request=mongo_cluster,
            )

            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(mongo_cluster.id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )

        except Exception as e:
            self.module.fail_json(msg="failed to update the Mongo Cluster: %s" % to_native(e))
        return mongo_cluster


    def _remove_object(self, existing_object, clients):
        dbaas_client = clients[0]
        clusters_api = ionoscloud_dbaas_mongo.ClustersApi(dbaas_client)

        try:
            if existing_object.metadata.state != 'DESTROYING':
                clusters_api.clusters_delete(existing_object.id)

            if self.module.params.get('wait'):
                try:
                    dbaas_client.wait_for(
                        fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
                        fn_check=lambda _: False,
                        scaleup=10000,
                        timeout=self.module.params.get('wait_timeout'),
                    )
                except ionoscloud_dbaas_mongo.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the Mongo cluster: %s" % to_native(e))


    def restore_object(self, clients):
        dbaas_client = clients[0]
        mongo_cluster_api = ionoscloud_dbaas_mongo.ClustersApi(dbaas_client)

        mongo_cluster_id = get_resource_id(
            self.module,
            mongo_cluster_api.clusters_get(),
            self.module.params.get('mongo_cluster'),
            [['id'], ['properties', 'display_name']],
        )

        restore_request = ionoscloud_dbaas_mongo.CreateRestoreRequest(
            backup_id=self.module.params.get('backup_id'),
        )

        try:
            ionoscloud_dbaas_mongo.RestoresApi(dbaas_client).clusters_restore_post(mongo_cluster_id, restore_request)

            if self.module.params.get('wait'):
                dbaas_client.wait_for(
                    fn_request=lambda: mongo_cluster_api.clusters_find_by_id(mongo_cluster_id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )

            return {
                'action': 'restore',
                'changed': True,
                'id': mongo_cluster_id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to restore the Mongo cluster: %s" % to_native(e))
            return {
                'action': 'restore',
                'changed': False,
                'id': mongo_cluster_id,
            }


if __name__ == '__main__':
    ionos_module = MongoClusterModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='both ionoscloud and ionoscloud_dbaas_mongo are required for this module, '
                             'run `pip install ionoscloud ionoscloud_dbaas_mongo`')
    ionos_module.main()
