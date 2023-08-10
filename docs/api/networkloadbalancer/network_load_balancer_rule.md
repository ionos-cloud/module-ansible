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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | True | The name of the Network Load Balancer forwarding rule. |
  | algorithm<br /><span style="color:blue">\<str\></span> | True | Balancing algorithm |
  | protocol<br /><span style="color:blue">\<str\></span> | True | Balancing protocol |
  | listener_ip<br /><span style="color:blue">\<str\></span> | True | Listening (inbound) IP. |
  | listener_port<br /><span style="color:blue">\<str\></span> | True | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check<br /><span style="color:blue">\<dict\></span> | False | Health check properties for Network Load Balancer forwarding rule. |
  | targets<br /><span style="color:blue">\<list\></span> | True | Array of items in the collection. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the Network Load Balancer forwarding rule. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | forwarding_rule<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Network Loadbalancer forwarding rule. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the Network Load Balancer forwarding rule. |
  | algorithm<br /><span style="color:blue">\<str\></span> | False | Balancing algorithm |
  | protocol<br /><span style="color:blue">\<str\></span> | False | Balancing protocol |
  | listener_ip<br /><span style="color:blue">\<str\></span> | False | Listening (inbound) IP. |
  | listener_port<br /><span style="color:blue">\<str\></span> | False | Listening (inbound) port number; valid range is 1 to 65535. |
  | health_check<br /><span style="color:blue">\<dict\></span> | False | Health check properties for Network Load Balancer forwarding rule. |
  | targets<br /><span style="color:blue">\<list\></span> | False | Array of items in the collection. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | forwarding_rule<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Network Loadbalancer forwarding rule. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
