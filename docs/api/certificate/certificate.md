# certificate

This is a simple module that supports uploading, updating or deleting certificates in the Ionos Cloud Certificate Manager.

## Example Syntax


```yaml

    - name: Create Certificate
        certificate:
            certificate_name: "{{ certificate_name }}"
            certificate_file: "{{ certificate_path }}"
            private_key_file: "{{ certificate_key_path }}"
        register: certificate
  

    - name: Update Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            certificate_name: "{{ certificate_updated_name }}"
            state: update
        register: updated_certificate
  

    - name: Delete Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            state: delete
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
    - name: Create Certificate
        certificate:
            certificate_name: "{{ certificate_name }}"
            certificate_file: "{{ certificate_path }}"
            private_key_file: "{{ certificate_key_path }}"
        register: certificate
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | certificate_name | False | str |  | The certificate name. |
  | certificate_file | True | str |  | File containing the certificate body. |
  | private_key_file | True | str |  | File containing the private key blob. |
  | certificate_chain_file | False | str |  | File containing the certificate chain. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
    - name: Delete Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            state: delete
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | certificate | False | str |  | The certificate name or ID. |
  | certificate_name | False | str |  | The certificate name. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
    - name: Update Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            certificate_name: "{{ certificate_updated_name }}"
            state: update
        register: updated_certificate
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | certificate | True | str |  | The certificate name or ID. |
  | certificate_name | True | str |  | The certificate name. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
