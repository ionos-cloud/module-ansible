# nat_gateway_rule

This is a simple module that supports creating or removing NATGateway rules. This module has a dependency on ionos-cloud &gt;= 6.0.0

## Example Syntax


```yaml

  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      name: "{{ name }}"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: "{{ ipblock_response.ipblock.properties.ips[0] }}"
      wait: true
    register: nat_gateway_rule_response
  

  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
      public_ip: "{{ ipblock_response.ipblock.properties.ips[1] }}"
      name: "{{ name }} - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  

  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      name: "{{ name }}"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: "{{ ipblock_response.ipblock.properties.ips[0] }}"
      wait: true
    register: nat_gateway_rule_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the NAT Gateway rule. |
  | type | True | str |  | Type of the NAT Gateway rule. |
  | protocol | False | str |  | Protocol of the NAT Gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set. |
  | source_subnet | True | str |  | Source subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets source IP address. |
  | public_ip | True | str |  | Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource. |
  | target_subnet | False | str |  | Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address. |
  | target_port_range | False | str |  | Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | nat_gateway_id | True | str |  | The ID of the NAT Gateway. |
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
  
  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway rule. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | nat_gateway_id | True | str |  | The ID of the NAT Gateway. |
  | nat_gateway_rule_id | False | str |  | The ID of the NAT Gateway rule. |
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
<<<<<<< HEAD
    - name: Create NAT Gateway Rule
      nat_gateway_rule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        name: "{{ name }}"
        type: "SNAT"
        protocol: "TCP"
        source_subnet: "10.0.1.0/24"
        target_subnet: "10.0.1.0"
        target_port_range:
          start: 10000
          end: 20000
        public_ip: "{{ ipblock_response.ipblock.properties.ips[0] }}"
        wait: true
      register: nat_gateway_rule_response

    - name: Update NAT Gateway Rule
      nat_gateway_rule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
        public_ip: "{{ ipblock_response.ipblock.properties.ips[1] }}"
        name: "{{ name }} - UPDATED"
        type: "SNAT"
        protocol: "TCP"
        source_subnet: "10.0.1.0/24"
        wait: true
        state: update
      register: nat_gateway_rule_update_response

    - name: Delete NAT Gateway Rule
      nat_gateway_rule:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
        state: absent
    
=======
  
  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      nat_gateway_rule_id: "{{ nat_gateway_rule_response.nat_gateway_rule.id }}"
      public_ip: "{{ ipblock_response.ipblock.properties.ips[1] }}"
      name: "{{ name }} - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  
>>>>>>> 00db8fa... feat: generate docs (#61)
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway rule. |
  | type | False | str |  | Type of the NAT Gateway rule. |
  | protocol | False | str |  | Protocol of the NAT Gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set. |
  | source_subnet | False | str |  | Source subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets source IP address. |
  | public_ip | False | str |  | Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource. |
  | target_subnet | False | str |  | Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address. |
  | target_port_range | False | str |  | Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | nat_gateway_id | True | str |  | The ID of the NAT Gateway. |
  | nat_gateway_rule_id | False | str |  | The ID of the NAT Gateway rule. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
