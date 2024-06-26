# nat_gateway

This is a simple module that supports creating or removing NATGateways. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

name: Create NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  datacenter: ''
  name: 'AnsibleAutoTestNAT'
  public_ips: ''
  lans:
  - id: ''
    gateway_ips:
    - 10.11.2.5/24
  wait_timeout: 2000
  wait: true
register: nat_gateway_response


name: Update NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  datacenter: ''
  name: 'AnsibleAutoTestNAT - UPDATED'
  public_ips: ''
  nat_gateway: ''
  wait_timeout: 2000
  wait: true
  state: update
register: nat_gateway_response_update


name: Remove NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  nat_gateway: ''
  datacenter: ''
  wait: false
  wait_timeout: 2000
  state: absent

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "action": "create",
    "nat_gateway": {
        "entities": {
            "flowlogs": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0/flowlogs",
                "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0/flowlogs",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "rules": {
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0/rules",
                "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0/rules",
                "items": null,
                "type": "collection"
            }
        },
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0",
        "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T11:46:08+00:00",
            "etag": "f64f5fbd951032447f9e9a9b0d7ab1a2",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T11:46:08+00:00",
            "state": "AVAILABLE"
        },
        "properties": {
            "lans": [],
            "name": "AnsibleAutoTestNAT",
            "public_ips": [
                "<IP1>",
                "<IP2>"
            ]
        },
        "type": "natgateway"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/natgateway).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  datacenter: ''
  name: 'AnsibleAutoTestNAT'
  public_ips: ''
  lans:
  - id: ''
    gateway_ips:
    - 10.11.2.5/24
  wait_timeout: 2000
  wait: true
register: nat_gateway_response

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
  <td>Name of the NAT Gateway.</td>
  </tr>
  <tr>
  <td>public_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location.</td>
  </tr>
  <tr>
  <td>lans<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
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
  
name: Remove NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  nat_gateway: ''
  datacenter: ''
  wait: false
  wait_timeout: 2000
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
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Name of the NAT Gateway.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>nat_gateway<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the NAT Gateway.</td>
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
  
name: Update NAT Gateway
ionoscloudsdk.ionoscloud.nat_gateway:
  datacenter: ''
  name: 'AnsibleAutoTestNAT - UPDATED'
  public_ips: ''
  nat_gateway: ''
  wait_timeout: 2000
  wait: true
  state: update
register: nat_gateway_response_update

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
  <td>Name of the NAT Gateway.</td>
  </tr>
  <tr>
  <td>public_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location.</td>
  </tr>
  <tr>
  <td>lans<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>nat_gateway<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the NAT Gateway.</td>
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
