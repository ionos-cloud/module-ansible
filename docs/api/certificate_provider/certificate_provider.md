# certificate_provider

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

## Example Syntax


```yaml

name: Create Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  private_key_file: 'key.pem'
register: certificate


name: Create Certificate no change
ionoscloudsdk.ionoscloud.certificate:
  state: update
  certificate: ''
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  allow_replace: false
register: certificatenochange


name: Delete Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate: ''
  state: absent

```


### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/certificate_provider).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * provider_email 
  * provider_server 
  * key_id 
  * key_secret 
&nbsp;

# state: **present**
```yaml
  
name: Create Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  private_key_file: 'key.pem'
register: certificate

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
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
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
  
name: Delete Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate: ''
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
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
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
  
name: Create Certificate no change
ionoscloudsdk.ionoscloud.certificate:
  state: update
  certificate: ''
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  allow_replace: false
register: certificatenochange

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
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>provider_server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
  </tr>
  <tr>
  <td>key_secret<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The certificate name.</td>
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
