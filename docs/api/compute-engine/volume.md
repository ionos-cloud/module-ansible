# volume

Allows you to create, update or remove a volume from a Ionos datacenter.

## Example Syntax


```yaml
# Create Multiple Volumes
    - name: Create volumes
      volume:
        datacenter: "AnsibleDatacenter"
        name: "AnsibleAutoTestCompute %02d"
        disk_type: SSD Premium
        image: "centos:7"
        image_password: "<password>"
        count: 2
        size: 20
        availability_zone: AUTO
        cpu_hot_plug: false
        ram_hot_plug: true
        nic_hot_plug: true
        nic_hot_unplug: true
        disc_virtio_hot_plug: true
        disc_virtio_hot_unplug: true
        wait_timeout: 600
        wait: true
        state: present
      register: volume_create_response
  
# Update Volumes - only one ID if renaming
    - name: Update volume
      volume:
        datacenter: "AnsibleDatacenter"
        instance_ids:
          - "AnsibleAutoTestCompute 01"
        name: "AnsibleAutoTestCompute modified"
        size: 25
        cpu_hot_plug: false
        ram_hot_plug: true
        nic_hot_plug: true
        nic_hot_unplug: true
        disc_virtio_hot_plug: true
        disc_virtio_hot_unplug: true
        wait_timeout: 600
        wait: true
        state: update
  
# Remove Volumes
  - name: Delete volumes
      volume:
        datacenter: "{{ datacenter }}"
        instance_ids:
          - "AnsibleAutoTestCompute modified"
          - "AnsibleAutoTestCompute 02"
        wait_timeout: 600
        state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "volumes": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/ea545f2e-4c15-4be7-8fb8-867fb6e9d330/volumes/9be90788-1b11-4d1b-bfb3-857f0c7bd5a3",
            "id": "9be90788-1b11-4d1b-bfb3-857f0c7bd5a3",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-29T09:43:18+00:00",
                "etag": "1e8b91b7c574e42452b1628408959166",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-05-29T09:43:18+00:00",
                "state": "BUSY"
            },
            "properties": {
                "availability_zone": null,
                "backupunit_id": null,
                "boot_order": "AUTO",
                "boot_server": null,
                "bus": "VIRTIO",
                "cpu_hot_plug": false,
                "device_number": null,
                "disc_virtio_hot_plug": false,
                "disc_virtio_hot_unplug": false,
                "image": null,
                "image_alias": null,
                "image_password": null,
                "licence_type": "OTHER",
                "name": "AnsibleAutoTestCompute-data",
                "nic_hot_plug": false,
                "nic_hot_unplug": false,
                "pci_slot": null,
                "ram_hot_plug": false,
                "size": 20.0,
                "ssh_keys": [],
                "type": "HDD",
                "user_data": null
            },
            "type": "volume"
        }
    ],
    "action": "create",
    "instance_ids": [
        "9be90788-1b11-4d1b-bfb3-857f0c7bd5a3"
    ]
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create Multiple Volumes
    - name: Create volumes
      volume:
        datacenter: "AnsibleDatacenter"
        name: "AnsibleAutoTestCompute %02d"
        disk_type: SSD Premium
        image: "centos:7"
        image_password: "<password>"
        count: 2
        size: 20
        availability_zone: AUTO
        cpu_hot_plug: false
        ram_hot_plug: true
        nic_hot_plug: true
        nic_hot_unplug: true
        disc_virtio_hot_plug: true
        disc_virtio_hot_unplug: true
        wait_timeout: 600
        wait: true
        state: present
      register: volume_create_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | server | False | str |  | The server to which to attach the volume. |
  | name | True | str |  | The name of the  resource. |
  | size | False | int | 10 | The size of the volume in GB. |
  | bus | False | str | VIRTIO | The bus type for this volume; default is VIRTIO. |
  | image | False | str |  | Image or snapshot ID to be used as template for this volume. |
  | image_password | False | str |  | Initial password to be set for installed OS. Works with public images only. Not modifiable, forbidden in update requests. Password rules allows all characters from a-z, A-Z, 0-9. |
  | ssh_keys | False | list |  | Public SSH keys are set on the image as authorized keys for appropriate SSH login to the instance using the corresponding private key. This field may only be set in creation requests. When reading, it always returns null. SSH keys are only supported if a public Linux image is used for the volume creation. |
  | disk_type | False | str | HDD | The disk type of the volume. |
  | licence_type | False | str | UNKNOWN | OS type for this volume. |
  | availability_zone | False | str |  | The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD. |
  | count | False | int | 1 | The number of volumes you wish to create. |
  | backupunit | False | str |  | The ID of the backup unit that the user has access to. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property. |
  | user_data | False | str |  | The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property. |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required). |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required). |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
  - name: Delete volumes
      volume:
        datacenter: "{{ datacenter }}"
        instance_ids:
          - "AnsibleAutoTestCompute modified"
          - "AnsibleAutoTestCompute 02"
        wait_timeout: 600
        state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | name | False | str |  | The name of the  resource. |
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
    - name: Update volume
      volume:
        datacenter: "AnsibleDatacenter"
        instance_ids:
          - "AnsibleAutoTestCompute 01"
        name: "AnsibleAutoTestCompute modified"
        size: 25
        cpu_hot_plug: false
        ram_hot_plug: true
        nic_hot_plug: true
        nic_hot_unplug: true
        disc_virtio_hot_plug: true
        disc_virtio_hot_unplug: true
        wait_timeout: 600
        wait: true
        state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter in which to create the volumes. |
  | name | False | str |  | The name of the  resource. |
  | size | False | int | 10 | The size of the volume in GB. |
  | bus | False | str | VIRTIO | The bus type for this volume; default is VIRTIO. |
  | availability_zone | False | str |  | The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD. |
  | instance_ids | False | list |  | list of instance ids or names. Should only contain one ID if renaming in update state |
  | cpu_hot_plug | False | bool |  | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug | False | bool |  | Hot-plug capable RAM (no reboot required). |
  | nic_hot_plug | False | bool |  | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug | False | bool |  | Hot-unplug capable NIC (no reboot required). |
  | disc_virtio_hot_plug | False | bool |  | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug | False | bool |  | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
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
