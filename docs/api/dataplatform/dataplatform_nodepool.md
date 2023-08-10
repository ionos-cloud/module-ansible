# dataplatform_nodepool

This is a simple module that supports creating or removing Data Platform Nodepools. This module has a dependency on ionoscloud_dataplatform &gt;= 1.0.0

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

  - name: Create Data Platform nodepool
    dataplatform_nodepool:
      name: NodepoolName
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: 1
      ram_size: 2048
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: 100
  

  - name: Update Data Platform nodepool
    dataplatform_nodepool:
      nodepool: NodepoolName
      cluster: ClusterName
      node_count: 1
      cores_count: 1
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      state: update
  

  - name: Delete Data Platform nodepool
    dataplatform_nodepool:
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "dataplatform_nodepool": {
        "id": "6fcf85d2-d503-41e7-9f08-cbfa9ac6be80",
        "type": "nodepool",
        "href": "https://api.ionos.com/dataplatform/clusters/fe6a5792-7473-4067-ba83-6d135582e623/nodepools/6fcf85d2-d503-41e7-9f08-cbfa9ac6be80",
        "metadata": {
            "e_tag": null,
            "created_date": "2023-05-29T14:06:54+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_in_contract_number": "31909592",
            "last_modified_date": "2023-05-29T14:06:54+00:00",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "current_data_platform_version": "22.11",
            "current_data_platform_revision": 1,
            "available_upgrade_versions": [],
            "state": "DEPLOYING"
        },
        "properties": {
            "name": "my-nodepool",
            "data_platform_version": null,
            "datacenter_id": "f68205d8-8334-43b0-9f64-b06babcf5bd6",
            "node_count": 2,
            "cpu_family": "INTEL_SKYLAKE",
            "cores_count": 1,
            "ram_size": 2048,
            "availability_zone": "AUTO",
            "storage_type": "HDD",
            "storage_size": 100,
            "maintenance_window": {
                "time": "12:02:00",
                "day_of_the_week": "Wednesday"
            },
            "labels": {
                "color": "red",
                "foo": "bar",
                "size": "10"
            },
            "annotations": {
                "ann1": "value1",
                "ann2": "value2"
            }
        }
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Data Platform nodepool
    dataplatform_nodepool:
      name: NodepoolName
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: 1
      ram_size: 2048
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: 100
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span class="blue-span">str</span> | True | The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | cluster<br /><span class="blue-span">str</span> | True | The name or ID of the Data Platform cluster. |
  | node_count<br /><span class="blue-span">int</span> | True | The number of nodes that make up the node pool. |
  | cpu_family<br /><span class="blue-span">str</span> | True | A valid CPU family name or `AUTO` if the platform shall choose the best fitting option. Available CPU architectures can be retrieved from the data center resource. |
  | cores_count<br /><span class="blue-span">int</span> | True | The number of CPU cores per node. |
  | ram_size<br /><span class="blue-span">int</span> | True | The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a minimum size is of 2048 MB. |
  | availability_zone<br /><span class="blue-span">str</span> | True | The availability zone of the virtual data center region where the node pool resources should be provisioned. |
  | storage_type<br /><span class="blue-span">str</span> | True | The type of hardware for the volume. |
  | storage_size<br /><span class="blue-span">int</span> | True | The size of the volume in GB. The size must be greater than 10 GB. |
  | maintenance_window<br /><span class="blue-span">dict</span> | False | Starting time of a weekly 4 hour-long window, during which maintenance might occur in hh:mm:ss format |
  | labels<br /><span class="blue-span">dict</span> | False | Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) |
  | annotations<br /><span class="blue-span">dict</span> | False | Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Data Platform nodepool
    dataplatform_nodepool:
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | cluster<br /><span class="blue-span">str</span> | True | The name or ID of the Data Platform cluster. |
  | nodepool<br /><span class="blue-span">str</span> | True | The name or ID of the Data Platform nodepool. |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Data Platform nodepool
    dataplatform_nodepool:
      nodepool: NodepoolName
      cluster: ClusterName
      node_count: 1
      cores_count: 1
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span class="blue-span">str</span> | False | The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | cluster<br /><span class="blue-span">str</span> | True | The name or ID of the Data Platform cluster. |
  | nodepool<br /><span class="blue-span">str</span> | True | The name or ID of the Data Platform nodepool. |
  | node_count<br /><span class="blue-span">int</span> | False | The number of nodes that make up the node pool. |
  | maintenance_window<br /><span class="blue-span">dict</span> | False | Starting time of a weekly 4 hour-long window, during which maintenance might occur in hh:mm:ss format |
  | labels<br /><span class="blue-span">dict</span> | False | Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) |
  | annotations<br /><span class="blue-span">dict</span> | False | Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
