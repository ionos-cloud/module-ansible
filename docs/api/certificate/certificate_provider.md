# certificate_provider

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

## Example Syntax


```yaml

name: Create Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider_name: 'Let's Encrypt'
  provider_email: 'sdk-go-v6@cloud.ionos.com'
  provider_server: 'https://acme-staging-v02.api.letsencrypt.org/directory'
  key_id: 'some-key-id'
  key_secret: 'secret'
  allow_replace: true
register: certificate_provider


name: Update Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider: ''
  provider_name: 'Let's Encrypt UPDATED'
  allow_replace: false
  state: update
register: certificateproviderupdate


name: Delete Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider: ''
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
    "certificate_provider": {
        "id": "f9debe0b-8c4e-4bae-ab9a-5b634d7d054e",
        "type": "provider",
        "href": "/providers/f9debe0b-8c4e-4bae-ab9a-5b634d7d054e",
        "metadata": {
            "created_date": "2025-09-26T14:55:11.643007+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T13:48:11Z",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "resource_urn": "<URN>",
            "state": "AVAILABLE",
            "message": "Ready"
        },
        "properties": {
            "name": "Let's Encrypt",
            "email": "<EMAIL>",
            "server": "<SERVR>",
            "external_account_binding": {
                "key_id": "some-key-id",
                "key_secret": null
            }
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/certificate).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * provider_email 
  * provider_server 
  * key_id 
  * key_secret (Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!)
&nbsp;

# state: **present**
```yaml
  
name: Create Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider_name: 'Let's Encrypt'
  provider_email: 'sdk-go-v6@cloud.ionos.com'
  provider_server: 'https://acme-staging-v02.api.letsencrypt.org/directory'
  key_id: 'some-key-id'
  key_secret: 'secret'
  allow_replace: true
register: certificate_provider

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
  <td>provider_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the certificate provider.</td>
  </tr>
  <tr>
  <td>provider_email<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The email address of the certificate requester.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The URL of the certificate provider.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key ID of the external account binding.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The secret of the external account binding.</td>
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
  
name: Delete Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider: ''
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
  <td>provider<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The provider name or ID.</td>
  </tr>
  <tr>
  <td>provider_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the certificate provider.</td>
  </tr>
  <tr>
  <td>provider_email<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The email address of the certificate requester.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The URL of the certificate provider.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key ID of the external account binding.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The secret of the external account binding.</td>
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
  
name: Update Certificate Provider
ionoscloudsdk.ionoscloud.certificate_provider:
  provider: ''
  provider_name: 'Let's Encrypt UPDATED'
  allow_replace: false
  state: update
register: certificateproviderupdate

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
  <td>provider<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The provider name or ID.</td>
  </tr>
  <tr>
  <td>provider_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the certificate provider.</td>
  </tr>
  <tr>
  <td>provider_email<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The email address of the certificate requester.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The URL of the certificate provider.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key ID of the external account binding.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The secret of the external account binding.</td>
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
