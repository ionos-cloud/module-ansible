# postgres_backup_info

This is a simple module that supports listing existing Postgres Cluster backups

## Example Syntax


```yaml

    - name: List Postgres Cluster Backups
        postgres_cluster_info:
            postgres_cluster: backuptest-04
        register: postgres_clusters_response

    - name: Show Postgres Cluster Backups
        debug:
            var: postgres_clusters_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| postgres_cluster<br /><span class="blue-span">str</span> | False | The ID or name of an existing Postgres Cluster. |
| filters<br /><span class="blue-span">dict</span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><span class="blue-span">str</span> | False | The Ionos API certificate fingerprint. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
