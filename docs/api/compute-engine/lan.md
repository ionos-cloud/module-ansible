# lan

This module allows you to create or remove a LAN.

## Example Syntax


```yaml

name: Create LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  public: false
register: ionos_cloud_lan


name: Update LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  pcc: ''
  state: update


name: Remove LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  state: absent
  wait: true

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "lan": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/lans/1",
        "id": "1",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T09:26:00+00:00",
            "etag": "5200f351d90b89ae0282b81a8da77efe",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T09:26:00+00:00",
            "state": "BUSY"
        },
        "properties": {
            "ip_failover": null,
            "name": "AnsibleAutoTestCompute",
            "pcc": null,
            "public": true
        },
        "type": "lan"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  public: false
register: ionos_cloud_lan

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
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>pcc<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The unique identifier of the Cross Connect the LAN is connected to, if any. It needs to be ensured that IP addresses of the NICs of all LANs connected to a given Cross Connect is not duplicated and belongs to the same subnet range.</td>
  </tr>
  <tr>
  <td>public<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the LAN is connected to the internet or not.<br />Default: False</td>
  </tr>
  <tr>
  <td>ipv6_cidr<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>For a GET request, this value is either 'null' or contains the LAN's /64 IPv6 CIDR block if this LAN is IPv6 enabled. For POST/PUT/PATCH requests, 'AUTO' will result in enabling this LAN for IPv6 and automatically assign a /64 IPv6 CIDR block to this LAN and /80 IPv6 CIDR blocks to the NICs and one /128 IPv6 address to each connected NIC. If you choose the IPv6 CIDR block for the LAN on your own, then you must provide a /64 block, which is inside the IPv6 CIDR block of the virtual datacenter and unique inside all LANs from this virtual datacenter. If you enable IPv6 on a LAN with NICs, those NICs will get a /80 IPv6 CIDR block and one IPv6 address assigned to each automatically, unless you specify them explicitly on the LAN and on the NICs. A virtual data center is limited to a maximum of 256 IPv6-enabled LANs.</td>
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
  
name: Remove LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  state: absent
  wait: true

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
  <td>lan<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The LAN name or UUID.</td>
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
  
name: Update LAN
ionoscloudsdk.ionoscloud.lan:
  datacenter: 'AnsibleAutoTestCompute'
  lan: 'AnsibleAutoTestCompute'
  pcc: ''
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
  <td>lan<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The LAN name or UUID.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>pcc<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The unique identifier of the Cross Connect the LAN is connected to, if any. It needs to be ensured that IP addresses of the NICs of all LANs connected to a given Cross Connect is not duplicated and belongs to the same subnet range.</td>
  </tr>
  <tr>
  <td>ip_failover<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>IP failover configurations for lan</td>
  </tr>
  <tr>
  <td>public<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the LAN is connected to the internet or not.<br />Default: False</td>
  </tr>
  <tr>
  <td>ipv6_cidr<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>For a GET request, this value is either 'null' or contains the LAN's /64 IPv6 CIDR block if this LAN is IPv6 enabled. For POST/PUT/PATCH requests, 'AUTO' will result in enabling this LAN for IPv6 and automatically assign a /64 IPv6 CIDR block to this LAN and /80 IPv6 CIDR blocks to the NICs and one /128 IPv6 address to each connected NIC. If you choose the IPv6 CIDR block for the LAN on your own, then you must provide a /64 block, which is inside the IPv6 CIDR block of the virtual datacenter and unique inside all LANs from this virtual datacenter. If you enable IPv6 on a LAN with NICs, those NICs will get a /80 IPv6 CIDR block and one IPv6 address assigned to each automatically, unless you specify them explicitly on the LAN and on the NICs. A virtual data center is limited to a maximum of 256 IPv6-enabled LANs.</td>
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
