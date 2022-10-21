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
          datacenter: "{{ datacenter }} - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  
- name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster_id: "{{ cluster_response.mongo_cluster.id }}"
      state: absent
  
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
          datacenter: "{{ datacenter }} - DBaaS Mongo"
          lan: "test_lan"
      display_name: backuptest-04
      wait: true
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | maintenance_window | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the maintenance) and &quot;day_of_the_week&quot; (the Day Of the week when to perform the maintenance). |
  | mongo_db_version | True | str |  | The MongoDB version of your cluster |
  | instances | True | int |  | The total number of instances in the cluster (one master and n-1 standbys). |
  | connections | True | list |  | Array of VDCs to connect to your cluster. |
  | template_id | True | str |  | The unique template ID |
  | location | True | str |  | The physical location where the cluster will be created. This will be where all of your instances live. Property cannot be modified after datacenter creation (disallowed in update requests) |
  | display_name | True | str |  | The friendly name of your cluster. |
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
  - name: Delete Mongo Cluster
    mongo_cluster:
      mongo_cluster_id: "{{ cluster_response.mongo_cluster.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | mongo_cluster | True | str |  | The ID or name of an existing Mongo Cluster. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
