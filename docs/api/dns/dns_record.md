# dns_record

This is a module that supports creating, updating or destroying DNS Records

## Example Syntax


```yaml
name: Create Record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  name: 'sdk-team-test-record'
  type: 'CNAME'
  content: '1.2.3.4'
  ttl: '3600'
  priority: '35535'
  enabled: 'True'
register: record_response

name: Update record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  record: 'sdk-team-test-record'
  type: 'CNAME'
  content: '2.2.3.4'
  ttl: '1800'
  priority: '16'
  enabled: 'False'
  allow_replace: false
  state: update
register: updated_record_response

name: Delete Record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  record: ''
  wait: true
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
    "record": {
        "id": "c76bf816-c11a-5dfc-8ef3-badfbee48451",
        "type": "record",
        "href": "/zones/b4021310-5e39-50bb-95f6-448b21bf0142/records/c76bf816-c11a-5dfc-8ef3-badfbee48451",
        "metadata": {
            "last_modified_date": "2023-10-05T14:38:56+00:00",
            "created_date": "2023-10-05T14:38:56+00:00",
            "state": "AVAILABLE",
            "fqdn": "<FQDN>",
            "zone_id": "b4021310-5e39-50bb-95f6-448b21bf0142"
        },
        "properties": {
            "name": "<RECORD_NAME>",
            "type": "CNAME",
            "content": "<CONTENT>",
            "ttl": 3600,
            "priority": 0,
            "enabled": true
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dns).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * name 
&nbsp;

# state: **present**
```yaml
  name: Create Record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  name: 'sdk-team-test-record'
  type: 'CNAME'
  content: '1.2.3.4'
  ttl: '3600'
  priority: '35535'
  enabled: 'True'
register: record_response

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
  <td>The Record name.</td>
  </tr>
  <tr>
  <td>type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Holds supported DNS resource record types. In the DNS context a record is a DNS resource record.</td>
  </tr>
  <tr>
  <td>content<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The conted of the Record.</td>
  </tr>
  <tr>
  <td>ttl<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Time to live for the record, recommended 3600.</td>
  </tr>
  <tr>
  <td>priority<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI record types and ignored for all other types.</td>
  </tr>
  <tr>
  <td>enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>When true - the record is visible for lookup.</td>
  </tr>
  <tr>
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  name: Delete Record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  record: ''
  wait: true
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
  <td>record<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Record.</td>
  </tr>
  <tr>
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone.</td>
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
  name: Update record
ionoscloudsdk.ionoscloud.dns_record:
  zone: 'test.example.test.ansible.com'
  record: 'sdk-team-test-record'
  type: 'CNAME'
  content: '2.2.3.4'
  ttl: '1800'
  priority: '16'
  enabled: 'False'
  allow_replace: false
  state: update
register: updated_record_response

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
  <td>The Record name.</td>
  </tr>
  <tr>
  <td>type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Holds supported DNS resource record types. In the DNS context a record is a DNS resource record.</td>
  </tr>
  <tr>
  <td>content<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The conted of the Record.</td>
  </tr>
  <tr>
  <td>ttl<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Time to live for the record, recommended 3600.</td>
  </tr>
  <tr>
  <td>priority<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI record types and ignored for all other types.</td>
  </tr>
  <tr>
  <td>enabled<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>When true - the record is visible for lookup.</td>
  </tr>
  <tr>
  <td>record<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Record.</td>
  </tr>
  <tr>
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
