# group_info

This is a simple module that supports listing group.

## Example Syntax


```yaml

name: List Groups
ionoscloudsdk.ionoscloud.group_info: null
register: group_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "groups": [
        {
            "entities": {
                "resources": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/groups/df2b761d-c55e-4db4-ac66-667bd5b0d41e/resources",
                    "id": "df2b761d-c55e-4db4-ac66-667bd5b0d41e/resources",
                    "items": null,
                    "type": "collection"
                },
                "users": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/groups/df2b761d-c55e-4db4-ac66-667bd5b0d41e/users",
                    "id": "df2b761d-c55e-4db4-ac66-667bd5b0d41e/users",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/df2b761d-c55e-4db4-ac66-667bd5b0d41e",
            "id": "df2b761d-c55e-4db4-ac66-667bd5b0d41e",
            "properties": {
                "access_activity_log": true,
                "access_and_manage_certificates": true,
                "access_and_manage_dns": false,
                "access_and_manage_monitoring": true,
                "create_backup_unit": true,
                "create_data_center": true,
                "create_flow_log": true,
                "create_internet_access": true,
                "create_k8s_cluster": true,
                "create_pcc": true,
                "create_snapshot": true,
                "manage_dbaas": true,
                "manage_dataplatform": false,
                "manage_registry": false,
                "name": "AnsibleAutoTestUM",
                "reserve_ip": true,
                "s3_privilege": true
            },
            "type": "group"
        },
        {
            "entities": {
                "resources": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/groups/cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce/resources",
                    "id": "cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce/resources",
                    "items": null,
                    "type": "collection"
                },
                "users": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/groups/cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce/users",
                    "id": "cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce/users",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce",
            "id": "cc72a0b7-bb6e-433c-8bc8-e06a4aa9adce",
            "properties": {
                "access_activity_log": true,
                "access_and_manage_certificates": false,
                "access_and_manage_dns": false,
                "access_and_manage_monitoring": false,
                "create_backup_unit": true,
                "create_data_center": true,
                "create_flow_log": false,
                "create_internet_access": true,
                "create_k8s_cluster": true,
                "create_pcc": true,
                "create_snapshot": true,
                "manage_dbaas": false,
                "manage_dataplatform": false,
                "manage_registry": false,
                "name": "AnsibleAutoTestUM2",
                "reserve_ip": true,
                "s3_privilege": true
            },
            "type": "group"
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
  <td align="center">False</td>
  <td>The ID or name of the user.</td>
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
