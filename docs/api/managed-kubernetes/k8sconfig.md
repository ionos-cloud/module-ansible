# Kubernetes configuration

## Example Syntax

```text
    - name: Get k8s config
      ionoscloudsdk.ionoscloud.k8s_config:
        k8s_cluster_id: {{k8s.id}}"
        config_file: 'config.yaml'
        state: present
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| k8s\_cluster\_id | **yes** | string |  | The ID of the cluster. |
| config\_file | **yes** | string |  | The name of the file that will contain the configuration of the cluster. |

