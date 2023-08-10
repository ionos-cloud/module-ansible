# dataplatform_cluster

This is a simple module that supports creating or removing Data Platform Clusters. This module has a dependency on ionoscloud &gt;= 6.0.2

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

  - name: Create Data Platform cluster
    dataplatform_cluster:
      name: ClusterName
  

  - name: Update Data Platform cluster
    dataplatform_cluster:
      cluster: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      dataplatform_version: 1.17.8
      state: update
  

  - name: Delete Data Platform cluster
    dataplatform_cluster:
      cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "dataplatform_cluster": {
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
            "state": "DEPLOYING"
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
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Data Platform cluster
    dataplatform_cluster:
      name: ClusterName
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:#003d8f">str</span> | True | The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | dataplatform_version<br /><span style="color:#003d8f">str</span> | False | The version of the data platform. |
  | datacenter<br /><span style="color:#003d8f">str</span> | True | The UUID of the virtual data center (VDC) the cluster is provisioned. |
  | maintenance_window<br /><span style="color:#003d8f">dict</span> | False | Starting time of a weekly 4 hour-long window, during which maintenance might occur in hh:mm:ss format |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Data Platform cluster
    dataplatform_cluster:
      cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | cluster<br /><span style="color:#003d8f">str</span> | True | The ID or name of the Data Platform cluster. |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Data Platform cluster
    dataplatform_cluster:
      cluster: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      dataplatform_version: 1.17.8
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:#003d8f">str</span> | False | The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | cluster<br /><span style="color:#003d8f">str</span> | True | The ID or name of the Data Platform cluster. |
  | dataplatform_version<br /><span style="color:#003d8f">str</span> | True | The version of the data platform. |
  | datacenter<br /><span style="color:#003d8f">str</span> | False | The UUID of the virtual data center (VDC) the cluster is provisioned. |
  | maintenance_window<br /><span style="color:#003d8f">dict</span> | True | Starting time of a weekly 4 hour-long window, during which maintenance might occur in hh:mm:ss format |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
