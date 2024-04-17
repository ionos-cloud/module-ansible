# firewall_rule

This module allows you to create, update or remove a firewall rule.

## Example Syntax


```yaml

name: Create a firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  name: SSH
  protocol: ICMPv6
  source_mac: 01:23:45:67:89:00
  ip_version: IPv6
  state: present


name: Update firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  port_range_start: 22
  port_range_end: 23
  state: update


name: Remove firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  wait: true
  wait_timeout: '500'
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
            "source_mac": "<MAC>",
            "target_ip": null,
            "type": null
        },
        "type": "firewall-rule"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create a firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  name: SSH
  protocol: ICMPv6
  source_mac: 01:23:45:67:89:00
  ip_version: IPv6
  state: present

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter name or UUID in which to operate.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The server name or UUID.</td>
  </tr>
  <tr>
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The NIC name or UUID.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The protocol for the rule. Property cannot be modified after it is created (disallowed in update requests).<br />Options: ['TCP', 'UDP', 'ICMP', 'ICMPv6', 'GRE', 'VRRP', 'ESP', 'AH', 'ANY']</td>
  </tr>
  <tr>
  <td>source_mac<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address.</td>
  </tr>
  <tr>
  <td>source_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Only traffic originating from the respective IP address (or CIDR block) is allowed. Value null allows traffic from any IP address (according to the selected ipVersion).</td>
  </tr>
  <tr>
  <td>target_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>If the target NIC has multiple IP addresses, only the traffic directed to the respective IP address (or CIDR block) of the NIC is allowed. Value null allows traffic to any target IP address (according to the selected ipVersion).</td>
  </tr>
  <tr>
  <td>port_range_start<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the start range of the allowed port (from 1 to 65535) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports.</td>
  </tr>
  <tr>
  <td>port_range_end<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the end range of the allowed port (from 1 to 65535) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports.</td>
  </tr>
  <tr>
  <td>icmp_type<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen. Value null allows all types.</td>
  </tr>
  <tr>
  <td>icmp_code<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen. Value null allows all codes.</td>
  </tr>
  <tr>
  <td>ip_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The IP version for this rule. If sourceIp or targetIp are specified, you can omit this value - the IP version will then be deduced from the IP address(es) used; if you specify it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp are specified, this rule allows traffic only for the specified IP version. If neither sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic.<br />Options: ['IPv4', 'IPv6']</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Remove firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  wait: true
  wait_timeout: '500'
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter name or UUID in which to operate.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The server name or UUID.</td>
  </tr>
  <tr>
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The NIC name or UUID.</td>
  </tr>
  <tr>
  <td>firewall_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The Firewall Rule name or UUID.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update firewall rule
ionoscloudsdk.ionoscloud.firewall_rule:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
  firewall_rule: SSH
  port_range_start: 22
  port_range_end: 23
  state: update

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter name or UUID in which to operate.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The server name or UUID.</td>
  </tr>
  <tr>
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The NIC name or UUID.</td>
  </tr>
  <tr>
  <td>firewall_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The Firewall Rule name or UUID.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The protocol for the rule. Property cannot be modified after it is created (disallowed in update requests).<br />Options: ['TCP', 'UDP', 'ICMP', 'ICMPv6', 'GRE', 'VRRP', 'ESP', 'AH', 'ANY']</td>
  </tr>
  <tr>
  <td>source_mac<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows traffic from any MAC address.</td>
  </tr>
  <tr>
  <td>source_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Only traffic originating from the respective IP address (or CIDR block) is allowed. Value null allows traffic from any IP address (according to the selected ipVersion).</td>
  </tr>
  <tr>
  <td>target_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>If the target NIC has multiple IP addresses, only the traffic directed to the respective IP address (or CIDR block) of the NIC is allowed. Value null allows traffic to any target IP address (according to the selected ipVersion).</td>
  </tr>
  <tr>
  <td>port_range_start<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the start range of the allowed port (from 1 to 65535) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports.</td>
  </tr>
  <tr>
  <td>port_range_end<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the end range of the allowed port (from 1 to 65535) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports.</td>
  </tr>
  <tr>
  <td>icmp_type<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the allowed type (from 0 to 254) if the protocol ICMP or ICMPv6 is chosen. Value null allows all types.</td>
  </tr>
  <tr>
  <td>icmp_code<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Defines the allowed code (from 0 to 254) if protocol ICMP or ICMPv6 is chosen. Value null allows all codes.</td>
  </tr>
  <tr>
  <td>ip_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The IP version for this rule. If sourceIp or targetIp are specified, you can omit this value - the IP version will then be deduced from the IP address(es) used; if you specify it anyway, it must match the specified IP address(es). If neither sourceIp nor targetIp are specified, this rule allows traffic only for the specified IP version. If neither sourceIp, targetIp nor ipVersion are specified, this rule will only allow IPv4 traffic.<br />Options: ['IPv4', 'IPv6']</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
