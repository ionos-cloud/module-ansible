# Backup unit

## Example Syntax

```text
    - name: Create backupunit
      backupunit:
        backupunit_email: "{{ email }}"
        backupunit_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a backupunit
      backupunit:
        backupunit_id: "{{backupunit.id}}"
        backupunit_email: "{{ updated_email }}"
        backupunit_password:  "{{ updated_password }}"
        state: update

    - name: Remove backupunit
      backupunit:
        backupunit_id: "{{backupunit.id}}"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The resource name \(only alphanumeric characters are acceptable\). Only required when state = 'present'. |
| backupunit\_email | **yes**/no | string |  | The email associated with the backup unit. This email does not have to be the same as the user's email.  Only required when state = 'present'. |
| backupunit\_password | **yes**/no | string |  | The password associated to that resource.  Only required when state = 'present'. |
| backupunit\_id | **yes**/no | string |  | The ID of the backupunit.  Required when state = 'update' or state = 'absent'. |

