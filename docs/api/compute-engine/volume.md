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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span style="color:#003d8f">str</span> | True | The datacenter in which to create the volumes. |
  | server<br /><span style="color:#003d8f">str</span> | False | The server to which to attach the volume. |
  | name<br /><span style="color:#003d8f">str</span> | True | The name of the  resource. |
  | size<br /><span style="color:#003d8f">int</span> | False | The size of the volume in GB.<br />Default: 10 |
  | bus<br /><span style="color:#003d8f">str</span> | False | The bus type for this volume; default is VIRTIO.<br />Default: VIRTIO<br />Options: ['VIRTIO', 'IDE', 'UNKNOWN'] |
  | image<br /><span style="color:#003d8f">str</span> | False | Image or snapshot ID to be used as template for this volume. |
  | image_password<br /><span style="color:#003d8f">str</span> | False | Initial password to be set for installed OS. Works with public images only. Not modifiable, forbidden in update requests. Password rules allows all characters from a-z, A-Z, 0-9. |
  | ssh_keys<br /><span style="color:#003d8f">list</span> | False | Public SSH keys are set on the image as authorized keys for appropriate SSH login to the instance using the corresponding private key. This field may only be set in creation requests. When reading, it always returns null. SSH keys are only supported if a public Linux image is used for the volume creation.<br />Default:  |
  | disk_type<br /><span style="color:#003d8f">str</span> | False | The disk type of the volume.<br />Default: HDD<br />Options: ['HDD', 'SSD', 'SSD Premium', 'SSD Standard'] |
  | licence_type<br /><span style="color:#003d8f">str</span> | False | OS type for this volume.<br />Default: UNKNOWN<br />Options: ['UNKNOWN', 'WINDOWS', 'WINDOWS2016', 'WINDOWS2022', 'RHEL', 'LINUX', 'OTHER'] |
  | availability_zone<br /><span style="color:#003d8f">str</span> | False | The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3'] |
  | count<br /><span style="color:#003d8f">int</span> | False | The number of volumes you wish to create.<br />Default: 1 |
  | backupunit<br /><span style="color:#003d8f">str</span> | False | The ID of the backup unit that the user has access to. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property. |
  | user_data<br /><span style="color:#003d8f">str</span> | False | The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property. |
  | cpu_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable RAM (no reboot required). |
  | nic_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug<br /><span style="color:#003d8f">bool</span> | False | Hot-unplug capable NIC (no reboot required). |
  | disc_virtio_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug<br /><span style="color:#003d8f">bool</span> | False | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span style="color:#003d8f">str</span> | True | The datacenter in which to create the volumes. |
  | name<br /><span style="color:#003d8f">str</span> | False | The name of the  resource. |
  | instance_ids<br /><span style="color:#003d8f">list</span> | False | list of instance ids or names. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span style="color:#003d8f">str</span> | True | The datacenter in which to create the volumes. |
  | name<br /><span style="color:#003d8f">str</span> | False | The name of the  resource. |
  | size<br /><span style="color:#003d8f">int</span> | False | The size of the volume in GB.<br />Default: 10 |
  | bus<br /><span style="color:#003d8f">str</span> | False | The bus type for this volume; default is VIRTIO.<br />Default: VIRTIO<br />Options: ['VIRTIO', 'IDE', 'UNKNOWN'] |
  | availability_zone<br /><span style="color:#003d8f">str</span> | False | The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3'] |
  | instance_ids<br /><span style="color:#003d8f">list</span> | False | list of instance ids or names. Should only contain one ID if renaming in update state<br />Default:  |
  | cpu_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable CPU (no reboot required). |
  | ram_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable RAM (no reboot required). |
  | nic_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable NIC (no reboot required). |
  | nic_hot_unplug<br /><span style="color:#003d8f">bool</span> | False | Hot-unplug capable NIC (no reboot required). |
  | disc_virtio_hot_plug<br /><span style="color:#003d8f">bool</span> | False | Hot-plug capable Virt-IO drive (no reboot required). |
  | disc_virtio_hot_unplug<br /><span style="color:#003d8f">bool</span> | False | Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
