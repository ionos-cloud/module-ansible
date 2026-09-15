# mariadb_cluster_v2

This module supports creating, updating, restoring or destroying MariaDB Clusters using the DBaaS MariaDB v2 API. The cluster region is selected through the I(location) option; I(api_url) overrides the base API URL globally (for a proxy/test endpoint, not for region selection).

## Example Syntax


```yaml

name: Create Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_version: '11.4'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaSMariaDB - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.2.101/24
  name: 'ansible-test-v2'
  description: Ansible test MariaDB v2 cluster
  maintenance_window:
    day_of_the_week: Sunday
    time: 09:00:00
  backup_location: 'eu-central-3'
  backup_retention_days: 7
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  wait: true
  wait_timeout: '3600'
register: cluster_response


name: Update Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  cores: 2
  ram: 6
  storage_size: 20
  backup_retention_days: 14
  description: Updated Ansible test MariaDB v2 cluster
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: update
  wait: true
  wait_timeout: '3600'
register: updated_cluster_response


name: Restore Cluster (in-place)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  recovery_target_time: ''
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: restore
  wait: true
  wait_timeout: '3600'
register: restored_cluster_response


name: Delete Cluster (async)
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  state: absent
  wait: false

```


### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-mariadb).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * connection 
  * backup_location 
&nbsp;

