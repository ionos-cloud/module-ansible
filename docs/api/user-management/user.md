# user

This module allows you to create, update or remove a user.

## Example Syntax


```yaml
# Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: john.doe@example.com
      user_password: secretpassword123
      administrator: true
      state: present
  
# Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: john.doe@example.com
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  
# Remove a user
  - name: Remove user
    user:
      user: john.doe@example.com
      state: absent
  
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
      email: john.doe@example.com
      user_password: secretpassword123
      administrator: true
      state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | firstname | True | str |  | The user's first name. |
  | lastname | True | str |  | The user's last name. |
  | email | True | str |  | The user's email |
  | user_password | True | str |  | A password for the user. |
  | administrator | False | bool |  | Boolean value indicating if the user has administrative rights. |
  | force_sec_auth | False | bool |  | Boolean value indicating if secure (two-factor) authentication should be forced for the user. |
  | groups | False | list |  | A list of group IDs or names where the user (non-administrator) is to be added.Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active | False | bool |  | Indicates if secure authentication is active for the user. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
      user: john.doe@example.com
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
      email: john.doe@example.com
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
  | firstname | False | str |  | The user's first name. |
  | lastname | False | str |  | The user's last name. |
  | email | False | str |  | The user's email |
  | user | True | str |  | The ID or name of the user. |
  | user_password | False | str |  | A password for the user. |
  | administrator | False | bool |  | Boolean value indicating if the user has administrative rights. |
  | force_sec_auth | False | bool |  | Boolean value indicating if secure (two-factor) authentication should be forced for the user. |
  | groups | False | list |  | A list of group IDs or names where the user (non-administrator) is to be added.Set to empty list ([]) to remove the user from all groups. |
  | sec_auth_active | False | bool |  | Indicates if secure authentication is active for the user. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
