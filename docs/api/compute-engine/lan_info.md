# lan_info

This is a simple module that supports listing LANs.

## Example Syntax


```yaml
name: List LANs
ionoscloudsdk.ionoscloud.lan_info:
  datacenter: 'AnsibleAutoTestCompute'
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
  <td>The datacenter name or UUID in which to operate.</td>
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
