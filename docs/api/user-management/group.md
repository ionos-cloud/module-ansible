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
      name: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  
# Remove a group
  - name: Remove group
    group:
      name: guests
      state: absent
  
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
  | name | True | str |  | The name of the group. |
  | create_datacenter | False | bool |  | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot | False | bool |  | Boolean value indicating if the group is allowed to create snapshots. |
  | reserve_ip | False | bool |  | Boolean value indicating if the group is allowed to reserve IP addresses. |
  | access_activity_log | False | bool |  | Boolean value indicating if the group is allowed to access the activity log. |
  | create_pcc | False | bool |  | Boolean value indicating if the group is allowed to create PCCs. |
  | s3_privilege | False | bool |  | Boolean value indicating if the group has S3 privilege. |
  | create_backup_unit | False | bool |  | Boolean value indicating if the group is allowed to create backup units. |
  | create_internet_access | False | bool |  | Boolean value indicating if the group is allowed to create internet access. |
  | create_k8s_cluster | False | bool |  | Boolean value indicating if the group is allowed to create k8s clusters. |
  | create_flow_log | False | bool |  | Boolean value indicating if the group is allowed to create flowlogs. |
  | access_and_manage_monitoring | False | bool |  | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates | False | bool |  | Privilege for a group to access and manage certificates. |
  | manage_dbaas | False | bool |  | Privilege for a group to manage DBaaS related functionality. |
  | users | False | list |  | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | api_url | False | str |  | The Ionos API base URL. |
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
      name: guests
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the group. |
  | api_url | False | str |  | The Ionos API base URL. |
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
      name: guests
      create_datacenter: false
      users:
        - john.smith@test.com
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the group. |
  | create_datacenter | False | bool |  | Boolean value indicating if the group is allowed to create virtual data centers. |
  | create_snapshot | False | bool |  | Boolean value indicating if the group is allowed to create snapshots. |
  | reserve_ip | False | bool |  | Boolean value indicating if the group is allowed to reserve IP addresses. |
  | access_activity_log | False | bool |  | Boolean value indicating if the group is allowed to access the activity log. |
  | create_pcc | False | bool |  | Boolean value indicating if the group is allowed to create PCCs. |
  | s3_privilege | False | bool |  | Boolean value indicating if the group has S3 privilege. |
  | create_backup_unit | False | bool |  | Boolean value indicating if the group is allowed to create backup units. |
  | create_internet_access | False | bool |  | Boolean value indicating if the group is allowed to create internet access. |
  | create_k8s_cluster | False | bool |  | Boolean value indicating if the group is allowed to create k8s clusters. |
  | create_flow_log | False | bool |  | Boolean value indicating if the group is allowed to create flowlogs. |
  | access_and_manage_monitoring | False | bool |  | Privilege for a group to access and manage monitoring related functionality (access metrics, CRUD on alarms, alarm-actions etc) using Monotoring-as-a-Service (MaaS). |
  | access_and_manage_certificates | False | bool |  | Privilege for a group to access and manage certificates. |
  | manage_dbaas | False | bool |  | Privilege for a group to manage DBaaS related functionality. |
  | users | False | list |  | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list ([]) to remove all users from the group. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
