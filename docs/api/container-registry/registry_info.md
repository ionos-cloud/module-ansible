# registry_info

This is a simple module that supports listing existing Registries

## Example Syntax


```yaml
name: List Registries
ionoscloudsdk.ionoscloud.registry_info: null
register: registries_response

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
