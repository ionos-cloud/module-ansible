# NAT Gateway Rule

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

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the NAT gateway rule. Required only for state = 'present'.|
| type | no | string |  | The type of the NAT gateway rule. Accepted values: "SNAT". |
| protocol | no | string |  | Protocol of the NAT gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set. Accepted values: "TCP", "UDP","ICMP", "ALL". |
| source_subnet | **yes**/no | string |  | Source subnet of the NAT gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets source IP address. Required only for state = 'present'. |
| public_ip | **yes**/no | string |  | Public IP address of the NAT gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT gateway resource. Required only for state = 'present'. |
| target_subnet | no | string |  | Target or destination subnet of the NAT gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address. |
| target_port_range | no | Dict containing: 'start' and 'end'. |  | Target port range of the NAT gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port|
| datacenter_id | **yes** | string |  | The ID of the datacenter. |
| nat_gateway_id | **yes** | string |  | The ID of the NAT Gateway. |
| nat_gateway_rule_id | **yes**/no | string |  | The ID of the NAT Gateway Rule. Required when state = 'update' or state = 'absent'.|
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

