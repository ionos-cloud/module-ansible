# nic_flowlog

This is a simple module that supports creating or removing NIC Flowlogs. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
- name: Create a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
  register: flowlog_response
  
- name: Update a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
    flowlog: "{{ flowlog_response.flowlog.id }}"
  register: flowlog_update_response
  
- name: Delete a nic flowlog
  nic_flowlog:
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
    flowlog: "{{ flowlog_response.flowlog.id }}"
    name: "{{ name }}"
    state: absent
    wait: true
  register: flowlog_delete_response
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
  register: flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Flowlog. |
  | datacenter | True | str |  | The ID or name of the virtual datacenter. |
  | server | True | str |  | The ID or name of the Server. |
  | nic | True | str |  | The ID or name of the NIC. |
  | action | True | str |  | Specifies the traffic action pattern. |
  | direction | True | str |  | Specifies the traffic direction pattern. |
  | bucket | True | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
  - name: Delete a nic flowlog
  nic_flowlog:
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
    flowlog: "{{ flowlog_response.flowlog.id }}"
    name: "{{ name }}"
    state: absent
    wait: true
  register: flowlog_delete_response
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | flowlog | True | str |  | The ID or name of an existing Flowlog. |
  | datacenter | True | str |  | The ID or name of the virtual datacenter. |
  | server | True | str |  | The ID or name of the Server. |
  | nic | True | str |  | The ID or name of the NIC. |
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
  - name: Update a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: "{{ datacenter_response.datacenter.id }}"
    server: "{{ server_response.machines[0].id }}"
    nic: "{{ nic_response.nic.id }}"
    flowlog: "{{ flowlog_response.flowlog.id }}"
  register: flowlog_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Flowlog. |
  | flowlog | True | str |  | The ID or name of an existing Flowlog. |
  | datacenter | True | str |  | The ID or name of the virtual datacenter. |
  | server | True | str |  | The ID or name of the Server. |
  | nic | True | str |  | The ID or name of the NIC. |
  | action | False | str |  | Specifies the traffic action pattern. |
  | direction | False | str |  | Specifies the traffic direction pattern. |
  | bucket | False | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
