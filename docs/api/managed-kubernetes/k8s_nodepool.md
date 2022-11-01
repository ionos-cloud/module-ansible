# k8s_nodepool

This is a simple module that supports creating or removing K8s Nodepools. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter_id: "4d495548-e330-434d-83a9-251bfa645875"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: "1"
      ram_size: "2048"
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: "100"
  

  - name: Update k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      nodepool_id: "6e9efcc6-649a-4514-bee5-6165b614c89e"
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
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      datacenter_id: "4d495548-e330-434d-83a9-251bfa645875"
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | nodepool_name | True | str |  | The name of the K8s Nodepool. |
  | k8s_cluster_id | True | str |  | The ID of the K8s cluster. |
  | k8s_version | False | str |  | The Kubernetes version the nodepool is running. |
  | datacenter_id | True | str |  | A valid ID of the data center, to which the user has access. |
  | lan_ids | False | list |  | Array of additional LANs attached to worker nodes. |
  | node_count | False | int |  | The number of nodes that make up the node pool. |
  | cpu_family | True | str |  | A valid CPU family name. |
  | cores_count | True | str |  | The number of cores for the node. |
  | ram_size | True | str |  | The RAM size for the node. Must be set in multiples of 1024 MB, with minimum size is of 2048 MB. |
  | availability_zone | True | str |  | The availability zone in which the target VM should be provisioned. |
  | storage_type | True | str |  | The type of hardware for the volume. |
  | storage_size | True | str |  | The size of the volume in GB. The size should be greater than 10GB. |
  | maintenance_window | False | dict |  | The maintenance window is used for updating the software on the nodepool's nodes and for upgrading the nodepool's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | labels | False | dict |  | Map of labels attached to node pool. |
  | annotations | False | dict |  | Map of annotations attached to node pool. |
  | auto_scaling | False | dict |  | Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled. |
  | public_ips | False | list |  | Optional array of reserved public IP addresses to be used by the nodes. IPs must be from same location as the data center used for the node pool. The array must contain one more IP than maximum number possible number of nodes (nodeCount+1 for fixed number of nodes or maxNodeCount+1 when auto scaling is used). The extra IP is used when the nodes are rebuilt. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete k8s cluster nodepool
    k8s_nodepools:
      k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | k8s_cluster_id | True | str |  | The ID of the K8s cluster. |
  | nodepool_id | True | str |  | The ID of the K8s nodepool. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update k8s cluster nodepool
    k8s_nodepools:
      cluster_name: "{{ name }}"
      k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      nodepool_id: "6e9efcc6-649a-4514-bee5-6165b614c89e"
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | nodepool_name | False | str |  | The name of the K8s Nodepool. |
  | k8s_cluster_id | True | str |  | The ID of the K8s cluster. |
  | k8s_version | False | str |  | The Kubernetes version the nodepool is running. |
  | nodepool_id | True | str |  | The ID of the K8s nodepool. |
  | datacenter_id | False | str |  | A valid ID of the data center, to which the user has access. |
  | lan_ids | False | list |  | Array of additional LANs attached to worker nodes. |
  | node_count | False | int |  | The number of nodes that make up the node pool. |
  | maintenance_window | False | dict |  | The maintenance window is used for updating the software on the nodepool's nodes and for upgrading the nodepool's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | labels | False | dict |  | Map of labels attached to node pool. |
  | annotations | False | dict |  | Map of annotations attached to node pool. |
  | auto_scaling | False | dict |  | Property to be set when auto-scaling needs to be enabled for the nodepool. By default, auto-scaling is not enabled. |
  | public_ips | False | list |  | Optional array of reserved public IP addresses to be used by the nodes. IPs must be from same location as the data center used for the node pool. The array must contain one more IP than maximum number possible number of nodes (nodeCount+1 for fixed number of nodes or maxNodeCount+1 when auto scaling is used). The extra IP is used when the nodes are rebuilt. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
