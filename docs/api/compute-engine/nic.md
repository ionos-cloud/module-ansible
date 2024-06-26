# nic

This module allows you to create, update or remove a NIC.

## Example Syntax


```yaml

name: Create NIC
ionoscloudsdk.ionoscloud.nic:
  name: 'AnsibleAutoTestCompute'
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  lan: 2
  dhcp: true
  firewall_active: true
  ips:
  - 10.0.0.1
  wait: true
  wait_timeout: '500'
  state: present
register: ionos_cloud_nic


name: Update NIC
ionoscloudsdk.ionoscloud.nic:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  name: new-nic
  nic: ''
  dhcp: false
  wait: true
  wait_timeout: '500'
  state: update
register: updated_nic


name: Remove NIC
ionoscloudsdk.ionoscloud.nic:
  nic: ''
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
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
    "nic": {
        "entities": {
            "firewallrules": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/nics/6e9dd9af-5132-4f8d-a285-62c86956a5da/firewallrules",
                "id": "6e9dd9af-5132-4f8d-a285-62c86956a5da/firewallrules",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "flowlogs": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/nics/6e9dd9af-5132-4f8d-a285-62c86956a5da/flowlogs",
                "id": "6e9dd9af-5132-4f8d-a285-62c86956a5da/flowlogs",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            }
        },
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/nics/6e9dd9af-5132-4f8d-a285-62c86956a5da",
        "id": "6e9dd9af-5132-4f8d-a285-62c86956a5da",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T09:27:48+00:00",
            "etag": "758f25397e05ac5dace2c18fa851879e",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T09:27:48+00:00",
            "state": "AVAILABLE"
        },
        "properties": {
            "device_number": null,
            "dhcp": true,
            "firewall_active": true,
            "firewall_type": "INGRESS",
            "ips": [
                "<IP>"
            ],
            "lan": 1,
            "mac": "<MAC>",
            "name": "AnsibleAutoTestCompute",
            "pci_slot": 6
        },
        "type": "nic"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create NIC
ionoscloudsdk.ionoscloud.nic:
  name: 'AnsibleAutoTestCompute'
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  lan: 2
  dhcp: true
  firewall_active: true
  ips:
  - 10.0.0.1
  wait: true
  wait_timeout: '500'
  state: present
register: ionos_cloud_nic

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
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the  resource.</td>
  </tr>
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
  <td>lan<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The LAN ID the NIC will be on. If the LAN ID does not exist, it will be implicitly created.</td>
  </tr>
  <tr>
  <td>dhcp<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the NIC will reserve an IP using DHCP.</td>
  </tr>
  <tr>
  <td>dhcpv6<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the NIC will receive an IPv6 using DHCP. It can be set to 'true' or 'false' only if this NIC is connected to an IPv6 enabled LAN.</td>
  </tr>
  <tr>
  <td>firewall_active<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activate or deactivate the firewall. By default, an active firewall without any defined rules will block all incoming network traffic except for the firewall rules that explicitly allows certain protocols, IP addresses and ports.</td>
  </tr>
  <tr>
  <td>ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Collection of IP addresses, assigned to the NIC. Explicitly assigned public IPs need to come from reserved IP blocks. Passing value null or empty array will assign an IP address automatically.</td>
  </tr>
  <tr>
  <td>ipv6_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>If this NIC is connected to an IPv6 enabled LAN then this property contains the IPv6 IP addresses of the NIC. The maximum number of IPv6 IP addresses per NIC is 50, if you need more, contact support. If you leave this property 'null' when adding a NIC, when changing the NIC's IPv6 CIDR block, when changing the LAN's IPv6 CIDR block or when moving the NIC to a different IPv6 enabled LAN, then we will automatically assign the same number of IPv6 addresses which you had before from the NICs new CIDR block. If you leave this property 'null' while not changing the CIDR block, the IPv6 IP addresses won't be changed either. You can also provide your own self choosen IPv6 addresses, which then must be inside the IPv6 CIDR block of this NIC.</td>
  </tr>
  <tr>
  <td>ipv6_cidr<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>If this NIC is connected to an IPv6 enabled LAN then this property contains the /80 IPv6 CIDR block of the NIC. If you leave this property 'null' when adding a NIC to an IPv6-enabled LAN, then an IPv6 CIDR block will automatically be assigned to the NIC, but you can also specify an /80 IPv6 CIDR block for the NIC on your own, which must be inside the /64 IPv6 CIDR block of the LAN and unique. This value can only be set, if the LAN already has an IPv6 CIDR block assigned. An IPv6-enabled LAN is limited to a maximum of 65,536 NICs.</td>
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
  
name: Remove NIC
ionoscloudsdk.ionoscloud.nic:
  nic: ''
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
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
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing NIC.</td>
  </tr>
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
  
name: Update NIC
ionoscloudsdk.ionoscloud.nic:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  name: new-nic
  nic: ''
  dhcp: false
  wait: true
  wait_timeout: '500'
  state: update
register: updated_nic

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
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing NIC.</td>
  </tr>
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
  <td>lan<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The LAN ID the NIC will be on. If the LAN ID does not exist, it will be implicitly created.</td>
  </tr>
  <tr>
  <td>dhcp<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the NIC will reserve an IP using DHCP.</td>
  </tr>
  <tr>
  <td>dhcpv6<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the NIC will receive an IPv6 using DHCP. It can be set to 'true' or 'false' only if this NIC is connected to an IPv6 enabled LAN.</td>
  </tr>
  <tr>
  <td>firewall_active<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Activate or deactivate the firewall. By default, an active firewall without any defined rules will block all incoming network traffic except for the firewall rules that explicitly allows certain protocols, IP addresses and ports.</td>
  </tr>
  <tr>
  <td>ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Collection of IP addresses, assigned to the NIC. Explicitly assigned public IPs need to come from reserved IP blocks. Passing value null or empty array will assign an IP address automatically.</td>
  </tr>
  <tr>
  <td>ipv6_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>If this NIC is connected to an IPv6 enabled LAN then this property contains the IPv6 IP addresses of the NIC. The maximum number of IPv6 IP addresses per NIC is 50, if you need more, contact support. If you leave this property 'null' when adding a NIC, when changing the NIC's IPv6 CIDR block, when changing the LAN's IPv6 CIDR block or when moving the NIC to a different IPv6 enabled LAN, then we will automatically assign the same number of IPv6 addresses which you had before from the NICs new CIDR block. If you leave this property 'null' while not changing the CIDR block, the IPv6 IP addresses won't be changed either. You can also provide your own self choosen IPv6 addresses, which then must be inside the IPv6 CIDR block of this NIC.</td>
  </tr>
  <tr>
  <td>ipv6_cidr<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>If this NIC is connected to an IPv6 enabled LAN then this property contains the /80 IPv6 CIDR block of the NIC. If you leave this property 'null' when adding a NIC to an IPv6-enabled LAN, then an IPv6 CIDR block will automatically be assigned to the NIC, but you can also specify an /80 IPv6 CIDR block for the NIC on your own, which must be inside the /64 IPv6 CIDR block of the LAN and unique. This value can only be set, if the LAN already has an IPv6 CIDR block assigned. An IPv6-enabled LAN is limited to a maximum of 65,536 NICs.</td>
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
