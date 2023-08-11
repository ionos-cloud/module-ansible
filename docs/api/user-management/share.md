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
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "shares": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/137d33b4-a730-4323-98fd-ad0e3b078a5b/shares/2dd792c1-a5dc-45b6-8aa1-346478d53978",
            "id": "2dd792c1-a5dc-45b6-8aa1-346478d53978",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/137d33b4-a730-4323-98fd-ad0e3b078a5b/shares/9364dbea-d63f-4799-aaf6-e0cf6c21cafc",
            "id": "9364dbea-d63f-4799-aaf6-e0cf6c21cafc",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        }
    ]
}

```

&nbsp;

&nbsp;

# state: **present**
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
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | edit_privilege<br /><mark style="color:blue;">\<bool\></mark> | False | edit privilege on a resource |
  | share_privilege<br /><mark style="color:blue;">\<bool\></mark> | False | share privilege on a resource |
  | group<br /><mark style="color:blue;">\<str\></mark> | True | The name or ID of the group. |
  | resource_ids<br /><mark style="color:blue;">\<list\></mark> | True | A list of resource IDs to add, update or remove as shares. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | group<br /><mark style="color:blue;">\<str\></mark> | True | The name or ID of the group. |
  | resource_ids<br /><mark style="color:blue;">\<list\></mark> | True | A list of resource IDs to add, update or remove as shares. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | edit_privilege<br /><mark style="color:blue;">\<bool\></mark> | False | edit privilege on a resource |
  | share_privilege<br /><mark style="color:blue;">\<bool\></mark> | False | share privilege on a resource |
  | group<br /><mark style="color:blue;">\<str\></mark> | True | The name or ID of the group. |
  | resource_ids<br /><mark style="color:blue;">\<list\></mark> | True | A list of resource IDs to add, update or remove as shares. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
