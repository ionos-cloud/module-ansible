# network_load_balancer_rule

This is a simple module that supports creating or removing NATGateway Flowlog rules. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      name: RuleName
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      targets:
        - ip: "22.231.2.2"
          port: "8080"
          weight: "123"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_forwarding_rule_response
  

  - name: Update Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      wait: true
      state: update
    register: nlb_forwarding_rule_update_response
  

  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: "RuleName - UPDATED"
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
    "forwarding_rule": {
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/89d7e3e1-a688-4ebd-ab01-8beac27e1f8a/networkloadbalancers/c8fb9d9b-a8ef-4358-a275-c23717aebb51/forwardingrules/6dec4e0c-dd8d-4348-acd1-2d0bf16d00e2",
        "id": "6dec4e0c-dd8d-4348-acd1-2d0bf16d00e2",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T13:08:44+00:00",
            "etag": "fb2a7f7680346fe0677dc3d76d652be6",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T13:08:44+00:00",
            "state": "BUSY"
        },
        "properties": {
            "algorithm": "ROUND_ROBIN",
            "health_check": {
                "client_timeout": 50,
                "connect_timeout": 5000,
                "retries": 1,
                "target_timeout": 5000
            },
            "listener_ip": "<IP>",
            "listener_port": 8081,
            "name": "AnsibleAutoTestNLB",
            "protocol": "TCP",
            "targets": [
                {
                    "health_check": null,
                    "ip": "<IP>",
                    "port": 8080,
                    "weight": 123
                }
            ]
        },
        "type": "forwarding-rule"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      name: RuleName
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      targets:
        - ip: "22.231.2.2"
          port: "8080"
          weight: "123"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_forwarding_rule_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Network Load Balancer forwarding rule. |
  | algorithm | True | str |  | Balancing algorithm |
  | protocol | True | str |  | Balancing protocol |
  | listener_ip | True | str |  | Listening (inbound) IP. |
  | listener_port | True | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check | False | dict |  | Health check properties for Network Load Balancer forwarding rule. |
  | targets | True | list |  | Array of items in the collection. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
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
  
  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: "RuleName - UPDATED"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Network Load Balancer forwarding rule. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
  | forwarding_rule | True | str |  | The ID or name of the Network Loadbalancer forwarding rule. |
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
  
  - name: Update Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
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
  | name | False | str |  | The name of the Network Load Balancer forwarding rule. |
  | algorithm | False | str |  | Balancing algorithm |
  | protocol | False | str |  | Balancing protocol |
  | listener_ip | False | str |  | Listening (inbound) IP. |
  | listener_port | False | str |  | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check | False | dict |  | Health check properties for Network Load Balancer forwarding rule. |
  | targets | False | list |  | Array of items in the collection. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
  | forwarding_rule | True | str |  | The ID or name of the Network Loadbalancer forwarding rule. |
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
