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

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "type": "user",
            "metadata": {
                "created_date": "2023-05-30T14:20:09+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>"
            },
            "properties": {
                "username": "testuser",
                "password": null,
                "roles": [
                    {
                        "role": "read",
                        "database": "test"
                    }
                ]
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
| mongo_cluster | True | str |  | The UUID or name of an existing Mongo Cluster. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
