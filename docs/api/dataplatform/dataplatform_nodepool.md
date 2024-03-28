# dataplatform_nodepool

This is a simple module that supports creating or removing Data Platform Nodepools. This module has a dependency on ionoscloud_dataplatform &gt;= 1.0.0

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

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

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dataplatform).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * name 
  * cpu_family 
  * cores_count 
  * ram_size 
  * availability_zone 
  * storage_type 
  * storage_size 
&nbsp;

# state: **present**
```yaml
  
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

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the Data Platform cluster.</td>
  </tr>
  <tr>
  <td>node_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of nodes that make up the node pool.</td>
  </tr>
  <tr>
  <td>cpu_family<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>A valid CPU family name or `AUTO` if the platform shall choose the best fitting option. Available CPU architectures can be retrieved from the data center resource.</td>
  </tr>
  <tr>
  <td>cores_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of CPU cores per node.</td>
  </tr>
  <tr>
  <td>ram_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a minimum size is of 2048 MB.</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The availability zone of the virtual data center region where the node pool resources should be provisioned.</td>
  </tr>
  <tr>
  <td>storage_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The type of hardware for the volume.</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The size of the volume in GB. The size must be greater than 10 GB.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Starting time of a weekly 4-hour-long window, during which maintenance might occur in the `HH:MM:SS` format.</td>
  </tr>
  <tr>
  <td>labels<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).</td>
  </tr>
  <tr>
  <td>annotations<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete DataPlatform cluster nodepool
ionoscloudsdk.ionoscloud.dataplatform_nodepool:
  cluster: ''
  nodepool: ''
  wait: true
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the Data Platform cluster.</td>
  </tr>
  <tr>
  <td>nodepool<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the Data Platform nodepool.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
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

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the Data Platform cluster.</td>
  </tr>
  <tr>
  <td>nodepool<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the Data Platform nodepool.</td>
  </tr>
  <tr>
  <td>node_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of nodes that make up the node pool.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Starting time of a weekly 4-hour-long window, during which maintenance might occur in the `HH:MM:SS` format.</td>
  </tr>
  <tr>
  <td>labels<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).</td>
  </tr>
  <tr>
  <td>annotations<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
