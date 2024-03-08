# certificate_info

This is a simple module that supports listing uploaded Certificates

## Example Syntax


```yaml
name: List Certificates
ionoscloudsdk.ionoscloud.certificate_info: null
register: certificates_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "58da84bd-5dea-4838-9c43-391b7c75124a",
            "type": "certificate",
            "href": "https://api.ionos.com/certificatemanager/certificates/58da84bd-5dea-4838-9c43-391b7c75124a",
            "metadata": {
                "etag": null,
                "created_date": "2023-05-29T13:48:11Z",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-05-29T13:48:11Z",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "state": "AVAILABLE"
            },
            "properties": {
                "name": "test_certificate",
                "certificate": "<CERTIFICATE>",
                "certificate_chain": null
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/certificate).

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
