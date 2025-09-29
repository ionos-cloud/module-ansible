# auto_certificate

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

## Example Syntax


```yaml

name: Create Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  certificate_name: 'autoCertificateTest'
  common_name: 'devsdkionos.net'
  provider: ''
  key_algorithm: 'rsa4096'
  allow_replace: true
register: auto_certificate


name: Update Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: ''
  certificate_name: 'autoCertificateTestUpdated'
  allow_replace: false
  state: update
register: auto_certificate_update


name: Delete Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: 'autoCertificateTestUpdated'
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
    "auto_certificate": {
        "id": "c2a80f2c-d97d-47b8-ad38-6ff09881c8a8",
        "type": "auto-certificate",
        "href": "/auto-certificates/c2a80f2c-d97d-47b8-ad38-6ff09881c8a8",
        "metadata": {
            "created_date": "2025-09-29T11:14:24.072501+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": "2025-09-29T11:14:24.072501+00:00",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "resource_urn": "<URN>",
            "state": "PROVISIONING",
            "message": "Issue in progress.",
            "last_issued_certificate": null
        },
        "properties": {
            "provider": "92f64cc8-f137-4238-bd0a-3de9c6019ab7",
            "common_name": "devsdkionos.net",
            "key_algorithm": "rsa4096",
            "name": "autoCertificateTest",
            "subject_alternative_names": []
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/certificate).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * common_name 
  * provider 
  * key_algorithm 
  * subject_alternative_names 
&nbsp;

# state: **present**
```yaml
  
name: Create Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  certificate_name: 'autoCertificateTest'
  common_name: 'devsdkionos.net'
  provider: ''
  key_algorithm: 'rsa4096'
  allow_replace: true
register: auto_certificate

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
  <td>certificate_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A certificate name used for management purposes.</td>
  </tr>
  <tr>
  <td>common_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The common name (DNS) of the certificate to issue. The common name needs to be part of a zone in IONOS Cloud DNS.</td>
  </tr>
  <tr>
  <td>provider<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate provider used to issue the certificates.</td>
  </tr>
  <tr>
  <td>key_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key algorithm used to generate the certificate.</td>
  </tr>
  <tr>
  <td>subject_alternative_names<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Optional additional names to be added to the issued certificate. The additional names needs to be part of a zone in IONOS Cloud DNS.</td>
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
  
name: Delete Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: 'autoCertificateTestUpdated'
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
  <td>auto_certificate<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name or ID.</td>
  </tr>
  <tr>
  <td>certificate_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A certificate name used for management purposes.</td>
  </tr>
  <tr>
  <td>common_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The common name (DNS) of the certificate to issue. The common name needs to be part of a zone in IONOS Cloud DNS.</td>
  </tr>
  <tr>
  <td>provider<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate provider used to issue the certificates.</td>
  </tr>
  <tr>
  <td>key_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key algorithm used to generate the certificate.</td>
  </tr>
  <tr>
  <td>subject_alternative_names<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Optional additional names to be added to the issued certificate. The additional names needs to be part of a zone in IONOS Cloud DNS.</td>
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
  
name: Update Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: ''
  certificate_name: 'autoCertificateTestUpdated'
  allow_replace: false
  state: update
register: auto_certificate_update

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
  <td>auto_certificate<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The certificate name or ID.</td>
  </tr>
  <tr>
  <td>certificate_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>A certificate name used for management purposes.</td>
  </tr>
  <tr>
  <td>common_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The common name (DNS) of the certificate to issue. The common name needs to be part of a zone in IONOS Cloud DNS.</td>
  </tr>
  <tr>
  <td>provider<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate provider used to issue the certificates.</td>
  </tr>
  <tr>
  <td>key_algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The key algorithm used to generate the certificate.</td>
  </tr>
  <tr>
  <td>subject_alternative_names<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Optional additional names to be added to the issued certificate. The additional names needs to be part of a zone in IONOS Cloud DNS.</td>
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
