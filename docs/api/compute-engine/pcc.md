# pcc

This is a simple module that supports creating or removing Private Cross Connects. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create pcc
    pcc:
      name: PCCName
      description: "Description for my PCC"
  

  - name: Update pcc
    pcc:
      pcc: PCCName
      name: NewPCCName
      description: "New description for my PCC"
      state: update
  

  - name: Remove pcc
    pcc:
      pcc: NewPCCName
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
    "pcc": {
        "href": "https://api.ionos.com/cloudapi/v6/pccs/9574d5dd-14be-4e4c-b9fb-962bdadc954d",
        "id": "9574d5dd-14be-4e4c-b9fb-962bdadc954d",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": null,
            "created_date": "2023-05-29T12:52:28+00:00",
            "etag": "90244ee1b3bb5db489f5e25999ee177d",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": null,
            "last_modified_date": "2023-05-29T12:52:28+00:00",
            "state": "BUSY"
        },
        "properties": {
            "connectable_datacenters": [],
            "description": "Ansible Compute test description",
            "name": "AnsibleAutoTestCompute",
            "peers": []
        },
        "type": "pcc"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create pcc
    pcc:
      name: PCCName
      description: "Description for my PCC"
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the  resource. |
  | description | True | str |  | Human-readable description. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
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
  
  - name: Remove pcc
    pcc:
      pcc: NewPCCName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | pcc | True | str |  | The ID or name of an existing PCC. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
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
  
  - name: Update pcc
    pcc:
      pcc: PCCName
      name: NewPCCName
      description: "New description for my PCC"
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the  resource. |
  | pcc | True | str |  | The ID or name of an existing PCC. |
  | description | False | str |  | Human-readable description. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
