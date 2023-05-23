# application_load_balancer

This is a simple module that supports creating or removing Application Loadbalancers.

## Example Syntax


```yaml

  - name: Create Application Load Balancer
    application_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
    register: alb_response
  

  - name: Update Application Load Balancer
    application_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
      state: update
    register: alb_response_update
  

  - name: Remove Application Load Balancer
    application_load_balancer:
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      datacenter: "{{ datacenter_response.datacenter.id }}"
      wait: true
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer
    application_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
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
  
  - name: Remove Application Load Balancer
    application_load_balancer:
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      datacenter: "{{ datacenter_response.datacenter.id }}"
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
      datacenter: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer: "{{ alb_response.application_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
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
