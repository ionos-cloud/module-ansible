# postgres_cluster_v2

This module supports creating, updating, restoring or destroying Postgres Clusters using the DBaaS PostgreSQL v2 API. The cluster region is selected through the I(location) option; I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).

## Example Syntax


```yaml

name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_version: '16'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  replication_mode: ASYNCHRONOUS
  maintenance_window: ''
  backup_location: ''
  backup_retention_days: 7
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  wait: true
  wait_timeout: ''
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  storage_size: 20
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
  state: update
  wait: true
  wait_timeout: ''
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  postgres_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
  state: restore
  wait: true


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  state: absent
  wait: false

```


### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-postgres).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * connection 
  * backup_location 
&nbsp;

# state: **present**
```yaml
  
name: Create Cluster
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_version: '16'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaS - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.1.101/24
  name: ''
  replication_mode: ASYNCHRONOUS
  maintenance_window: ''
  backup_location: ''
  backup_retention_days: 7
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
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
  <td>postgres_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The PostgreSQL version for the cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of instances in the cluster (one primary and n-1 secondary).</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of memory per instance in gigabytes (GB).</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of storage per instance in gigabytes (GB).</td>
  </tr>
  <tr>
  <td>connection<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>Connection information of the PostgreSQL cluster. A dict with keys `datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask of the cluster's primary instance, e.g. 192.168.1.101/24).</td>
  </tr>
  <tr>
  <td>replication_mode<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Defines the replication mode across instances. - `ASYNCHRONOUS`: Propagates updates to other instances without waiting for confirmation. Offers higher performance but may result in temporary data inconsistencies during replication delays. - `STRICTLY_SYNCHRONOUS`: Only supported for clusters with at least 3 instances. Requires all instances to acknowledge the update before it is committed, guaranteeing strong consistency at the cost of potential performance impact in high-latency environments.<br />Options: ['ASYNCHRONOUS', 'STRICTLY_SYNCHRONOUS']</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your PostgreSQL cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the master database user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the master database user. Must meet the following requirements: - At least 8 characters long. - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp;</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to be created. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>connection_pooler<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Defines how database connections are managed and reused. Default value is DISABLED. DISABLED: No connection pooling is used. Each request opens a new connection, which is closed immediately after use. It ensures isolation but may impact performance due to frequent connection setup and teardown. TRANSACTION: Connections are pooled and reused for the duration of a transaction. Once the transaction completes, the connection is returned to the pool. This mode balances efficiency with transactional integrity. SESSION: Connections are retained for the entire session and reused across multiple transactions. Offers the highest performance by minimizing connection overhead, but may tie up resources longer.<br />Options: ['DISABLED', 'TRANSACTION', 'SESSION']</td>
  </tr>
  <tr>
  <td>backup_location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The Object Storage location where the backup will be created. The BackupLocations provides a list of supported locations.</td>
  </tr>
  <tr>
  <td>backup_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Configures how many days cluster backups are retained.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Allows or disallows the collection and reporting of logs for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; log collection will not be enabled until the observability service is activated.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Allows or disallows the collection and reporting of metrics for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; metric collection will not be enabled until the observability service is activated.</td>
  </tr>
  <tr>
  <td>backup_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID of the backup to initialize the cluster from when creating (restore from an existing backup).</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation, or for an in-place restore when state is `restore`.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;. The api_url, if set, overrides this.</td>
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
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
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
  <td>postgres_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Postgres Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;. The api_url, if set, overrides this.</td>
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
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  location: ''
  postgres_cluster: ''
  instances: 2
  cores: 2
  ram: 6
  storage_size: 20
  db_username: clusteruser
  db_password: 7357Cluster!x
  db_database: testdb
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
  <td>postgres_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The PostgreSQL version for the cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of instances in the cluster (one primary and n-1 secondary).</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory per instance in gigabytes (GB).</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of storage per instance in gigabytes (GB).</td>
  </tr>
  <tr>
  <td>replication_mode<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Defines the replication mode across instances. - `ASYNCHRONOUS`: Propagates updates to other instances without waiting for confirmation. Offers higher performance but may result in temporary data inconsistencies during replication delays. - `STRICTLY_SYNCHRONOUS`: Only supported for clusters with at least 3 instances. Requires all instances to acknowledge the update before it is committed, guaranteeing strong consistency at the cost of potential performance impact in high-latency environments.<br />Options: ['ASYNCHRONOUS', 'STRICTLY_SYNCHRONOUS']</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your PostgreSQL cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the master database user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the master database user. Must meet the following requirements: - At least 8 characters long. - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp;</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to be created. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>connection_pooler<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Defines how database connections are managed and reused. Default value is DISABLED. DISABLED: No connection pooling is used. Each request opens a new connection, which is closed immediately after use. It ensures isolation but may impact performance due to frequent connection setup and teardown. TRANSACTION: Connections are pooled and reused for the duration of a transaction. Once the transaction completes, the connection is returned to the pool. This mode balances efficiency with transactional integrity. SESSION: Connections are retained for the entire session and reused across multiple transactions. Offers the highest performance by minimizing connection overhead, but may tie up resources longer.<br />Options: ['DISABLED', 'TRANSACTION', 'SESSION']</td>
  </tr>
  <tr>
  <td>backup_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Configures how many days cluster backups are retained.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Allows or disallows the collection and reporting of logs for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; log collection will not be enabled until the observability service is activated.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Allows or disallows the collection and reporting of metrics for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect; metric collection will not be enabled until the observability service is activated.</td>
  </tr>
  <tr>
  <td>postgres_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Postgres Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;. The api_url, if set, overrides this.</td>
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
ionoscloudsdk.ionoscloud.postgres_cluster_v2:
  postgres_cluster: ''
  recovery_target_time: "2023-07-01T13:00:00Z"
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
  <td align="center">True</td>
  <td>The username of the master database user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the master database user. Must meet the following requirements: - At least 8 characters long. - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp;</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to be created. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation, or for an in-place restore when state is `restore`.</td>
  </tr>
  <tr>
  <td>postgres_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Postgres Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) in which the cluster will be created. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;. The api_url, if set, overrides this.</td>
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
