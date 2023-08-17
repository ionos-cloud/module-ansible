# pcc_info

This is a simple module that supports listing PCCs.

## Example Syntax


```yaml

    - name: Get all PCCs
      pcc_info:
      register: pcc_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "pccs": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/pccs/d1052016-7097-40df-95d5-cda7671ae046",
            "id": "d1052016-7097-40df-95d5-cda7671ae046",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": null,
                "created_date": "2023-08-03T11:46:33+00:00",
                "etag": "6119e91e1ad7a920bcc5c021fee61683",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": null,
                "last_modified_date": "2023-08-03T11:46:33+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "connectable_datacenters": [
                    {
                        "id": "1a48f14a-9964-49f8-8b4a-254c59a6857c",
                        "location": "de/txl",
                        "name": "AnsibleAutoTestCompute"
                    },
                    {
                        "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26",
                        "location": "de/fra",
                        "name": "AnsibleVMAutoscaling"
                    },
                    {
                        "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513",
                        "location": "de/fra",
                        "name": "SDK AUTO-TEST"
                    }
                ],
                "description": "Ansible Compute test description",
                "name": "AnsibleAutoTestCompute",
                "peers": []
            },
            "type": "pcc"
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
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name'</td>
  </tr>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
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
