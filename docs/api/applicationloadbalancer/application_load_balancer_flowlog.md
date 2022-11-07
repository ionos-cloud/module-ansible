# application_load_balancer_flowlog

This is a simple module that supports creating or removing Application Loadbalancer Flowlogs.

## Example Syntax


```yaml

  - name: Create Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      name: "{{ name }}"
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      wait: true
    register: alb_flowlog_response
  

  - name: Update Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      flowlog: "{{ alb_flowlog_response.flowlog.id }}"
      name: "{{ name }}"
      action: "ALL"
      direction: "INGRESS"
      bucket: "sdktest"
      wait: true
      state: update
    register: alb_flowlog_update_response
  

  - name: Delete Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      flowlog: "{{ alb_flowlog_response.flowlog.id }}"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Application Load Balancer Flowlog
    application_load_balancer_flowlog:
      name: "{{ name }}"
      action: "ACCEPTED"
      direction: "INGRESS"
      bucket: "sdktest"
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      wait: true
    register: alb_flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the flowlog. |
  | action | True | str |  | Specifies the traffic action pattern. |
  | direction | True | str |  | Specifies the traffic direction pattern. |
  | bucket | True | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | flowlog | False | str |  | The ID or name of the Flowlog. |
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
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      flowlog: "{{ alb_flowlog_response.flowlog.id }}"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the flowlog. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | flowlog | False | str |  | The ID or name of the Flowlog. |
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
      datacenter_id: "{{ datacenter_response.datacenter.id }}"
      application_load_balancer_id: "{{ alb_response.application_load_balancer.id }}"
      flowlog: "{{ alb_flowlog_response.flowlog.id }}"
      name: "{{ name }}"
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
  | name | False | str |  | The name of the flowlog. |
  | action | False | str |  | Specifies the traffic action pattern. |
  | direction | False | str |  | Specifies the traffic direction pattern. |
  | bucket | False | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | datacenter_id | True | str |  | The ID of the datacenter. |
  | application_load_balancer_id | True | str |  | The ID of the Application Loadbalancer. |
  | flowlog | False | str |  | The ID or name of the Flowlog. |
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
