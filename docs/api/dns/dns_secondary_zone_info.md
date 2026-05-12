# dns_secondary_zone_info

This is a simple module that supports listing DNS Secondary Zones.

## Example Syntax


```yaml

name: List Zones
ionoscloudsdk.ionoscloud.dns_secondary_zone_info: null
register: zones_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "zones": [
        {
            "id": "23da7378-a656-5d3a-9807-d283500753b6",
            "type": "secondaryzone",
            "href": "/secondaryzones/23da7378-a656-5d3a-9807-d283500753b6",
            "metadata": {
                "last_modified_date": "2023-10-24T13:12:37+00:00",
                "created_date": "2023-10-24T13:12:07+00:00",
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
                "primary_ips": [
                    "<IP1>",
                    "<IP2>"
                ]
            }
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dns).

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
