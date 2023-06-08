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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the resource. |
  | create_datacenter | False | bool |  | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot | False | bool |  | Create snapshot privilege. |
  | reserve_ip | False | bool |  | Reserve IP block privilege. |
  | access_activity_log | False | bool |  | Activity log access privilege. |
  | create_pcc | False | bool |  | Create pcc privilege. |
  | s3_privilege | False | bool |  | S3 privilege. |
  | create_backup_unit | False | bool |  | Create backup unit privilege. |
  | create_internet_access | False | bool |  | Create internet access privilege. |
  | create_k8s_cluster | False | bool |  | Create Kubernetes cluster privilege. |
  | create_flow_log | False | bool |  | Create Flow Logs privilege. |
  | access_and_manage_monitoring | False | bool |  | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates | False | bool |  | Privilege for a group to access and manage certificates. |
  | manage_dbaas | False | bool |  | Privilege for a group to manage DBaaS related functionality. |
  | users | False | list |  | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the resource. |
  | group | True | str |  | The ID or name of the group. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the resource. |
  | group | True | str |  | The ID or name of the group. |
  | create_datacenter | False | bool |  | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot | False | bool |  | Create snapshot privilege. |
  | reserve_ip | False | bool |  | Reserve IP block privilege. |
  | access_activity_log | False | bool |  | Activity log access privilege. |
  | create_pcc | False | bool |  | Create pcc privilege. |
  | s3_privilege | False | bool |  | S3 privilege. |
  | create_backup_unit | False | bool |  | Create backup unit privilege. |
  | create_internet_access | False | bool |  | Create internet access privilege. |
  | create_k8s_cluster | False | bool |  | Create Kubernetes cluster privilege. |
  | create_flow_log | False | bool |  | Create Flow Logs privilege. |
  | access_and_manage_monitoring | False | bool |  | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates | False | bool |  | Privilege for a group to access and manage certificates. |
  | manage_dbaas | False | bool |  | Privilege for a group to manage DBaaS related functionality. |
  | users | False | list |  | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
