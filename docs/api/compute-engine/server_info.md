# server_info

This is a simple module that supports listing servers.

## Example Syntax


```yaml
name: List Servers
ionoscloudsdk.ionoscloud.server_info:
  datacenter: 'AnsibleAutoTestCompute'
register: server_list_response

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
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).

&nbsp;
### Available parameters:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>upgrade_needed<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Filter servers that can or that cannot be upgraded.</td>
  </tr>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  </tbody>
</table>
