from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible import __version__

HAS_SDK = True

try:
    import ionoscloud
    import ionoscloud_dataplatform
    from ionoscloud_dataplatform import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
CLOUDAPI_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dataplatform/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'dataplatform'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Data Platform Cluster'
RETURNED_KEY = 'dataplatform_cluster'

OPTIONS = {
    'name': {
        'description': ['The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'cluster': {
        'description': ['The ID or name of the Data Platform cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'dataplatform_version': {
        'description': ['The version of the data platform.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The UUID of the virtual data center (VDC) the cluster is provisioned.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': ['Starting time of a weekly 4-hour-long window, during which maintenance might occur in the `HH:MM:SS` format.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "datacenter", "note": "" },
]

DOCUMENTATION = """
module: dataplatform_cluster
short_description: Create or destroy a Data Platform Cluster.
description:
     - This is a simple module that supports creating or removing Data Platform Clusters.
       This module has a dependency on ionoscloud >= 6.0.2
     - ⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.
version_added: "2.0"
options:
    ilowuerhfgwoqrghbqwoguh
requirements:
    - "python >= 2.6"
    - "ionoscloud_dataplatform >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create Data Platform cluster
    dataplatform_cluster:
      name: ClusterName
  ''',
  'update' : '''
  - name: Update Data Platform cluster
    dataplatform_cluster:
      cluster: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      dataplatform_version: 1.17.8
      state: update
  ''',
  'absent' : '''
  - name: Delete Data Platform cluster
    dataplatform_cluster:
      cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class DataPlatformClusterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dataplatform, ionoscloud]
        self.user_agent = USER_AGENT
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        datacenter_id = get_resource_id(
            self.module,
            ionoscloud.DataCentersApi(clients[1]).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        return (
            datacenter_id is not None
            and existing_object.properties.datacenter_id != datacenter_id
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('dataplatform_version') is not None
            and existing_object.properties.data_platform_version != self.module.params.get('dataplatform_version')
            or self.module.params.get('maintenance_window') is not None
            and (
                existing_object.properties.maintenance_window.day_of_the_week != self.module.params.get('maintenance_window').get('day_of_the_week')
                or existing_object.properties.maintenance_window.time != self.module.params.get('maintenance_window').get('time')
            )
        )


    def _get_object_list(self, clients):
        return ionoscloud_dataplatform.DataPlatformClusterApi(clients[0]).get_clusters()


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('cluster')


    def _create_object(self, existing_object, clients):
        dataplatform_client = clients[0]
        cloudapi_client = clients[1]
        name = self.module.params.get('name')
        dataplatform_version = self.module.params.get('dataplatform_version')
        maintenance = self.module.params.get('maintenance_window')

        datacenter_id = get_resource_id(
            self.module,
            ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        maintenance_window = None
        if maintenance:
            maintenance_window = dict(maintenance)
            maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            dataplatform_version = existing_object.properties.dataplatform_version if dataplatform_version is None else dataplatform_version
            datacenter_id = existing_object.properties.datacenter_id if datacenter_id is None else datacenter_id
            maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance

        dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(dataplatform_client)
        
        cluster_properties = ionoscloud_dataplatform.CreateClusterProperties(
            name=name,
            data_platform_version=dataplatform_version,
            maintenance_window=maintenance_window,
            datacenter_id=datacenter_id,
        )
        cluster = ionoscloud_dataplatform.CreateClusterRequest(properties=cluster_properties)

        try:
            response = dataplatform_cluster_api.create_cluster(create_cluster_request=cluster)

            if self.module.params.get('wait'):
                dataplatform_client.wait_for(
                    fn_request=lambda: dataplatform_cluster_api.get_clusters(),
                    fn_check=lambda r: list(filter(
                        lambda e: e.properties.name == name,
                        r.items
                    ))[0].metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )
        except ionoscloud_dataplatform.ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        dataplatform_version = self.module.params.get('dataplatform_version')
        maintenance = self.module.params.get('maintenance_window')

        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

        dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client)

        _cluster_properties = ionoscloud_dataplatform.PatchClusterProperties(
            name=name,
            data_platform_version=dataplatform_version,
            maintenance_window=maintenance_window,
        )
        patch_cluster = ionoscloud_dataplatform.PatchClusterRequest(properties=_cluster_properties)

        try:
            response = dataplatform_cluster_api.patch_cluster(existing_object.id, patch_cluster)
            
            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: dataplatform_cluster_api.get_clusters(),
                    fn_check=lambda r: list(filter(
                        lambda e: e.properties.name == name,
                        r.items
                    ))[0].metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )

            return response
        except ionoscloud_dataplatform.ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client)

        try:
            if existing_object.metadata.state == 'AVAILABLE':
                dataplatform_cluster_api.delete_cluster(existing_object.id)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: dataplatform_cluster_api.get_clusters(),
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
    ionos_module = DataPlatformClusterModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_dataplatform are required for this module, run `pip install ionoscloud ionoscloud_dataplatform`')
    ionos_module.main()
