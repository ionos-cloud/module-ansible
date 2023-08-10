# user

This module allows you to create, update or remove a user.

## Example Syntax


```yaml
# Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: <email>
      user_password: <password>
      administrator: true
      state: present
  
# Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: <email>
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  
# Remove a user
  - name: Remove user
    user:
      user: <email>
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
    "user": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
        "id": "<USER_ID>",
        "metadata": {
            "created_date": "2023-05-31T13:41:25+00:00",
            "etag": "37a6259cc0c1dae299a7866489dff0bd",
            "last_login": null
        },
        "properties": {
            "active": true,
            "administrator": false,
            "email": "<EMAIL>",
            "firstname": "John2",
            "force_sec_auth": false,
            "lastname": "Doe",
            "s3_canonical_user_id": null,
            "sec_auth_active": false
        },
        "type": "user"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: <email>
      user_password: <password>
      administrator: true
      state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | firstname<br /><span style="color:#003d8f">str</span> | True | The first name of the user. |
  | lastname<br /><span style="color:#003d8f">str</span> | True | The last name of the user. |
  | email<br /><span style="color:#003d8f">str</span> | True | The email address of the user. |
  | user_password<br /><span style="color:#003d8f">str</span> | True | A password for the user. |
  | administrator<br /><span style="color:#003d8f">bool</span> | False | Indicates if the user has admin rights. |
  | force_sec_auth<br /><span style="color:#003d8f">bool</span> | False | Indicates if secure authentication should be forced on the user. |
  | groups<br /><span style="color:#003d8f">list</span> | False | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active<br /><span style="color:#003d8f">bool</span> | False | Indicates if secure authentication is active for the user. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove a user
  - name: Remove user
    user:
      user: <email>
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | user<br /><span style="color:#003d8f">str</span> | True | The ID or name of the user. |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  # Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: <email>
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | firstname<br /><span style="color:#003d8f">str</span> | False | The first name of the user. |
  | lastname<br /><span style="color:#003d8f">str</span> | False | The last name of the user. |
  | email<br /><span style="color:#003d8f">str</span> | False | The email address of the user. |
  | user<br /><span style="color:#003d8f">str</span> | True | The ID or name of the user. |
  | user_password<br /><span style="color:#003d8f">str</span> | False | A password for the user. |
  | administrator<br /><span style="color:#003d8f">bool</span> | False | Indicates if the user has admin rights. |
  | force_sec_auth<br /><span style="color:#003d8f">bool</span> | False | Indicates if secure authentication should be forced on the user. |
  | groups<br /><span style="color:#003d8f">list</span> | False | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active<br /><span style="color:#003d8f">bool</span> | False | Indicates if secure authentication is active for the user. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
