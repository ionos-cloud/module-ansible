# Kubernetes cluster

## Example Syntax

```yaml
    - name: Create k8s cluster
      k8s_cluster:
        name: "{{ cluster_name }}"

    - name: Delete k8s cluster
      k8s_cluster:
        k8s_cluster_id: "{{k8s.id}}"
        state: absent

    - name: Update k8s cluster
      k8s_cluster:
        k8s_cluster_id: "{{k8s.id}}"
        maintenance_window:
          day: 'Tuesday'
          time: '13:03:00'
        k8s_version: 1.17.8
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| cluster\_name | **yes**/no | string |  | The name of the cluster. Required only for state = 'present' and state = 'update' |
| public | no | string |  | The indicator if the cluster is public or private |
| api_subnet_allow_list | list | string |  | Access to the K8s API server is restricted to these CIDRs. Traffic, internal to the cluster, is not affected by this restriction. If no allowlist is specified, access is not restricted. If an IP without subnet mask is provided, the default value is used: 32 for IPv4 and 128 for IPv6. |
| s3_buckets | no | list |  | List of S3 bucket configured for K8s usage. For now it contains only an S3 bucket used to store K8s API audit logs. |
| k8s\_cluster\_id | **yes** | string |  | The ID of the cluster. Required only for state = 'update' or state = 'absent' |
| k8s\_version | no | string |  | The kubernetes version in which the cluster is running. |
| maintenance\_window | no | dict |  | The day and time for the maintenance. Contains 'day_of_the_week' and 'time'. |

