# registry

This is a module that supports creating, updating or destroying Registries

## Example Syntax


```yaml
- name: Create Registry
    registry:
      name: test_registry
      location: de/fra
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: registry_response
  
- name: Update Registry
    registry:
      name: test_registry
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: updated_registry_response
  
- name: Delete Registry
    registry:
      name: test_registry
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
    "registry": {
        "href": "",
        "id": "9bc72c7b-14d3-493e-a700-f9bc06b25614",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T13:51:25+00:00",
            "last_modified_by": null,
            "last_modified_by_user_id": null,
            "last_modified_date": null,
            "state": "New"
        },
        "properties": {
            "garbage_collection_schedule": {
                "days": [
                    "Wednesday"
                ],
                "time": "04:17:00+00:00"
            },
            "hostname": "",
            "location": "de/fra",
            "name": "ansibletest123",
            "storage_usage": {
                "bytes": 0,
                "updated_at": null
            }
        },
        "type": "registry"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Registry
    registry:
      name: test_registry
      location: de/fra
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: registry_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | garbage_collection_schedule<br /><span>\<dict\></span> | False | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | location<br /><span>\<str\></span> | True | The location of your registry |
  | name<br /><span>\<str\></span> | True | The name of your registry. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
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
  - name: Delete Registry
    registry:
      name: test_registry
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | registry<br /><span>\<str\></span> | True | The ID or name of an existing Registry. |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
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
  - name: Update Registry
    registry:
      name: test_registry
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: updated_registry_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | garbage_collection_schedule<br /><span>\<dict\></span> | False | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | location<br /><span>\<str\></span> | False | The location of your registry |
  | name<br /><span>\<str\></span> | False | The name of your registry. |
  | registry<br /><span>\<str\></span> | True | The ID or name of an existing Registry. |
  | do_not_replace<br /><span>\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span>\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span>\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span>\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
