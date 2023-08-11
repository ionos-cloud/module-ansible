# application_load_balancer_forwardingrule

This is a simple module that supports creating or removing Application Loadbalancer Flowlog rules.

## Example Syntax


```yaml

  - name: Create Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      name: RuleName
      protocol: "HTTP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      client_timeout: 50
      http_rules:
        - name: "Ansible HTTP Rule"
          type : static
          response_message: "<>"
          content_type: "application/json"
          conditions:
            - type: "HEADER"
              condition: "STARTS_WITH"
              value: "Friday"

      wait: true
    register: alb_forwarding_rule_response
  

  - name: Update Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      protocol: "HTTP"
      wait: true
      state: update
    register: alb_forwarding_rule_update_response
  

  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
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
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/0c0e3049-ebbd-4465-a766-62f6950c109e/applicationloadbalancers/5c0b9b00-ae36-4626-bff6-e6c30e6d2809/forwardingrules/e64fb339-1a81-4828-83b1-5e72c238f0a5",
        "id": "e64fb339-1a81-4828-83b1-5e72c238f0a5",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T13:12:17+00:00",
            "etag": "7d16bc2be7483c6544330b4b3ecdbf8f",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T13:12:17+00:00",
            "state": "BUSY"
        },
        "properties": {
            "client_timeout": null,
            "http_rules": [
                {
                    "conditions": [
                        {
                            "condition": "STARTS_WITH",
                            "key": null,
                            "negate": false,
                            "type": "HEADER",
                            "value": "Friday"
                        }
                    ],
                    "content_type": "application/json",
                    "drop_query": null,
                    "location": null,
                    "name": "Ansible HTTP Rule",
                    "response_message": "<>",
                    "status_code": null,
                    "target_group": null,
                    "type": "static"
                }
            ],
            "listener_ip": "10.12.118.224",
            "listener_port": 8081,
            "name": "AnsibleAutoTestALB",
            "protocol": "HTTP",
            "server_certificates": []
        },
        "type": "forwarding-rule"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      name: RuleName
      protocol: "HTTP"
      listener_ip: "10.12.118.224"
      listener_port: "8081"
      client_timeout: 50
      http_rules:
        - name: "Ansible HTTP Rule"
          type : static
          response_message: "<>"
          content_type: "application/json"
          conditions:
            - type: "HEADER"
              condition: "STARTS_WITH"
              value: "Friday"

      wait: true
    register: alb_forwarding_rule_response
  
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
  <td>The name of the Application Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Balancing algorithm.</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The balancing protocol.</td>
  </tr>
  <tr>
  <td>listener_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The listening (inbound) IP.</td>
  </tr>
  <tr>
  <td>listener_port<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The listening (inbound) port number; the valid range is 1 to 65535.</td>
  </tr>
  <tr>
  <td>client_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The maximum time in milliseconds to wait for the client to acknowledge or send data; default is 50,000 (50 seconds).</td>
  </tr>
  <tr>
  <td>http_rules<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>An array of items in the collection. The original order of rules is preserved during processing, except that rules of the 'FORWARD' type are processed after the rules with other defined actions. The relative order of the 'FORWARD' type rules is also preserved during the processing.</td>
  </tr>
  <tr>
  <td>server_certificates<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Array of items in the collection.</td>
  </tr>
  <tr>
  <td>new_server_certificates<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>An array of dict with information used to uploade new certificates and add them to the forwarding rule.A dict should contain 'certificate_file', 'private_key_file', 'certificate_chain_file'(optional), 'certificate_name' as keys.File paths should be absolute.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>application_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Application Loadbalancer.</td>
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
  
  - name: Delete Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: "RuleName - UPDATED"
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
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the Application Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>application_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Application Loadbalancer.</td>
  </tr>
  <tr>
  <td>forwarding_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Application Loadbalancer forwarding rule.</td>
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
  
  - name: Update Application Load Balancer Forwarding Rule
    application_load_balancer_forwardingrule:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      forwarding_rule: RuleName
      name: "RuleName - UPDATED"
      protocol: "HTTP"
      wait: true
      state: update
    register: alb_forwarding_rule_update_response
  
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
  <td>The name of the Application Load Balancer forwarding rule.</td>
  </tr>
  <tr>
  <td>algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Balancing algorithm.</td>
  </tr>
  <tr>
  <td>protocol<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The balancing protocol.</td>
  </tr>
  <tr>
  <td>listener_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The listening (inbound) IP.</td>
  </tr>
  <tr>
  <td>listener_port<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The listening (inbound) port number; the valid range is 1 to 65535.</td>
  </tr>
  <tr>
  <td>client_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The maximum time in milliseconds to wait for the client to acknowledge or send data; default is 50,000 (50 seconds).</td>
  </tr>
  <tr>
  <td>http_rules<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>An array of items in the collection. The original order of rules is preserved during processing, except that rules of the 'FORWARD' type are processed after the rules with other defined actions. The relative order of the 'FORWARD' type rules is also preserved during the processing.</td>
  </tr>
  <tr>
  <td>server_certificates<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Array of items in the collection.</td>
  </tr>
  <tr>
  <td>new_server_certificates<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>An array of dict with information used to uploade new certificates and add them to the forwarding rule.A dict should contain 'certificate_file', 'private_key_file', 'certificate_chain_file'(optional), 'certificate_name' as keys.File paths should be absolute.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>application_load_balancer<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Application Loadbalancer.</td>
  </tr>
  <tr>
  <td>forwarding_rule<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Application Loadbalancer forwarding rule.</td>
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
