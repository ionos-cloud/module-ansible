# dataplatform_nodepool_info

This is a simple module that supports listing existing DataPlatform Nodepools

## Example Syntax


```yaml

    - name: List DataPlatform Nodepools
        dataplatform_nodepool_info:
        register: dataplatform_nodepools_response


    - name: Show DataPlatform Clusters
        debug:
            var: dataplatform_nodepools_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| cluster | True | str |  | The ID of the Data Platform cluster. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
