# network_load_balancer_rule

This is a simple module that supports creating or removing NATGateway Flowlog rules. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      name: RuleName
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      targets:
        - ip: "22.231.2.2"
          port: "8080"
          weight: "123"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_forwarding_rule_response
  

  - name: Update Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      wait: true
      state: update
    register: nlb_forwarding_rule_update_response
  

  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: "RuleName - UPDATED"
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
    "forwarding_rule": {
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/89d7e3e1-a688-4ebd-ab01-8beac27e1f8a/networkloadbalancers/c8fb9d9b-a8ef-4358-a275-c23717aebb51/forwardingrules/6dec4e0c-dd8d-4348-acd1-2d0bf16d00e2",
        "id": "6dec4e0c-dd8d-4348-acd1-2d0bf16d00e2",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T13:08:44+00:00",
            "etag": "fb2a7f7680346fe0677dc3d76d652be6",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T13:08:44+00:00",
            "state": "BUSY"
        },
        "properties": {
            "algorithm": "ROUND_ROBIN",
            "health_check": {
                "client_timeout": 50,
                "connect_timeout": 5000,
                "retries": 1,
                "target_timeout": 5000
            },
            "listener_ip": "<IP>",
            "listener_port": 8081,
            "name": "AnsibleAutoTestNLB",
            "protocol": "TCP",
            "targets": [
                {
                    "health_check": null,
                    "ip": "<IP>",
                    "port": 8080,
                    "weight": 123
                }
            ]
        },
        "type": "forwarding-rule"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      name: RuleName
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      targets:
        - ip: "22.231.2.2"
          port: "8080"
          weight: "123"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_forwarding_rule_response
  
```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the Network Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Balancing algorithm</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Balancing protocol</td>
  </tr>
  <tr>
  <td>listener_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Listening (inbound) IP.</td>
  </tr>
  <tr>
  <td>listener_port<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Listening (inbound) port number; valid range is 1 to 65535.</td>
  </tr>
  <tr>
  <td>health_check<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Health check properties for Network Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>targets<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>Array of items in the collection.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>network_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Network Loadbalancer.</td>
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
  
  - name: Delete Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: "RuleName - UPDATED"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the Network Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>network_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Network Loadbalancer.</td>
  </tr>
  <tr>
  <td>forwarding_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Network Loadbalancer forwarding rule.</td>
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
  
  - name: Update Network Load Balancer Forwarding Rule
    network_load_balancer_rule:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "TCP"
      wait: true
      state: update
    register: nlb_forwarding_rule_update_response
  
```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the Network Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Balancing algorithm</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Balancing protocol</td>
  </tr>
  <tr>
  <td>listener_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Listening (inbound) IP.</td>
  </tr>
  <tr>
  <td>listener_port<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Listening (inbound) port number; valid range is 1 to 65535.</td>
  </tr>
  <tr>
  <td>health_check<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Health check properties for Network Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>targets<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Array of items in the collection.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>network_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Network Loadbalancer.</td>
  </tr>
  <tr>
  <td>forwarding_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Network Loadbalancer forwarding rule.</td>
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
