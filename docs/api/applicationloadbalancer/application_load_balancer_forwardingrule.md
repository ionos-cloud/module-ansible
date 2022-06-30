# application_load_balancer_forwardingrule

This is a simple module that supports creating or removing Application Loadbalancer Flowlog rules.

## Example Syntax


```yaml

  - name: Create Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }}"
      protocol: "HTTP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
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
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }}"
      protocol: "HTTP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
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
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Application Load Balancer forwarding rule. |
  | algorithm | False | str |  | Balancing algorithm. |
  | protocol | True | str |  | Balancing protocol. |
  | listener_ip | True | str |  | Listening (inbound) IP. |
  | listener_port | True | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | client_timeout | False | int |  | The maximum time in milliseconds to wait for the client to acknowledge or send data; default is 50,000 (50 seconds). |
  | http_rules | False | list |  | An array of items in the collection. The original order of rules is perserved during processing, except for Forward-type rules are processed after the rules with other action defined. The relative order of Forward-type rules is also preserved during the processing. |
  | server_certificates | False | list |  | An array of items in the collection. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      forwarding_rule_id: "{{ alb_forwarding_rule_response.forwarding_rule.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Application Load Balancer forwarding rule. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | forwarding_rule_id | False | str |  | The ID of the Application Loadbalancer forwarding rule. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
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
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Application Load Balancer forwarding rule. |
  | algorithm | False | str |  | Balancing algorithm. |
  | protocol | False | str |  | Balancing protocol. |
  | listener_ip | False | str |  | Listening (inbound) IP. |
  | listener_port | False | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | client_timeout | False | int |  | The maximum time in milliseconds to wait for the client to acknowledge or send data; default is 50,000 (50 seconds). |
  | http_rules | False | list |  | An array of items in the collection. The original order of rules is perserved during processing, except for Forward-type rules are processed after the rules with other action defined. The relative order of Forward-type rules is also preserved during the processing. |
  | server_certificates | False | list |  | An array of items in the collection. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | forwarding_rule_id | False | str |  | The ID of the Application Loadbalancer forwarding rule. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
