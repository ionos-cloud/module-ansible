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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span>\<str\></span> | True | The name of the  resource. |
  | description<br /><span>\<str\></span> | True | Human-readable description. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | pcc<br /><span>\<str\></span> | True | The ID or name of an existing PCC. |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span>\<str\></span> | False | The name of the  resource. |
  | pcc<br /><span>\<str\></span> | True | The ID or name of an existing PCC. |
  | description<br /><span>\<str\></span> | False | Human-readable description. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
