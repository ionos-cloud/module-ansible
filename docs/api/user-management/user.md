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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | firstname | True | str |  | The first name of the user. |
  | lastname | True | str |  | The last name of the user. |
  | email | True | str |  | The email address of the user. |
  | user_password | True | str |  | A password for the user. |
  | administrator | False | bool |  | Indicates if the user has admin rights. |
  | force_sec_auth | False | bool |  | Indicates if secure authentication should be forced on the user. |
  | groups | False | list |  | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active | False | bool |  | Indicates if secure authentication is active for the user. |
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
  # Remove a user
  - name: Remove user
    user:
      user: <email>
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | user | True | str |  | The ID or name of the user. |
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | firstname | False | str |  | The first name of the user. |
  | lastname | False | str |  | The last name of the user. |
  | email | False | str |  | The email address of the user. |
  | user | True | str |  | The ID or name of the user. |
  | user_password | False | str |  | A password for the user. |
  | administrator | False | bool |  | Indicates if the user has admin rights. |
  | force_sec_auth | False | bool |  | Indicates if secure authentication should be forced on the user. |
  | groups | False | list |  | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active | False | bool |  | Indicates if secure authentication is active for the user. |
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
