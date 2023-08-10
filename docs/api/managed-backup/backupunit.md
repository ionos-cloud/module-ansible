# backupunit

This is a simple module that supports creating or removing Backup Units. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
# Create a Backup Unit
  - name: Create Backup Unit
    backupunit:
      backupunit_email: <email>
      backupunit_password: <password>
      name: BackupUnitName
  
# Update a Backup Unit
  - name: Update a Backup Unit
    backupunit:
      backupunit: BackupUnitName
      backupunit_email: <newEmail>
      backupunit_password: <newPassword>
      state: update
  
# Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit: BackupUnitName
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "update",
    "backupunit": {
        "href": "https://api.ionos.com/cloudapi/v6/backupunits/a23da1a9-33d9-4e39-b111-42e35f20833d",
        "id": "a23da1a9-33d9-4e39-b111-42e35f20833d",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-03-10T14:16:47+00:00",
            "etag": "210a96f62538bed984fd21654ba0f713",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T11:28:27+00:00",
            "state": "BUSY"
        },
        "properties": {
            "email": "<EMAIL>",
            "name": "My AnsibleAutoTestBackup",
            "password": null
        },
        "type": "backupunit"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a Backup Unit
  - name: Create Backup Unit
    backupunit:
      backupunit_email: <email>
      backupunit_password: <password>
      name: BackupUnitName
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:blue">\<str\></span> | True | The name of the  resource (alphanumeric characters only). |
  | backupunit_password<br /><span style="color:blue">\<str\></span> | False | The password associated with that resource. |
  | backupunit_email<br /><span style="color:blue">\<str\></span> | True | The email associated with the backup unit. Bear in mind that this email does not be the same email as of the user. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit: BackupUnitName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | backupunit<br /><span style="color:blue">\<str\></span> | True | The ID or name of the virtual Backup Unit. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  # Update a Backup Unit
  - name: Update a Backup Unit
    backupunit:
      backupunit: BackupUnitName
      backupunit_email: <newEmail>
      backupunit_password: <newPassword>
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | backupunit<br /><span style="color:blue">\<str\></span> | True | The ID or name of the virtual Backup Unit. |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
