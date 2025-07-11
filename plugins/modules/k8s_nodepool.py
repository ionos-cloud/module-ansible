HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import KubernetesNodePool, KubernetesNodePoolProperties, \
        KubernetesNodePoolPropertiesForPut, KubernetesNodePoolForPut
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'K8s Nodepool'
RETURNED_KEY = 'nodepool'

OPTIONS = {
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'k8s_nodepool': {
        'description': ['The ID or name of the K8s nodepool.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'name': {
        'description': ['A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.'],
        'available': ['update', 'present'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'lans': {
        'description': ['The array of existing private LANs to attach to worker nodes.'],
        'available': ['update', 'present'],
        'type': 'list',
        'elements': 'dict',
    },
    'node_count': {
        'description': ['The number of worker nodes of the node pool.'],
        'available': ['update', 'present'],
        'type': 'int',
    },
    'cpu_family': {
        'description': ['The CPU type for the nodes. If this field is null or omitted from the request, an available CPU architecture will be automatically selected. Supplying an empty string is not accepted.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'cores_count': {
        'description': ['The total number of cores for the nodes.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'ram_size': {
        'description': ['The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'availability_zone': {
        'description': ['The availability zone in which the target VM should be provisioned.'],
        'available': ['update', 'present'],
        'choices_docs': ['AUTO', 'ZONE_1', 'ZONE_2'],
        'type': 'str',
    },
    'storage_type': {
        'description': ['The storage type for the nodes.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'choices_docs': ['HDD', 'SSD'],
        'type': 'str',
    },
    'storage_size': {
        'description': ['The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'int',
    },
    'maintenance_window': {
        'description': ['The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'labels': {
        'description': ['The labels attached to the node pool.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'annotations': {
        'description': ['The annotations attached to the node pool.'],
        'available': ['present','update'],
        'type': 'dict',
    },
    'auto_scaling': {
        'description': ['Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'public_ips': {
        'description': ['Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool\'s data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    **get_default_options_with_replace(STATES),
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 3600,
        'available': STATES,
        'type': 'int',
    },
}

IMMUTABLE_OPTIONS = [
    { "name": "datacenter", "note": "" },
    { "name": "name", "note": "" },
    { "name": "cpu_family", "note": "" },
    { "name": "cores_count", "note": "" },
    { "name": "ram_size", "note": "" },
    { "name": "availability_zone", "note": "" },
    { "name": "storage_type", "note": "" },
    { "name": "storage_size", "note": "" },
]

DOCUMENTATION = """
module: k8s_nodepool
short_description: Create or destroy K8s Nodepools
description:
     - This is a simple module that supports creating or removing K8s Nodepools.
       This module has a dependency on ionoscloud >= 6.0.2
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
        - The annotations attached to the node pool.
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    auto_scaling:
        description:
        - Property to be set when auto-scaling needs to be enabled for the nodepool. By
            default, auto-scaling is not enabled.
        required: false
    availability_zone:
        choices:
        - AUTO
        - ZONE_1
        - ZONE_2
        description:
        - The availability zone in which the target VM should be provisioned.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    cores_count:
        description:
        - The total number of cores for the nodes.
        required: false
    cpu_family:
        description:
        - The CPU type for the nodes. If this field is null or omitted from the request,
            an available CPU architecture will be automatically selected. Supplying an
            empty string is not accepted.
        required: false
    datacenter:
        description:
        - The unique identifier of the VDC where the worker nodes of the node pool are
            provisioned.Note that the data center is located in the exact place where
            the parent cluster of the node pool is located.
        required: false
    k8s_cluster:
        description:
        - The ID or name of the K8s cluster.
        required: true
    k8s_nodepool:
        description:
        - The ID or name of the K8s nodepool.
        required: false
    k8s_version:
        description:
        - The Kubernetes version running in the node pool. Note that this imposes restrictions
            on which Kubernetes versions can run in the node pools of a cluster. Also,
            not all Kubernetes versions are suitable upgrade targets for all earlier versions.
        required: false
    labels:
        description:
        - The labels attached to the node pool.
        required: false
    lans:
        description:
        - The array of existing private LANs to attach to worker nodes.
        elements: dict
        required: false
    maintenance_window:
        description:
        - The maintenance window is used to update the software on the node pool nodes
            and update the K8s version of the node pool. If no value is specified, a value
            is selected dynamically, so there is no fixed default value.
        required: false
    name:
        description:
        - A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters
            or less and must be empty or begin and end with an alphanumeric character
            ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics
            between.
        required: false
    node_count:
        description:
        - The number of worker nodes of the node pool.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    public_ips:
        description:
        - Optional array of reserved public IP addresses to be used by the nodes. The
            IPs must be from the exact location of the node pool's data center. If autoscaling
            is used, the array must contain one more IP than the maximum possible number
            of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The
            extra IP is used when the nodes are rebuilt.
        elements: str
        required: false
    ram_size:
        description:
        - The RAM size for the nodes. Must be specified in multiples of 1024 MB, with
            a minimum size of 2048 MB.
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
        - The allocated volume size in GB. The allocated volume size in GB. To achieve
            good performance, we recommend a size greater than 100GB for SSD.
        required: false
    storage_type:
        choices:
        - HDD
        - SSD
        description:
        - The storage type for the nodes.
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
        default: 3600
        description:
        - How long before wait gives up, in seconds.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
name: Create k8s cluster nodepool
ionoscloudsdk.ionoscloud.k8s_nodepool:
  name: my-nodepool-
  k8s_cluster: ''
  datacenter: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: 100
  public_ips: ''
  lans:
  - id: ''
    dhcp: false
  auto_scaling:
    min_node_count: 1
    max_node_count: 3
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
register: result
''',
  'update' : '''
name: Update k8s cluster nodepool no change
ionoscloudsdk.ionoscloud.k8s_nodepool:
  k8s_cluster: ''
  datacenter: ''
  k8s_nodepool: ''
  name: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: '1'
  ram_size: '2048'
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  public_ips: ''
  lans:
  - id: ''
    dhcp: false
  auto_scaling:
    min_node_count: 1
    max_node_count: 3
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
  state: update
register: result_no_change
''',
  'absent' : '''
name: Delete k8s cluster nodepool
ionoscloudsdk.ionoscloud.k8s_nodepool:
  k8s_cluster: ''
  k8s_nodepool: ''
  wait: false
  state: absent
''',
}

EXAMPLES = """
name: Create k8s cluster nodepool
ionoscloudsdk.ionoscloud.k8s_nodepool:
  name: my-nodepool-
  k8s_cluster: ''
  datacenter: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: 1
  ram_size: 2048
  availability_zone: AUTO
  storage_type: HDD
  storage_size: 100
  public_ips: ''
  lans:
  - id: ''
    dhcp: false
  auto_scaling:
    min_node_count: 1
    max_node_count: 3
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
register: result


name: Update k8s cluster nodepool no change
ionoscloudsdk.ionoscloud.k8s_nodepool:
  k8s_cluster: ''
  datacenter: ''
  k8s_nodepool: ''
  name: ''
  node_count: 2
  cpu_family: INTEL_SKYLAKE
  cores_count: '1'
  ram_size: '2048'
  availability_zone: AUTO
  storage_type: HDD
  storage_size: '100'
  public_ips: ''
  lans:
  - id: ''
    dhcp: false
  auto_scaling:
    min_node_count: 1
    max_node_count: 3
  labels:
    foo: bar
    color: red
    size: '10'
  annotations:
    ann1: value1
    ann2: value2
  wait: true
  state: update
register: result_no_change


name: Delete k8s cluster nodepool
ionoscloudsdk.ionoscloud.k8s_nodepool:
  k8s_cluster: ''
  k8s_nodepool: ''
  wait: false
  state: absent
"""


def _get_lans(lans_param):
    if lans_param is None:
        return []
    def _get_routes(routes_param):
        return [
            ionoscloud.KubernetesNodePoolLanRoutes(
                network=route['network'],
                gateway_ip=route['gateway_ip'],
            ) for route in routes_param
        ]
    return [
        ionoscloud.KubernetesNodePoolLan(
            id=lan_param['id'],
            dhcp=lan_param['dhcp'],
            routes=_get_routes(lan_param.get('routes', [])),
        ) for lan_param in lans_param
    ]


class K8SClusterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        datacenter_id = get_resource_id(
            self.module, 
            get_paginated(ionoscloud.DataCentersApi(clients[0]).datacenters_get),
            self.module.params.get('datacenter'),
        )
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
            or datacenter_id is not None
            and existing_object.properties.datacenter_id != datacenter_id
        )


    def _should_update_object(self, existing_object, clients):
        def sort_func(el):
            return el['id']
        def sort_func_routes(el):
            return el['gateway_ip'], el['network']

        if self.module.params.get('lans'):
            existing_lans = sorted(map(
                lambda x: {
                    'id': str(x.id),
                    'dhcp': x.dhcp,
                    'routes': sorted(
                        map(
                            lambda y: {
                                'gateway_ip': y.gateway_ip,
                                'network': y.network,
                            },
                            x.routes if x.routes else [],
                        ),
                        key=sort_func_routes,
                    ),
                },
                existing_object.properties.lans,
            ), key=sort_func)
            lans_input = self.module.params.get('lans')
            for lan_input in lans_input:
                lan_input['routes'] = sorted(lan_input.get('routes', []), key=sort_func_routes)
            new_lans = sorted(self.module.params.get('lans'), key=sort_func)

        return (
            self.module.params.get('k8s_version') is not None
            and existing_object.properties.k8s_version != self.module.params.get('k8s_version')
            or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            )
            or self.module.params.get('lans') is not None
            and existing_lans != new_lans
            or self.module.params.get('public_ips') is not None
            and sorted(existing_object.properties.public_ips) != sorted(self.module.params.get('public_ips'))
            or self.module.params.get('node_count') is not None
            and existing_object.properties.node_count != self.module.params.get('node_count')
            or self.module.params.get('labels') is not None
            and existing_object.properties.labels != self.module.params.get('labels')
            or self.module.params.get('annotations') is not None
            and existing_object.properties.annotations != self.module.params.get('annotations')
            or self.module.params.get('auto_scaling') is not None
            and (
                existing_object.properties.auto_scaling.min_node_count != self.module.params.get('auto_scaling').get('min_node_count')
                or existing_object.properties.auto_scaling.max_node_count != self.module.params.get('auto_scaling').get('max_node_count')
            )
        )


    def _get_object_list(self, clients):
        client = clients[0]
        k8s_cluster_id = get_resource_id(
            self.module, 
            ionoscloud.KubernetesApi(client).k8s_get(depth=1),
            self.module.params.get('k8s_cluster'),
        )

        return ionoscloud.KubernetesApi(client).k8s_nodepools_get(k8s_cluster_id, depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('k8s_nodepool')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        k8s_cluster_id = get_resource_id(
            self.module, 
            ionoscloud.KubernetesApi(client).k8s_get(depth=1),
            self.module.params.get('k8s_cluster'),
        )
        datacenter_id = get_resource_id(
            self.module, 
            get_paginated(ionoscloud.DataCentersApi(client).datacenters_get),
            self.module.params.get('datacenter'),
        )
        k8s_version = self.module.params.get('k8s_version')
        name = self.module.params.get('name')
        lans = _get_lans(self.module.params.get('lans'))
        node_count = self.module.params.get('node_count')
        cpu_family = self.module.params.get('cpu_family')
        cores_count = self.module.params.get('cores_count')
        ram_size = self.module.params.get('ram_size')
        availability_zone = self.module.params.get('availability_zone')
        storage_type = self.module.params.get('storage_type')
        storage_size = self.module.params.get('storage_size')
        maintenance = self.module.params.get('maintenance_window')
        auto_scaling_dict = self.module.params.get('auto_scaling')
        labels = self.module.params.get('labels')
        annotations = self.module.params.get('annotations')
        public_ips = self.module.params.get('public_ips')

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        auto_scaling = None
        if auto_scaling_dict:
            auto_scaling = dict(auto_scaling_dict)
            auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
            auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
            lans = existing_object.properties.lans if lans is None else lans
            datacenter_id = existing_object.properties.datacenter_id if datacenter_id is None else datacenter_id
            node_count = existing_object.properties.node_count if node_count is None else node_count
            cpu_family = existing_object.properties.cpu_family if cpu_family is None else cpu_family
            cores_count = existing_object.properties.cores_count if cores_count is None else cores_count
            ram_size = existing_object.properties.ram_size if ram_size is None else ram_size
            availability_zone = existing_object.properties.availability_zone if availability_zone is None else availability_zone
            storage_type = existing_object.properties.storage_type if storage_type is None else storage_type
            storage_size = existing_object.properties.storage_size if storage_size is None else storage_size
            labels = existing_object.properties.labels if labels is None else labels
            annotations = existing_object.properties.annotations if annotations is None else annotations
            maintenance_window = existing_object.properties.maintenance_window if maintenance is None else maintenance_window
            auto_scaling = existing_object.properties.auto_scaling if auto_scaling is None else auto_scaling
            public_ips = existing_object.properties.public_ips if public_ips is None else public_ips

        k8s_nodepool_properties = KubernetesNodePoolProperties(
            name=name,
            datacenter_id=datacenter_id,
            node_count=node_count,
            cpu_family=cpu_family,
            cores_count=cores_count,
            ram_size=ram_size,
            availability_zone=availability_zone,
            storage_type=storage_type,
            storage_size=storage_size,
            k8s_version=k8s_version,
            maintenance_window=maintenance_window,
            auto_scaling=auto_scaling,
            lans=lans,
            labels=labels,
            annotations=annotations,
            public_ips=public_ips,
        )
        k8s_nodepool = KubernetesNodePool(properties=k8s_nodepool_properties)

        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            k8s_response = k8s_api.k8s_nodepools_post(k8s_cluster_id=k8s_cluster_id, kubernetes_node_pool=k8s_nodepool)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                        k8s_cluster_id,
                        k8s_response.id,
                    ).metadata.state,
                    fn_check=lambda r: r == 'ACTIVE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
        return k8s_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        k8s_cluster_id = get_resource_id(
            self.module, 
            ionoscloud.KubernetesApi(client).k8s_get(depth=1),
            self.module.params.get('k8s_cluster'),
        )
        node_count = self.module.params.get('node_count')
        maintenance = self.module.params.get('maintenance_window')
        auto_scaling_dict = self.module.params.get('auto_scaling')
        lans = _get_lans(self.module.params.get('lans'))
        k8s_version = self.module.params.get('k8s_version')
        public_ips = self.module.params.get('public_ips')
        labels = self.module.params.get('labels')
        annotations = self.module.params.get('annotations')

        if not node_count:
            node_count = existing_object.properties.node_count

        auto_scaling = None
        if auto_scaling_dict:
            auto_scaling = dict(auto_scaling_dict)
            auto_scaling['minNodeCount'] = auto_scaling.pop('min_node_count')
            auto_scaling['maxNodeCount'] = auto_scaling.pop('max_node_count')

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
            
        k8s_nodepool_properties = KubernetesNodePoolPropertiesForPut(
            node_count=node_count,
            k8s_version=k8s_version,
            maintenance_window=maintenance_window,
            auto_scaling=auto_scaling,
            lans=lans,
            public_ips=public_ips,
            labels=labels,
            annotations=annotations,
        )

        k8s_nodepool = KubernetesNodePoolForPut(properties=k8s_nodepool_properties)

        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            k8s_response = k8s_api.k8s_nodepools_put(
                k8s_cluster_id=k8s_cluster_id,
                nodepool_id=existing_object.id,
                kubernetes_node_pool=k8s_nodepool,
            )

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_nodepools_find_by_id(
                        k8s_cluster_id,
                        k8s_response.id,
                    ).metadata.state,
                    fn_check=lambda r: r == 'ACTIVE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )

            return k8s_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        k8s_cluster_id = get_resource_id(
            self.module, 
            ionoscloud.KubernetesApi(client).k8s_get(depth=1),
            self.module.params.get('k8s_cluster'),
        )

        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            if existing_object.metadata.state != 'DESTROYING':
                k8s_api.k8s_nodepools_delete_with_http_info(k8s_cluster_id=k8s_cluster_id, nodepool_id=existing_object.id)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_nodepools_get(k8s_cluster_id=k8s_cluster_id, depth=1),
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
    ionos_module = K8SClusterModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    if (
        ionos_module.module.params.get('state') == 'present'
        and not ionos_module.module.params.get('node_count')
        and not ionos_module.module.params.get('auto_scaling')
    ):
        ionos_module.module.params.get('node_count').module.fail_json(
            msg='either node_count or auto_scaling parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME),
        )
    ionos_module.main()
