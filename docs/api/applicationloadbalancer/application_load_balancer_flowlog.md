# application_load_balancer_flowlog

This is a simple module that supports creating or removing Application Loadbalancer Flowlogs.

## Example Syntax


```yaml

  - name: Create Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      wait: true
    register: alb_flowlog_response
  

  - name: Update Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      flowlog:FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: alb_flowlog_update_response
  

  - name: Delete Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      flowlog:FlowlogName
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
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/d5b16e3b-d162-441b-9567-d9cca96fb191/applicationloadbalancers/ac62eabb-38da-4d1e-b2c6-4711ce86cfda/flowlogs/48cfe165-18f0-417c-a1ee-4ef0d22167c8",
        "id": "48cfe165-18f0-417c-a1ee-4ef0d22167c8",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T13:34:06+00:00",
            "etag": "c1ded9c35b5f413afd00360eb9daa807",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T13:34:06+00:00",
            "state": "BUSY"
        },
        "properties": {
            "action": "ACCEPTED",
            "bucket": "sdktest",
            "direction": "INGRESS",
            "name": "AnsibleAutoTestALB"
        },
        "type": "flow-log"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      name: FlowlogName
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      wait: true
    register: alb_flowlog_response
  
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
  | application_load_balancer | True | str |  | The ID or name of the Application Loadbalancer. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
  
  - name: Delete Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      flowlog:FlowlogName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The resource name. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | application_load_balancer | True | str |  | The ID or name of the Application Loadbalancer. |
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
  
  - name: Update Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter: DatacenterName
      application_load_balancer: AppLoadBalancerName
      flowlog:FlowlogName
      name: FlowlogName
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: alb_flowlog_update_response
  
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
  | application_load_balancer | True | str |  | The ID or name of the Application Loadbalancer. |
  | flowlog | True | str |  | The ID or name of the Flowlog. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
