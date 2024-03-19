# mariadb_cluster

This is a module that supports creating, updating or destroying MariaDB Clusters

## Example Syntax


```yaml
- name: Create MariaDB Cluster
    mariadb_cluster:
      mariadb_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
- name: Update MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      mariadb_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  
- name: Delete MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      state: absent

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "action": "create",
    "mariadb_cluster": {
        "id": "7182ab85-3671-45e5-b2bb-e943c4479e03",
        "metadata": {
            "created_date": "2024-02-27T16:02:55+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": "2024-02-27T16:02:55+00:00",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "state": "AVAILABLE"
        },
        "properties": {
            "display_name": "MariaDB-cluster",
            "mariadb_version": "10.6",
            "dns_name": "<CLUSTER_DNS>",
            "instances": 1,
            "ram": 4,
            "cores": 4,
            "storage_size": 10,
            "connections": [
                {
                    "datacenter_id": "3e223566-5a98-495a-9e4c-2c5fc71c057b",
                    "lan_id": "2",
                    "cidr": "<CIDR"
                }
            ],
            "maintenance_window": {
                "time": "14:17:42",
                "day_of_the_week": "Tuesday"
            }
        }
    }
}

```

&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * mariadb_version 
  * connections 
&nbsp;

# state: **present**
```yaml
  - name: Create MariaDB Cluster
    mariadb_cluster:
      mariadb_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      connections:
        - cidr: 192.168.1.106/24
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      db_username: test
      db_password: 7357cluster
      wait: true
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
  <td align="center">False</td>
  <td>A weekly 4 hour-long window, during which maintenance might occur.</td>
  </tr>
  <tr>
  <td>mariadb_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The MariaDB version of your cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of instances in the cluster (one master and n-1 standbys).</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The number of CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of memory per instance in megabytes. Has to be a multiple of 1024.</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The amount of storage per instance in megabytes.</td>
  </tr>
  <tr>
  <td>connections<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>Array of datacenters to connect to your cluster.</td>
  </tr>
  <tr>
  <td>display_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The friendly name of your cluster.</td>
  </tr>
  <tr>
  <td>db_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username for the initial MariaDB user. Some system usernames are restricted (e.g. &quot;mariadb&quot;, &quot;admin&quot;, &quot;standby&quot;).</td>
  </tr>
  <tr>
  <td>db_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password for a MariaDB user.</td>
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
  - name: Delete MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      state: absent
  
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
  - name: Update MariaDB Cluster
    mariadb_cluster:
      mariadb_cluster: backuptest-04
      mariadb_version: 12
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
  <td>A weekly 4 hour-long window, during which maintenance might occur.</td>
  </tr>
  <tr>
  <td>mariadb_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The MariaDB version of your cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of instances in the cluster (one master and n-1 standbys).</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of CPU cores per instance.</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory per instance in megabytes. Has to be a multiple of 1024.</td>
  </tr>
  <tr>
  <td>storage_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of storage per instance in megabytes.</td>
  </tr>
  <tr>
  <td>display_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The friendly name of your cluster.</td>
  </tr>
  <tr>
  <td>mariadb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing MariaDB Cluster.</td>
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
