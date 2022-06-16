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
  | name | True | str |  | The name of the snapshot. |
  | description | False | str |  | The description of the snapshot. |
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
  | id | False | str |  | The id of the snapshot. |
  | name | False | str |  | The name of the snapshot. |
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
  | id | False | str |  | The id of the snapshot. |
  | name | False | str |  | The name of the snapshot. |
  | licence_type | False | str |  | The license type used |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | cpu_hot_unplug | False | bool |  | Hot-unplug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required) |
  | ram_hot_unplug | False | bool |  | Hot-unplug capable RAM (no reboot required). |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required) |
  | disc_scsi_hot_plug | False | bool |  | Hot-plug capable SCSI drive (no reboot required). |
  | disc_scsi_hot_unplug | False | bool |  | Hot-unplug capable SCSI drive (no reboot required). Not supported with Windows VMs. |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
  | api_url | False | str |  | The Ionos API base URL. |
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
  | id | False | str |  | The id of the snapshot. |
  | name | False | str |  | The name of the snapshot. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
