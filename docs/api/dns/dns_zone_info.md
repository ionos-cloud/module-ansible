# dns_zone_info

This is a simple module that supports listing DNS Zones.

## Example Syntax


```yaml

    - name: Get all DNS Zones
      dns_zone_info:
      register: dns_zone_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "zones": [
        {
            "id": "36d63502-7110-57f3-8794-a24fe8959d18",
            "type": "zone",
            "href": "/zones/36d63502-7110-57f3-8794-a24fe8959d18",
            "metadata": {
                "last_modified_date": "2023-10-05T14:38:51+00:00",
                "created_date": "2023-10-05T14:38:51+00:00",
                "state": "AVAILABLE",
                "nameservers": [
                    "<NAMESERVER1>",
                    "<NAMESERVER2>",
                    "<NAMESERVER3>",
                    "<NAMESERVER4>"
                ]
            },
            "properties": {
                "zone_name": "<ZONE_NAME>",
                "description": "test_description",
                "enabled": true
            }
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
