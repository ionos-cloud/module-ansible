from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible import __version__

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import KubernetesCluster, KubernetesClusterProperties, KubernetesClusterForPut, \
        KubernetesClusterPropertiesForPut, S3Bucket
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'K8s Cluster'
RETURNED_KEY = 'cluster'

OPTIONS = {
    'cluster_name': {
        'description': ['The name of the K8s cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The Kubernetes version that the cluster is running. This limits which Kubernetes versions can run in a cluster\'s node pools. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': ['The maintenance window is used to update the control plane and the K8s version of the cluster. If no value is specified, it is chosen dynamically, so there is no fixed default value.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
    },
    'api_subnet_allow_list': {
        'description': ['Access to the K8s API server is restricted to these CIDRs. Intra-cluster traffic is not affected by this restriction. If no AllowList is specified, access is not limited. If an IP is specified without a subnet mask, the default value is 32 for IPv4 and 128 for IPv6.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    's3_buckets_param': {
        'description': ['List of S3 buckets configured for K8s usage. At the moment, it contains only one S3 bucket that is used to store K8s API audit logs.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    'public': {
        'description': ['The indicator if the cluster is public or private.'],
        'available': ['present'],
        'type': 'bool'
    },
    'location': {
        'description': 'The location of the cluster if the cluster is private. This property is immutable. The '
                       'location must be enabled for your contract or you must have a Datacenter within that '
                       'location. This attribute is mandatory if the cluster is private.',
        'available': ['present'],
        'type': 'str'
    },
    'nat_gateway_ip': {
        'description': 'The nat gateway IP of the cluster if the cluster is private.',
        'available': ['present'],
        'type': 'str'
    },
    'node_subnet': {
        'description': 'The node subnet of the cluster if the cluster is private.',
        'available': ['present'],
        'type': 'str'
    },
    **get_default_options(STATES),
}


DOCUMENTATION = """
module: k8s_cluster
short_description: Create or destroy a K8s Cluster.
description:
     - This is a simple module that supports creating or removing K8s Clusters.
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
    api_subnet_allow_list:
        description:
        - Access to the K8s API server is restricted to these CIDRs. Intra-cluster traffic
            is not affected by this restriction. If no AllowList is specified, access
            is not limited. If an IP is specified without a subnet mask, the default value
            is 32 for IPv4 and 128 for IPv6.
        elements: str
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
    cluster_name:
        description:
        - The name of the K8s cluster.
        required: false
    k8s_cluster:
        description:
        - The ID or name of the K8s cluster.
        required: false
    k8s_version:
        description:
        - The Kubernetes version that the cluster is running. This limits which Kubernetes
            versions can run in a cluster's node pools. Also, not all Kubernetes versions
            are suitable upgrade targets for all earlier versions.
        required: false
    location:
        description: The location of the cluster if the cluster is private. This property
            is immutable. The location must be enabled for your contract or you must have
            a Datacenter within that location. This attribute is mandatory if the cluster
            is private.
        required: false
    maintenance_window:
        description:
        - The maintenance window is used to update the control plane and the K8s version
            of the cluster. If no value is specified, it is chosen dynamically, so there
            is no fixed default value.
        required: false
    nat_gateway_ip:
        description: The nat gateway IP of the cluster if the cluster is private.
        required: false
    node_subnet:
        description: The node subnet of the cluster if the cluster is private.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    public:
        description:
        - The indicator if the cluster is public or private.
        required: false
    s3_buckets_param:
        description:
        - List of S3 buckets configured for K8s usage. At the moment, it contains only
            one S3 bucket that is used to store K8s API audit logs.
        elements: str
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
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create k8s cluster
    k8s_cluster:
      name: ClusterName
  ''',
  'update' : '''
  - name: Update k8s cluster
    k8s_cluster:
      k8s_cluster: ClusterName
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      k8s_version: 1.17.8
      state: update
  ''',
  'absent' : '''
  - name: Delete k8s cluster
    k8s_cluster:
      k8s_cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  ''',
}

EXAMPLES = """
  - name: Create k8s cluster
    k8s_cluster:
      name: ClusterName
  

  - name: Update k8s cluster
    k8s_cluster:
      k8s_cluster: ClusterName
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      k8s_version: 1.17.8
      state: update
  

  - name: Delete k8s cluster
    k8s_cluster:
      k8s_cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
"""


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
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('cluster_name') is not None
            and existing_object.properties.name != self.module.params.get('cluster_name')
            or self.module.params.get('k8s_version') is not None
            and existing_object.properties.k8s_version != self.module.params.get('k8s_version')
            or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            ) or self.module.params.get('api_subnet_allow_list') is not None
            and sorted(existing_object.properties.api_subnet_allow_list) != sorted(self.module.params.get('api_subnet_allow_list'))
            or self.module.params.get('s3_buckets_param') is not None
            and sorted(list(map(lambda o: o.name, existing_object.properties.s3_buckets))) != sorted(self.module.params.get('s3_buckets_param'))
        )


    def _get_object_list(self, clients):
        return ionoscloud.KubernetesApi(clients[0]).k8s_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('cluster_name')


    def _get_object_identifier(self):
        return self.module.params.get('k8s_cluster')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        cluster_name = self.module.params.get('cluster_name')
        k8s_version = self.module.params.get('k8s_version')
        maintenance = self.module.params.get('maintenance_window')
        public = self.module.params.get('public')
        location = self.module.params.get('location')
        nat_gateway_ip = self.module.params.get('nat_gateway_ip')
        node_subnet = self.module.params.get('node_subnet')
        wait = self.module.params.get('wait')
        api_subnet_allow_list = self.module.params.get('api_subnet_allow_list')
        s3_buckets = list(map(lambda bucket_name: S3Bucket(name=bucket_name), self.module.params.get('s3_buckets_param'))) if self.module.params.get('s3_buckets_param') else None

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
            api_subnet_allow_list = existing_object.properties.api_subnet_allow_list if api_subnet_allow_list is None else api_subnet_allow_list
            s3_buckets = existing_object.properties.s3_buckets if s3_buckets is None else s3_buckets
            maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            k8s_cluster_properties = KubernetesClusterProperties(
                name=cluster_name,
                k8s_version=k8s_version,
                maintenance_window=maintenance_window,
                api_subnet_allow_list=api_subnet_allow_list,
                s3_buckets=s3_buckets,
                public=public,
                nat_gateway_ip=nat_gateway_ip,
                node_subnet=node_subnet,
                location=location
            )
            k8s_cluster = KubernetesCluster(properties=k8s_cluster_properties)

            k8s_response = k8s_api.k8s_post(kubernetes_cluster=k8s_cluster)

            if wait:
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_find_by_cluster_id(k8s_response.id).metadata.state,
                    fn_check=lambda r: r == 'ACTIVE',
                    scaleup=10000,
                    timeout=wait_timeout,
                )
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
        return k8s_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        cluster_name = self.module.params.get('cluster_name')
        k8s_version = self.module.params.get('k8s_version')
        maintenance = self.module.params.get('maintenance_window')
        api_subnet_allow_list = self.module.params.get('api_subnet_allow_list')

        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        s3_buckets = list(map(lambda bucket_name: S3Bucket(name=bucket_name), self.module.params.get('s3_buckets_param'))) if self.module.params.get('s3_buckets_param') else None

        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
        kubernetes_cluster_properties = KubernetesClusterPropertiesForPut(
            name=cluster_name,
            k8s_version=k8s_version,
            s3_buckets=s3_buckets,
            api_subnet_allow_list=api_subnet_allow_list,
            maintenance_window=maintenance_window,
        )
        kubernetes_cluster = KubernetesClusterForPut(properties=kubernetes_cluster_properties)

        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            k8s_response = k8s_api.k8s_put(k8s_cluster_id=existing_object.id, kubernetes_cluster=kubernetes_cluster)
            if wait:
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_find_by_cluster_id(existing_object.id).metadata.state,
                    fn_check=lambda r: r == 'ACTIVE',
                    scaleup=10000,
                    timeout=wait_timeout,
                )

            return k8s_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        k8s_api = ionoscloud.KubernetesApi(api_client=client)

        try:
            if existing_object.metadata.state != 'DESTROYING':
                k8s_api.k8s_delete_with_http_info(k8s_cluster_id=existing_object.id)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_get(depth=1),
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
    ionos_module.main()
