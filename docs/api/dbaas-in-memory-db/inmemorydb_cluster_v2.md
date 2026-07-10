# inmemorydb_cluster_v2

This module supports creating, updating, restoring or destroying In-Memory DB Clusters using the DBaaS In-Memory DB v2 API. The cluster region is selected through the I(location) option; I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).

## Example Syntax


```yaml

name: Create Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  version: '9.0'
  instances: 1
  cores: 1
  ram: 4
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - InMemoryDB v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  eviction_policy: noeviction
  persistence_mode: RDB
  maintenance_window: ''
  snapshot_location: ''
  snapshot_retention_days: 7
  snapshot_hours:
    - 2
  db_username: clusteruser
  db_password_hash: ''
  wait: true
  wait_timeout: ''
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  db_username: clusteruser
  db_password_hash: ''
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  inmemorydb_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  db_username: clusteruser
  db_password_hash: ''
  state: restore
  wait: true


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  state: absent
  wait: false

```


### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-in-memory-db).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * connection 
  * snapshot_location 
&nbsp;

# state: **present**
```yaml
  
name: Create Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  version: '9.0'
  instances: 1
  cores: 1
  ram: 4
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - InMemoryDB v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  eviction_policy: noeviction
  persistence_mode: RDB
  maintenance_window: ''
  snapshot_location: ''
  snapshot_retention_days: 7
  snapshot_hours:
    - 2
  db_username: clusteruser
  db_password_hash: ''
  wait: true
  wait_timeout: ''
register: cluster_response

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
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>A weekly 4 hour-long window, during which maintenance might occur. A dict with keys `time` (start of the maintenance window in UTC, e.g. &quot;16:30:00&quot;) and `day_of_the_week` (e.g. &quot;Sunday&quot;).</td>
  </tr>
  <tr>
  <td>version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The In-Memory DB version of the cluster. Use the inmemorydb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of instances in the cluster. A value of 1 creates a standalone instance; values 2-5 create a replicated setup with one primary and n-1 passive secondaries.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of dedicated CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of memory per instance in gigabytes (GB). RAM cannot be downgraded because storage size is automatically derived from RAM.</td>
  </tr>
  <tr>
  <td>connection<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>Connection information of the In-Memory DB cluster. A dict with keys `datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask of the cluster's primary instance in CIDR notation, e.g. 192.168.1.101/24).</td>
  </tr>
  <tr>
  <td>eviction_policy<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The key eviction policy applied when the memory limit is reached.<br />Options: ['noeviction', 'allkeys-lru', 'allkeys-lfu', 'allkeys-random', 'volatile-lru', 'volatile-lfu', 'volatile-random', 'volatile-ttl']</td>
  </tr>
  <tr>
  <td>persistence_mode<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies how and whether data is persisted to disk. `None` disables persistence; `AOF` logs every write operation; `RDB` takes periodic point-in-time snapshots; `RDB_AOF` combines both.<br />Options: ['None', 'AOF', 'RDB', 'RDB_AOF']</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your In-Memory DB cluster. Must be 2-63 characters and must begin and end with an alphanumeric character (`[A-Za-z0-9]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username for the initial In-Memory DB user. Must be 2-16 characters and may only contain alphanumeric characters (`[A-Za-z0-9]`) and underscores (`_`). Restricted usernames (for example, admin, standby) are not allowed. Required when creating a cluster; on update and restore it may be omitted to keep the existing user unchanged. Supply db_username and db_password_hash together to (re)set the user or rotate its password; because the API never returns the hash for comparison, providing them always triggers an update (reported as changed).</td>
  </tr>
  <tr>
  <td>db_password_hash<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The pre-hashed password for the initial In-Memory DB user. The hex-encoded hash of the password; must be exactly 64 lowercase hexadecimal characters (the standard output of SHA-256). Note: base64-encoded SHA-256 hashes (44 characters) are not accepted. The plaintext password is never sent to nor returned by the API. Required when creating a cluster; on update and restore it may be omitted to leave the current password unchanged. Supplying it (together with db_username) always (re)sets the password and reports the task as changed, since the API never returns the hash for comparison; omit it for idempotent runs.</td>
  </tr>
  <tr>
  <td>db_password_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The hashing algorithm used to produce db_password_hash.<br />Default: SHA-256<br />Options: ['SHA-256']</td>
  </tr>
  <tr>
  <td>snapshot_location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The Object Storage location where snapshots will be stored. For added data safety, use a different location than the cluster. The inmemorydb_snapshot_location_v2_info module provides a list of supported locations. Changing this forces the cluster to be re-created.</td>
  </tr>
  <tr>
  <td>snapshot_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of days snapshots are retained before being automatically deleted. Reducing this value causes the platform to purge any existing snapshots that fall outside the new retention window.</td>
  </tr>
  <tr>
  <td>snapshot_hours<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>Hours of the day (UTC) at which snapshots are scheduled to be taken. Each value must be between 0 and 23. At least one hour must be specified.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A human-readable description for the cluster.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates log collection and reporting for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates metrics collection and reporting for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.</td>
  </tr>
  <tr>
  <td>source_snapshot_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID of the snapshot to initialize the cluster from when creating (restore from an existing snapshot).</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Recovery target time (ISO 8601). Restores the cluster from the most recent snapshot taken at or before that time. Optional on create (used together with source_snapshot_id); required for an in-place restore when state is `restore`. In-Memory DB does not provide continuous point-in-time recovery; the nearest preceding snapshot is used.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/fra&quot;. The api_url, if set, overrides this.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  state: absent
  wait: false

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
  <td>inmemorydb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing In-Memory DB Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/fra&quot;. The api_url, if set, overrides this.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update Cluster
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  location: ''
  inmemorydb_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  db_username: clusteruser
  db_password_hash: ''
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response

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
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>A weekly 4 hour-long window, during which maintenance might occur. A dict with keys `time` (start of the maintenance window in UTC, e.g. &quot;16:30:00&quot;) and `day_of_the_week` (e.g. &quot;Sunday&quot;).</td>
  </tr>
  <tr>
  <td>version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The In-Memory DB version of the cluster. Use the inmemorydb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of instances in the cluster. A value of 1 creates a standalone instance; values 2-5 create a replicated setup with one primary and n-1 passive secondaries.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of dedicated CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory per instance in gigabytes (GB). RAM cannot be downgraded because storage size is automatically derived from RAM.</td>
  </tr>
  <tr>
  <td>eviction_policy<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key eviction policy applied when the memory limit is reached.<br />Options: ['noeviction', 'allkeys-lru', 'allkeys-lfu', 'allkeys-random', 'volatile-lru', 'volatile-lfu', 'volatile-random', 'volatile-ttl']</td>
  </tr>
  <tr>
  <td>persistence_mode<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies how and whether data is persisted to disk. `None` disables persistence; `AOF` logs every write operation; `RDB` takes periodic point-in-time snapshots; `RDB_AOF` combines both.<br />Options: ['None', 'AOF', 'RDB', 'RDB_AOF']</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your In-Memory DB cluster. Must be 2-63 characters and must begin and end with an alphanumeric character (`[A-Za-z0-9]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The username for the initial In-Memory DB user. Must be 2-16 characters and may only contain alphanumeric characters (`[A-Za-z0-9]`) and underscores (`_`). Restricted usernames (for example, admin, standby) are not allowed. Required when creating a cluster; on update and restore it may be omitted to keep the existing user unchanged. Supply db_username and db_password_hash together to (re)set the user or rotate its password; because the API never returns the hash for comparison, providing them always triggers an update (reported as changed).</td>
  </tr>
  <tr>
  <td>db_password_hash<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The pre-hashed password for the initial In-Memory DB user. The hex-encoded hash of the password; must be exactly 64 lowercase hexadecimal characters (the standard output of SHA-256). Note: base64-encoded SHA-256 hashes (44 characters) are not accepted. The plaintext password is never sent to nor returned by the API. Required when creating a cluster; on update and restore it may be omitted to leave the current password unchanged. Supplying it (together with db_username) always (re)sets the password and reports the task as changed, since the API never returns the hash for comparison; omit it for idempotent runs.</td>
  </tr>
  <tr>
  <td>db_password_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The hashing algorithm used to produce db_password_hash.<br />Default: SHA-256<br />Options: ['SHA-256']</td>
  </tr>
  <tr>
  <td>snapshot_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of days snapshots are retained before being automatically deleted. Reducing this value causes the platform to purge any existing snapshots that fall outside the new retention window.</td>
  </tr>
  <tr>
  <td>snapshot_hours<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Hours of the day (UTC) at which snapshots are scheduled to be taken. Each value must be between 0 and 23. At least one hour must be specified.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A human-readable description for the cluster.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates log collection and reporting for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates metrics collection and reporting for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect until the service is activated.</td>
  </tr>
  <tr>
  <td>inmemorydb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing In-Memory DB Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/fra&quot;. The api_url, if set, overrides this.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **restore**
```yaml
  
name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.inmemorydb_cluster_v2:
  inmemorydb_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  db_username: clusteruser
  db_password_hash: ''
  state: restore
  wait: true

```
### Available parameters for state **restore**:
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
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The username for the initial In-Memory DB user. Must be 2-16 characters and may only contain alphanumeric characters (`[A-Za-z0-9]`) and underscores (`_`). Restricted usernames (for example, admin, standby) are not allowed. Required when creating a cluster; on update and restore it may be omitted to keep the existing user unchanged. Supply db_username and db_password_hash together to (re)set the user or rotate its password; because the API never returns the hash for comparison, providing them always triggers an update (reported as changed).</td>
  </tr>
  <tr>
  <td>db_password_hash<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The pre-hashed password for the initial In-Memory DB user. The hex-encoded hash of the password; must be exactly 64 lowercase hexadecimal characters (the standard output of SHA-256). Note: base64-encoded SHA-256 hashes (44 characters) are not accepted. The plaintext password is never sent to nor returned by the API. Required when creating a cluster; on update and restore it may be omitted to leave the current password unchanged. Supplying it (together with db_username) always (re)sets the password and reports the task as changed, since the API never returns the hash for comparison; omit it for idempotent runs.</td>
  </tr>
  <tr>
  <td>db_password_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The hashing algorithm used to produce db_password_hash.<br />Default: SHA-256<br />Options: ['SHA-256']</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Recovery target time (ISO 8601). Restores the cluster from the most recent snapshot taken at or before that time. Optional on create (used together with source_snapshot_id); required for an in-place restore when state is `restore`. In-Memory DB does not provide continuous point-in-time recovery; the nearest preceding snapshot is used.</td>
  </tr>
  <tr>
  <td>inmemorydb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing In-Memory DB Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/fra&quot;. The api_url, if set, overrides this.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
