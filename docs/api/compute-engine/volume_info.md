# volume_info

This is a simple module that supports listing volumes.

## Example Syntax


```yaml

    - name: Get all volumes for a given datacenter
      volume_info:
        datacenter: "AnsibleDatacenter"
      register: volume_list_response
      
    - name: Get all volumes for a given server
      volume_info:
        datacenter: "AnsibleDatacenter"
        server: "AnsibleServerName"
      register: volume_list_server_response

    - name: Show all volumes for the datacenter
      debug:
        var: volume_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "action": "info",
    "changed": false,
    "servers": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/volumes/0d3e108d-8f58-47c7-a3fb-705a2979083b",
            "id": "0d3e108d-8f58-47c7-a3fb-705a2979083b",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-06-06T11:37:52+00:00",
                "etag": "72761afffbe760fe1207ef4397b2df9f",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-06-06T11:37:52+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "backupunit_id": null,
                "boot_order": "NONE",
                "boot_server": null,
                "bus": null,
                "cpu_hot_plug": true,
                "device_number": null,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image": "01abcc20-a6b9-11ed-9e9f-e60bb43016ef",
                "image_alias": null,
                "image_password": null,
                "licence_type": "UNKNOWN",
                "name": "AnsibleAutoTestCompute 02",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "pci_slot": null,
                "ram_hot_plug": true,
                "size": 20.0,
                "ssh_keys": null,
                "type": "SSD Premium",
                "user_data": null
            },
            "type": "volume"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/volumes/81472d47-f6b1-4fe5-a345-d2e03db68fea",
            "id": "81472d47-f6b1-4fe5-a345-d2e03db68fea",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-06-06T11:35:19+00:00",
                "etag": "42ade3221dbec89ee4873048af14028b",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-06-06T11:35:19+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "backupunit_id": null,
                "boot_order": "NONE",
                "boot_server": null,
                "bus": null,
                "cpu_hot_plug": true,
                "device_number": null,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image": "01abcc20-a6b9-11ed-9e9f-e60bb43016ef",
                "image_alias": null,
                "image_password": null,
                "licence_type": "UNKNOWN",
                "name": "AnsibleAutoTestCompute 01",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "pci_slot": null,
                "ram_hot_plug": true,
                "size": 20.0,
                "ssh_keys": null,
                "type": "SSD Premium",
                "user_data": null
            },
            "type": "volume"
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
| datacenter | True | str |  | The ID or name of the datacenter. |
| server | False | str |  | The ID or name of the server. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
