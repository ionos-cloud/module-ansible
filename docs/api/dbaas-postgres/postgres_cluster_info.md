# postgres_cluster_info

This is a simple module that supports listing existing Postgres Clusters

## Example Syntax


```yaml

    - name: List Postgres Clusters
        postgres_cluster_info:
        register: postgres_clusters_response


    - name: Show Postgres Clusters
        debug:
            var: postgres_clusters_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| filters<br /><span>\<dict\></span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
| username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
