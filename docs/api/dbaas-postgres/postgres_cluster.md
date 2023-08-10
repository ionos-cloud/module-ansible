# postgres_cluster

This is a module that supports creating, updating, restoring or destroying Postgres Clusters

## Example Syntax


```yaml
- name: Create Postgres Cluster
    postgres_cluster:
      postgres_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      storage_type: HDD
      location: de/fra
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
- name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: backuptest-04
      postgres_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  
- name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: backuptest-04
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
    "postgres_cluster": {
        "type": "cluster",
        "id": "46c151c7-55f8-42a4-86c3-06ad6b4b91ea",
        "metadata": {
            "created_date": "2023-05-30T14:35:40+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": null,
            "last_modified_by": null,
            "last_modified_by_user_id": null,
            "state": "BUSY"
        },
        "properties": {
            "display_name": "backuptest-04",
            "postgres_version": "12",
            "location": "de/fra",
            "backup_location": "eu-central-2",
            "instances": 1,
            "ram": 2048,
            "cores": 1,
            "storage_size": 20480,
            "storage_type": "SSD Premium",
            "connections": [
                {
                    "datacenter_id": "03a8fdf1-fbc4-43f6-91ce-0506444e17dd",
                    "lan_id": "2",
                    "cidr": "<CIDR>"
                }
            ],
            "maintenance_window": {
                "time": "12:15:19",
                "day_of_the_week": "Monday"
            },
            "synchronization_mode": "ASYNCHRONOUS"
        }
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Postgres Cluster
    postgres_cluster:
      postgres_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      storage_type: HDD
      location: de/fra
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | maintenance_window<br /><span style="color:blue">\<dict\></span> | False | A weekly 4 hour-long window, during which maintenance might occur. |
  | postgres_version<br /><span style="color:blue">\<str\></span> | True | The PostgreSQL version of your cluster. |
  | instances<br /><span style="color:blue">\<int\></span> | True | The total number of instances in the cluster (one master and n-1 standbys). |
  | cores<br /><span style="color:blue">\<int\></span> | True | The number of CPU cores per instance. |
  | ram<br /><span style="color:blue">\<int\></span> | True | The amount of memory per instance in megabytes. Has to be a multiple of 1024. |
  | storage_size<br /><span style="color:blue">\<int\></span> | True | The amount of storage per instance in megabytes. |
  | storage_type<br /><span style="color:blue">\<str\></span> | True | The storage type used in your cluster. (Value &quot;SSD&quot; is deprecated. Use the equivalent &quot;SSD Premium&quot; instead)<br />Options: ['HDD', 'SSD', 'SSD Standard', 'SSD Premium'] |
  | connections<br /><span style="color:blue">\<list\></span> | True | Array of VDCs to connect to your cluster. |
  | location<br /><span style="color:blue">\<str\></span> | True | The physical location where the cluster will be created. This will be where all of your instances live. Property cannot be modified after datacenter creation. |
  | display_name<br /><span style="color:blue">\<str\></span> | True | The friendly name of your cluster. |
  | db_username<br /><span style="color:blue">\<str\></span> | True | The username for the initial PostgreSQL user. Some system usernames are restricted (e.g. &quot;postgres&quot;, &quot;admin&quot;, &quot;standby&quot;). |
  | db_password<br /><span style="color:blue">\<str\></span> | True | The password for the initial postgres user. |
  | synchronization_mode<br /><span style="color:blue">\<str\></span> | True | Represents different modes of replication. |
  | backup_location<br /><span style="color:blue">\<str\></span> | False | The S3 location where the backups will be stored. |
  | backup_id<br /><span style="color:blue">\<str\></span> | False | The ID of the backup to be used. |
  | recovery_target_time<br /><span style="color:blue">\<str\></span> | False | Recovery target time. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: backuptest-04
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | postgres_cluster<br /><span style="color:blue">\<str\></span> | True | The ID or name of an existing Postgres Cluster. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: backuptest-04
      postgres_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | maintenance_window<br /><span style="color:blue">\<dict\></span> | False | A weekly 4 hour-long window, during which maintenance might occur. |
  | postgres_version<br /><span style="color:blue">\<str\></span> | False | The PostgreSQL version of your cluster. |
  | instances<br /><span style="color:blue">\<int\></span> | False | The total number of instances in the cluster (one master and n-1 standbys). |
  | cores<br /><span style="color:blue">\<int\></span> | False | The number of CPU cores per instance. |
  | ram<br /><span style="color:blue">\<int\></span> | False | The amount of memory per instance in megabytes. Has to be a multiple of 1024. |
  | storage_size<br /><span style="color:blue">\<int\></span> | False | The amount of storage per instance in megabytes. |
  | display_name<br /><span style="color:blue">\<str\></span> | False | The friendly name of your cluster. |
  | postgres_cluster<br /><span style="color:blue">\<str\></span> | True | The ID or name of an existing Postgres Cluster. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore'] |

&nbsp;

&nbsp;
# state: **restore**
```yaml
  
```
### Available parameters for state **restore**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | backup_id<br /><span style="color:blue">\<str\></span> | True | The ID of the backup to be used. |
  | recovery_target_time<br /><span style="color:blue">\<str\></span> | False | Recovery target time. |
  | postgres_cluster<br /><span style="color:blue">\<str\></span> | True | The ID or name of an existing Postgres Cluster. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore'] |

&nbsp;

&nbsp;
