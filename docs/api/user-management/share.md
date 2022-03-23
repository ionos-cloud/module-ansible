# share

This module allows you to add, update or remove resource shares.

## Example Syntax


```yaml
# Create shares
  - name: Create share
    share:
      group: Demo
      edit_privilege: true
      share_privilege: true
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
      state: present
  
# Update shares
  - name: Update shares
    share:
      group: Demo
      edit_privilege: false
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      state: update
  
# Remove shares
  - name: Remove shares
    share:
      group: Demo
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
<<<<<<< HEAD
    - name: Create shares
      share:
        group: Demo
        edit_privilege: true
        share_privilege: true
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
          - ba7efccb-a761-11e7-90a7-525400f64d8d
        state: present

    - name: Update shares
      share:
        group: Demo
        edit_privilege: false
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        state: update
=======
  # Create shares
  - name: Create share
    share:
      group: Demo
      edit_privilege: true
      share_privilege: true
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
      state: present
  
>>>>>>> 00db8fa... feat: generate docs (#61)
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | edit_privilege | False | bool |  | Boolean value indicating that the group has permission to edit privileges on the resource. |
  | share_privilege | False | bool |  | Boolean value indicating that the group has permission to share the resource. |
  | group | True | str |  | The name or ID of the group. |
  | resource_ids | True | list |  | A list of resource IDs to add, update or remove as shares. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove shares
  - name: Remove shares
    share:
      group: Demo
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        - ba7efccb-a761-11e7-90a7-525400f64d8d
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | group | True | str |  | The name or ID of the group. |
  | resource_ids | True | list |  | A list of resource IDs to add, update or remove as shares. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  # Update shares
  - name: Update shares
    share:
      group: Demo
      edit_privilege: false
      resource_ids:
        - b50ba74e-b585-44d6-9b6e-68941b2ce98e
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | edit_privilege | False | bool |  | Boolean value indicating that the group has permission to edit privileges on the resource. |
  | share_privilege | False | bool |  | Boolean value indicating that the group has permission to share the resource. |
  | group | True | str |  | The name or ID of the group. |
  | resource_ids | True | list |  | A list of resource IDs to add, update or remove as shares. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
