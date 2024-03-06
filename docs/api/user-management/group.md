# group

This module allows you to create, update or remove a group.

## Example Syntax


```yaml
name: Create group
ionoscloudsdk.ionoscloud.group:
  name: 'AnsibleAutoTestUM'
  create_datacenter: true
  create_snapshot: true
  reserve_ip: true
  access_activity_log: true
  create_pcc: true
  s3_privilege: true
  create_backup_unit: true
  create_internet_access: true
  create_k8s_cluster: true
  create_flow_log: true
  access_and_manage_monitoring: true
  access_and_manage_certificates: true
  manage_dbaas: true
register: group_response

name: Add user1 to group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  users:
  - ''
  state: update

name: Delete group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
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
    "group": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/um/groups/247c2dbf-e0d4-484f-934b-03d4bc09b772",
        "id": "247c2dbf-e0d4-484f-934b-03d4bc09b772",
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
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  name: Create group
ionoscloudsdk.ionoscloud.group:
  name: 'AnsibleAutoTestUM'
  create_datacenter: true
  create_snapshot: true
  reserve_ip: true
  access_activity_log: true
  create_pcc: true
  s3_privilege: true
  create_backup_unit: true
  create_internet_access: true
  create_k8s_cluster: true
  create_flow_log: true
  access_and_manage_monitoring: true
  access_and_manage_certificates: true
  manage_dbaas: true
register: group_response

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the resource.</td>
  </tr>
  <tr>
  <td>create_datacenter<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean value indicating if the group is allowed to create virtual data centers.</td>
  </tr>
  <tr>
  <td>create_snapshot<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create snapshot privilege.</td>
  </tr>
  <tr>
  <td>reserve_ip<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Reserve IP block privilege.</td>
  </tr>
  <tr>
  <td>access_activity_log<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activity log access privilege.</td>
  </tr>
  <tr>
  <td>create_pcc<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>User privilege to create a cross connect.</td>
  </tr>
  <tr>
  <td>s3_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>S3 privilege.</td>
  </tr>
  <tr>
  <td>create_backup_unit<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create backup unit privilege.</td>
  </tr>
  <tr>
  <td>create_internet_access<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create internet access privilege.</td>
  </tr>
  <tr>
  <td>create_k8s_cluster<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create Kubernetes cluster privilege.</td>
  </tr>
  <tr>
  <td>create_flow_log<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create Flow Logs privilege.</td>
  </tr>
  <tr>
  <td>access_and_manage_monitoring<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS).</td>
  </tr>
  <tr>
  <td>access_and_manage_certificates<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to access and manage certificates.</td>
  </tr>
  <tr>
  <td>manage_dbaas<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to manage DBaaS related functionality.</td>
  </tr>
  <tr>
  <td>users<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  name: Delete group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the resource.</td>
  </tr>
  <tr>
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the group.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  name: Add user1 to group
ionoscloudsdk.ionoscloud.group:
  group: 'AnsibleAutoTestUM'
  users:
  - ''
  state: update

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the resource.</td>
  </tr>
  <tr>
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the group.</td>
  </tr>
  <tr>
  <td>create_datacenter<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean value indicating if the group is allowed to create virtual data centers.</td>
  </tr>
  <tr>
  <td>create_snapshot<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create snapshot privilege.</td>
  </tr>
  <tr>
  <td>reserve_ip<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Reserve IP block privilege.</td>
  </tr>
  <tr>
  <td>access_activity_log<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activity log access privilege.</td>
  </tr>
  <tr>
  <td>create_pcc<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>User privilege to create a cross connect.</td>
  </tr>
  <tr>
  <td>s3_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>S3 privilege.</td>
  </tr>
  <tr>
  <td>create_backup_unit<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create backup unit privilege.</td>
  </tr>
  <tr>
  <td>create_internet_access<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create internet access privilege.</td>
  </tr>
  <tr>
  <td>create_k8s_cluster<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create Kubernetes cluster privilege.</td>
  </tr>
  <tr>
  <td>create_flow_log<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Create Flow Logs privilege.</td>
  </tr>
  <tr>
  <td>access_and_manage_monitoring<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS).</td>
  </tr>
  <tr>
  <td>access_and_manage_certificates<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to access and manage certificates.</td>
  </tr>
  <tr>
  <td>manage_dbaas<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Privilege for a group to manage DBaaS related functionality.</td>
  </tr>
  <tr>
  <td>users<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
