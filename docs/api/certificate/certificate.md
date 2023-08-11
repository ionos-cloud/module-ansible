# Certificate

## certificate

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

### Example Syntax

```yaml

    - name: Create Certificate
        certificate:
            certificate_name: CertificateName
            certificate_file: "certificate.pem"
            private_key_file: "key.pem"
        register: certificate
  

    - name: Update Certificate
        certificate:
            certificate: CertificateName
            certificate_name: CertificateNewName
            state: update
        register: updated_certificate
  

    - name: Delete Certificate
        certificate:
            certificate: CertificateNewName
            state: delete
  
```

&#x20;

&#x20;

### Returned object

```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "certificate": {
        "id": "58da84bd-5dea-4838-9c43-391b7c75124a",
        "type": "certificate",
        "href": "https://api.ionos.com/certificatemanager/certificates/58da84bd-5dea-4838-9c43-391b7c75124a",
        "metadata": {
            "etag": null,
            "created_date": "2023-05-29T13:48:11Z",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T13:48:11Z",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "state": "AVAILABLE"
        },
        "properties": {
            "name": "test_certificate",
            "certificate": "<CERTIFICATE>",
            "certificate_chain": null
        }
    }
}

```

&#x20;

&#x20;

## state: **present**

```yaml
  
    - name: Create Certificate
        certificate:
            certificate_name: CertificateName
            certificate_file: "certificate.pem"
            private_key_file: "key.pem"
        register: certificate
  
```

#### Available parameters for state **present**:

&#x20;

<table><thead><tr><th width="194.33333333333331">Name</th><th width="138" align="center">Required</th><th>Description</th></tr></thead><tbody><tr><td>certificate_name<br>&#x3C;str></td><td align="center">False</td><td>The certificate name.</td></tr><tr><td>certificate_file<br>&#x3C;str></td><td align="center">True</td><td>File containing the certificate body.</td></tr><tr><td>private_key_file<br>&#x3C;str></td><td align="center">True</td><td>File containing the private key blob.</td></tr><tr><td>certificate_chain_file<br>&#x3C;str></td><td align="center">False</td><td>File containing the certificate chain.</td></tr><tr><td>do_not_replace<br>&#x3C;bool></td><td align="center">False</td><td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br>Default: False</td></tr><tr><td>api_url<br>&#x3C;str></td><td align="center">False</td><td>The Ionos API base URL.</td></tr><tr><td>username<br>&#x3C;str></td><td align="center">False</td><td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td></tr><tr><td>password<br>&#x3C;str></td><td align="center">False</td><td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td></tr><tr><td>token<br>&#x3C;str></td><td align="center">False</td><td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td></tr><tr><td>wait<br>&#x3C;bool></td><td align="center">False</td><td>Wait for the resource to be created before returning.<br>Default: True<br>Options: [True, False]</td></tr><tr><td>wait_timeout<br>&#x3C;int></td><td align="center">False</td><td>How long before wait gives up, in seconds.<br>Default: 600</td></tr><tr><td>state<br>&#x3C;str></td><td align="center">False</td><td>Indicate desired state of the resource.<br>Default: present<br>Options: ['present', 'absent', 'update']</td></tr></tbody></table>

&#x20;

&#x20;

## state: **absent**

```yaml
  
    - name: Delete Certificate
        certificate:
            certificate: CertificateNewName
            state: delete
  
```

#### Available parameters for state **absent**:

&#x20;

<table><thead><tr><th width="213.33333333333331">Name</th><th align="center">Required</th><th>Description</th></tr></thead><tbody><tr><td>certificate<br>&#x3C;str></td><td align="center">False</td><td>The certificate name or ID.</td></tr><tr><td>certificate_name<br>&#x3C;str></td><td align="center">False</td><td>The certificate name.</td></tr><tr><td>api_url<br>&#x3C;str></td><td align="center">False</td><td>The Ionos API base URL.</td></tr><tr><td>username<br>&#x3C;str></td><td align="center">False</td><td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td></tr><tr><td>password<br>&#x3C;str></td><td align="center">False</td><td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td></tr><tr><td>token<br>&#x3C;str></td><td align="center">False</td><td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td></tr><tr><td>wait<br>&#x3C;bool></td><td align="center">False</td><td>Wait for the resource to be created before returning.<br>Default: True<br>Options: [True, False]</td></tr><tr><td>wait_timeout<br>&#x3C;int></td><td align="center">False</td><td>How long before wait gives up, in seconds.<br>Default: 600</td></tr><tr><td>state<br>&#x3C;str></td><td align="center">False</td><td>Indicate desired state of the resource.<br>Default: present<br>Options: ['present', 'absent', 'update']</td></tr></tbody></table>

&#x20;

&#x20;

## state: **update**

```yaml
  
    - name: Update Certificate
        certificate:
            certificate: CertificateName
            certificate_name: CertificateNewName
            state: update
        register: updated_certificate
  
```

#### Available parameters for state **update**:

&#x20;

| Name                                  | Required | Description                                                                                                                                                                                                                                                                                |
| ------------------------------------- | :------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p>certificate<br>&#x3C;str></p>      |   True   | The certificate name or ID.                                                                                                                                                                                                                                                                |
| <p>certificate_name<br>&#x3C;str></p> |   True   | The certificate name.                                                                                                                                                                                                                                                                      |
| <p>do_not_replace<br>&#x3C;bool></p>  |   False  | <p>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br>Default: False</p> |
| <p>api_url<br>&#x3C;str></p>          |   False  | The Ionos API base URL.                                                                                                                                                                                                                                                                    |
| <p>username<br>&#x3C;str></p>         |   False  | The Ionos username. Overrides the IONOS\_USERNAME environment variable.                                                                                                                                                                                                                    |
| <p>password<br>&#x3C;str></p>         |   False  | The Ionos password. Overrides the IONOS\_PASSWORD environment variable.                                                                                                                                                                                                                    |
| <p>token<br>&#x3C;str></p>            |   False  | The Ionos token. Overrides the IONOS\_TOKEN environment variable.                                                                                                                                                                                                                          |
| <p>wait<br>&#x3C;bool></p>            |   False  | <p>Wait for the resource to be created before returning.<br>Default: True<br>Options: [True, False]</p>                                                                                                                                                                                    |
| <p>wait_timeout<br>&#x3C;int></p>     |   False  | <p>How long before wait gives up, in seconds.<br>Default: 600</p>                                                                                                                                                                                                                          |
| <p>state<br>&#x3C;str></p>            |   False  | <p>Indicate desired state of the resource.<br>Default: present<br>Options: ['present', 'absent', 'update']</p>                                                                                                                                                                             |

&#x20;

&#x20;
