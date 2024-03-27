HAS_SDK = True

try:
    import ionoscloud_dataplatform
    from ionoscloud_dataplatform import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dataplatform/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'dataplatform'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Data Platform Nodepool'
RETURNED_KEY = 'dataplatform_nodepool'

OPTIONS = {
    'name': {
        'description': ['The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'cluster': {
        'description': ['The name or ID of the Data Platform cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nodepool': {
        'description': ['The name or ID of the Data Platform nodepool.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'node_count': {
        'description': ['The number of nodes that make up the node pool.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'cpu_family': {
        'description': ['A valid CPU family name or `AUTO` if the platform shall choose the best fitting option. Available CPU architectures can be retrieved from the data center resource.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'cores_count': {
        'description': ['The number of CPU cores per node.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'int',
    },
    'ram_size': {
        'description': ['The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a minimum size is of 2048 MB.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'int',
    },
    'availability_zone': {
        'description': ['The availability zone of the virtual data center region where the node pool resources should be provisioned.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_type': {
        'description': ['The type of hardware for the volume.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'storage_size': {
        'description': ['The size of the volume in GB. The size must be greater than 10 GB.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'int',
    },
    'maintenance_window': {
        'description': ['Starting time of a weekly 4-hour-long window, during which maintenance might occur in the `HH:MM:SS` format.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': ['Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'annotations': {
        'description': ['Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).'],
        'available': ['present','update'],
        'type': 'dict',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "name", "note": "" },
    { "name": "cpu_family", "note": "" },
    { "name": "cores_count", "note": "" },
    { "name": "ram_size", "note": "" },
    { "name": "availability_zone", "note": "" },
    { "name": "storage_type", "note": "" },
    { "name": "storage_size", "note": "" },
]

DOCUMENTATION = """
module: dataplatform_nodepool
short_description: Create or destroy Data Platform Nodepools
description:
     - This is a simple module that supports creating or removing Data Platform Nodepools.
       This module has a dependency on ionoscloud_dataplatform >= 1.0.0
     - ⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.
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
    annotations:
        description:
        - Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    availability_zone:
        description:
        - The availability zone of the virtual data center region where the node pool
            resources should be provisioned.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    cluster:
        description:
        - The name or ID of the Data Platform cluster.
        required: true
    cores_count:
        description:
        - The number of CPU cores per node.
        required: false
    cpu_family:
        description:
        - A valid CPU family name or `AUTO` if the platform shall choose the best fitting
            option. Available CPU architectures can be retrieved from the data center
            resource.
        required: false
    labels:
        description:
        - Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).
        required: false
    maintenance_window:
        description:
        - Starting time of a weekly 4-hour-long window, during which maintenance might
            occur in the `HH:MM:SS` format.
        required: false
    name:
        description:
        - The name of your node pool. Must be 63 characters or less and must begin and
            end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores
            (`_`), dots (`.`), and alphanumerics between.
        required: false
    node_count:
        description:
        - The number of nodes that make up the node pool.
        required: false
    nodepool:
        description:
        - The name or ID of the Data Platform nodepool.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    ram_size:
        description:
        - The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a
            minimum size is of 2048 MB.
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
    storage_size:
        description:
        - The size of the volume in GB. The size must be greater than 10 GB.
        required: false
    storage_type:
        description:
        - The type of hardware for the volume.
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
    - "ionoscloud_dataplatform >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
name: Create DataPlatform cluster nodepool
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  name: my-nodepool
  cluster: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
  wait_timeout: 7200
register: result
''',
  'update' : '''
name: Update DataPlatform cluster nodepool no change
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  cluster: ''
  nodepool: ''
  name: my-nodepool
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  allow_replace: false
  wait: true
  wait_timeout: 7200
  state: update
register: result_no_change
''',
  'absent' : '''
name: Delete DataPlatform cluster nodepool
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  cluster: ''
  nodepool: ''
  wait: true
  state: absent
''',
}

EXAMPLES = """
name: Create DataPlatform cluster nodepool
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  name: my-nodepool
  cluster: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
  wait_timeout: 7200
register: result


name: Update DataPlatform cluster nodepool no change
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  cluster: ''
  nodepool: ''
  name: my-nodepool
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  allow_replace: false
  wait: true
  wait_timeout: 7200
  state: update
register: result_no_change


name: Delete DataPlatform cluster nodepool
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  cluster: ''
  nodepool: ''
  wait: true
  state: absent
"""


class DataPlatformNodepoolModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dataplatform]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('cpu_family') is not None
            and existing_object.properties.cpu_family != self.module.params.get('cpu_family')
            or self.module.params.get('cores_count') is not None
            and existing_object.properties.cores_count != self.module.params.get('cores_count')
            or self.module.params.get('ram_size') is not None
            and existing_object.properties.ram_size != self.module.params.get('ram_size')
            or self.module.params.get('availability_zone') is not None
            and existing_object.properties.availability_zone != self.module.params.get('availability_zone')
            or self.module.params.get('storage_type') is not None
            and existing_object.properties.storage_type != self.module.params.get('storage_type')
            or self.module.params.get('storage_size') is not None
            and existing_object.properties.storage_size != self.module.params.get('storage_size')
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            )
            or self.module.params.get('node_count') is not None
            and existing_object.properties.node_count != self.module.params.get('node_count')
            or self.module.params.get('labels') is not None
            and existing_object.properties.labels != self.module.params.get('labels')
            or self.module.params.get('annotations') is not None
            and existing_object.properties.annotations != self.module.params.get('annotations')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        cluster_id = get_resource_id(
            self.module, ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters(),
            self.module.params.get('cluster'),
        )
        return ionoscloud_dataplatform.DataPlatformNodePoolApi(client).get_cluster_nodepools(cluster_id)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('nodepool')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        node_count = self.module.params.get('node_count')
        cpu_family = self.module.params.get('cpu_family')
        cores_count = self.module.params.get('cores_count')
        ram_size = self.module.params.get('ram_size')
        availability_zone = self.module.params.get('availability_zone')
        storage_type = self.module.params.get('storage_type')
        storage_size = self.module.params.get('storage_size')
        maintenance = self.module.params.get('maintenance_window')
        labels = self.module.params.get('labels')
        annotations = self.module.params.get('annotations')

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        if existing_object is not None:
            nodepool_name = existing_object.properties.name if nodepool_name is None else nodepool_name
            k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
            node_count = existing_object.properties.node_count if node_count is None else node_count
            cpu_family = existing_object.properties.cpu_family if cpu_family is None else cpu_family
            cores_count = existing_object.properties.cores_count if cores_count is None else cores_count
            ram_size = existing_object.properties.ram_size if ram_size is None else ram_size
            availability_zone = existing_object.properties.availability_zone if availability_zone is None else availability_zone
            storage_type = existing_object.properties.storage_type if storage_type is None else storage_type
            storage_size = existing_object.properties.storage_size if storage_size is None else storage_size
            labels = existing_object.properties.labels if labels is None else labels
            annotations = existing_object.properties.annotations if annotations is None else annotations
            maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance_window

        dataplatform_nodepool_properties = ionoscloud_dataplatform.CreateNodePoolProperties(
            name=name,
            node_count=node_count,
            cpu_family=cpu_family,
            cores_count=cores_count,
            ram_size=ram_size,
            availability_zone=availability_zone,
            storage_type=storage_type,
            storage_size=storage_size,
            maintenance_window=maintenance_window,
            labels=labels,
            annotations=annotations,
        )
        dataplatform_nodepool = ionoscloud_dataplatform.CreateNodePoolRequest(properties=dataplatform_nodepool_properties)
        dataplatform_nodepool_api = ionoscloud_dataplatform.DataPlatformNodePoolApi(api_client=client)

        try:
            cluster_id = get_resource_id(
                self.module, ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters(),
                self.module.params.get('cluster'),
            )
            response = dataplatform_nodepool_api.create_cluster_nodepool(cluster_id, dataplatform_nodepool)
            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: dataplatform_nodepool_api.get_cluster_nodepool(
                        cluster_id,response.id,
                    ).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )
        except ionoscloud_dataplatform.ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        node_count = self.module.params.get('node_count')
        maintenance = self.module.params.get('maintenance_window')
        labels = self.module.params.get('labels')
        annotations = self.module.params.get('annotations')

        if not node_count:
            node_count = existing_object.properties.node_count

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
            
        dataplatform_nodepool_properties = ionoscloud_dataplatform.PatchNodePoolProperties(
            node_count=node_count,
            maintenance_window=maintenance_window,
            labels=labels,
            annotations=annotations,
        )
        dataplatform_patch_nodepool_request = ionoscloud_dataplatform.PatchNodePoolRequest(properties=dataplatform_nodepool_properties)
        
        dataplatform_nodepool_api = ionoscloud_dataplatform.DataPlatformNodePoolApi(api_client=client)
        try:
            cluster_id = get_resource_id(
                self.module, ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters(),
                self.module.params.get('cluster'),
            )

            response = dataplatform_nodepool_api.patch_cluster_nodepool(
                cluster_id, existing_object.id, dataplatform_patch_nodepool_request,
            )

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: dataplatform_nodepool_api.get_cluster_nodepool(
                        cluster_id,response.id,
                    ).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )

            return response
        except ionoscloud_dataplatform.ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        dataplatform_nodepool_api = ionoscloud_dataplatform.DataPlatformNodePoolApi(api_client=client)

        try:
            cluster_id = get_resource_id(
                self.module, ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters(),
                self.module.params.get('cluster'),
            )
            if existing_object.metadata.state == 'AVAILABLE':
                dataplatform_nodepool_api.delete_cluster_nodepool(
                    cluster_id=cluster_id, nodepool_id=existing_object.id,
                )

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: dataplatform_nodepool_api.get_cluster_nodepools(cluster_id),
                    fn_check=lambda r: len(list(filter(
                        lambda e: e.id == existing_object.id,
                        r.items
                    ))) < 1,
                    console_print='.',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )
        except Exception as e:
            self.module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


if __name__ == '__main__':
    ionos_module = DataPlatformNodepoolModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dataplatform is required for this module, run `pip install ionoscloud_dataplatform`')
    ionos_module.main()
