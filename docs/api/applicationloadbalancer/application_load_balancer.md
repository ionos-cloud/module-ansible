# application_load_balancer

This is a simple module that supports creating or removing Application Loadbalancers.

## Example Syntax


```yaml

  - name: Create Application Load Balancer
    application_load_balancer:
      datacenter: DatacenterName
      name:AppLbName
      ips:
        - "10.12.118.224"
      listener_lan: 1
      target_lan: 2
      wait: true
    register: alb_response
  

  - name: Update Application Load Balancer
    application_load_balancer:
      datacenter: DatacenterName
      application_load_balancer: ApplicationLoadBalancerName
      name: "AppLbName - UPDATE"
      listener_lan: 1
      target_lan: 2
      wait: true
      state: update
    register: alb_response_update
  

  - name: Remove Application Load Balancer
    application_load_balancer:
      application_load_balancer: ApplicationLoadBalancerName
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
    "application_load_balancer": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/0c0e3049-ebbd-4465-a766-62f6950c109e/applicationloadbalancers/5c0b9b00-ae36-4626-bff6-e6c30e6d2809",
        "id": "5c0b9b00-ae36-4626-bff6-e6c30e6d2809",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T13:08:28+00:00",
            "etag": "45f17e1cad28dd4973ab127082018599",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T13:08:28+00:00",
            "state": "BUSY"
        },
        "properties": {
            "ips": [
                "<IP>"
            ],
            "lb_private_ips": null,
            "listener_lan": 1,
            "name": "AnsibleAutoTestALB",
            "target_lan": 2
        },
        "type": "applicationloadbalancer"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer
    application_load_balancer:
      datacenter: DatacenterName
      name:AppLbName
      ips:
        - "10.12.118.224"
      listener_lan: 1
      target_lan: 2
      wait: true
    register: alb_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The Application Load Balancer name. |
  | listener_lan | True | str |  | The ID of the listening (inbound) LAN. |
  | ips | False | list |  | Collection of the Application Load Balancer IP addresses. (Inbound and outbound) IPs of the 'listenerLan' are customer-reserved public IPs for the public load balancers, and private IPs for the private load balancers. |
  | target_lan | True | str |  | The ID of the balanced private target LAN (outbound). |
  | lb_private_ips | False | list |  | Collection of private IP addresses with the subnet mask of the Application Load Balancer. IPs must contain valid a subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
  
  - name: Remove Application Load Balancer
    application_load_balancer:
      application_load_balancer: ApplicationLoadBalancerName
      datacenter: DatacenterName
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The Application Load Balancer name. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | application_load_balancer | True | str |  | The ID or name of the Application Loadbalancer. |
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
  
  - name: Update Application Load Balancer
    application_load_balancer:
      datacenter: DatacenterName
      application_load_balancer: ApplicationLoadBalancerName
      name: "AppLbName - UPDATE"
      listener_lan: 1
      target_lan: 2
      wait: true
      state: update
    register: alb_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The Application Load Balancer name. |
  | listener_lan | True | str |  | The ID of the listening (inbound) LAN. |
  | ips | False | list |  | Collection of the Application Load Balancer IP addresses. (Inbound and outbound) IPs of the 'listenerLan' are customer-reserved public IPs for the public load balancers, and private IPs for the private load balancers. |
  | target_lan | True | str |  | The ID of the balanced private target LAN (outbound). |
  | lb_private_ips | False | list |  | Collection of private IP addresses with the subnet mask of the Application Load Balancer. IPs must contain valid a subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | application_load_balancer | True | str |  | The ID or name of the Application Loadbalancer. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
