# nic_flowlog

This is a simple module that supports creating or removing NIC Flowlogs. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
- name: Create a nic flowlog
  nic_flowlog:
    name: FlowlogName
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
  register: flowlog_response
  
- name: Update a nic flowlog
  nic_flowlog:
    name: "FlowlogName"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
  register: flowlog_update_response
  
- name: Delete a nic flowlog
  nic_flowlog:
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
    name: "FlowlogName"
    state: absent
    wait: true
  register: flowlog_delete_response
  
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
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/47724f5f-625d-46e3-8187-0fce19c74e5c/servers/4e55f7f3-78f2-46c0-9c61-8de00d7cd484/nics/c386eede-b756-441e-97a7-5de4da8518ed/flowlogs/37a775b2-4dad-418a-8cbd-0499ad34d713",
        "id": "37a775b2-4dad-418a-8cbd-0499ad34d713",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-06-06T14:06:00+00:00",
            "etag": "043560db87ade8f005d69efbec1eedea",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-06-06T14:06:00+00:00",
            "state": "BUSY"
        },
        "properties": {
            "action": "ACCEPTED",
            "bucket": "sdktest",
            "direction": "INGRESS",
            "name": "AnsibleAutoTestCompute"
        },
        "type": "flow-log"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create a nic flowlog
  nic_flowlog:
    name: FlowlogName
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
  register: flowlog_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | True | The resource name. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the virtual datacenter. |
  | server<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the Server. |
  | nic<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the NIC. |
  | action<br /><mark style="color:blue;">\<str\></mark> | True | Specifies the traffic action pattern. |
  | direction<br /><mark style="color:blue;">\<str\></mark> | True | Specifies the traffic direction pattern. |
  | bucket<br /><mark style="color:blue;">\<str\></mark> | True | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete a nic flowlog
  nic_flowlog:
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
    name: "FlowlogName"
    state: absent
    wait: true
  register: flowlog_delete_response
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | flowlog<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of an existing Flowlog. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the virtual datacenter. |
  | server<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the Server. |
  | nic<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the NIC. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update a nic flowlog
  nic_flowlog:
    name: "FlowlogName"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
  register: flowlog_update_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | False | The resource name. |
  | flowlog<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of an existing Flowlog. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the virtual datacenter. |
  | server<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the Server. |
  | nic<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the NIC. |
  | action<br /><mark style="color:blue;">\<str\></mark> | False | Specifies the traffic action pattern. |
  | direction<br /><mark style="color:blue;">\<str\></mark> | False | Specifies the traffic direction pattern. |
  | bucket<br /><mark style="color:blue;">\<str\></mark> | False | The S3 bucket name of an existing IONOS Cloud S3 bucket. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
