# mongo_cluster

This is a module that supports creating and destroying Mongo Clusters

## Example Syntax


```yaml
- name: Create Cluster
    mongo_cluster:
      mongo_db_version: 5.0
      instances: 3
      location: de/fra
      template_id: 6b78ea06-ee0e-4689-998c-fc9c46e781f6
      connections:
        - cidr_list: 
            - 192.168.1.116/24
            - 192.168.1.117/24
            - 192.168.1.118/24
          datacenter: "Datacenter - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  
- name: Update Cluster
    mongo_cluster:
      mongo_cluster: backuptest-04
      display_name: backuptest-05
      state: update
      do_not_replace: true
      wait: true
    register: cluster_response
  
- name: Restore Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      backup_id: 9ab6545c-b138-4a86-b6ca-0d872a2b0953
      state: restore
  
- name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
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
    "mongo_cluster": {
        "type": "cluster",
        "id": "3fdd2940-f9b4-425d-b52b-4199a84188d2",
        "metadata": {
            "created_date": "2023-05-30T13:43:20+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": null,
            "last_modified_by": null,
            "last_modified_by_user_id": null,
            "state": "BUSY",
            "health": "UNKNOWN"
        },
        "properties": {
            "display_name": "AnsibleTestMongoDBCluster",
            "mongo_db_version": "5.0",
            "location": "de/fra",
            "instances": 3,
            "connections": [
                {
                    "datacenter_id": "6b36f398-2089-414b-a57f-85f7b88aee5b",
                    "lan_id": "1",
                    "cidr_list": [
                        "<CIDR1>",
                        "<CIDR2>",
                        "<CIDR3>"
                    ]
                }
            ],
            "maintenance_window": {
                "time": "14:13:28",
                "day_of_the_week": "Thursday"
            },
            "template_id": "6b78ea06-ee0e-4689-998c-fc9c46e781f6",
            "connection_string": "<CONNECTION_STRING>"
        }
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Cluster
    mongo_cluster:
      mongo_db_version: 5.0
      instances: 3
      location: de/fra
      template_id: 6b78ea06-ee0e-4689-998c-fc9c46e781f6
      connections:
        - cidr_list: 
            - 192.168.1.116/24
            - 192.168.1.117/24
            - 192.168.1.118/24
          datacenter: "Datacenter - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>A weekly window of 4 hours during which maintenance work can be performed.</td>
  </tr>
  <tr>
  <td>mongo_db_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The MongoDB version of your cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The total number of instances in the cluster (one primary and n-1 secondaries).</td>
  </tr>
  <tr>
  <td>connections<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>Array of VDCs to connect to your cluster.</td>
  </tr>
  <tr>
  <td>template_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The unique ID of the template, which specifies the number of cores, storage size, and memory. You cannot downgrade to a smaller template or minor edition (e.g. from business to playground). To get a list of all templates to confirm the changes use the /templates endpoint.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The physical location where the cluster will be created. This is the location where all your instances will be located. This property is immutable.</td>
  </tr>
  <tr>
  <td>display_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your cluster.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
  - name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
  - name: Update Cluster
    mongo_cluster:
      mongo_cluster: backuptest-04
      display_name: backuptest-05
      state: update
      do_not_replace: true
      wait: true
    register: cluster_response
  
```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>A weekly window of 4 hours during which maintenance work can be performed.</td>
  </tr>
  <tr>
  <td>mongo_db_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The MongoDB version of your cluster.</td>
  </tr>
  <tr>
  <td>instances<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The total number of instances in the cluster (one primary and n-1 secondaries).</td>
  </tr>
  <tr>
  <td>connections<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Array of VDCs to connect to your cluster.</td>
  </tr>
  <tr>
  <td>template_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The unique ID of the template, which specifies the number of cores, storage size, and memory. You cannot downgrade to a smaller template or minor edition (e.g. from business to playground). To get a list of all templates to confirm the changes use the /templates endpoint.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The physical location where the cluster will be created. This is the location where all your instances will be located. This property is immutable.</td>
  </tr>
  <tr>
  <td>display_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your cluster.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
  - name: Restore Mongo Cluster
    mongo_cluster:
      mongo_cluster: backuptest-05
      backup_id: 9ab6545c-b138-4a86-b6ca-0d872a2b0953
      state: restore
  
```
### Available parameters for state **restore**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>backup_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID of the backup to be used.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
