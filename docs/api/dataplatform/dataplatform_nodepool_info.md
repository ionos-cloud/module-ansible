# dataplatform_nodepool_info

This is a simple module that supports listing existing DataPlatform Nodepools

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

    - name: List DataPlatform Nodepools
        dataplatform_nodepool_info:
            cluster: ClusterName
        register: dataplatform_nodepools_response


    - name: Show DataPlatform Clusters
        debug:
            var: dataplatform_nodepools_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| filters<br /><span class="blue-span">dict</span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| cluster<br /><span class="blue-span">str</span> | True | The ID of the Data Platform cluster. |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
