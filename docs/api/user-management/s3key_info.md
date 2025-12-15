# s3key_info

This is a simple module that supports listing S3Keys.

## Example Syntax


```yaml

name: List s3keys
ionoscloudsdk.ionoscloud.s3key_info:
  user: ''
register: s3key_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "s3keys": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/s3keys/<ID>",
            "id": "<ID>",
            "metadata": {
                "created_date": "2023-08-03T14:09:10",
                "etag": "f245addf606d4e505be3ce87c622bf75"
            },
            "properties": {
                "active": true,
                "secret_key": "<SECRET_KEY>"
            },
            "type": "s3key"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/s3keys/<ID>",
            "id": "<ID>",
            "metadata": {
                "created_date": "2023-08-03T14:09:11",
                "etag": "0c24df8cd19a7e35da34e4f4370f305a"
            },
            "properties": {
                "active": true,
                "secret_key": "<SECRET_KEY>"
            },
            "type": "s3key"
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
  <td>user<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or email of the user</td>
  </tr>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
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
