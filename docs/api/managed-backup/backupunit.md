# Datacenter

This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers. This module has a dependency on ionos-cloud &gt;= 1.0.0

## Example Syntax


```yaml
# Create a Backup Unit
  - name: Create Backup Unit
    backupunit:
      backupunit_email: "{{ email }}"
      backupunit_password: "{{ password }}"
      name: "{{ name }}"
  
# Update a Backup Unit
  - name: Update a Backup Unit
    backupunit:
      backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
      backupunit_email: "{{ updated_email }}"
      backupunit_password:  "{{ updated_password }}"
      state: update
  
# Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a Backup Unit
  - name: Create Backup Unit
    backupunit:
      backupunit_email: "{{ email }}"
      backupunit_password: "{{ password }}"
      name: "{{ name }}"
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the virtual Backup Unit. |
  | backupunit_password | False | str |  | The password of the Backup Unit. |
  | backupunit_email | True | str |  | The email of the Backup Unit. |
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
  # Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual Backup Unit. |
  | backupunit_id | True | str |  | The ID of the virtual Backup Unit. |
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
  # Update a Backup Unit
  - name: Update a Backup Unit
    backupunit:
      backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
      backupunit_email: "{{ updated_email }}"
      backupunit_password:  "{{ updated_password }}"
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual Backup Unit. |
  | backupunit_id | True | str |  | The ID of the virtual Backup Unit. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
