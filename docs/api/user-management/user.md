# User

## Example Syntax

```yaml
    - name: Create user
      user:
        firstname: John
        lastname: Doe
        email: john.doe@example.com
        user_password: secretpassword123
        administrator: true

    - name: Update user
      user:
        firstname: John
        lastname: Doe
        email: john.doe@example.com
        administrator: false
        groups:
          - Developers
          - Testers
        state: update

    - name: Add user to group
      user:
        email: "{{ random_user }}"
        groups:
          - "{{ name }}"
        state: update

    - name: Remove user from group
      user:
        email: "{{ random_user }}"
        groups: []
        state: update

    - name: Delete user
      user:
        email: "{{ random_user }}"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| firstname | **yes**/no | string |  | The user's first name. Required for `state='present'` only. |
| lastname | **yes**/no | string |  | The user's last name. Required for `state='present'` only. |
| email | **yes** | string |  | The user's email. |
| user\_password | **yes**/no | string |  | A password for the user. Required for `state='present'` only. |
| administrator | no | boolean |  | Indicates if the user has administrative rights. |
| force\_sec\_auth | no | boolean |  | Indicates if secure \(two-factor\) authentication should be forced for the user. |
| groups | no | list |  | A list of group IDs or names where the user \(non-administrator\) is to be added. Set to empty list \(`[]`\) to remove the user from all groups. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

