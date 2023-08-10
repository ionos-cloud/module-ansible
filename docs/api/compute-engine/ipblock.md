# ipblock

This module allows you to create or remove an IPBlock.

## Example Syntax


```yaml
# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  
# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
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
    "ipblock": {
        "href": "https://api.ionos.com/cloudapi/v6/ipblocks/0bce3fe3-67fd-4d7e-ba86-2e734ad2a79b",
        "id": "0bce3fe3-67fd-4d7e-ba86-2e734ad2a79b",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T11:45:10+00:00",
            "etag": "59558fb22d91e9d6d7a9750aba57fa47",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T11:45:10+00:00",
            "state": "BUSY"
        },
        "properties": {
            "ip_consumers": [],
            "ips": [
                "<IP1>",
                "<IP2>"
            ],
            "location": "gb/lhr",
            "name": "AnsibleAutoTestCompute",
            "size": 2
        },
        "type": "ipblock"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the  resource. |
  | location<br /><span style="color:blue">\<str\></span> | True | Location of that IP block. Property cannot be modified after it is created (disallowed in update requests).<br />Default: us/las<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'] |
  | size<br /><span style="color:blue">\<int\></span> | False | The size of the IP block.<br />Default: 1 |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | ipblock<br /><span style="color:blue">\<str\></span> | True | The name or ID of an existing IPBlock. |
  | name<br /><span style="color:blue">\<str\></span> | False | The name of the  resource. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:blue">\<str\></span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent'] |

&nbsp;

&nbsp;
