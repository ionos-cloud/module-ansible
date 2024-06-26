# registry

This is a module that supports creating, updating or destroying Registries

## Example Syntax


```yaml

name: Create Registry
ionoscloudsdk.ionoscloud.registry:
  name: 'ansibletest123-'
  location: de/fra
  garbage_collection_schedule:
    days:
    - Wednesday
    time: 04:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  wait: true
register: registry_response


name: Update Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  garbage_collection_schedule:
    days:
    - Wednesday
    - Sunday
    time: 06:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  allow_replace: false
  state: update
register: updated_registry_response


name: Delete Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
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
    "registry": {
        "href": "",
        "id": "9bc72c7b-14d3-493e-a700-f9bc06b25614",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T13:51:25+00:00",
            "last_modified_by": null,
            "last_modified_by_user_id": null,
            "last_modified_date": null,
            "state": "New"
        },
        "properties": {
            "garbage_collection_schedule": {
                "days": [
                    "Wednesday"
                ],
                "time": "04:17:00+00:00"
            },
            "hostname": "",
            "location": "de/fra",
            "name": "ansibletest123",
            "storage_usage": {
                "bytes": 0,
                "updated_at": null
            }
        },
        "type": "registry"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/container-registry).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * name 
  * location 
  * features (changing features.vulnerability_scanning.enabled from true to false will trigger a resource replacement)
&nbsp;

# state: **present**
```yaml
  
name: Create Registry
ionoscloudsdk.ionoscloud.registry:
  name: 'ansibletest123-'
  location: de/fra
  garbage_collection_schedule:
    days:
    - Wednesday
    time: 04:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  wait: true
register: registry_response

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
  <td>garbage_collection_schedule<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection).</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The location of your registry</td>
  </tr>
  <tr>
  <td>features<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Optional registry features. Format: 'vulnerability_scanning' key having a dict for value containing the 'enabled' key with a boolean value Note: Vulnerability scanning for images is enabled by default. This is a paid add-on, please make sure you specify if you do not want it enabled</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your registry.</td>
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
  
name: Delete Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
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
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
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
  
name: Update Registry
ionoscloudsdk.ionoscloud.registry:
  registry: ''
  garbage_collection_schedule:
    days:
    - Wednesday
    - Sunday
    time: 06:17:00+00:00
  features:
    vulnerability_scanning:
      enabled: true
  allow_replace: false
  state: update
register: updated_registry_response

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
  <td>garbage_collection_schedule<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection).</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location of your registry</td>
  </tr>
  <tr>
  <td>features<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Optional registry features. Format: 'vulnerability_scanning' key having a dict for value containing the 'enabled' key with a boolean value Note: Vulnerability scanning for images is enabled by default. This is a paid add-on, please make sure you specify if you do not want it enabled</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your registry.</td>
  </tr>
  <tr>
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
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
