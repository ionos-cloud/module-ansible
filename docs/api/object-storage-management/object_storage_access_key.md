# object_storage_access_key

This is a module that supports creating and destroying Ionos Cloud Object Storage Access Keys

## Example Syntax


```yaml

name: Create Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        diff: true
    register: access_key_create_result


name: Update Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: update
        diff: true
    register: access_key_update_result


name: Renew Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: renew
    register: access_key_renew_result


name: Delete an Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id  }}"
        state: absent
    register: access_key_create_result

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "action": "create",
    "access_key": {
        "id": "<ID>",
        "type": "accesskey",
        "href": "https://s3.ionos.com/accesskeys/<ID>",
        "metadata": {
            "created_date": "2025-12-11T14:24:16.707651+00:00",
            "created_by": "ionos:iam:cloud::users/<USER_ID>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": "2025-12-11T14:24:22.196873+00:00",
            "last_modified_by": "ionos:iam:cloud::users/<USER_ID>",
            "last_modified_by_user_id": "<USER_ID>",
            "resource_urn": "ionos:s3::<CONTRACT>:accesskeys/<ID>",
            "status": "AVAILABLE",
            "status_message": null,
            "administrative": true,
            "supported_regions": [
                "eu-central-2",
                "eu-south-2",
                "eu-central-3",
                "us-central-1",
                "de"
            ]
        },
        "properties": {
            "description": "Test description",
            "access_key": "ACCESS_KEY",
            "secret_key": null,
            "canonical_user_id": "canonical_user_id",
            "contract_user_id": "contract_user_id"
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/object-storage-management).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
&nbsp;

# state: **present**
```yaml
  
name: Create Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        diff: true
    register: access_key_create_result

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
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Description of the Access key.</td>
  </tr>
  <tr>
  <td>idempotency<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Flag that dictates respecting idempotency. If an s3key already exists, returns with already existing key instead of creating more.<br />Default: False<br />Options: [True, False]</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete an Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id  }}"
        state: absent
    register: access_key_create_result

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
  <td>access_key<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID of an existing access key, not the access key field.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: update
        diff: true
    register: access_key_update_result

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
  <td>access_key<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID of an existing access key, not the access key field.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Description of the Access key.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **renew**
```yaml
  
name: Renew Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: renew
    register: access_key_renew_result

```
### Available parameters for state **renew**:
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
  <td>access_key<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID of an existing access key, not the access key field.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
