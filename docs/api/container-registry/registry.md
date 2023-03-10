# registry

This is a module that supports creating, updating or destroying Registries

⚠️ **Note:** Container Registry is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | garbage_collection_schedule | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | location | True | str |  | The location of your registry |
  | name | True | str |  | The name of your registry. |
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
  - name: Delete Registry
    registry:
      name: test_registry
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | registry | True | str |  | The ID or name of an existing Registry. |
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | garbage_collection_schedule | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | location | False | str |  | The location of your registry |
  | name | False | str |  | The name of your registry. |
  | registry | True | str |  | The ID or name of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
