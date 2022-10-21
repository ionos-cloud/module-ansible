# nat_gateway

This is a simple module that supports creating or removing NATGateways. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create NAT Gateway
    nat_gateway:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      public_ips: "{{ ipblock_response_create.ipblock.properties.ips }}"
      lans:
        - id: "{{ lan_response.lan.id }}"
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  

  - name: Update NAT Gateway
    nat_gateway:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }} - UPDATED"
      public_ips: "{{ ipblock_response_update.ipblock.properties.ips }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      wait: true
      state: update
    register: nat_gateway_response_update
  

  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      wait: true
      wait_timeout: 2000
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create NAT Gateway
    nat_gateway:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }}"
      public_ips: "{{ ipblock_response_create.ipblock.properties.ips }}"
      lans:
        - id: "{{ lan_response.lan.id }}"
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the NAT Gateway. |
  | public_ips | True | list |  | Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location. |
  | lans | False | list |  | Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
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
  
  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      wait: true
      wait_timeout: 2000
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | nat_gateway_id | False | str |  | The ID of the NAT Gateway. |
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
  
  - name: Update NAT Gateway
    nat_gateway:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      name: "{{ name }} - UPDATED"
      public_ips: "{{ ipblock_response_update.ipblock.properties.ips }}"
      nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
      wait: true
      state: update
    register: nat_gateway_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NAT Gateway. |
  | public_ips | False | list |  | Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location. |
  | lans | False | list |  | Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | nat_gateway_id | False | str |  | The ID of the NAT Gateway. |
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
