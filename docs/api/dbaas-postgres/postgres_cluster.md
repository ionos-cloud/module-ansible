# Postgres Cluster

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
          datacenterId: "{{ datacenter_response.datacenter.id }}"
          lanId: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response

  - name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster_id: "{{ cluster_response.postgres_cluster.id }}"
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
      postgres_cluster_id: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |

| postgres_version | **yes** | string |  | The PostgreSQL version of your cluster. |
| instances | **yes** | string |  | The total number of instances in the cluster (one master and n-1 standbys). |
| cores | **yes** | string |  | The number of CPU cores per instance. |
| ram | **yes** | string |  | The amount of memory per instance(should be a multiple of 1024). |
| storage_size | **yes** | string |  | The amount of storage per instance. |
| storage_type | **yes** | string |  | The storage type used in your cluster. |
| connections | **yes** | string |  | Array of VDCs to connect to your cluster. |
| location | **yes** | string |  | The description of the datacenter. |
| display_name | **yes** | string |  | The description of the datacenter. |
| db_username | **yes** | string |  | The description of the datacenter. |
| db_password | **yes** | string |  | The description of the datacenter. |
| synchronization_mode | **yes** | string |  | The description of the datacenter. |
| backup_id | **yes** | string |  | The description of the datacenter. |
| recovery_target_time | **yes** | string |  | The description of the datacenter. |
| maintenance\_window | **yes** | dict |  | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'. |


| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

