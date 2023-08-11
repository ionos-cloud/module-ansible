# k8s_nodepool

This is a simple module that supports creating or removing K8s Nodepools. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter: "4d495548-e330-434d-83a9-251bfa645875"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: "1"
      ram_size: "2048"
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: "100"
  

  - name: Update k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      k8s_nodepool: "6e9efcc6-649a-4514-bee5-6165b614c89e"
      node_count: 1
      cores_count: "1"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      auto_scaling:
        min_node_count: 1
        max_node_count: 3
      state: update
  

  - name: Delete k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      k8s_nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
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

&nbsp;

# state: **present**
```yaml
  
  - name: Create k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter: "4d495548-e330-434d-83a9-251bfa645875"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: "1"
      ram_size: "2048"
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: "100"
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | k8s_cluster<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the K8s cluster. |
  | name<br /><mark style="color:blue;">\<str\></mark> | True | A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | k8s_version<br /><mark style="color:blue;">\<str\></mark> | False | The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located. |
  | lans<br /><mark style="color:blue;">\<list\></mark> | False | The array of existing private LANs to attach to worker nodes. |
  | node_count<br /><mark style="color:blue;">\<int\></mark> | False | The number of worker nodes of the node pool. |
  | cpu_family<br /><mark style="color:blue;">\<str\></mark> | True | The CPU type for the nodes. |
  | cores_count<br /><mark style="color:blue;">\<int\></mark> | True | The total number of cores for the nodes. |
  | ram_size<br /><mark style="color:blue;">\<int\></mark> | True | The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB. |
  | availability_zone<br /><mark style="color:blue;">\<str\></mark> | False | The availability zone in which the target VM should be provisioned.<br />Default: AUTO<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2'] |
  | storage_type<br /><mark style="color:blue;">\<str\></mark> | True | The storage type for the nodes.<br />Options: ['HDD', 'SSD'] |
  | storage_size<br /><mark style="color:blue;">\<int\></mark> | True | The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD. |
  | maintenance_window<br /><mark style="color:blue;">\<dict\></mark> | False | The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value. |
  | labels<br /><mark style="color:blue;">\<dict\></mark> | False | The labels attached to the node pool. |
  | annotations<br /><mark style="color:blue;">\<dict\></mark> | False | The annotations attached to the node pool. |
  | auto_scaling<br /><mark style="color:blue;">\<dict\></mark> | False | Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled. |
  | public_ips<br /><mark style="color:blue;">\<list\></mark> | False | Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool's data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 3600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      k8s_nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | k8s_cluster<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the K8s cluster. |
  | k8s_nodepool<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the K8s nodepool. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 3600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      k8s_nodepool: "6e9efcc6-649a-4514-bee5-6165b614c89e"
      node_count: 1
      cores_count: "1"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      auto_scaling:
        min_node_count: 1
        max_node_count: 3
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | k8s_cluster<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the K8s cluster. |
  | k8s_nodepool<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the K8s nodepool. |
  | name<br /><mark style="color:blue;">\<str\></mark> | False | A Kubernetes node pool name. Valid Kubernetes node pool name must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | k8s_version<br /><mark style="color:blue;">\<str\></mark> | False | The Kubernetes version running in the node pool. Note that this imposes restrictions on which Kubernetes versions can run in the node pools of a cluster. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | False | The unique identifier of the VDC where the worker nodes of the node pool are provisioned.Note that the data center is located in the exact place where the parent cluster of the node pool is located. |
  | lans<br /><mark style="color:blue;">\<list\></mark> | False | The array of existing private LANs to attach to worker nodes. |
  | node_count<br /><mark style="color:blue;">\<int\></mark> | False | The number of worker nodes of the node pool. |
  | cpu_family<br /><mark style="color:blue;">\<str\></mark> | False | The CPU type for the nodes. |
  | cores_count<br /><mark style="color:blue;">\<int\></mark> | False | The total number of cores for the nodes. |
  | ram_size<br /><mark style="color:blue;">\<int\></mark> | False | The RAM size for the nodes. Must be specified in multiples of 1024 MB, with a minimum size of 2048 MB. |
  | availability_zone<br /><mark style="color:blue;">\<str\></mark> | False | The availability zone in which the target VM should be provisioned.<br />Default: AUTO<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2'] |
  | storage_type<br /><mark style="color:blue;">\<str\></mark> | False | The storage type for the nodes.<br />Options: ['HDD', 'SSD'] |
  | storage_size<br /><mark style="color:blue;">\<int\></mark> | False | The allocated volume size in GB. The allocated volume size in GB. To achieve good performance, we recommend a size greater than 100GB for SSD. |
  | maintenance_window<br /><mark style="color:blue;">\<dict\></mark> | False | The maintenance window is used to update the software on the node pool nodes and update the K8s version of the node pool. If no value is specified, a value is selected dynamically, so there is no fixed default value. |
  | labels<br /><mark style="color:blue;">\<dict\></mark> | False | The labels attached to the node pool. |
  | annotations<br /><mark style="color:blue;">\<dict\></mark> | False | The annotations attached to the node pool. |
  | auto_scaling<br /><mark style="color:blue;">\<dict\></mark> | False | Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled. |
  | public_ips<br /><mark style="color:blue;">\<list\></mark> | False | Optional array of reserved public IP addresses to be used by the nodes. The IPs must be from the exact location of the node pool's data center. If autoscaling is used, the array must contain one more IP than the maximum possible number of nodes (nodeCount+1 for a fixed number of nodes or maxNodeCount+1). The extra IP is used when the nodes are rebuilt. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 3600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
