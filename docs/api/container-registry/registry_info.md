# registry_info

This is a simple module that supports listing existing Registries

## Example Syntax


```yaml

    - name: List Registries
        registry_info:
        register: registries_response


    - name: Show Registries
        debug:
            var: registries_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "href": "",
            "id": "9bc72c7b-14d3-493e-a700-f9bc06b25614",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-29T13:51:25+00:00",
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "last_modified_date": null,
                "state": "WaitingForStorage"
            },
            "properties": {
                "garbage_collection_schedule": {
                    "days": [
                        "Wednesday"
                    ],
                    "time": "04:17:00+00:00"
                },
                "hostname": "",
                "location": "de/fra",
                "name": "ansibletest123",
                "storage_usage": {
                    "bytes": 0,
                    "updated_at": null
                }
            },
            "type": "registry"
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
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
