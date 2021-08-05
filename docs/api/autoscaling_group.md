# Datacenter

## Example Syntax

```text
    - name: Create autoscaling group
      autoscaling_group:
        name: ANSIBLE_TEST
        datacenter:
          id: 2284dc16-b284-4826-846a-be283de60216
        template:
          id: "{{ template_response.template.id }}"
        max_replica_count: 5
        min_replica_count: 1
        target_replica_count: 1
        policy:
          metric: INSTANCE_CPU_UTILIZATION_AVERAGE
          range: P1D
          scale_in_action:
            amount: 1
            amount_type: ABSOLUTE
            cooldown_period: 5m
          scale_in_threshold: 33
          scale_out_action:
            amount: 1
            amount_type: ABSOLUTE
            cooldown_period: PT5M
          scale_out_threshold: 77
          unit: PER_HOUR
        wait: true
      register: autoscaling_group_response

    - name: Update autoscaling_group
      autoscaling_group:
        name: ANSIBLE_TEST_UPDATED
        datacenter:
          id: 2284dc16-b284-4826-846a-be283de60216
        template:
          id: "{{ template_response.template.id }}"
        group_id: "{{ autoscaling_group_response.autoscaling_group.id }}"
        max_replica_count: 0
        min_replica_count: 0
        policy:
          metric: INSTANCE_NETWORK_IN_BYTES
          range: P1D
          scale_in_action:
            amount: 1
            amount_type: ABSOLUTE
            cooldown_period: 5m
          scale_in_threshold: 33
          scale_out_action:
            amount: 1
            amount_type: ABSOLUTE
            cooldown_period: PT5M
          scale_out_threshold: 86
          unit: PER_MINUTE
        wait: true
        state: update
      register: updated_autoscaling_group

    - name: Remove autoscaling_group
      autoscaling_group:
        group_id: "{{ autoscaling_group_response.autoscaling_group.id }}"
        state: absent
      register: deleted_autoscaling_group
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | no | string |  | User-defined name for the Autoscaling Group. |
| location | no | string | us/las | Location of the datacenter. This location is the same as the one from the selected template. The location is read only. |
| datacenter | **yes** | string |  | VMs for this Autoscaling Group will be created in this Virtual Datacenter. Please note, that it have the same `location` as the `template`. |
| template | **yes** | string |  | VMs for this Autoscaling Group will be created using this Template. |
| min_replica_count | **yes** | string |  | Minimum replica count value for `targetReplicaCount`. Will be enforced for both automatic and manual changes. |
| max_replica_count | **yes** | string |  | Maximum replica count value for `targetReplicaCount`. Will be enforced for both automatic and manual changes. |
| target_replica_count |  | string |  | The target number of VMs in this Group. Depending on the scaling policy, this number will be adjusted automatically. VMs will be created or destroyed automatically in order to adjust the actual number of VMs to this number. This value can be set only at Group creation time, subsequent change via update (PUT) request is not possible |
| group_id | no | string |  | The ID of the Group. |
| policy | **yes** | string |  | Specifies the behavior of this Autoscaling Group. A policy consists of Triggers and Actions, whereby an Action is some kind of automated behavior, and a Trigger is defined by the circumstances under which the Action is triggered. Currently, two separate Actions, namely Scaling In and Out are supported, triggered through Thresholds defined on a given Metric. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

