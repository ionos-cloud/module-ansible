# Network Load Balancer Forwarding Rule

## Example Syntax

```text
    - name: Create Network Load Balancer Forwarding Rule
      network_load_balancer_rule:
        name: "{{ name }}"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        listener_ip: "10.12.118.224"
        listener_port: "8081"
        targets:
          - ip: "22.231.2.2"
            port: "8080"
            weight: "123"
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
        wait: true
      register: nlb_forwarding_rule_response

    - name: Update Network Load Balancer Forwarding Rule
      network_load_balancer_rule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
        forwarding_rule_id: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
        name: "{{ name }} - UPDATED"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        wait: true
        state: update
      register: nlb_forwarding_rule_update_response

    - name: Delete Network Load Balancer Forwarding Rule
      network_load_balancer_rule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
        forwarding_rule_id: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
        state: absent
    
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the Network Load Balancer forwarding rule. Required only for state = 'present'. |
| algorithm | **yes**/no  | string |  | Algorithm for the balancing. Accepted values: "ROUND_ROBIN", "LEAST_CONNECTION", "RANDOM", "SOURCE_IP". Required only for state = 'present'. |
| protocol |  **yes**/no | string |  | Protocol of the balancing. Accepted value: "TCP". Required only for state = 'present'. |
| listener_ip |  **yes**/no | string |  | Listening IP. (inbound) Required only for state = 'present'.|
| listener_port | **yes**/no  | string |  | Listening port number. (inbound) (range: 1 to 65535). Required only for state = 'present'. |
| health_check | no | Dict containing: client_timeout, check_timeout, connect_timeout, target_timeout, retries. |  | Health check attributes for Network Load Balancer forwarding rule. |
| targets |  **yes**/no | Dict containing: ip, port, weight, health_check. | | The list of targets. Required only for state = 'present'. |
| datacenter_id | **yes**| string |  | The ID of the datacenter. |
| forwarding_rule_id |**yes**/no | string |  | The ID of the Forwarding Rule. Required when state = 'update' or state = 'absent'. |
| network_load_balancer_id | **yes**| string |  | The ID of the Network Load Balancer. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

