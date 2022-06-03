# postgres_backup_info

This is a simple module that supports listing existing Postgres Cluster backups

## Example Syntax


```yaml

    - name: List Postgres Cluster Backups
        postgres_cluster_info:
            postgres_cluster: {{ postgres_cluster.id }}
        register: postgres_clusters_response

    - name: Show Postgres Cluster Backups
        debug:
            var: postgres_clusters_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| postgres_cluster | False | str |  | The ID or name of an existing Postgres Cluster. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
