# dataplatform_cluster_info

This is a simple module that supports listing existing DataPlatform Clusters

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

name: Get all Data Platform clusters
ionoscloudsdk.ionoscloud.dataplatform_cluster_info: null
register: cluster_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "fe6a5792-7473-4067-ba83-6d135582e623",
            "type": "cluster",
            "href": "https://api.ionos.com/dataplatform/clusters/fe6a5792-7473-4067-ba83-6d135582e623",
            "metadata": {
                "e_tag": null,
                "created_date": "2023-05-29T13:55:51+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_in_contract_number": "31909592",
                "last_modified_date": "2023-05-29T13:55:51+00:00",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "current_data_platform_version": "22.11",
                "current_data_platform_revision": 1,
                "available_upgrade_versions": [],
                "state": "AVAILABLE"
            },
            "properties": {
                "name": "AnsibleAutoTestDataPlatform3",
                "data_platform_version": "22.11",
                "datacenter_id": "f68205d8-8334-43b0-9f64-b06babcf5bd6",
                "maintenance_window": {
                    "time": "12:02:00",
                    "day_of_the_week": "Wednesday"
                }
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dataplatform).

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
