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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The resource name. |
  | action | True | str |  | Specifies the traffic action pattern. |
  | direction | True | str |  | Specifies the traffic direction pattern. |
  | bucket | True | str |  | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The resource name. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
  | flowlog | True | str |  | The ID or name of the Flowlog. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The resource name. |
  | action | False | str |  | Specifies the traffic action pattern. |
  | direction | False | str |  | Specifies the traffic direction pattern. |
  | bucket | False | str |  | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | network_load_balancer | True | str |  | The ID or name of the Network Loadbalancer. |
  | flowlog | True | str |  | The ID or name of the Flowlog. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
