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

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "type": "cluster",
            "id": "46c151c7-55f8-42a4-86c3-06ad6b4b91ea",
            "metadata": {
                "created_date": "2023-05-30T14:35:40+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": "AVAILABLE"
            },
            "properties": {
                "display_name": "backuptest-04",
                "postgres_version": "12",
                "location": "de/fra",
                "backup_location": "eu-central-2",
                "instances": 1,
                "ram": 2048,
                "cores": 1,
                "storage_size": 20480,
                "storage_type": "SSD Premium",
                "connections": [
                    {
                        "datacenter_id": "03a8fdf1-fbc4-43f6-91ce-0506444e17dd",
                        "lan_id": "2",
                        "cidr": "<CIDR>"
                    }
                ],
                "maintenance_window": {
                    "time": "12:15:19",
                    "day_of_the_week": "Monday"
                },
                "synchronization_mode": "ASYNCHRONOUS"
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
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
