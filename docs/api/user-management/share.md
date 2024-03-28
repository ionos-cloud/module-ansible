# share

This module allows you to add, update or remove resource shares.

## Example Syntax


```yaml

name: Create share
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: true
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: present
register: share


name: Update shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: false
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: update


name: Remove shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  resource_ids:
  - ''
  - ''
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
    "shares": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/137d33b4-a730-4323-98fd-ad0e3b078a5b/shares/2dd792c1-a5dc-45b6-8aa1-346478d53978",
            "id": "2dd792c1-a5dc-45b6-8aa1-346478d53978",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/137d33b4-a730-4323-98fd-ad0e3b078a5b/shares/9364dbea-d63f-4799-aaf6-e0cf6c21cafc",
            "id": "9364dbea-d63f-4799-aaf6-e0cf6c21cafc",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        }
    ]
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/user-management).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create share
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: true
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: present
register: share

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
  <td>edit_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>edit privilege on a resource</td>
  </tr>
  <tr>
  <td>share_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>share privilege on a resource</td>
  </tr>
  <tr>
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the group.</td>
  </tr>
  <tr>
  <td>resource_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>A list of resource IDs to add, update or remove as shares.</td>
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
  
name: Remove shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  resource_ids:
  - ''
  - ''
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
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the group.</td>
  </tr>
  <tr>
  <td>resource_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>A list of resource IDs to add, update or remove as shares.</td>
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
  
name: Update shares
ionoscloudsdk.ionoscloud.share:
  group: Demo
  edit_privilege: false
  share_privilege: true
  resource_ids:
  - ''
  - ''
  state: update

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
  <td>edit_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>edit privilege on a resource</td>
  </tr>
  <tr>
  <td>share_privilege<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>share privilege on a resource</td>
  </tr>
  <tr>
  <td>group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or ID of the group.</td>
  </tr>
  <tr>
  <td>resource_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>A list of resource IDs to add, update or remove as shares.</td>
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
