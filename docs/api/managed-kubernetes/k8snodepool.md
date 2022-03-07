# Kubernetes nodepool

## Example Syntax

```yaml
    - name: Create k8s cluster nodepool
      ionoscloudsdk.ionoscloud.k8s_nodepools:
        cluster_name: "{{ name }}"
        k8s_cluster_id: "{{k8s.id}}"
        datacenter_id: "{{datacenter.id}}"
        node_count: "1"
        cpu_family: "AMD_OPTERON"
        cores_count: "1"
        ram_size: "2048"
        availability_zone: "AUTO"
        storage_type: "SSD"
        storage_size: "100"
        public_ips:
          - 185.132.45.40
          - 217.160.200.52
        state: present

    - name: Delete k8s cluster nodepool
      ionoscloudsdk.ionoscloud.k8s_nodepools:
        k8s_cluster_id: "{{k8s.id}}"
        nodepool_id: "{{nodepool.id}}"
        state: absent

    - name: Update k8s cluster nodepool
      ionoscloudsdk.ionoscloud.k8s_nodepools:
        cluster_name: "{{ name }}"
        k8s_cluster_id: "{{k8s.id}}"
        nodepool_id: "{{nodepool.id}}"
        node_count: 1
        cores_count: "1"
        maintenance_window:
          day: 'Tuesday'
          time: '13:03:00'
        auto_scaling:
          min_node_count: 1
          max_node_count: 3
        public_ips:
          - 185.132.45.40
          - 217.160.200.52
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| nodepool\_name | **yes** | string |  | The name of the nodepool. Required only for state = 'present' |
| k8s\_cluster\_id | **yes** | string |  | The ID of the cluster. |
| nodepool\_id | **yes**/no | string |  | The ID of the nodepool. Required for state = 'update' or state = 'absent' |
| datacenter\_id | **yes**/no | string |  | The ID of the datacenter. Required only for state = 'present' |
| node\_count | **yes**/no | int |  | The number of nodes in the nodepool. Required only for state = 'present' |
| cpu\_family | **yes**/no | string |  | A valid CPU family name. Required only for state = 'update' or state = 'absent' |
| cores\_count | **yes**/no | string |  | The number of cores. Required only for state = 'present' |
| ram\_size | **yes**/no | string |  | RAM size for node, minimum size 2048MB is recommended. Required only for state = 'present' |
| availability\_zone | **yes**/no | string |  | The availability zone in which the server should exist. Required only for state = 'present' |
| storage\_type | **yes**/no | string |  | Hardware type of the volume. Required only for state = 'present' |
| storage\_size | **yes**/no | string |  | The size of the volume in GB. The size should be greater than 10GB. Required only for state = 'present' |
| maintenance\_window | no | dict |  | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'. |
| auto\_scaling | no | dict |  | The minimum and maximum number of worker nodes that the managed node group can scale in. Contains 'min\_node\_count' and 'max\_node\_count'. |
| lan\_ids | no | list |  | Array of additional LANs attached to worker nodes |
| labels | no | dict |  | Map of labels attached to node pool |
| annotations | no | dict |  | Map of annotations attached to node pool |
| public\_ips | no | list |  | Optional array of reserved public IP addresses to be used by the nodes. IPs must be from same location as the data center used for the node pool. The array must contain one extra IP than maximum number of nodes could be. \(`node_count+1` if fixed node amount or `max_node_count+1` if auto scaling is used\). The extra provided IP Will be used during rebuilding of nodes. |
| gateway_ip | **yes**/no | string |  |Public IP address for the gateway performing source NAT for the node pool's nodes belonging to a private cluster. Required only if the node pool belongs to a private cluster. |

