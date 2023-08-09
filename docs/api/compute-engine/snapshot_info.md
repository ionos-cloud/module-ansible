# snapshot_info

This is a simple module that supports listing Snapshots.

## Example Syntax


```yaml

    - name: Get all Snapshots
      snapshot_info:
      register: snapshot_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "snapshots": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/snapshots/1f18a6ff-6365-4704-88d8-75cd9387aab7",
            "id": "1f18a6ff-6365-4704-88d8-75cd9387aab7",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T11:49:41+00:00",
                "etag": "6d66d25257bbcc92d4f4980309d7a073",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T11:49:41+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": "Ansible test snapshot",
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "licence_type": "UNKNOWN",
                "location": "gb/lhr",
                "name": "AnsibleAutoTestCompute",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "sec_auth_protection": false,
                "size": 10.0
            },
            "type": "snapshot"
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
