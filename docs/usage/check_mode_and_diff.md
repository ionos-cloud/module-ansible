# Using check_mode and diff

> **_NOTE:_** More info on using check_mode and diff can be found here https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html

Read bellow for info on how the IONOS Ansible module handles check mode and diff.

### Check Mode
When using check_mode the playbook will not make changes in the API and a message will be returned if such changes would have been made. Example: "user <email> would be updated.". The returned state is "changed".
For operations that do not cause changes the regular response will be returned.

### Diff
When using diff an additional property will be returned on the object showing the object states with before and after. These states only include the attributes which are checked by Ansible for update and recreate.
Diff is not shown for when the object does not exist or for when it ill be deleted

> **_NOTE:_** Check mode and diff more are independent! Using diff does not stop the changes from being made in the api. To check what changes will be made without actually making them use both check_mode and diff.

For now only the user modules offers support for check_mode and diff.

### Examples
Usage:
```yaml
tasks:
- name: Create user
    ionoscloudsdk.ionoscloud.user:
    firstname: John
    lastname: Doe
    email: <email>
    administrator: false
    user_password: <password>
    force_sec_auth: false
    state: present
    check_mode: true
    diff: true
```

Output:
```json
{
    "user_response": {
        "changed": true,
        "diff": {
            "after": {
                "administrator": false,
                "email": "<email>",
                "firstname": "John",
                "force_sec_auth": false,
                "groups": "",
                "lastname": "Doe",
                "user_password": "user password will be updated"
            },
            "before": {
                "administrator": false,
                "email": "<email>",
                "firstname": "John",
                "force_sec_auth": false,
                "groups": "",
                "lastname": "Doe",
                "user_password": ""
            }
        },
        "failed": false,
        "msg": "User <email> would be updated"
    }
}
