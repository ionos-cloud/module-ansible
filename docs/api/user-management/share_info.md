# share_info

This is a simple module that supports listing Shares.

## Example Syntax


```yaml

    - name: Get all Shares of a group
      share_info:
        group: "AnsibleIonosGroup"
      register: share_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "shares": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/0e191818-5dd6-4248-b226-a0c863c71d03/shares/82ad5ad2-7f10-4c2f-ad22-6ae36575f730",
            "id": "82ad5ad2-7f10-4c2f-ad22-6ae36575f730",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/0e191818-5dd6-4248-b226-a0c863c71d03/shares/b22cf038-aa2a-4806-a2c1-2a4e3507c37a",
            "id": "b22cf038-aa2a-4806-a2c1-2a4e3507c37a",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
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
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the group.</td>
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
