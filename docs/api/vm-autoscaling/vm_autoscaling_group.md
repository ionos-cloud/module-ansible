# vm_autoscaling_group

This is a module that supports creating, updating or destroying VM Autoscaling Groups

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
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
- name: Update Postgres Cluster
    postgres_cluster:
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
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
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
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | max_replica_count | True | int |  | The maximum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes. |
  | min_replica_count | True | int |  | The minimum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes |
  | name | True | str |  | The name of the VM Auto Scaling Group. This field must not be null or blank. |
  | datacenter | True | str |  | The VMs for this VM Auto Scaling Description are created in this virtual data center. |
  | metric | True | str |  | The metric that triggers the scaling actions. Metric values are checked at fixed intervals. |
  | range | True | str |  | Specifies the time range for which the samples are to be aggregated. Must be &gt;= 2 minutes. |
  | unit | True | str |  | The units of the applied metric. 'TOTAL' can only be combined with 'INSTANCE_CPU_UTILIZATION_AVERAGE'. |
  | scale_in_threshold | False | int |  | The lower threshold for the value of the 'metric'. Used with the `less than` (&lt;) operator. When this value is exceeded, a scale-in action is triggered, specified by the 'scaleInAction' property. The value must have a higher minimum delta to the 'scaleOutThreshold', depending on the 'metric', to avoid competing for actions at the same time. |
  | scale_out_threshold | False | int |  | The upper threshold for the value of the 'metric'. Used with the 'greater than' (&gt;) operator. A scale-out action is triggered when this value is exceeded, specified by the 'scaleOutAction' property. The value must have a lower minimum delta to the 'scaleInThreshold', depending on the metric, to avoid competing for actions simultaneously. If 'properties.policy.unit=TOTAL', a value &gt;= 40 must be chosen. |
  | scale_in_action | False | dict |  | Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is always about removing VMs associated with this VM Auto Scaling Group. By default, the termination policy is 'OLDEST_SERVER_FIRST' is effective. |
  | scale_out_action | False | dict |  | Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, scaling is always about adding new VMs to this VM Auto Scaling Group. |
  | nics | False | list |  | The list of NICs associated with this replica. |
  | volumes | False | list |  | List of volumes associated with this Replica. |
  | availability_zone | False | str |  | The zone where the VMs are created. The availability zone is always automatically set to 'AUTO' for performance reasons. Even if you set another value, e.g. 'null', or leave it empty. |
  | cores | False | str |  | The total number of cores for the VMs. |
  | cpu_family | False | str |  | The CPU family for the VMs created with this configuration. If the value is 'null', the VM is created with the default CPU family for the assigned site. |
  | ram | False | int |  | The size of the memory for the VMs in MB. The size must be in multiples of 256 MB, with a minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at least 1024 MB. If you set the RAM size to more than 240 GB, 'ramHotPlug=FALSE' is fixed. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
  - name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | vm_autoscaling_group | True | str |  | The ID or name of an existing VM Autoscaling Group. |
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
  - name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      postgres_version: 12
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | max_replica_count | False | int |  | The maximum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes. |
  | min_replica_count | False | int |  | The minimum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes |
  | name | False | str |  | The name of the VM Auto Scaling Group. This field must not be null or blank. |
  | datacenter | False | str |  | The VMs for this VM Auto Scaling Description are created in this virtual data center. |
  | metric | False | str |  | The metric that triggers the scaling actions. Metric values are checked at fixed intervals. |
  | range | False | str |  | Specifies the time range for which the samples are to be aggregated. Must be &gt;= 2 minutes. |
  | unit | False | str |  | The units of the applied metric. 'TOTAL' can only be combined with 'INSTANCE_CPU_UTILIZATION_AVERAGE'. |
  | scale_in_threshold | False | int |  | The lower threshold for the value of the 'metric'. Used with the `less than` (&lt;) operator. When this value is exceeded, a scale-in action is triggered, specified by the 'scaleInAction' property. The value must have a higher minimum delta to the 'scaleOutThreshold', depending on the 'metric', to avoid competing for actions at the same time. |
  | scale_out_threshold | False | int |  | The upper threshold for the value of the 'metric'. Used with the 'greater than' (&gt;) operator. A scale-out action is triggered when this value is exceeded, specified by the 'scaleOutAction' property. The value must have a lower minimum delta to the 'scaleInThreshold', depending on the metric, to avoid competing for actions simultaneously. If 'properties.policy.unit=TOTAL', a value &gt;= 40 must be chosen. |
  | scale_in_action | False | dict |  | Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is always about removing VMs associated with this VM Auto Scaling Group. By default, the termination policy is 'OLDEST_SERVER_FIRST' is effective. |
  | scale_out_action | False | dict |  | Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, scaling is always about adding new VMs to this VM Auto Scaling Group. |
  | nics | False | list |  | The list of NICs associated with this replica. |
  | volumes | False | list |  | List of volumes associated with this Replica. |
  | availability_zone | False | str |  | The zone where the VMs are created. The availability zone is always automatically set to 'AUTO' for performance reasons. Even if you set another value, e.g. 'null', or leave it empty. |
  | cores | False | str |  | The total number of cores for the VMs. |
  | cpu_family | False | str |  | The CPU family for the VMs created with this configuration. If the value is 'null', the VM is created with the default CPU family for the assigned site. |
  | ram | False | int |  | The size of the memory for the VMs in MB. The size must be in multiples of 256 MB, with a minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at least 1024 MB. If you set the RAM size to more than 240 GB, 'ramHotPlug=FALSE' is fixed. |
  | vm_autoscaling_group | True | str |  | The ID or name of an existing VM Autoscaling Group. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
