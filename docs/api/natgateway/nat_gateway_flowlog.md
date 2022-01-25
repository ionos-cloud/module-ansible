# NAT Gateway Flowlog

## Example Syntax

```yaml
    - name: Create NAT Gateway Flowlog
      nat_gateway_flowlog:
        name: "{{ name }}"
        action: "ACCEPTED"
        direction: "INGRESS"
        bucket: "sdktest"
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        wait: true
      register: nat_gateway_flowlog_response

    - name: Update NAT Gateway Flowlog
      nat_gateway_flowlog:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        flowlog_id: "{{ nat_gateway_flowlog_response.flowlog.id }}"
        name: "{{ name }}"
        action: "ALL"
        direction: "INGRESS"
        bucket: "sdktest"
        wait: true
        state: update
      register: nat_gateway_flowlog_update_response

    - name: Delete NAT Gateway Flowlog
      nat_gateway_flowlog:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        flowlog_id: "{{ nat_gateway_flowlog_response.flowlog.id }}"
        state: absent
    
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the Flowlog. Required only for state = 'present'. |
| action | **yes**/no | string |  | Specifies the traffic action pattern. Accepted values: "ACCEPTED", "REJECTED" or "ALL". Required only for state = 'present'.|
| direction | **yes**/no | string |  | Specifies the traffic direction pattern. Accepted values: "INGRESS", "EGRESS", "BIDIRECTIONAL". Required only for state = 'present'. |
| bucket | **yes**/no | string |  | S3 bucket name of an existing IONOS Cloud S3 bucket. Required only for state = 'present'. |
| datacenter_id | **yes** | string |  | The ID of the datacenter. |
| server_id | **yes** | string |  | The ID of the server. |
| flowlog_id | **yes**/no | string |  | The ID of the flowlog. Required when state = 'update' or state = 'absent'.|
| nat_gateway_id | **yes** | string |  | The ID of the NAT Gateway. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

