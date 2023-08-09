# lan_info

This is a simple module that supports listing LANs.

## Example Syntax


```yaml

    - name: Get all LANs for a given datacenter
      lan_info:
        datacenter: "AnsibleDatacenter"
      register: lan_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "lans": [
        {
            "entities": {
                "nics": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/lans/1/nics",
                    "id": "1/nics",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/lans/1",
            "id": "1",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T10:38:01+00:00",
                "etag": "933196ec0a8386cc137cd4b5ec1165d1",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T10:38:01+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "ip_failover": [],
                "name": "AnsibleAutoTestCompute",
                "pcc": null,
                "public": true
            },
            "type": "lan"
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
| datacenter | True | str |  | The datacenter name or UUID in which to operate. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
