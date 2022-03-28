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

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| api_url | False | str |  | The Ionos API base URL. |
| username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
