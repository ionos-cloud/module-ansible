# mongo_cluster_user_info

This is a simple module that supports listing existing Mongo Clusters

## Example Syntax


```yaml

    - name: List Mongo Clusters
        mongo_cluster_info:
        register: mongo_clusters_response


    - name: Show Mongo Clusters
        debug:
            var: mongo_clusters_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| mongo_cluster<br /><span style="color:#003d8f">str</span> | True | The UUID or name of an existing Mongo Cluster. |
| filters<br /><span style="color:#003d8f">dict</span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
| username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
