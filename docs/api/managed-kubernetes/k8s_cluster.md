# k8s_cluster

This is a simple module that supports creating or removing K8s Clusters. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create k8s cluster
    k8s_cluster:
      name: "{{ cluster_name }}"
  

  - name: Update k8s cluster
    k8s_cluster:
      k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      k8s_version: 1.17.8
      state: update
  

  - name: Delete k8s cluster
    k8s_cluster:
      k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create k8s cluster
    k8s_cluster:
      name: "{{ cluster_name }}"
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | cluster_name | True | str |  | The name of the K8s cluster. |
  | k8s_version | False | str |  | The description of the virtual datacenter. |
  | maintenance_window | False | dict |  | The datacenter location. |
  | api_subnet_allow_list | False | list |  | The datacenter location. |
  | s3_buckets_param | False | list |  | The datacenter location. |
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
  
  - name: Delete k8s cluster
    k8s_cluster:
      k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | k8s_cluster_id | True | str |  | The ID of the K8s cluster. |
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
  
  - name: Update k8s cluster
    k8s_cluster:
      k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      k8s_version: 1.17.8
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | cluster_name | True | str |  | The name of the K8s cluster. |
  | k8s_cluster_id | True | str |  | The ID of the K8s cluster. |
  | k8s_version | True | str |  | The description of the virtual datacenter. |
  | maintenance_window | True | dict |  | The datacenter location. |
  | api_subnet_allow_list | False | list |  | The datacenter location. |
  | s3_buckets_param | False | list |  | The datacenter location. |
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
