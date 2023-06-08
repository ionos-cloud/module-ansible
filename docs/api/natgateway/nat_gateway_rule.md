# nat_gateway_rule

This is a simple module that supports creating or removing NATGateway rules. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      name: RuleName
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: <ip>
      wait: true
    register: nat_gateway_rule_response
  

  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: RuleName
      public_ip: <newIp>
      name: "RuleName - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  

  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: "RuleName - UPDATED"
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "nat_gateway_rule": {
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0/rules/42c85463-5b4f-485e-9e97-47dadc6d37ef",
        "id": "42c85463-5b4f-485e-9e97-47dadc6d37ef",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T11:53:14+00:00",
            "etag": "a0caa44599f8ef081cc93343a66c6738",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T11:53:14+00:00",
            "state": "BUSY"
        },
        "properties": {
            "name": "AnsibleAutoTestNAT",
            "protocol": "TCP",
            "public_ip": "<IP1>",
            "source_subnet": "<SUBNET>",
            "target_port_range": {
                "end": 20000,
                "start": 10000
            },
            "target_subnet": "<SUBNET>",
            "type": "SNAT"
        },
        "type": "natgateway-rule"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      name: RuleName
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      target_subnet: "10.0.1.0"
      target_port_range:
        start: 10000
        end: 20000
      public_ip: <ip>
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
  | public_ip | True | str |  | Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource |
  | target_subnet | False | str |  | Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address. |
  | target_port_range | False | dict |  | Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | nat_gateway | True | str |  | The ID or name of the NAT Gateway. |
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
  
  - name: Delete NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: "RuleName - UPDATED"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway rule. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | nat_gateway | True | str |  | The ID or name of the NAT Gateway. |
  | nat_gateway_rule | True | str |  | The ID or name of the NAT Gateway rule. |
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
  
  - name: Update NAT Gateway Rule
    nat_gateway_rule:
      datacenter: Datacentername
      nat_gateway: NATGatewayName
      nat_gateway_rule: RuleName
      public_ip: <newIp>
      name: "RuleName - UPDATED"
      type: "SNAT"
      protocol: "TCP"
      source_subnet: "10.0.1.0/24"
      wait: true
      state: update
    register: nat_gateway_rule_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway rule. |
  | type | False | str |  | Type of the NAT Gateway rule. |
  | protocol | False | str |  | Protocol of the NAT Gateway rule. Defaults to ALL. If protocol is 'ICMP' then targetPortRange start and end cannot be set. |
  | source_subnet | False | str |  | Source subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets source IP address. |
  | public_ip | False | str |  | Public IP address of the NAT Gateway rule. Specifies the address used for masking outgoing packets source address field. Should be one of the customer reserved IP address already configured on the NAT Gateway resource |
  | target_subnet | False | str |  | Target or destination subnet of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on the packets destination IP address. If none is provided, rule will match any address. |
  | target_port_range | False | dict |  | Target port range of the NAT Gateway rule. For SNAT rules it specifies which packets this translation rule applies to based on destination port. If none is provided, rule will match any port |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | nat_gateway | True | str |  | The ID or name of the NAT Gateway. |
  | nat_gateway_rule | True | str |  | The ID or name of the NAT Gateway rule. |
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
