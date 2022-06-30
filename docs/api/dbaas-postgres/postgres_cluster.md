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
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
- name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
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
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
  
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
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | maintenance_window | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the maintenance) and &quot;day_of_the_week&quot; (the Day Of the week when to perform the maintenance). |
  | postgres_version | True | str |  | The PostgreSQL version of your cluster |
  | instances | True | int |  | The total number of instances in the cluster (one master and n-1 standbys). |
  | cores | True | int |  | The number of CPU cores per instance. |
  | ram | True | int |  | The amount of memory per instance(should be a multiple of 1024). |
  | storage_size | True | int |  | The amount of storage per instance. |
  | storage_type | True | str |  | The storage type used in your cluster. Value &quot;SSD&quot; is deprecated. Use the equivalent &quot;SSD Premium&quot; instead. |
  | connections | True | list |  | Array of VDCs to connect to your cluster. |
  | location | True | str |  | The physical location where the cluster will be created. This will be where all of your instances live. Property cannot be modified after datacenter creation (disallowed in update requests) |
  | display_name | True | str |  | The friendly name of your cluster. |
  | db_username | True | str |  | The username for the initial postgres user. Some system usernames are restricted (e.g. &quot;postgres&quot;, &quot;admin&quot;, &quot;standby&quot;) |
  | db_password | True | str |  | The username for the initial postgres user. |
  | synchronization_mode | True | str |  | Represents different modes of replication. |
  | backup_location | False | str |  | The S3 location where the backups will be stored. One of [&quot;de&quot;, &quot;eu-south-2&quot;, &quot;eu-central-2&quot;] |
  | backup_id | False | str |  | The ID of the backup to be used. |
  | recovery_target_time | False | str |  | Recovery target time. |
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
  - name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | postgres_cluster | True | str |  | The ID or name of an existing Postgres Cluster. |
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
  - name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | maintenance_window | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the maintenance) and &quot;day_of_the_week&quot; (the Day Of the week when to perform the maintenance). |
  | postgres_version | False | str |  | The PostgreSQL version of your cluster |
  | instances | False | int |  | The total number of instances in the cluster (one master and n-1 standbys). |
  | cores | False | int |  | The number of CPU cores per instance. |
  | ram | False | int |  | The amount of memory per instance(should be a multiple of 1024). |
  | storage_size | False | int |  | The amount of storage per instance. |
  | display_name | False | str |  | The friendly name of your cluster. |
  | postgres_cluster | True | str |  | The ID or name of an existing Postgres Cluster. |
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
# state: **restore**
```yaml
  
```
### Available parameters for state **restore**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | backup_id | True | str |  | The ID of the backup to be used. |
  | recovery_target_time | False | str |  | Recovery target time. |
  | postgres_cluster | True | str |  | The ID or name of an existing Postgres Cluster. |
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
