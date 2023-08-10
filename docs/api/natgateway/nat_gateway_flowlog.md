# nat_gateway_flowlog

This is a simple module that supports creating or removing NATGateway Flowlogs. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create NAT Gateway Flowlog
    nat_gateway_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      wait: true
    register: nat_gateway_flowlog_response
  

  - name: Update NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      flowlog: FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: nat_gateway_flowlog_update_response
  

  - name: Delete NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      flowlog: FlowlogName
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
    "flowlog": {
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/c731955d-f702-4094-bc71-ecb769698c89/natgateways/296af42c-c9ce-4f29-bcb8-f12be048bed8/flowlogs/82b024ed-71f5-47fb-89ca-8deaded744ea",
        "id": "82b024ed-71f5-47fb-89ca-8deaded744ea",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T12:29:48+00:00",
            "etag": "5a5c4d7049d5814f9e95984ecda08840",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T12:29:48+00:00",
            "state": "BUSY"
        },
        "properties": {
            "action": "ACCEPTED",
            "bucket": "sdktest",
            "direction": "INGRESS",
            "name": "AnsibleAutoTestNAT"
        },
        "type": "flow-log"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create NAT Gateway Flowlog
    nat_gateway_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      wait: true
    register: nat_gateway_flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | True | The resource name. |
  | action<br /><span style="color:blue">\<str\></span> | True | Specifies the traffic action pattern. |
  | direction<br /><span style="color:blue">\<str\></span> | True | Specifies the traffic direction pattern. |
  | bucket<br /><span style="color:blue">\<str\></span> | True | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | nat_gateway<br /><span style="color:blue">\<str\></span> | True | The ID or name of the NAT Gateway. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      flowlog: FlowlogName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The resource name. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | nat_gateway<br /><span style="color:blue">\<str\></span> | True | The ID or name of the NAT Gateway. |
  | flowlog<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Flowlog. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update NAT Gateway Flowlog
    nat_gateway_flowlog:
      datacenter: DatacenterName
      nat_gateway: NATGatewayName
      flowlog: FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: nat_gateway_flowlog_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The resource name. |
  | action<br /><span style="color:blue">\<str\></span> | False | Specifies the traffic action pattern. |
  | direction<br /><span style="color:blue">\<str\></span> | False | Specifies the traffic direction pattern. |
  | bucket<br /><span style="color:blue">\<str\></span> | False | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter<br /><span style="color:blue">\<str\></span> | True | The ID or name of the datacenter. |
  | nat_gateway<br /><span style="color:blue">\<str\></span> | True | The ID or name of the NAT Gateway. |
  | flowlog<br /><span style="color:blue">\<str\></span> | True | The ID or name of the Flowlog. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
