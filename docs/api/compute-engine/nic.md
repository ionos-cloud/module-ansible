# nic

This module allows you to create, update or remove a NIC.

## Example Syntax


```yaml
# Create a NIC
    - name: Create NIC
      nic:
       name: NicName
       datacenter: DatacenterName
       server: ServerName
       lan: 2
       dhcp: true
       firewall_active: true
       ips:
         - 10.0.0.1
       wait: true
       wait_timeout: 600
       state: present
      register: ionos_cloud_nic
  
# Update a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      lan: 1
      ips:
        - 158.222.103.23
        - 158.222.103.24
      dhcp: false
      state: update
  
# Remove a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      wait_timeout: 500
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
            "mac": "02:01:27:82:a8:45",
            "name": "AnsibleAutoTestCompute",
            "pci_slot": 6
        },
        "type": "nic"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a NIC
    - name: Create NIC
      nic:
       name: NicName
       datacenter: DatacenterName
       server: ServerName
       lan: 2
       dhcp: true
       firewall_active: true
       ips:
         - 10.0.0.1
       wait: true
       wait_timeout: 600
       state: present
      register: ionos_cloud_nic
  
```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
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
  <td>dhcp<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the NIC will reserve an IP using DHCP.</td>
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
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  # Remove a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      wait_timeout: 500
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
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
  # Update a NIC
  - nic:
      datacenter: DatacenterName
      server: ServerName
      nic: NicName
      lan: 1
      ips:
        - 158.222.103.23
        - 158.222.103.24
      dhcp: false
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="246">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
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
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
