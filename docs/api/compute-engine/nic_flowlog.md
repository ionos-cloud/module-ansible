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
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
  register: flowlog_response
  
- name: Update a nic flowlog
  nic_flowlog:
    name: "{{ name }}"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
  register: flowlog_update_response
  
- name: Delete a nic flowlog
  nic_flowlog:
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
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
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
  register: flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the Flowlog. |
  | datacenter_id | True | str |  | The ID of the virtual datacenter. |
  | server_id | True | str |  | The ID of the Server. |
  | nic_id | True | str |  | The ID of the NIC. |
  | action | True | str |  | Specifies the traffic action pattern. |
  | direction | True | str |  | Specifies the traffic direction pattern. |
  | bucket | True | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | api_url | False | str |  | The Ionos API base URL. |
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
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
    name: "{{ name }}"
    state: absent
    wait: true
  register: flowlog_delete_response
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Flowlog. |
  | flowlog_id | False | str |  | The ID of the Flowlog. |
  | datacenter_id | True | str |  | The ID of the virtual datacenter. |
  | server_id | True | str |  | The ID of the Server. |
  | nic_id | True | str |  | The ID of the NIC. |
  | api_url | False | str |  | The Ionos API base URL. |
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
    datacenter_id: "{{ datacenter_response.datacenter.id }}"
    server_id: "{{ server_response.machines[0].id }}"
    nic_id: "{{ nic_response.nic.id }}"
    flowlog_id: "{{ flowlog_response.flowlog.id }}"
  register: flowlog_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Flowlog. |
  | flowlog_id | False | str |  | The ID of the Flowlog. |
  | datacenter_id | True | str |  | The ID of the virtual datacenter. |
  | server_id | True | str |  | The ID of the Server. |
  | nic_id | True | str |  | The ID of the NIC. |
  | action | False | str |  | Specifies the traffic action pattern. |
  | direction | False | str |  | Specifies the traffic direction pattern. |
  | bucket | False | str |  | S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
