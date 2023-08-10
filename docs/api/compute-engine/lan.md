# lan

This module allows you to create or remove a LAN.

## Example Syntax


```yaml
# Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  
# Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  
# Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
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
    "lan": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/lans/1",
        "id": "1",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T09:26:00+00:00",
            "etag": "5200f351d90b89ae0282b81a8da77efe",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T09:26:00+00:00",
            "state": "BUSY"
        },
        "properties": {
            "ip_failover": null,
            "name": "AnsibleAutoTestCompute",
            "pcc": null,
            "public": true
        },
        "type": "lan"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span>\<str\></span> | True | The datacenter name or UUID in which to operate. |
  | name<br /><span>\<str\></span> | True | The name of the  resource. |
  | public<br /><span>\<bool\></span> | False | This LAN faces the public Internet.<br />Default: False |
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
  # Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span>\<str\></span> | True | The datacenter name or UUID in which to operate. |
  | lan<br /><span>\<str\></span> | True | The LAN name or UUID. |
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
  # Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span>\<str\></span> | True | The datacenter name or UUID in which to operate. |
  | lan<br /><span>\<str\></span> | True | The LAN name or UUID. |
  | name<br /><span>\<str\></span> | False | The name of the  resource. |
  | pcc<br /><span>\<str\></span> | False | The unique identifier of the private Cross-Connect the LAN is connected to, if any. |
  | ip_failover<br /><span>\<list\></span> | False | IP failover configurations for lan |
  | public<br /><span>\<bool\></span> | False | This LAN faces the public Internet.<br />Default: False |
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
