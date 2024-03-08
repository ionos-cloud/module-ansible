# volume

Allows you to create, update or remove a volume from a Ionos datacenter.

## Example Syntax


```yaml
name: Create volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  disk_type: SSD Premium
  image: 'centos:7'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
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

name: Update no change
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  disk_type: SSD Premium
  size: 20
  availability_zone: AUTO
  image: 01abcc20-a6b9-11ed-9e9f-e60bb43016ef
  licence_type: LINUX
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  allow_replace: false
  wait_timeout: 600
  wait: true
  state: update
register: volume_create_response_nochange

name: Delete volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute modified'
  - 'AnsibleAutoTestCompute 02'
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

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * size 
  * disk_type 
  * availability_zone 
  * licence_type 
  * user_data (Might trigger replace just by being set as this parameter is retrieved from the API as the image ID, so when using an alias it will always cause a resource replacement!)
  * image (Might trigger replace just by being set as this parameter is retrieved from the API as the image ID, so when using an alias it will always cause a resource replacement!)
  * image_password (Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!)
  * ssh_keys (Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!)
  * backupunit (Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!)
&nbsp;

# state: **present**
```yaml
  name: Create volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  disk_type: SSD Premium
  image: 'centos:7'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter in which to create the volumes.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The server to which to attach the volume.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The size of the volume in GB.</td>
  </tr>
  <tr>
  <td>bus<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The bus type for this volume; default is VIRTIO.<br />Default: VIRTIO<br />Options: ['VIRTIO', 'IDE', 'UNKNOWN']</td>
  </tr>
  <tr>
  <td>image<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Image or snapshot ID to be used as template for this volume.</td>
  </tr>
  <tr>
  <td>image_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Initial password to be set for installed OS. Works with public images only. Not modifiable, forbidden in update requests. Password rules allows all characters from a-z, A-Z, 0-9.</td>
  </tr>
  <tr>
  <td>ssh_keys<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Public SSH keys are set on the image as authorized keys for appropriate SSH login to the instance using the corresponding private key. This field may only be set in creation requests. When reading, it always returns null. SSH keys are only supported if a public Linux image is used for the volume creation.</td>
  </tr>
  <tr>
  <td>disk_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The disk type of the volume.<br />Options: ['HDD', 'SSD', 'SSD Premium', 'SSD Standard']</td>
  </tr>
  <tr>
  <td>licence_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>OS type for this volume.<br />Options: ['UNKNOWN', 'WINDOWS', 'WINDOWS2016', 'WINDOWS2022', 'RHEL', 'LINUX', 'OTHER']</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3']</td>
  </tr>
  <tr>
  <td>count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of volumes you wish to create.<br />Default: 1</td>
  </tr>
  <tr>
  <td>backupunit<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID of the backup unit that the user has access to. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' in conjunction with this property.</td>
  </tr>
  <tr>
  <td>user_data<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The cloud-init configuration for the volume as base64 encoded string. The property is immutable and is only allowed to be set on creation of a new a volume. It is mandatory to provide either 'public image' or 'imageAlias' that has cloud-init compatibility in conjunction with this property.</td>
  </tr>
  <tr>
  <td>cpu_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable CPU (no reboot required).</td>
  </tr>
  <tr>
  <td>ram_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable RAM (no reboot required).</td>
  </tr>
  <tr>
  <td>nic_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable NIC (no reboot required).</td>
  </tr>
  <tr>
  <td>nic_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable NIC (no reboot required).</td>
  </tr>
  <tr>
  <td>disc_virtio_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable Virt-IO drive (no reboot required).</td>
  </tr>
  <tr>
  <td>disc_virtio_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  name: Delete volumes
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute modified'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: 600
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter in which to create the volumes.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids or names. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  name: Update no change
ionoscloudsdk.ionoscloud.volume:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  disk_type: SSD Premium
  size: 20
  availability_zone: AUTO
  image: 01abcc20-a6b9-11ed-9e9f-e60bb43016ef
  licence_type: LINUX
  ram_hot_plug: true
  nic_hot_plug: true
  nic_hot_unplug: true
  disc_virtio_hot_plug: true
  disc_virtio_hot_unplug: true
  allow_replace: false
  wait_timeout: 600
  wait: true
  state: update
register: volume_create_response_nochange

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter in which to create the volumes.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The size of the volume in GB.</td>
  </tr>
  <tr>
  <td>bus<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The bus type for this volume; default is VIRTIO.<br />Default: VIRTIO<br />Options: ['VIRTIO', 'IDE', 'UNKNOWN']</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The availability zone in which the volume should be provisioned. The storage volume will be provisioned on as few physical storage devices as possible, but this cannot be guaranteed upfront. This is uavailable for DAS (Direct Attached Storage), and subject to availability for SSD.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3']</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids or names. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>cpu_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable CPU (no reboot required).</td>
  </tr>
  <tr>
  <td>ram_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable RAM (no reboot required).</td>
  </tr>
  <tr>
  <td>nic_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable NIC (no reboot required).</td>
  </tr>
  <tr>
  <td>nic_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable NIC (no reboot required).</td>
  </tr>
  <tr>
  <td>disc_virtio_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable Virt-IO drive (no reboot required).</td>
  </tr>
  <tr>
  <td>disc_virtio_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable Virt-IO drive (no reboot required). Not supported with Windows VMs.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
