# network_load_balancer

This is a simple module that supports creating or removing NetworkLoadbalancers. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create Network Load Balancer
    network_load_balancer:
      datacenter: DatacenterName
      name: NLBName
      ips:
        - "10.12.118.224"
      listener_lan: 1
      target_lan: 2
      wait: true
    register: nlb_response
  

  - name: Update Network Load Balancer
    network_load_balancer:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      name: "NLBName - UPDATE"
      listener_lan: 1
      target_lan: 2
      wait: true
      state: update
    register: nlb_response_update
  

  - name: Remove Network Load Balancer
    network_load_balancer:
      network_load_balancer: "NLBName - UPDATE"
      datacenter: DatacenterName
      wait: true
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
    "network_load_balancer": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/89d7e3e1-a688-4ebd-ab01-8beac27e1f8a/networkloadbalancers/c8fb9d9b-a8ef-4358-a275-c23717aebb51",
        "id": "c8fb9d9b-a8ef-4358-a275-c23717aebb51",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T13:04:34+00:00",
            "etag": "0f37a620e34ca7724e3c53370eddf75e",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T13:04:34+00:00",
            "state": "BUSY"
        },
        "properties": {
            "ips": [
                "<IP>"
            ],
            "lb_private_ips": null,
            "listener_lan": 1,
            "name": "AnsibleAutoTestNLB",
            "target_lan": 2
        },
        "type": "networkloadbalancer"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Network Load Balancer
    network_load_balancer:
      datacenter: DatacenterName
      name: NLBName
      ips:
        - "10.12.118.224"
      listener_lan: 1
      target_lan: 2
      wait: true
    register: nlb_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | True | The name of the Network Load Balancer. |
  | listener_lan<br /><mark style="color:blue;">\<str\></mark> | True | ID of the listening LAN (inbound). |
  | ips<br /><mark style="color:blue;">\<list\></mark> | False | Collection of the Network Load Balancer IP addresses. (Inbound and outbound) IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers. |
  | target_lan<br /><mark style="color:blue;">\<str\></mark> | True | ID of the balanced private target LAN (outbound). |
  | lb_private_ips<br /><mark style="color:blue;">\<list\></mark> | False | Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the datacenter. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Remove Network Load Balancer
    network_load_balancer:
      network_load_balancer: "NLBName - UPDATE"
      datacenter: DatacenterName
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | False | The name of the Network Load Balancer. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the Network Loadbalancer. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Network Load Balancer
    network_load_balancer:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      name: "NLBName - UPDATE"
      listener_lan: 1
      target_lan: 2
      wait: true
      state: update
    register: nlb_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | True | The name of the Network Load Balancer. |
  | listener_lan<br /><mark style="color:blue;">\<str\></mark> | True | ID of the listening LAN (inbound). |
  | ips<br /><mark style="color:blue;">\<list\></mark> | False | Collection of the Network Load Balancer IP addresses. (Inbound and outbound) IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers. |
  | target_lan<br /><mark style="color:blue;">\<str\></mark> | True | ID of the balanced private target LAN (outbound). |
  | lb_private_ips<br /><mark style="color:blue;">\<list\></mark> | False | Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the Network Loadbalancer. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
