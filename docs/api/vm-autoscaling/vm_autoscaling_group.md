# vm_autoscaling_group

This is a module that supports creating, updating or destroying VM Autoscaling Groups

## Example Syntax


```yaml
- name: Create VM Autoscaling Group
      vm_autoscaling_group:
        datacenter: DatacenterName
        name: TestName
        max_replica_count: 2
        min_replica_count: 1
        metric: "INSTANCE_CPU_UTILIZATION_AVERAGE"
        range: "PT24H"
        unit: "PER_HOUR"
        scale_in_threshold: 33
        scale_out_threshold: 77
        scale_in_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
            termination_policy: 'RANDOM'
            delete_volumes: true
        scale_out_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
        availability_zone: "AUTO"
        cores: 2
        cpu_family: INTEL_XEON
        ram: 1024
        nics: 
            - lan: 1
              name: 'SDK_TEST_NIC1'
              dhcp: true
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 50
              type: 'HDD'
              bus: 'IDE'
              boot_order: 'AUTO'
      register: vm_autoscaling_group_response
  
- name: Update VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ vm_autoscaling_group_response.vm_autoscaling_group.id }}"
        datacenter: DatacenterName2
        name: TestName2
        max_replica_count: 1
        min_replica_count: 0
        metric: "INSTANCE_NETWORK_IN_BYTES"
        range: "PT12H"
        unit: "PER_MINUTE"
        scale_in_threshold: 33
        scale_out_threshold: 86
        scale_in_action:
            amount: 50
            amount_type: 'PERCENTAGE'
            cooldown_period: 'PT10M'
            termination_policy: 'RANDOM'
            delete_volumes: false
        scale_out_action:
            amount: 2
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT15M'
        availability_zone: "AUTO"
        cores: 1
        cpu_family: "INTEL_SKYLAKE"
        ram: 2048
        nics: 
            - lan: 2
              name: 'SDK_TEST_NIC2'
              dhcp: false
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 100
              type: 'SSD'
              bus: 'IDE'
              boot_order: 'AUTO'
        state: update
      register: vm_autoscaling_group_response
  
- name: Remove VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ name }}"
        state: absent
      register: vm_autoscaling_group_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "vm_autoscaling_group": {
        "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66",
        "type": "autoscaling-group",
        "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-10-30T13:53:50.863223+00:00",
            "etag": "UqNMEcSKAhvN4GK+OeBxlYlLs0TS6SBCGvk5HgWgdJk=",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-10-30T13:53:54.378143+00:00",
            "state": "AVAILABLE"
        },
        "properties": {
            "datacenter": {
                "id": "8b8b9122-b8ef-4966-a36a-2e9cf8609121",
                "type": "datacenter",
                "href": "https://api.public.production.k8s.fra2.profitbricks.net/cloudapi/v6/datacenters/8b8b9122-b8ef-4966-a36a-2e9cf8609121"
            },
            "location": "us/las",
            "max_replica_count": 5,
            "min_replica_count": 1,
            "name": "AnsibleVMAutoscalingGroup",
            "policy": {
                "metric": "INSTANCE_CPU_UTILIZATION_AVERAGE",
                "range": "PT24H",
                "scale_in_action": {
                    "amount": 1.0,
                    "amount_type": "ABSOLUTE",
                    "cooldown_period": "PT5M",
                    "termination_policy": "RANDOM",
                    "delete_volumes": true
                },
                "scale_in_threshold": 33.0,
                "scale_out_action": {
                    "amount": 1.0,
                    "amount_type": "ABSOLUTE",
                    "cooldown_period": "PT5M"
                },
                "scale_out_threshold": 77.0,
                "unit": "PER_HOUR"
            },
            "replica_configuration": {
                "availability_zone": "AUTO",
                "cores": 2,
                "cpu_family": "INTEL_XEON",
                "nics": [
                    {
                        "lan": 1,
                        "name": "SDK_TEST_NIC1",
                        "dhcp": true,
                        "firewall_active": null,
                        "firewall_type": null,
                        "flow_logs": [],
                        "firewall_rules": [],
                        "target_group": null
                    },
                    {
                        "lan": 1,
                        "name": "SDK_TEST_NIC2",
                        "dhcp": false,
                        "firewall_active": null,
                        "firewall_type": null,
                        "flow_logs": [],
                        "firewall_rules": [],
                        "target_group": null
                    }
                ],
                "ram": 1024,
                "volumes": [
                    {
                        "image": "b6d8c6f2-febc-11ed-86e8-2e7f0689c849",
                        "image_alias": null,
                        "name": "SDK_TEST_VOLUME",
                        "size": 50,
                        "ssh_keys": [],
                        "type": "HDD",
                        "user_data": null,
                        "bus": "IDE",
                        "backupunit_id": null,
                        "boot_order": "AUTO",
                        "image_password": null
                    }
                ]
            }
        },
        "entities": {
            "actions": {
                "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions",
                "type": "collection",
                "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions"
            },
            "servers": {
                "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/servers",
                "type": "collection",
                "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/servers"
            }
        },
        "started_actions": [
            {
                "id": "4293fe77-1fc5-42e9-aff4-2ed8341c1b0e",
                "type": "autoscaling-action",
                "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions/4293fe77-1fc5-42e9-aff4-2ed8341c1b0e"
            }
        ]
    }
}

```

