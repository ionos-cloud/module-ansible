# Kubernetes cluster

## Example Syntax

```yaml
    - name: Create k8s cluster
      ionoscloudsdk.ionoscloud.k8s_cluster:
        name: "{{ cluster_name }}"

    - name: Delete k8s cluster
      ionoscloudsdk.ionoscloud.k8s_cluster:
        k8s_cluster_id: "{{k8s.id}}"
        state: absent

    - name: Update k8s cluster
      ionoscloudsdk.ionoscloud.k8s_cluster:
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
| cluster\_name | **yes**/no | string |  | The name of the cluster. Required only for state = 'present' |
| k8s\_cluster\_id | **yes** | string |  | The ID of the cluster. Required only for state = 'update' or state = 'absent' |
| k8s\_version | no | string |  | The kubernetes version in which the cluster is running. |
| maintenance\_window | no | dict |  | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'. |

