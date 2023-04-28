# firewall_rule

This module allows you to create, update or remove a firewall rule.

## Example Syntax


```yaml
# Create a firewall rule
- name: Create SSH firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow SSH
    protocol: TCP
    source_ip: 0.0.0.0
    port_range_start: 22
    port_range_end: 22
    state: present

- name: Create ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow Ping
    protocol: ICMP
    source_ip: 0.0.0.0
    icmp_type: 8
    icmp_code: 0
    state: present
  
# Update a firewall rule
- name: Allow SSH access
  firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update
  
# Remove a firewall rule
- name: Remove public ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: aa6c261b9c
    name: Allow Ping
    state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a firewall rule
- name: Create SSH firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow SSH
    protocol: TCP
    source_ip: 0.0.0.0
    port_range_start: 22
    port_range_end: 22
    state: present

- name: Create ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: 7341c2454f
    name: Allow Ping
    protocol: ICMP
    source_ip: 0.0.0.0
    icmp_type: 8
    icmp_code: 0
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | nic | True | str |  | The NIC name or UUID. |
  | name | True | str |  | The name or UUID of the firewall rule. |
  | protocol | True | str |  | The protocol for the firewall rule. |
  | source_mac | False | str |  | Only traffic originating from the respective MAC address is allowed. No value allows all source MAC addresses. |
  | source_ip | False | str |  | Only traffic originating from the respective IPv4 address is allowed. No value allows all source IPs. |
  | target_ip | False | str |  | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed.No value allows all target IPs. |
  | port_range_start | False | int |  | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave value empty to allow all ports. |
  | port_range_end | False | int |  | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave value empty to allow all ports. |
  | icmp_type | False | int |  | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. No value allows all types. |
  | icmp_code | False | int |  | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. No value allows all codes. |
  | ip_version | False | str |  | The IP version for this rule. If sourceIp or targetIp are specified, you can omit this value - the IP version will then be deduced from the IP address(es) used; if you specify it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp are specified, this rule allows traffic only for the specified IP version. If neither sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic. |
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
  # Remove a firewall rule
- name: Remove public ping firewall rule
  firewall_rule:
    datacenter: Virtual Datacenter
    server: node001
    nic: aa6c261b9c
    name: Allow Ping
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | nic | True | str |  | The NIC name or UUID. |
  | name | True | str |  | The name or UUID of the firewall rule. |
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
  # Update a firewall rule
- name: Allow SSH access
  firewall_rule:
      datacenter: Virtual Datacenter
      server: node001
      nic: 7341c2454f
      name: Allow Ping
      source_ip: 162.254.27.217
      source_mac: 01:23:45:67:89:00
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | server | True | str |  | The server name or UUID. |
  | nic | True | str |  | The NIC name or UUID. |
  | name | True | str |  | The name or UUID of the firewall rule. |
  | protocol | False | str |  | The protocol for the firewall rule. |
  | source_mac | False | str |  | Only traffic originating from the respective MAC address is allowed. No value allows all source MAC addresses. |
  | source_ip | False | str |  | Only traffic originating from the respective IPv4 address is allowed. No value allows all source IPs. |
  | target_ip | False | str |  | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed.No value allows all target IPs. |
  | port_range_start | False | int |  | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave value empty to allow all ports. |
  | port_range_end | False | int |  | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave value empty to allow all ports. |
  | icmp_type | False | int |  | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. No value allows all types. |
  | icmp_code | False | int |  | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. No value allows all codes. |
  | ip_version | False | str |  | The IP version for this rule. If sourceIp or targetIp are specified, you can omit this value - the IP version will then be deduced from the IP address(es) used; if you specify it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp are specified, this rule allows traffic only for the specified IP version. If neither sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic. |
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
