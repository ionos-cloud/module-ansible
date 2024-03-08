# user_info

This is a simple module that supports listing Users.

## Example Syntax


```yaml
name: List Users
ionoscloudsdk.ionoscloud.user_info: null
register: user_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "users": [
        {
            "entities": {
                "groups": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/groups",
                    "id": "<USER_ID>/groups",
                    "items": null,
                    "type": "collection"
                },
                "owns": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/owns",
                    "id": "<USER_ID>/owns",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
            "id": "<USER_ID>",
            "metadata": {
                "created_date": "2023-02-09T16:26:34+00:00",
                "etag": "37a6259cc0c1dae299a7866489dff0bd",
                "last_login": null
            },
            "properties": {
                "active": true,
                "administrator": false,
                "email": "<EMAIL>",
                "firstname": "John",
                "force_sec_auth": false,
                "lastname": "Doe",
                "s3_canonical_user_id": "<s3_canonical_user_id>",
                "sec_auth_active": false
            },
            "type": "user"
        },
        {
            "entities": {
                "groups": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/groups",
                    "id": "<USER_ID>/groups",
                    "items": null,
                    "type": "collection"
                },
                "owns": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/owns",
                    "id": "<USER_ID>/owns",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
            "id": "<USER_ID>",
            "metadata": {
                "created_date": "2023-08-03T14:07:59+00:00",
                "etag": "37a6259cc0c1dae299a7866489dff0bd",
                "last_login": null
            },
            "properties": {
                "active": true,
                "administrator": false,
                "email": "<EMAIL>",
                "firstname": "John1",
                "force_sec_auth": false,
                "lastname": "Doe",
                "s3_canonical_user_id": "<s3_canonical_user_id>",
                "sec_auth_active": false
            },
            "type": "user"
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/user-management).

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
  <td align="center">False</td>
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