&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * datacenter 
&nbsp;

# state: **present**
```yaml
  - name: Create VM Autoscaling Group
      vm_autoscaling_group:
        datacenter: DatacenterName
        name: TestName
        max_replica_count: 2
        min_replica_count: 1
        metric: "INSTANCE_CPU_UTILIZATION_AVERAGE"
        range: "PT24H"
        unit: "PER_HOUR"
        scale_in_threshold: 33
        scale_out_threshold: 77
        scale_in_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
            termination_policy: 'RANDOM'
            delete_volumes: true
        scale_out_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
        availability_zone: "AUTO"
        cores: 2
        cpu_family: INTEL_XEON
        ram: 1024
        nics: 
            - lan: 1
              name: 'SDK_TEST_NIC1'
              dhcp: true
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 50
              type: 'HDD'
              bus: 'IDE'
              boot_order: 'AUTO'
      register: vm_autoscaling_group_response
  
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
  <td>max_replica_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The maximum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes.</td>
  </tr>
  <tr>
  <td>min_replica_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The minimum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the VM Auto Scaling Group. This field must not be null or blank.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The VMs for this VM Auto Scaling Description are created in this virtual data center.</td>
  </tr>
  <tr>
  <td>metric<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The metric that triggers the scaling actions. Metric values are checked at fixed intervals.<br />Options: ['INSTANCE_CPU_UTILIZATION_AVERAGE', 'INSTANCE_NETWORK_IN_BYTES', 'INSTANCE_NETWORK_IN_PACKETS', 'INSTANCE_NETWORK_OUT_BYTES', 'INSTANCE_NETWORK_OUT_PACKETS']</td>
  </tr>
  <tr>
  <td>range<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies the time range for which the samples are to be aggregated. Must be &gt;= 2 minutes.</td>
  </tr>
  <tr>
  <td>unit<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The units of the applied metric. 'TOTAL' can only be combined with 'INSTANCE_CPU_UTILIZATION_AVERAGE'.<br />Options: ['PER_HOUR', 'PER_MINUTE', 'PER_SECOND', 'TOTAL']</td>
  </tr>
  <tr>
  <td>scale_in_threshold<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The lower threshold for the value of the 'metric'. Used with the `less than` (&lt;) operator. When this value is exceeded, a scale-in action is triggered, specified by the 'scaleInAction' property. The value must have a higher minimum delta to the 'scaleOutThreshold', depending on the 'metric', to avoid competing for actions at the same time.</td>
  </tr>
  <tr>
  <td>scale_out_threshold<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The upper threshold for the value of the 'metric'. Used with the 'greater than' (&gt;) operator. A scale-out action is triggered when this value is exceeded, specified by the 'scaleOutAction' property. The value must have a lower minimum delta to the 'scaleInThreshold', depending on the metric, to avoid competing for actions simultaneously. If 'properties.policy.unit=TOTAL', a value &gt;= 40 must be chosen.</td>
  </tr>
  <tr>
  <td>scale_in_action<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is always about removing VMs associated with this VM Auto Scaling Group. By default, the termination policy is 'OLDEST_SERVER_FIRST' is effective.</td>
  </tr>
  <tr>
  <td>scale_out_action<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, scaling is always about adding new VMs to this VM Auto Scaling Group.</td>
  </tr>
  <tr>
  <td>nics<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The list of NICs associated with this replica.</td>
  </tr>
  <tr>
  <td>volumes<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of volumes associated with this Replica.</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The zone where the VMs are created. The availability zone is always automatically set to 'AUTO' for performance reasons. Even if you set another value, e.g. 'null', or leave it empty.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The total number of cores for the VMs.</td>
  </tr>
  <tr>
  <td>cpu_family<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The CPU family for the VMs created with this configuration. If the value is 'null', the VM is created with the default CPU family for the assigned site.<br />Options: ['AMD_OPTERON', 'INTEL_SKYLAKE', 'INTEL_XEON']</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>The size of the memory for the VMs in MB. The size must be in multiples of 256 MB, with a minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at least 1024 MB. If you set the RAM size to more than 240 GB, 'ramHotPlug=FALSE' is fixed.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Remove VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ name }}"
        state: absent
      register: vm_autoscaling_group_response
  
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
  <td>vm_autoscaling_group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing VM Autoscaling Group.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ vm_autoscaling_group_response.vm_autoscaling_group.id }}"
        datacenter: DatacenterName2
        name: TestName2
        max_replica_count: 1
        min_replica_count: 0
        metric: "INSTANCE_NETWORK_IN_BYTES"
        range: "PT12H"
        unit: "PER_MINUTE"
        scale_in_threshold: 33
        scale_out_threshold: 86
        scale_in_action:
            amount: 50
            amount_type: 'PERCENTAGE'
            cooldown_period: 'PT10M'
            termination_policy: 'RANDOM'
            delete_volumes: false
        scale_out_action:
            amount: 2
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT15M'
        availability_zone: "AUTO"
        cores: 1
        cpu_family: "INTEL_SKYLAKE"
        ram: 2048
        nics: 
            - lan: 2
              name: 'SDK_TEST_NIC2'
              dhcp: false
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 100
              type: 'SSD'
              bus: 'IDE'
              boot_order: 'AUTO'
        state: update
      register: vm_autoscaling_group_response
  
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
  <td>max_replica_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The maximum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes.</td>
  </tr>
  <tr>
  <td>min_replica_count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The minimum value for the number of replicas for 'targetReplicaCount'. Must be &gt;= 0 and &lt;= 200. Will be enforced for both automatic and manual changes</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the VM Auto Scaling Group. This field must not be null or blank.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The VMs for this VM Auto Scaling Description are created in this virtual data center.</td>
  </tr>
  <tr>
  <td>metric<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The metric that triggers the scaling actions. Metric values are checked at fixed intervals.<br />Options: ['INSTANCE_CPU_UTILIZATION_AVERAGE', 'INSTANCE_NETWORK_IN_BYTES', 'INSTANCE_NETWORK_IN_PACKETS', 'INSTANCE_NETWORK_OUT_BYTES', 'INSTANCE_NETWORK_OUT_PACKETS']</td>
  </tr>
  <tr>
  <td>range<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies the time range for which the samples are to be aggregated. Must be &gt;= 2 minutes.</td>
  </tr>
  <tr>
  <td>unit<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The units of the applied metric. 'TOTAL' can only be combined with 'INSTANCE_CPU_UTILIZATION_AVERAGE'.<br />Options: ['PER_HOUR', 'PER_MINUTE', 'PER_SECOND', 'TOTAL']</td>
  </tr>
  <tr>
  <td>scale_in_threshold<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The lower threshold for the value of the 'metric'. Used with the `less than` (&lt;) operator. When this value is exceeded, a scale-in action is triggered, specified by the 'scaleInAction' property. The value must have a higher minimum delta to the 'scaleOutThreshold', depending on the 'metric', to avoid competing for actions at the same time.</td>
  </tr>
  <tr>
  <td>scale_out_threshold<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The upper threshold for the value of the 'metric'. Used with the 'greater than' (&gt;) operator. A scale-out action is triggered when this value is exceeded, specified by the 'scaleOutAction' property. The value must have a lower minimum delta to the 'scaleInThreshold', depending on the metric, to avoid competing for actions simultaneously. If 'properties.policy.unit=TOTAL', a value &gt;= 40 must be chosen.</td>
  </tr>
  <tr>
  <td>scale_in_action<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is always about removing VMs associated with this VM Auto Scaling Group. By default, the termination policy is 'OLDEST_SERVER_FIRST' is effective.</td>
  </tr>
  <tr>
  <td>scale_out_action<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, scaling is always about adding new VMs to this VM Auto Scaling Group.</td>
  </tr>
  <tr>
  <td>nics<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The list of NICs associated with this replica.</td>
  </tr>
  <tr>
  <td>volumes<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of volumes associated with this Replica.</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The zone where the VMs are created. The availability zone is always automatically set to 'AUTO' for performance reasons. Even if you set another value, e.g. 'null', or leave it empty.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The total number of cores for the VMs.</td>
  </tr>
  <tr>
  <td>cpu_family<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The CPU family for the VMs created with this configuration. If the value is 'null', the VM is created with the default CPU family for the assigned site.<br />Options: ['AMD_OPTERON', 'INTEL_SKYLAKE', 'INTEL_XEON']</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The size of the memory for the VMs in MB. The size must be in multiples of 256 MB, with a minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at least 1024 MB. If you set the RAM size to more than 240 GB, 'ramHotPlug=FALSE' is fixed.</td>
  </tr>
  <tr>
  <td>vm_autoscaling_group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing VM Autoscaling Group.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
