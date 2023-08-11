# certificate

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

## Example Syntax


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

&nbsp;

&nbsp;
## Returned object
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

&nbsp;

&nbsp;

# state: **present**
```yaml
  
    - name: Create Certificate
        certificate:
            certificate_name: CertificateName
            certificate_file: "certificate.pem"
            private_key_file: "key.pem"
        register: certificate
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | certificate_name<br /><mark style="color:blue;">\<str\></mark> | False | The certificate name. |
  | certificate_file<br /><mark style="color:blue;">\<str\></mark> | True | File containing the certificate body. |
  | private_key_file<br /><mark style="color:blue;">\<str\></mark> | True | File containing the private key blob. |
  | certificate_chain_file<br /><mark style="color:blue;">\<str\></mark> | False | File containing the certificate chain. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
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
  
    - name: Delete Certificate
        certificate:
            certificate: CertificateNewName
            state: delete
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | certificate<br /><mark style="color:blue;">\<str\></mark> | False | The certificate name or ID. |
  | certificate_name<br /><mark style="color:blue;">\<str\></mark> | False | The certificate name. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
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
  
    - name: Update Certificate
        certificate:
            certificate: CertificateName
            certificate_name: CertificateNewName
            state: update
        register: updated_certificate
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | certificate<br /><mark style="color:blue;">\<str\></mark> | True | The certificate name or ID. |
  | certificate_name<br /><mark style="color:blue;">\<str\></mark> | True | The certificate name. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
