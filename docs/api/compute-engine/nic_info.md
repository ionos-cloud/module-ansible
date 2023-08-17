# nic_info

This is a simple module that supports listing NICs.

## Example Syntax


```yaml

    - name: Get all NICs of a server
      nic_info:
        datacenter: "AnsibleDatacenter"
        server: "AnsibleServer"
      register: nic_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "nics": [
        {
            "entities": {
                "firewallrules": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/servers/73362db5-03c9-4445-907c-d539e7a0a160/nics/6e9d998f-9748-421d-8ad6-6e8bae893361/firewallrules",
                    "id": "6e9d998f-9748-421d-8ad6-6e8bae893361/firewallrules",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "flowlogs": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/servers/73362db5-03c9-4445-907c-d539e7a0a160/nics/6e9d998f-9748-421d-8ad6-6e8bae893361/flowlogs",
                    "id": "6e9d998f-9748-421d-8ad6-6e8bae893361/flowlogs",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/servers/73362db5-03c9-4445-907c-d539e7a0a160/nics/6e9d998f-9748-421d-8ad6-6e8bae893361",
            "id": "6e9d998f-9748-421d-8ad6-6e8bae893361",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T11:35:50+00:00",
                "etag": "7457e8713b1d864cbe352efbef5560fd",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T11:35:50+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "device_number": null,
                "dhcp": true,
                "firewall_active": true,
                "firewall_type": "INGRESS",
                "ips": [
                    "<IP>"
                ],
                "lan": 1,
                "mac": "<MAC>",
                "name": "AnsibleAutoTestCompute",
                "pci_slot": 6
            },
            "type": "nic"
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
| server | True | str |  | The ID or name of the Server. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
