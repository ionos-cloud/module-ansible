# firewall_rule_info

This is a simple module that supports listing Firewall Rules.

## Example Syntax


```yaml

name: List Firewall Rules
ionoscloudsdk.ionoscloud.firewall_rule_info:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
register: firewall_rule_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "firewall_rules": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/0487f06f-b02d-4b78-b4e4-f48d86daf293/servers/73362db5-03c9-4445-907c-d539e7a0a160/nics/6e9d998f-9748-421d-8ad6-6e8bae893361/firewallrules/f15bb976-52d9-4772-b5c9-1425dc4ffa3d",
            "id": "f15bb976-52d9-4772-b5c9-1425dc4ffa3d",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T11:36:10+00:00",
                "etag": "1285981bd52aad3afdc53954605ade82",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T11:36:10+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "icmp_code": null,
                "icmp_type": null,
                "ip_version": "IPv4",
                "name": "SSH",
                "port_range_end": 24,
                "port_range_start": 22,
                "protocol": "TCP",
                "source_ip": null,
                "source_mac": "<MAC>",
                "target_ip": null,
                "type": "INGRESS"
            },
            "type": "firewall-rule"
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).

&nbsp;
### Available parameters:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
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
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
  </tbody>
</table>
