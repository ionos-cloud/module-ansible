# application_load_balancer_flowlog

This is a simple module that supports creating or removing Application Loadbalancer Flowlogs.

## Example Syntax


```yaml

name: Create Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  name: 'AnsibleAutoTestALB'
  action: ACCEPTED
  direction: INGRESS
  bucket: sdktest
  datacenter: ''
  application_load_balancer: ''
  wait: true
  wait_timeout: 2000
register: alb_flowlog_response


name: Update Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  datacenter: ''
  application_load_balancer: ''
  flowlog: ''
  name: 'AnsibleAutoTestALB'
  action: ALL
  direction: INGRESS
  bucket: sdktest
  wait: true
  state: update
register: alb_flowlog_update_response


name: Delete Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  datacenter: ''
  application_load_balancer: ''
  flowlog: ''
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

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/applicationloadbalancer).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  name: 'AnsibleAutoTestALB'
  action: ACCEPTED
  direction: INGRESS
  bucket: sdktest
  datacenter: ''
  application_load_balancer: ''
  wait: true
  wait_timeout: 2000
register: alb_flowlog_response

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The resource name.</td>
  </tr>
  <tr>
  <td>action<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Specifies the traffic action pattern.</td>
  </tr>
  <tr>
  <td>direction<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Specifies the traffic direction pattern.</td>
  </tr>
  <tr>
  <td>bucket<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The bucket name of an existing IONOS Cloud Object storage bucket.</td>
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
  
name: Delete Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  datacenter: ''
  application_load_balancer: ''
  flowlog: ''
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The resource name.</td>
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
  <td>flowlog<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Flowlog.</td>
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
  
name: Update Application Load Balancer Flowlog
ionoscloudsdk.ionoscloud.application_load_balancer_flowlog:
  datacenter: ''
  application_load_balancer: ''
  flowlog: ''
  name: 'AnsibleAutoTestALB'
  action: ALL
  direction: INGRESS
  bucket: sdktest
  wait: true
  state: update
register: alb_flowlog_update_response

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The resource name.</td>
  </tr>
  <tr>
  <td>action<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies the traffic action pattern.</td>
  </tr>
  <tr>
  <td>direction<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Specifies the traffic direction pattern.</td>
  </tr>
  <tr>
  <td>bucket<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The bucket name of an existing IONOS Cloud Object storage bucket.</td>
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
  <td>flowlog<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Flowlog.</td>
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
