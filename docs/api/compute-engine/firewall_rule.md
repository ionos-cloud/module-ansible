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
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "firewall_rule": {
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/nics/6e9dd9af-5132-4f8d-a285-62c86956a5da/firewallrules/d48500c7-3483-455b-9f63-9c091a9c73a2",
        "id": "d48500c7-3483-455b-9f63-9c091a9c73a2",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T09:29:40+00:00",
            "etag": "de89018f9d0664828d9170c632db291a",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T09:29:40+00:00",
            "state": "BUSY"
        },
        "properties": {
            "icmp_code": null,
            "icmp_type": null,
            "ip_version": null,
            "name": "SSH",
            "port_range_end": 24,
            "port_range_start": 22,
            "protocol": "TCP",
            "source_ip": null,
            "source_mac": "01:23:45:67:89:00",
            "target_ip": null,
            "type": null
        },
        "type": "firewall-rule"
    }
}

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter name or UUID in which to operate. |
  | server<br /><span class="blue-span">str</span> | True | The server name or UUID. |
  | nic<br /><span class="blue-span">str</span> | True | The NIC name or UUID. |
  | name<br /><span class="blue-span">str</span> | True | The name of the  resource. |
  | protocol<br /><span class="blue-span">str</span> | True | The protocol for the rule. Property cannot be modified after it is created (disallowed in update requests).<br />Options: ['TCP', 'UDP', 'ICMP', 'ICMPv6', 'ANY'] |
  | source_mac<br /><span class="blue-span">str</span> | False | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address. |
  | source_ip<br /><span class="blue-span">str</span> | False | Only traffic originating from the respective IP address (or CIDR block) is allowed. Value null allows traffic from any IP address (according to the selected ipVersion). |
  | target_ip<br /><span class="blue-span">str</span> | False | If the target NIC has multiple IP addresses, only the traffic directed to the respective IP address (or CIDR block) of the NIC is allowed. Value null allows traffic to any target IP address (according to the selected ipVersion). |
  | port_range_start<br /><span class="blue-span">int</span> | False | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports. |
  | port_range_end<br /><span class="blue-span">int</span> | False | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports. |
  | icmp_type<br /><span class="blue-span">int</span> | False | Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen. Value null allows all types. |
  | icmp_code<br /><span class="blue-span">int</span> | False | Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen. Value null allows all codes. |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span class="blue-span">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter name or UUID in which to operate. |
  | server<br /><span class="blue-span">str</span> | True | The server name or UUID. |
  | nic<br /><span class="blue-span">str</span> | True | The NIC name or UUID. |
  | firewall_rule<br /><span class="blue-span">str</span> | True | The Firewall Rule name or UUID. |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span class="blue-span">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter name or UUID in which to operate. |
  | server<br /><span class="blue-span">str</span> | True | The server name or UUID. |
  | nic<br /><span class="blue-span">str</span> | True | The NIC name or UUID. |
  | firewall_rule<br /><span class="blue-span">str</span> | True | The Firewall Rule name or UUID. |
  | name<br /><span class="blue-span">str</span> | False | The name of the  resource. |
  | protocol<br /><span class="blue-span">str</span> | False | The protocol for the rule. Property cannot be modified after it is created (disallowed in update requests).<br />Options: ['TCP', 'UDP', 'ICMP', 'ICMPv6', 'ANY'] |
  | source_mac<br /><span class="blue-span">str</span> | False | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address. |
  | source_ip<br /><span class="blue-span">str</span> | False | Only traffic originating from the respective IP address (or CIDR block) is allowed. Value null allows traffic from any IP address (according to the selected ipVersion). |
  | target_ip<br /><span class="blue-span">str</span> | False | If the target NIC has multiple IP addresses, only the traffic directed to the respective IP address (or CIDR block) of the NIC is allowed. Value null allows traffic to any target IP address (according to the selected ipVersion). |
  | port_range_start<br /><span class="blue-span">int</span> | False | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports. |
  | port_range_end<br /><span class="blue-span">int</span> | False | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports. |
  | icmp_type<br /><span class="blue-span">int</span> | False | Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen. Value null allows all types. |
  | icmp_code<br /><span class="blue-span">int</span> | False | Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen. Value null allows all codes. |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span class="blue-span">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
