# dataplatform_nodepool_info

This is a simple module that supports listing existing DataPlatform Nodepools

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

    - name: List DataPlatform Nodepools
        dataplatform_nodepool_info:
            cluster: {{ cluster_id }}
        register: dataplatform_nodepools_response


    - name: Show DataPlatform Clusters
        debug:
            var: dataplatform_nodepools_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| cluster | True | str |  | The ID of the Data Platform cluster. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
