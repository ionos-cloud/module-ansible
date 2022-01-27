# Kubernetes cluster

## Example Syntax

```text
    - name: Create or edit k8s cluster
      k8s_cluster:
        cluster_name: "{{ cluster_name }}" 
        maintenance_window:
          day_of_the_week: 'Tuesday'
          time: '13:03:00'
        k8s_version: 1.20.10
      register: k8s_response

    - name: Update k8s version of cluster above
      k8s_cluster:
        k8s_cluster_id: "{{ k8s_response.cluster.id }}"
        cluster_name: "{{ k8s_response.cluster.properties.name }}"
        state: update

    - name: Delete a k8s cluster
      k8s_cluster:
        k8s_cluster_id: "{{ k8s.id }}"
        state: absent

```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| cluster\_name | **yes**/no | string |  | The name of the cluster. Required for state = 'present' and state = 'update' |
| k8s\_cluster\_id | **yes** | string |  | The ID of the cluster. Required only for state = 'update' or state = 'absent' |
| k8s\_version | no | string |  | The kubernetes version in which the cluster is running. |
| maintenance\_window | no | dict |  | The day and time for the maintenance. Contains 'day_of_the_week' and 'time'. |

