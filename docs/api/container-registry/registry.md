# registry

This is a module that supports creating, updating or destroying Registries

## Example Syntax


```yaml
- name: Create Registry
    registry:
      name: test_registry
      location: de
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: cluster_response
  
- name: Update Registry
    registry:
      name: test_registry
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: updated_cluster_response
  
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
      location: de
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: cluster_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | maintenance_window | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the maintenance) and &quot;days&quot; (the days when to perform the maintenance). |
  | garbage_collection_schedule | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | location | True | str |  | The location of your registry |
  | name | True | str |  | The name of your registry. |
  | api_url | False | str |  | The Ionos API base URL. |
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
  | name | False | str |  | The name of your registry. |
  | registry_id | False | str |  | The ID of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
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
      maintenance_window:
        days: 
            - Tuesday
            - Sunday
        time: 01:23:00+00:00
      garbage_collection_schedule:
        days: 
            - Wednesday
        time: 04:17:00+00:00
    register: updated_cluster_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | maintenance_window | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the maintenance) and &quot;days&quot; (the days when to perform the maintenance). |
  | garbage_collection_schedule | False | dict |  | Dict containing &quot;time&quot; (the time of the day when to perform the garbage_collection) and &quot;days&quot; (the days when to perform the garbage_collection). |
  | name | False | str |  | The name of your registry. |
  | registry_id | False | str |  | The ID of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
