# cube_template_info

This is a simple module that supports retrieving one or more Cube templates

## Example Syntax


```yaml


name: List templates
ionoscloudsdk.ionoscloud.cube_template_info: null
register: template_list

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "cube_templates": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/15c6dd2f-02d2-4987-b439-9a58dd59ecc3",
            "id": "15c6dd2f-02d2-4987-b439-9a58dd59ecc3",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:02:13+00:00",
                "etag": "4ff2f8ebb363005b447edb38563405a6",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:11:03+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 1.0,
                "name": "CUBES XS",
                "ram": 1024.0,
                "storage_size": 30.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/56ce4e71-b03a-42b2-85be-9a4520aa40be",
            "id": "56ce4e71-b03a-42b2-85be-9a4520aa40be",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:08:50+00:00",
                "etag": "f528ce3bcba9ff1332d7c181f221984c",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:11:57+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 8.0,
                "name": "CUBES XXL",
                "ram": 32768.0,
                "storage_size": 640.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/5ae1bfbd-05f2-47f5-a736-eaca3dcce41b",
            "id": "5ae1bfbd-05f2-47f5-a736-eaca3dcce41b",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:03:51+00:00",
                "etag": "6e68d67158a63d6d644a7c680342b26f",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:10:49+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 1.0,
                "name": "CUBES S",
                "ram": 2048.0,
                "storage_size": 50.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/5e98b425-1887-44e4-b782-a654bfbe7eaa",
            "id": "5e98b425-1887-44e4-b782-a654bfbe7eaa",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:07:39+00:00",
                "etag": "106988fd270d48ffd1734a210801a33d",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:11:45+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 6.0,
                "name": "CUBES XL",
                "ram": 16384.0,
                "storage_size": 320.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/5f56da3e-3549-4639-a19e-e8fc94323556",
            "id": "5f56da3e-3549-4639-a19e-e8fc94323556",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-09-29T17:24:05+00:00",
                "etag": "55ad04163ee8415a0cee1a88ea5e2bfd",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-10-28T11:14:16+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 16.0,
                "name": "CUBES 4XL",
                "ram": 65536.0,
                "storage_size": 1280.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/7f8dfdb3-594b-4ae2-ae2e-a9dfcbf05f74",
            "id": "7f8dfdb3-594b-4ae2-ae2e-a9dfcbf05f74",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:05:17+00:00",
                "etag": "fbb4194b718ce3e456437dbc55405273",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:11:22+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 2.0,
                "name": "CUBES M",
                "ram": 4096.0,
                "storage_size": 80.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/99d022bd-55ea-4af1-9ba7-6d4174d9fc22",
            "id": "99d022bd-55ea-4af1-9ba7-6d4174d9fc22",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-02-13T17:06:25+00:00",
                "etag": "2fd7e4e39bbbb7b33920bf4d7b5509a6",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-08-10T10:11:35+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 4.0,
                "name": "CUBES L",
                "ram": 8192.0,
                "storage_size": 160.0
            },
            "type": "template"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/templates/ebf7a788-28ed-4693-ae6d-411c288176db",
            "id": "ebf7a788-28ed-4693-ae6d-411c288176db",
            "metadata": {
                "created_by": "[UNKNOWN]",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-09-29T17:22:14+00:00",
                "etag": "6cc1968f4e67e25f184568d4fa51b718",
                "last_modified_by": "[UNKNOWN]",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-10-28T11:14:22+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cores": 12.0,
                "name": "CUBES 3XL",
                "ram": 49152.0,
                "storage_size": 960.0
            },
            "type": "template"
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
  <td>template_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID of the template.</td>
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
