# network_load_balancer_flowlog

This is a simple module that supports creating or removing NetworkLoadbalancer Flowlogs. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_flowlog_response
  

  - name: Update Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      flowlog: FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: nlb_flowlog_update_response
  

  - name: Delete Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      datacenter: DatacenterName
      network_load_balancer: NLBName
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
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/85d05a60-0884-4337-ae24-b0b26d3f5b59/networkloadbalancers/16827845-2470-4903-ba35-acdb3c98e714/flowlogs/9521264d-e208-46b3-b3a0-796bd5907a30",
        "id": "9521264d-e208-46b3-b3a0-796bd5907a30",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T13:29:56+00:00",
            "etag": "6ccdd322a08ae377ceb9ab00f49d27b3",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T13:29:56+00:00",
            "state": "BUSY"
        },
        "properties": {
            "action": "ACCEPTED",
            "bucket": "sdktest",
            "direction": "INGRESS",
            "name": "AnsibleAutoTestNLB"
        },
        "type": "flow-log"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      network_load_balancer: NLBName
      wait: true
    register: nlb_flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span>\<str\></span> | True | The resource name. |
  | action<br /><span>\<str\></span> | True | Specifies the traffic action pattern. |
  | direction<br /><span>\<str\></span> | True | Specifies the traffic direction pattern. |
  | bucket<br /><span>\<str\></span> | True | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter<br /><span>\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span>\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      flowlog: FlowlogName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span>\<str\></span> | False | The resource name. |
  | datacenter<br /><span>\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span>\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | flowlog<br /><span>\<str\></span> | True | The ID or name of the Flowlog. |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Network Load Balancer Flowlog
    network_load_balancer_flowlog:
      datacenter: DatacenterName
      network_load_balancer: NLBName
      flowlog: FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: nlb_flowlog_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span>\<str\></span> | False | The resource name. |
  | action<br /><span>\<str\></span> | False | Specifies the traffic action pattern. |
  | direction<br /><span>\<str\></span> | False | Specifies the traffic direction pattern. |
  | bucket<br /><span>\<str\></span> | False | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter<br /><span>\<str\></span> | True | The ID or name of the datacenter. |
  | network_load_balancer<br /><span>\<str\></span> | True | The ID or name of the Network Loadbalancer. |
  | flowlog<br /><span>\<str\></span> | True | The ID or name of the Flowlog. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
