# Postgres Cluster

## Example Syntax

```yaml
  - name: Create Postgres Cluster
    ionoscloudsdk.ionoscloud.postgres_cluster:
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
    ionoscloudsdk.ionoscloud.postgres_cluster:
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
    ionoscloudsdk.ionoscloud.postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| postgres_version | **yes**/no | string |  | The PostgreSQL version of your cluster. Required only for state = 'present' |
| instances | **yes**/no | string |  | The total number of instances in the cluster (one master and n-1 standbys). Required only for state = 'present' |
| cores | **yes**/no | string |  | The number of CPU cores per instance. Required only for state = 'present' |
| ram | **yes**/no | string |  | The amount of memory per instance(should be a multiple of 1024). Required only for state = 'present' |
| storage_size | **yes**/no | string |  | The amount of storage per instance. Required only for state = 'present' |
| storage_type | **yes**/no | string |  | The storage type used in your cluster. Required only for state = 'present' |
| connections | **yes**/no | string |  | Array of VDCs to connect to your cluster. A VDC is described as a dict containing 'datacenter', 'lan' and 'cidr'. For datacenter and lan either name or UUID may be specified. Required only for state = 'present' |
| location | **yes**/no | string |  | The physical location where the cluster will be created. This will be where all of your instances live. (disallowed in update requests). Required only for state = 'present' |
| display_name | **yes**/no | string |  | The friendly name of your cluster. Required only for state = 'present' |
| db_username | **yes**/no | string |  | The username for the initial postgres user. Some system usernames are restricted (e.g. "postgres", "admin", standby"). Required only for state = 'present' |
| db_password | **yes**/no | string |  | The password for the initial postgres user. Required only for state = 'present' |
| synchronization_mode | **yes**/no | string |  | Represents different modes of replication. Required only for state = 'present' |
| backup_id | no | string |  | The unique ID of the backup you want to restore. |
| recovery_target_time | no | string |  | If this value is supplied as ISO 8601 timestamp, the backup will be replayed up until the given timestamp. If empty, the backup will be applied completely. |
| maintenance\_window | no | dict |  | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'. |
| postgres_cluster | **yes**/no | string |  | Either a UUID or a display name of the Postgres cluster. Required only for state = 'absent', state = 'update' or state = 'restore' |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update or restore |

