# server_info

This is a simple module that supports listing servers.

## Example Syntax


```yaml

    - name: Get all servers for a given datacenter
      server_info:
        datacenter: AnsibleDatacenter
      register: server_list_response

    - name: Get only the servers that need to be upgraded
      server_info:
        datacenter: AnsibleDatacenter
        upgrade_needed: true
      register: servers_list_upgrade_response

    - name: Show all servers for the created datacenter
      debug:
        var: server_list_response

    - name: Show servers that need an upgrade
      debug:
        var: servers_list_upgrade_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "servers": [
        {
            "entities": {
                "cdroms": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/364213b3-3aca-43e3-8028-9a92c875e8e2/cdroms",
                    "id": "364213b3-3aca-43e3-8028-9a92c875e8e2/cdroms",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "nics": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/364213b3-3aca-43e3-8028-9a92c875e8e2/nics",
                    "id": "364213b3-3aca-43e3-8028-9a92c875e8e2/nics",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/364213b3-3aca-43e3-8028-9a92c875e8e2/volumes",
                    "id": "364213b3-3aca-43e3-8028-9a92c875e8e2/volumes",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/364213b3-3aca-43e3-8028-9a92c875e8e2",
            "id": "364213b3-3aca-43e3-8028-9a92c875e8e2",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T12:20:08+00:00",
                "etag": "aecac065f240d80cf71bd3a58e26363a",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T12:20:08+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "ZONE_1",
                "boot_cdrom": null,
                "boot_volume": {
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/volumes/54a002f5-f6f9-4a03-afdb-5bfb3a956dce",
                    "id": "54a002f5-f6f9-4a03-afdb-5bfb3a956dce",
                    "type": "volume"
                },
                "cores": 1,
                "cpu_family": "INTEL_SKYLAKE",
                "name": "AnsibleAutoTestCompute 02",
                "ram": 1024,
                "template_uuid": null,
                "type": "ENTERPRISE",
                "vm_state": "RUNNING"
            },
            "type": "server"
        },
        {
            "entities": {
                "cdroms": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/5d62b51a-3160-478b-a7e6-0986fb9c6381/cdroms",
                    "id": "5d62b51a-3160-478b-a7e6-0986fb9c6381/cdroms",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "nics": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/5d62b51a-3160-478b-a7e6-0986fb9c6381/nics",
                    "id": "5d62b51a-3160-478b-a7e6-0986fb9c6381/nics",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/5d62b51a-3160-478b-a7e6-0986fb9c6381/volumes",
                    "id": "5d62b51a-3160-478b-a7e6-0986fb9c6381/volumes",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/servers/5d62b51a-3160-478b-a7e6-0986fb9c6381",
            "id": "5d62b51a-3160-478b-a7e6-0986fb9c6381",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T12:18:20+00:00",
                "etag": "44fa3f5099b8c38abfbc4cc8534be243",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T12:18:20+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "ZONE_1",
                "boot_cdrom": null,
                "boot_volume": {
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/44d57e0c-40c9-475f-9c23-53c369a1593e/volumes/f29e9f2b-d2ba-47a0-9c0c-8263ff51c160",
                    "id": "f29e9f2b-d2ba-47a0-9c0c-8263ff51c160",
                    "type": "volume"
                },
                "cores": 1,
                "cpu_family": "INTEL_SKYLAKE",
                "name": "AnsibleAutoTestCompute 01",
                "ram": 1024,
                "template_uuid": null,
                "type": "ENTERPRISE",
                "vm_state": "RUNNING"
            },
            "type": "server"
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
| upgrade_needed | False | bool |  | Filter servers that can or that cannot be upgraded. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
