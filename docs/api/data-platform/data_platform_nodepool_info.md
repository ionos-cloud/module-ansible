# data_platform_nodepool_info

This is a simple module that supports listing existing DataPlatform Nodepools

## Example Syntax


```yaml

    - name: List DataPlatform Nodepools
        data_platform_nodepool_info:
        register: data_platform_nodepools_response


    - name: Show DataPlatform Clusters
        debug:
            var: data_platform_nodepools_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| data_platform_cluster_id | True | str |  | The ID of the Data Platform cluster. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
