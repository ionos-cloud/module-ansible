# group

This module allows you to create, update or remove a group.

## Example Syntax


```yaml
# Create a group
  - name: Create group
    group:
      name: guests
      create_datacenter: true
      create_snapshot: true
      reserve_ip: false
      access_activity_log: false
      state: present
  
# Update a group
  - name: Update group
    group:
      group: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  
# Remove a group
  - name: Remove group
    group:
      group: guests
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
  # Create a group
  - name: Create group
    group:
      name: guests
      create_datacenter: true
      create_snapshot: true
      reserve_ip: false
      access_activity_log: false
      state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | True | The name of the resource. |
  | create_datacenter<br /><span style="color:blue">\<bool\></span> | False | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot<br /><span style="color:blue">\<bool\></span> | False | Create snapshot privilege. |
  | reserve_ip<br /><span style="color:blue">\<bool\></span> | False | Reserve IP block privilege. |
  | access_activity_log<br /><span style="color:blue">\<bool\></span> | False | Activity log access privilege. |
  | create_pcc<br /><span style="color:blue">\<bool\></span> | False | Create pcc privilege. |
  | s3_privilege<br /><span style="color:blue">\<bool\></span> | False | S3 privilege. |
  | create_backup_unit<br /><span style="color:blue">\<bool\></span> | False | Create backup unit privilege. |
  | create_internet_access<br /><span style="color:blue">\<bool\></span> | False | Create internet access privilege. |
  | create_k8s_cluster<br /><span style="color:blue">\<bool\></span> | False | Create Kubernetes cluster privilege. |
  | create_flow_log<br /><span style="color:blue">\<bool\></span> | False | Create Flow Logs privilege. |
  | access_and_manage_monitoring<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to access and manage certificates. |
  | manage_dbaas<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to manage DBaaS related functionality. |
  | users<br /><span style="color:blue">\<list\></span> | False | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove a group
  - name: Remove group
    group:
      group: guests
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the resource. |
  | group<br /><span style="color:blue">\<str\></span> | True | The ID or name of the group. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  # Update a group
  - name: Update group
    group:
      group: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the resource. |
  | group<br /><span style="color:blue">\<str\></span> | True | The ID or name of the group. |
  | create_datacenter<br /><span style="color:blue">\<bool\></span> | False | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot<br /><span style="color:blue">\<bool\></span> | False | Create snapshot privilege. |
  | reserve_ip<br /><span style="color:blue">\<bool\></span> | False | Reserve IP block privilege. |
  | access_activity_log<br /><span style="color:blue">\<bool\></span> | False | Activity log access privilege. |
  | create_pcc<br /><span style="color:blue">\<bool\></span> | False | Create pcc privilege. |
  | s3_privilege<br /><span style="color:blue">\<bool\></span> | False | S3 privilege. |
  | create_backup_unit<br /><span style="color:blue">\<bool\></span> | False | Create backup unit privilege. |
  | create_internet_access<br /><span style="color:blue">\<bool\></span> | False | Create internet access privilege. |
  | create_k8s_cluster<br /><span style="color:blue">\<bool\></span> | False | Create Kubernetes cluster privilege. |
  | create_flow_log<br /><span style="color:blue">\<bool\></span> | False | Create Flow Logs privilege. |
  | access_and_manage_monitoring<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to access and manage certificates. |
  | manage_dbaas<br /><span style="color:blue">\<bool\></span> | False | Privilege for a group to manage DBaaS related functionality. |
  | users<br /><span style="color:blue">\<list\></span> | False | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
