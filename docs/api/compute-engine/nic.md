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
  | name | True | str |  | The name of the NIC. |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | dhcp | False | bool |  | Boolean value indicating if the NIC is using DHCP or not. |
  | dhcpv6 | False | bool |  | [The IPv6 feature is in beta phase and not ready for production usage.] Indicates if the NIC will reserve an IPv6 using DHCP. It can be set to 'true' or 'false' only if this NIC is connected to an IPv6-enabled LAN. |
  | firewall_active | False | bool |  | Boolean value indicating if the firewall is active. |
  | ips | False | list |  | A list of IPs to be assigned to the NIC. |
  | ipv6_ips | False | list |  | [The IPv6 feature is in beta phase and not ready for production usage.] The IPv6 IP addresses if this NIC is connected to an IPv6-enabled LAN. The maximum number of IPv6 IP addresses per NIC is 50. If you leave this 'null' when adding a NIC, when changing the NIC's IPv6 CIDR block, or when moving the NIC to a different IPv6-enabled LAN, we will automatically assign the new IPv6 CIDR block's first IP address to this NIC. If you leave this 'null' while not changing the CIDR block, the IPv6 IP addresses won't be changed either. You can also provide your own self choosen IPv6 addresses, which then must be inside the IPv6 CIDR block of this NIC. |
  | ipv6_cidr | False | str |  | [The IPv6 feature is in beta phase and not ready for production usage.] The /80 IPv6 CIDR block if this NIC is connected to an IPv6-enabled LAN. If you leave this 'null' when adding a NIC to an IPv6-enabled LAN, an IPv6 block will be automatically assigned to the NIC, but you can also specify an /80 IPv6 CIDR block for the NIC on your own, which then must be inside the IPv6 CIDR block of the LAN. An IPv6-enabled LAN is limited to a maximum of 65,536 NICs. |
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
  | nic | True | str |  | The ID or name of an existing NIC. |
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
  | nic | True | str |  | The ID or name of an existing NIC. |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | lan | False | str |  | The LAN to place the NIC on. You can pass a LAN that doesn't exist and it will be created. Required on create. |
  | dhcp | False | bool |  | Boolean value indicating if the NIC is using DHCP or not. |
  | dhcpv6 | False | bool |  | [The IPv6 feature is in beta phase and not ready for production usage.] Indicates if the NIC will reserve an IPv6 using DHCP. It can be set to 'true' or 'false' only if this NIC is connected to an IPv6-enabled LAN. |
  | firewall_active | False | bool |  | Boolean value indicating if the firewall is active. |
  | ips | False | list |  | A list of IPs to be assigned to the NIC. |
  | ipv6_ips | False | list |  | [The IPv6 feature is in beta phase and not ready for production usage.] The IPv6 IP addresses if this NIC is connected to an IPv6-enabled LAN. The maximum number of IPv6 IP addresses per NIC is 50. If you leave this 'null' when adding a NIC, when changing the NIC's IPv6 CIDR block, or when moving the NIC to a different IPv6-enabled LAN, we will automatically assign the new IPv6 CIDR block's first IP address to this NIC. If you leave this 'null' while not changing the CIDR block, the IPv6 IP addresses won't be changed either. You can also provide your own self choosen IPv6 addresses, which then must be inside the IPv6 CIDR block of this NIC. |
  | ipv6_cidr | False | str |  | [The IPv6 feature is in beta phase and not ready for production usage.] The /80 IPv6 CIDR block if this NIC is connected to an IPv6-enabled LAN. If you leave this 'null' when adding a NIC to an IPv6-enabled LAN, an IPv6 block will be automatically assigned to the NIC, but you can also specify an /80 IPv6 CIDR block for the NIC on your own, which then must be inside the IPv6 CIDR block of the LAN. An IPv6-enabled LAN is limited to a maximum of 65,536 NICs. |
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
