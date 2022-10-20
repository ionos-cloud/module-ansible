# image

This is a simple module that supports updating or removing Images. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
# Update an image
  - name: Update image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      name: "CentOS-8.3.2011-x86_64-boot-renamed.iso"
      description: "An image used for testing the Ansible Module"
      cpu_hot_plug: true
      cpu_hot_unplug: false
      ram_hot_plug: true
      ram_hot_unplug: true
      nic_hot_plug: true
      nic_hot_unplug: true
      disc_virtio_hot_plug: true
      disc_virtio_hot_unplug: true
      disc_scsi_hot_plug: true
      disc_scsi_hot_unplug: false
      licence_type: "LINUX"
      cloud_init: V1
      state: update
  
# Destroy an image
  - name: Delete image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **absent**
```yaml
  # Destroy an image
  - name: Delete image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | image_id | True | str |  | The ID of the image. |
  | name | False | str |  | The name of the image. |
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
  # Update an image
  - name: Update image
    image:
      image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
      name: "CentOS-8.3.2011-x86_64-boot-renamed.iso"
      description: "An image used for testing the Ansible Module"
      cpu_hot_plug: true
      cpu_hot_unplug: false
      ram_hot_plug: true
      ram_hot_unplug: true
      nic_hot_plug: true
      nic_hot_unplug: true
      disc_virtio_hot_plug: true
      disc_virtio_hot_unplug: true
      disc_scsi_hot_plug: true
      disc_scsi_hot_unplug: false
      licence_type: "LINUX"
      cloud_init: V1
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | image_id | True | str |  | The ID of the image. |
  | name | False | str |  | The name of the image. |
  | description | False | str |  | The description of the image. |
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
  | licence_type | True | str |  | OS type for this image. |
  | cloud_init | False | str |  | Cloud init compatibility. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
