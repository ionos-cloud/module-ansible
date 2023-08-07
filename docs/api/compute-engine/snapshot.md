# snapshot

This module allows you to create or remove a snapshot.

## Example Syntax


```yaml
# Create a snapshot
  - name: Create snapshot
    snapshot:
      datacenter: production DC
      volume: master
      name: boot volume image
      state: present

  
# Update a snapshot
  - name: Update snapshot
    snapshot:
      name: "boot volume image"
      description: Ansible test snapshot - RENAME
      state: update
  
# Restore a snapshot
  - name: Restore snapshot
    snapshot:
      datacenter: production DC
      volume: slave
      name: boot volume image
      state: restore
  
# Remove a snapshot
  - name: Remove snapshot
    snapshot:
      name: master-Snapshot-11/30/2017
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
    "snapshot": {
        "href": "https://api.ionos.com/cloudapi/v6/snapshots/c77c9be7-fb6d-4747-ac3d-a8489d8499d1",
        "id": "c77c9be7-fb6d-4747-ac3d-a8489d8499d1",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T12:57:58+00:00",
            "etag": "f47933bc5bead5ca05821105dc943e9f",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T12:57:58+00:00",
            "state": "BUSY"
        },
        "properties": {
            "cpu_hot_plug": false,
            "cpu_hot_unplug": false,
            "description": "Ansible test snapshot",
            "disc_scsi_hot_plug": false,
            "disc_scsi_hot_unplug": false,
            "disc_virtio_hot_plug": false,
            "disc_virtio_hot_unplug": false,
            "licence_type": "UNKNOWN",
            "location": "gb/lhr",
            "name": "AnsibleAutoTestCompute",
            "nic_hot_plug": false,
            "nic_hot_unplug": false,
            "ram_hot_plug": false,
            "ram_hot_unplug": false,
            "sec_auth_protection": false,
            "size": 10.0
        },
        "type": "snapshot"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a snapshot
  - name: Create snapshot
    snapshot:
      datacenter: production DC
      volume: master
      name: boot volume image
      state: present

  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which the volumes reside. |
  | volume | True | str |  | The name or UUID of the volume. |
  | description | False | str |  | Human-readable description. |
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
  # Remove a snapshot
  - name: Remove snapshot
    snapshot:
      name: master-Snapshot-11/30/2017
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | snapshot | True | str |  | The ID or name of an existing snapshot. |
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
  # Update a snapshot
  - name: Update snapshot
    snapshot:
      name: "boot volume image"
      description: Ansible test snapshot - RENAME
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | snapshot | True | str |  | The ID or name of an existing snapshot. |
  | licence_type | False | str |  | OS type of this snapshot |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | cpu_hot_unplug | False | bool |  | Hot-unplug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required). |
  | ram_hot_unplug | False | bool |  | Hot-unplug capable RAM (no reboot required). |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required). |
  | disc_scsi_hot_plug | False | bool |  | Hot-plug capable SCSI drive (no reboot required). |
  | disc_scsi_hot_unplug | False | bool |  | Is capable of SCSI drive hot unplug (no reboot required). This works only for non-Windows virtual Machines. |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
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
# state: **restore**
```yaml
  # Restore a snapshot
  - name: Restore snapshot
    snapshot:
      datacenter: production DC
      volume: slave
      name: boot volume image
      state: restore
  
```
### Available parameters for state **restore**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which the volumes reside. |
  | volume | True | str |  | The name or UUID of the volume. |
  | snapshot | True | str |  | The ID or name of an existing snapshot. |
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
