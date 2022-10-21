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
  | k8s_version | False | str |  | The Kubernetes version the cluster is running. This imposes restrictions on what Kubernetes versions can be run in a cluster's nodepools. Additionally, not all Kubernetes versions are viable upgrade targets for all prior versions. |
  | maintenance_window | False | dict |  | The maintenance window is used for updating the cluster's control plane and for upgrading the cluster's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | api_subnet_allow_list | False | list |  | Access to the K8s API server is restricted to these CIDRs. Traffic, internal to the cluster, is not affected by this restriction. If no allowlist is specified, access is not restricted. If an IP without subnet mask is provided, the default value is used: 32 for IPv4 and 128 for IPv6. |
  | s3_buckets_param | False | list |  | List of S3 bucket configured for K8s usage. For now it contains only an S3 bucket used to store K8s API audit logs. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 3600 | How long before wait gives up, in seconds. |
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
  | k8s_cluster | True | str |  | The ID or name of the K8s cluster. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 3600 | How long before wait gives up, in seconds. |
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
  | cluster_name | False | str |  | The name of the K8s cluster. |
  | k8s_cluster | True | str |  | The ID or name of the K8s cluster. |
  | k8s_version | True | str |  | The Kubernetes version the cluster is running. This imposes restrictions on what Kubernetes versions can be run in a cluster's nodepools. Additionally, not all Kubernetes versions are viable upgrade targets for all prior versions. |
  | maintenance_window | True | dict |  | The maintenance window is used for updating the cluster's control plane and for upgrading the cluster's K8s version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | api_subnet_allow_list | False | list |  | Access to the K8s API server is restricted to these CIDRs. Traffic, internal to the cluster, is not affected by this restriction. If no allowlist is specified, access is not restricted. If an IP without subnet mask is provided, the default value is used: 32 for IPv4 and 128 for IPv6. |
  | s3_buckets_param | False | list |  | List of S3 bucket configured for K8s usage. For now it contains only an S3 bucket used to store K8s API audit logs. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 3600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
