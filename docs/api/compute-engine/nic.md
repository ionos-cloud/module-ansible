# nic

This module allows you to create, update or remove a NIC.

## Example Syntax


```yaml
# Create a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    lan: 2
    wait_timeout: 500
    state: present
  
# Update a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    lan: 1
    ips:
      - 158.222.103.23
      - 158.222.103.24
    dhcp: false
    state: update
  
# Remove a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    wait_timeout: 500
    state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    lan: 2
    wait_timeout: 500
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NIC. |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | dhcp | False | bool |  | Boolean value indicating if the NIC is using DHCP or not. |
  | firewall_active | False | bool |  | Boolean value indicating if the firewall is active. |
  | ips | False | list |  | A list of IPs to be assigned to the NIC. |
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
  # Remove a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    wait_timeout: 500
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the NIC. |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
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
  # Update a NIC
  - nic:
    datacenter: Tardis One
    server: node002
    name: 7341c2454f
    lan: 1
    ips:
      - 158.222.103.23
      - 158.222.103.24
    dhcp: false
    state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the NIC. |
  | id | False | str |  | The ID of the NIC. |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | lan | False | str |  | The LAN to place the NIC on. You can pass a LAN that doesn't exist and it will be created. Required on create. |
  | dhcp | False | bool |  | Boolean value indicating if the NIC is using DHCP or not. |
  | firewall_active | False | bool |  | Boolean value indicating if the firewall is active. |
  | ips | False | list |  | A list of IPs to be assigned to the NIC. |
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
