# volume

Allows you to create, update or remove a volume from a Ionos datacenter.

## Example Syntax


```yaml
# Create Multiple Volumes
  - volume:
    datacenter: Tardis One
    name: vol%02d
    count: 5
    wait_timeout: 500
    state: present
  
# Update Volumes - only one ID if renaming
  - volume:
    name: 'new_vol_name'
    datacenter: Tardis One
    instance_ids: 'vol01'
    size: 50
    bus: IDE
    wait_timeout: 500
    state: update
  
# Remove Volumes
  - volume:
    datacenter: Tardis One
    instance_ids:
      - 'vol01'
      - 'vol02'
    wait_timeout: 500
    state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create Multiple Volumes
  - volume:
    datacenter: Tardis One
    name: vol%02d
    count: 5
    wait_timeout: 500
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | server | False | str |  | The server to which to attach the volume. |
  | name | True | str |  | The name of the volumes. Names are enumerated if count &gt; 1. |
  | size | False | int | 10 | The size of the volume. |
  | bus | False | str | VIRTIO | The bus type. |
  | image | False | str |  | The image alias or ID for the volume. This can also be a snapshot image ID. |
  | image_password | False | str |  | Password set for the administrative user. |
  | ssh_keys | False | list |  | Public SSH keys allowing access to the virtual machine. |
  | disk_type | False | str | HDD | The disk type of the volume. |
  | licence_type | False | str | UNKNOWN | The licence type for the volume. This is used when the image is non-standard. |
  | availability_zone | False | str |  | The storage availability zone assigned to the volume. |
  | count | False | int | 1 | The number of volumes you wish to create. |
  | backupunit | False | str |  | The ID or name of the backup unit that the user has access to. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property. |
  | user_data | False | str |  | The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property. |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required) |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required) |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
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
  # Remove Volumes
  - volume:
    datacenter: Tardis One
    instance_ids:
      - 'vol01'
      - 'vol02'
    wait_timeout: 500
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | name | False | str |  | The name of the volumes. Names are enumerated if count &gt; 1. |
  | instance_ids | False | list |  | list of instance ids or names. Should only contain one ID if renaming in update state |
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
  # Update Volumes - only one ID if renaming
  - volume:
    name: 'new_vol_name'
    datacenter: Tardis One
    instance_ids: 'vol01'
    size: 50
    bus: IDE
    wait_timeout: 500
    state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | name | False | str |  | The name of the volumes. Names are enumerated if count &gt; 1. |
  | size | False | int | 10 | The size of the volume. |
  | bus | False | str | VIRTIO | The bus type. |
  | availability_zone | False | str |  | The storage availability zone assigned to the volume. |
  | instance_ids | False | list |  | list of instance ids or names. Should only contain one ID if renaming in update state |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required) |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required) |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
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
