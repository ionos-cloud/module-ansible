# registry_token_info

This is a simple module that supports listing existing Registry Tokens

## Example Syntax


```yaml

name: List Registry Tokens
ionoscloudsdk.ionoscloud.registry_token_info:
  registry: ''
register: registry_tokens_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "href": "",
            "id": "1e9f63b6-ff23-41ab-8f7e-57dd1008d6b5",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-29T13:51:29+00:00",
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "last_modified_date": null,
                "state": "enabled"
            },
            "properties": {
                "credentials": {
                    "password": "",
                    "username": "testRegistryToken"
                },
                "expiry_date": null,
                "name": "testRegistryToken",
                "scopes": [
                    {
                        "actions": [
                            "pull",
                            "push"
                        ],
                        "name": "nume",
                        "type": "repo"
                    }
                ],
                "status": "enabled"
            },
            "type": "token"
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/container-registry).

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
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
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
