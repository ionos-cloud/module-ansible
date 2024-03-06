# k8s_nodepool

This is a simple module that supports creating or removing K8s Nodepools. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
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

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "nodepool": {
        "href": "https://api.ionos.com/cloudapi/v6/k8s/b08b63ff-8bee-4091-ad5f-f8296eedd93b/nodepools/2d5b0b1c-67aa-4b9f-a899-c729619fa4ce",
        "id": "2d5b0b1c-67aa-4b9f-a899-c729619fa4ce",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T09:48:08+00:00",
            "etag": "ddb146ab080132c5d4ecc05871c32c74",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T09:48:08+00:00",
            "state": "DEPLOYING"
        },
        "properties": {
            "annotations": {
                "ann1": "value1",
                "ann2": "value2"
            },
            "auto_scaling": {
                "max_node_count": 3,
                "min_node_count": 1
            },
            "availability_zone": "AUTO",
            "available_upgrade_versions": null,
            "cores_count": 1,
            "cpu_family": "INTEL_SKYLAKE",
            "datacenter_id": "c38a3861-3af3-4ecf-9c83-54021512e9d9",
            "k8s_version": null,
            "labels": {
                "foo": "bar",
                "color": "red",
                "size": "10"
            },
            "lans": [
                {
                    "datacenter_id": null,
                    "dhcp": false,
                    "id": 1,
                    "routes": []
                }
            ],
            "maintenance_window": {
                "day_of_the_week": "Friday",
                "time": "22:00:08Z"
            },
            "name": "my-nodepool-54",
            "node_count": 2,
            "public_ips": [
                "<IP1>",
                "<IP2>",
                "<IP3>",
                "<IP4>"
            ],
            "ram_size": 2048,
            "storage_size": 100,
            "storage_type": "HDD"
        },
        "type": "nodepool"
    }
}

```

&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * datacenter 
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
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>k8s_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located.</td>
  </tr>
  <tr>
  <td>lans<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The array of existing private LANs to attach to worker nodes.</td>
  </tr>
  <tr>
  <td>node_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of worker nodes of the node pool.</td>
  </tr>
  <tr>
  <td>cpu_family<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The CPU type for the nodes.</td>
  </tr>
  <tr>
  <td>cores_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of cores for the nodes.</td>
  </tr>
  <tr>
  <td>ram_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB.</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The availability zone in which the target VM should be provisioned.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2']</td>
  </tr>
  <tr>
  <td>storage_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The storage type for the nodes.<br />Options: ['HDD', 'SSD']</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value.</td>
  </tr>
  <tr>
  <td>labels<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The labels attached to the node pool.</td>
  </tr>
  <tr>
  <td>annotations<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The annotations attached to the node pool.</td>
  </tr>
  <tr>
  <td>auto_scaling<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled.</td>
  </tr>
  <tr>
  <td>public_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool's data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt.</td>
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
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
  name: Delete k8s cluster nodepool
ionoscloudsdk.ionoscloud.k8s_nodepool:
  k8s_cluster: ''
  k8s_nodepool: ''
  wait: false
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
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>k8s_nodepool<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s nodepool.</td>
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
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
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>k8s_nodepool<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s nodepool.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>k8s_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located.</td>
  </tr>
  <tr>
  <td>lans<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The array of existing private LANs to attach to worker nodes.</td>
  </tr>
  <tr>
  <td>node_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of worker nodes of the node pool.</td>
  </tr>
  <tr>
  <td>cpu_family<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The CPU type for the nodes.</td>
  </tr>
  <tr>
  <td>cores_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of cores for the nodes.</td>
  </tr>
  <tr>
  <td>ram_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB.</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The availability zone in which the target VM should be provisioned.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2']</td>
  </tr>
  <tr>
  <td>storage_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The storage type for the nodes.<br />Options: ['HDD', 'SSD']</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value.</td>
  </tr>
  <tr>
  <td>labels<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The labels attached to the node pool.</td>
  </tr>
  <tr>
  <td>annotations<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The annotations attached to the node pool.</td>
  </tr>
  <tr>
  <td>auto_scaling<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled.</td>
  </tr>
  <tr>
  <td>public_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool's data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt.</td>
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
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
