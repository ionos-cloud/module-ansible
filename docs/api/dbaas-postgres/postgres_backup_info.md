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

&nbsp;

&nbsp;
## Returned object
```json
{
    "postgres_backups": [
        {
            "type": "backup",
            "id": "06b53b38-398a-4fc6-8eed-a8f3d4847a76-4oymiqu-12",
            "metadata": {
                "created_date": "2023-08-09T14:55:33+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "id": null,
                "cluster_id": "06b53b38-398a-4fc6-8eed-a8f3d4847a76",
                "version": "12",
                "is_active": true,
                "earliest_recovery_target_time": "2023-08-09T15:07:48+00:00"
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| postgres_cluster | False | str |  | The ID or name of an existing Postgres Cluster. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
