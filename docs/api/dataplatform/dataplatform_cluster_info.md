# dataplatform_cluster_info

This is a simple module that supports listing existing DataPlatform Clusters

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

    - name: List DataPlatform Clusters
        dataplatform_cluster_info:
        register: dataplatform_clusters_response


    - name: Show DataPlatform Clusters
        debug:
            var: dataplatform_clusters_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| filters<br /><mark style="color:blue;">\<dict\></mark> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
| username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
