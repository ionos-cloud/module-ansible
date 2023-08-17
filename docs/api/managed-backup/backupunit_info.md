# backupunit_info

This is a simple module that supports listing Backupunits.

## Example Syntax


```yaml

    - name: Get all Backupunits
      backupunit_info:
      register: backupunit_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "backupunits": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/backupunits/5553a540-3952-4b8b-a4c0-7e09d7108f8e",
            "id": "5553a540-3952-4b8b-a4c0-7e09d7108f8e",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-07-26T14:53:22+00:00",
                "etag": "83840eb6560db5cec2d10a5bedad7947",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-07-26T14:54:05+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "email": "<EMAIL>",
                "name": "test",
                "password": null
            },
            "type": "backupunit"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/backupunits/67f31927-0f2f-4be1-b1f0-833e29396c10",
            "id": "67f31927-0f2f-4be1-b1f0-833e29396c10",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2022-10-21T14:33:06+00:00",
                "etag": "7ebf13e8f909d267ed6ca752cbb28a5e",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-04T08:47:38+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "email": "<EMAIL>",
                "name": "My AnsibleAutoTestBackup",
                "password": null
            },
            "type": "backupunit"
        }
    ],
    "failed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
