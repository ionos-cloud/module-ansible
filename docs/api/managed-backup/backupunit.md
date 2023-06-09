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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the  resource (alphanumeric characters only). |
  | backupunit_password | False | str |  | The password associated with that resource. |
  | backupunit_email | True | str |  | The email associated with the backup unit. Bear in mind that this email does not be the same email as of the user. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
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
  # Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit: BackupUnitName
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | backupunit | True | str |  | The ID or name of the virtual Backup Unit. |
  | api_url | False | str |  | The Ionos API base URL. |
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

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | backupunit | True | str |  | The ID or name of the virtual Backup Unit. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
