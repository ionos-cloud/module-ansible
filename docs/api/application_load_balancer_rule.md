# Application Load Balancer Forwarding Rule

## Example Syntax

```text
    - name: Create Application Load Balancer Forwarding Rule
      application_load_balancer_forwardingrule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
        name: "{{ name }}"
        protocol: "HTTP"
        listener_ip: "10.12.118.224"
        listener_port: "8081"
        health_check:
          client_timeout: 50
        http_rules:
          - name: "Ansible HTTP Rule"
            type : static
            response_message: "<>"
            content_type: "application/json"
            conditions:
              - type: "HEADER"
                condition: "STARTS_WITH"
                value: "Friday"

        wait: true
      register: alb_forwarding_rule_response

    - name: Update Application Load Balancer Forwarding Rule
      application_load_balancer_forwardingrule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
        forwarding_rule_id: "{{ alb_forwarding_rule_response.forwarding_rule.id }}"
        name: "{{ name }} - UPDATED"
        protocol: "HTTP"
        wait: true
        state: update
      register: alb_forwarding_rule_update_response


    - name: Delete Application Load Balancer Forwarding Rule
      application_load_balancer_forwardingrule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
        forwarding_rule_id: "{{ alb_forwarding_rule_response.forwarding_rule.id }}"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the Application Load Balancer forwarding rule. Required only for state = 'present'. |
| protocol |  **yes**/no | string |  | Protocol of the balancing. Accepted value: "TCP". Required only for state = 'present'. |
| listener_ip |  **yes**/no | string |  | Listening IP. (inbound) Required only for state = 'present'.|
| listener_port | **yes**/no  | string |  | Listening port number. (inbound) (range: 1 to 65535). Required only for state = 'present'. |
| health_check | no | Dict containing: client_timeout. |  | Health check attributes for Application Load Balancer forwarding rule. |
| server_certificates | no | List |  | List of the server certificates. |
| http_rules | no | List of Http Rules. A Http Rule contains: name, type, target_group, drop_query, location, status_code, response_message, content_type and conditions. |  | Health check attributes for Application Load Balancer forwarding rule. |
| datacenter_id | **yes**| string |  | The ID of the datacenter. |
| forwarding_rule_id |**yes**/no | string |  | The ID of the Forwarding Rule. Required when state = 'update' or state = 'absent'. |
| application_load_balancer_id | **yes**| string |  | The ID of the Application Load Balancer. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

