# ipblock_info

This is a simple module that supports listing IP Blocks.

## Example Syntax


```yaml

    - name: Get all IP Blocks
      ipblock_info:
      register: ipblock_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "ipblocks": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/ipblocks/ac83f2d3-2751-4601-8687-6ea5d5c638a7",
            "id": "ac83f2d3-2751-4601-8687-6ea5d5c638a7",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T11:38:58+00:00",
                "etag": "e8267c0bfb11065927d961a4f1635a83",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T11:38:58+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "ip_consumers": [],
                "ips": [
                    "<IP1>",
                    "<IP2>"
                ],
                "location": "gb/lhr",
                "name": "AnsibleAutoTestCompute",
                "size": 2
            },
            "type": "ipblock"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/ipblocks/5122cd25-7e8d-4147-9818-4fd8ab07c88c",
            "id": "5122cd25-7e8d-4147-9818-4fd8ab07c88c",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-07-27T13:17:15+00:00",
                "etag": "d02824d7af8198abc00817248afb5e8f",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-07-27T13:17:15+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "ip_consumers": [],
                "ips": [
                    "<IP1>"
                ],
                "location": "us/las",
                "name": "IP_BLOCK_2023-07-27T13:17:15Z",
                "size": 1
            },
            "type": "ipblock"
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
