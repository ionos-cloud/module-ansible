# network_load_balancer

This is a simple module that supports creating or removing NetworkLoadbalancers. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create Network Load Balancer
    network_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
    register: nlb_response
  

  - name: Update Network Load Balancer
    network_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer: "{{ nlb_response.network_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
      state: update
    register: nlb_response_update
  

  - name: Remove Network Load Balancer
    network_load_balancer:
      network_load_balancer: "{{ nlb_response.network_load_balancer.id }}"
      datacenter: "{{ datacenter_response.datacenter.id }}"
      wait: true
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Network Load Balancer
    network_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      ips:
        - "10.12.118.224"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
    register: nlb_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Network Loadbalancer. |
  | listener_lan | True | str |  | ID of the listening LAN (inbound). |
  | ips | False | list |  | Collection of the Network Load Balancer IP addresses. (Inbound and outbound) IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers. |
  | target_lan | True | str |  | ID of the balanced private target LAN (outbound). |
  | lb_private_ips | False | list |  | Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
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
  
  - name: Remove Network Load Balancer
    network_load_balancer:
      network_load_balancer: "{{ nlb_response.network_load_balancer.id }}"
      datacenter: "{{ datacenter_response.datacenter.id }}"
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Network Loadbalancer. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
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
  
  - name: Update Network Load Balancer
    network_load_balancer:
      datacenter: "{{ datacenter_response.datacenter.id }}"
      network_load_balancer: "{{ nlb_response.network_load_balancer.id }}"
      name: "{{ name }} - UPDATE"
      listener_lan: "{{ listener_lan.lan.id }}"
      target_lan: "{{ target_lan.lan.id }}"
      wait: true
      state: update
    register: nlb_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Network Loadbalancer. |
  | listener_lan | True | str |  | ID of the listening LAN (inbound). |
  | ips | False | list |  | Collection of the Network Load Balancer IP addresses. (Inbound and outbound) IPs of the listenerLan must be customer-reserved IPs for public Load Balancers, and private IPs for private Load Balancers. |
  | target_lan | True | str |  | ID of the balanced private target LAN (outbound). |
  | lb_private_ips | False | list |  | Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
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
