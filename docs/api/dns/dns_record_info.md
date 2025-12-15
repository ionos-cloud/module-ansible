# dns_record_info

This is a simple module that supports listing DNS Records.

## Example Syntax


```yaml

name: List all Records in zone
ionoscloudsdk.ionoscloud.dns_record_info:
  zone: 'test.example.test.ansible.com'
register: records_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "records": [
        {
            "id": "c76bf816-c11a-5dfc-8ef3-badfbee48451",
            "type": "record",
            "href": "/zones/b4021310-5e39-50bb-95f6-448b21bf0142/records/c76bf816-c11a-5dfc-8ef3-badfbee48451",
            "metadata": {
                "last_modified_date": "2023-10-05T14:38:56+00:00",
                "created_date": "2023-10-05T14:38:56+00:00",
                "state": "AVAILABLE",
                "fqdn": "<FQDN>",
                "zone_id": "b4021310-5e39-50bb-95f6-448b21bf0142"
            },
            "properties": {
                "name": "<RECORD_NAME>",
                "type": "CNAME",
                "content": "<CONTENT>",
                "ttl": 3600,
                "priority": 0,
                "enabled": true
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
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing Zone. Will be prioritized if both this and secondary_zone are set.</td>
  </tr>
  <tr>
  <td>secondary_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing Secondary Zone.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of properties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
