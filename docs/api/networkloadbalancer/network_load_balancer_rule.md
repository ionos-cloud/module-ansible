# network_load_balancer_rule

This is a simple module that supports creating or removing NATGateway Flowlogs. This module has a dependency on ionos-cloud &gt;= 6.0.0

## Example Syntax


```yaml

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
&nbsp;

&nbsp;

# state: **present**
```yaml
  
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
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Network Loadbalancer forwarding rule. |
  | algorithm | True | str |  | Balancing algorithm. |
  | protocol | True | str |  | Balancing protocol. |
  | listener_ip | True | str |  | Listening (inbound) IP. |
  | listener_port | True | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check | True | dict |  | Health check properties for Network Load Balancer forwarding rule. |
  | targets | True | list |  | Array of targets. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | network_load_balancer_id | True | str |  | The ID of the Network Loadbalancer. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
      forwarding_rule_id: "{{ nlb_forwarding_rule_response.forwarding_rule.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Network Loadbalancer forwarding rule. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | network_load_balancer_id | True | str |  | The ID of the Network Loadbalancer. |
  | forwarding_rule_id | False | str |  | The ID of the Network Loadbalancer forwarding rule. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
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
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Network Loadbalancer forwarding rule. |
  | algorithm | False | str |  | Balancing algorithm. |
  | protocol | False | str |  | Balancing protocol. |
  | listener_ip | False | str |  | Listening (inbound) IP. |
  | listener_port | False | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check | False | dict |  | Health check properties for Network Load Balancer forwarding rule. |
  | targets | False | list |  | Array of targets. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | network_load_balancer_id | True | str |  | The ID of the Network Loadbalancer. |
  | forwarding_rule_id | False | str |  | The ID of the Network Loadbalancer forwarding rule. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