# state: **present**
```yaml
  
name: Create Cluster
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_version: '11.4'
  instances: 1
  cores: 1
  ram: 4
  storage_size: 10
  connection:
    datacenter: 'AnsibleAutoTestDBaaSMariaDB - DBaaS v2'
    lan: test_lan1
    primary_instance_address: 192.168.2.101/24
  name: 'ansible-test-v2'
  description: Ansible test MariaDB v2 cluster
  maintenance_window:
    day_of_the_week: Sunday
    time: 09:00:00
  backup_location: 'eu-central-3'
  backup_retention_days: 7
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  wait: true
  wait_timeout: '3600'
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
  <td>mariadb_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The MariaDB version of the cluster. Use the mariadb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of instances in the cluster. A value of 1 creates a single-instance cluster; values 2 to 5 create a replicated cluster with one primary and n-1 secondary instances.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of CPU cores per instance. Accepted values are 1 to 62. On update, cores can be increased or decreased.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of memory per instance in gigabytes (GB). Accepted values are 4 to 240. On update, RAM can be increased or decreased.</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of storage per instance in gigabytes (GB). Accepted values are 10 to 4096. On update, storage size can only be increased; it cannot be reduced.</td>
  </tr>
  <tr>
  <td>connection<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>Connection information of the MariaDB cluster. A dict with keys `datacenter` (ID or name), `lan` (ID or name) and `primary_instance_address` (IP and netmask of the cluster's primary instance in CIDR notation, e.g. 192.168.2.101/24).</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your MariaDB cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A human-readable description for the cluster.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the initial MariaDB user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`). Some usernames are reserved for platform use (for example `mariadb`, `admin`, `standby`). The credentials block is re-sent in full on every update and restore, so this option is also required for those states.</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the initial MariaDB user. Must be between 10 and 256 characters long. For a strong password we recommend that it also meets the following criteria, though these are not enforced: - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp; The password is never returned by the API, so it must be supplied again on update and restore, and a change to it alone cannot be detected: a task whose only difference is a new db_password reports changed=false and sends no request.</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to create and grant the user access to. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>backup_location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The Object Storage location where the backups are created. The mariadb_backup_location_v2_info module provides a list of supported locations. Changing this forces the cluster to be re-created.</td>
  </tr>
  <tr>
  <td>backup_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of days cluster backups are retained. Accepted values are 1 to 365. If you reduce this value, backups older than the new retention window are purged.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates the collection and reporting of logs for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Log collection does not start until the observability service is active.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates the collection and reporting of metrics for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Metric collection does not start until the observability service is active.</td>
  </tr>
  <tr>
  <td>backup_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID of the backup to initialize the cluster from when creating (restore from an existing backup).</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation (together with backup_id), or for an in-place restore when state is `restore`.</td>
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
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
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
  <td>mariadb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing MariaDB Cluster.</td>
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
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  cores: 2
  ram: 6
  storage_size: 20
  backup_retention_days: 14
  description: Updated Ansible test MariaDB v2 cluster
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: update
  wait: true
  wait_timeout: '3600'
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
  <td>mariadb_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The MariaDB version of the cluster. Use the mariadb_version_v2_info module (GET /versions) to retrieve the list of supported versions. To upgrade, provide a version listed in `can_upgrade_to` for the current version; downgrades are not supported.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of instances in the cluster. A value of 1 creates a single-instance cluster; values 2 to 5 create a replicated cluster with one primary and n-1 secondary instances.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of CPU cores per instance. Accepted values are 1 to 62. On update, cores can be increased or decreased.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory per instance in gigabytes (GB). Accepted values are 4 to 240. On update, RAM can be increased or decreased.</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of storage per instance in gigabytes (GB). Accepted values are 10 to 4096. On update, storage size can only be increased; it cannot be reduced.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your MariaDB cluster. Must be 63 characters or less and must begin and end with an alphanumeric character (`[a-z0-9A-Z]`) with dashes (`-`), underscores (`_`), dots (`.`), and alphanumerics between.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A human-readable description for the cluster.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the initial MariaDB user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`). Some usernames are reserved for platform use (for example `mariadb`, `admin`, `standby`). The credentials block is re-sent in full on every update and restore, so this option is also required for those states.</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the initial MariaDB user. Must be between 10 and 256 characters long. For a strong password we recommend that it also meets the following criteria, though these are not enforced: - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp; The password is never returned by the API, so it must be supplied again on update and restore, and a change to it alone cannot be detected: a task whose only difference is a new db_password reports changed=false and sends no request.</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to create and grant the user access to. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>backup_retention_days<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of days cluster backups are retained. Accepted values are 1 to 365. If you reduce this value, backups older than the new retention window are purged.</td>
  </tr>
  <tr>
  <td>logs_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates the collection and reporting of logs for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Log collection does not start until the observability service is active.</td>
  </tr>
  <tr>
  <td>metrics_enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activates or deactivates the collection and reporting of metrics for this cluster's observability. If the observability service is not activated on the contract, this setting is accepted but has no effect. Metric collection does not start until the observability service is active.</td>
  </tr>
  <tr>
  <td>mariadb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing MariaDB Cluster.</td>
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
ionoscloudsdk.ionoscloud.mariadb_cluster_v2:
  location: 'de/fra'
  mariadb_cluster: ''
  recovery_target_time: ''
  db_username: 'dbadmin'
  db_password: ''
  db_database: 'my_database'
  state: restore
  wait: true
  wait_timeout: '3600'
register: restored_cluster_response

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
  <td>The username of the initial MariaDB user. Must be 16 characters or less and must include only alphanumeric characters (`[A-Za-z0-9_]`) and underscores (`_`). Some usernames are reserved for platform use (for example `mariadb`, `admin`, `standby`). The credentials block is re-sent in full on every update and restore, so this option is also required for those states.</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for the initial MariaDB user. Must be between 10 and 256 characters long. For a strong password we recommend that it also meets the following criteria, though these are not enforced: - Contains at least one lowercase letter. - Contains at least one uppercase letter. - Contains at least one digit (0-9). - Contains at least one special character from the set: @$!%*?&amp; The password is never returned by the API, so it must be supplied again on update and restore, and a change to it alone cannot be detected: a task whose only difference is a new db_password reports changed=false and sends no request.</td>
  </tr>
  <tr>
  <td>db_database<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the initial database to create and grant the user access to. Must be 63 characters or less and must include only alphanumeric characters (`[a-z0-9A-Z]`) and underscores (`_`).</td>
  </tr>
  <tr>
  <td>recovery_target_time<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Recovery target time (ISO 8601). Used to replay backups up to the specified time on creation (together with backup_id), or for an in-place restore when state is `restore`.</td>
  </tr>
  <tr>
  <td>mariadb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing MariaDB Cluster.</td>
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
