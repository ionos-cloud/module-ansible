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
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "update",
    "image": {
        "href": "https://api.ionos.com/cloudapi/v6/images/87fe5b95-05e4-11ee-a7cb-028794406dc9",
        "id": "87fe5b95-05e4-11ee-a7cb-028794406dc9",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-06-08T10:09:18+00:00",
            "etag": "1a305d1a2beaabd6027d5ad4fe5940a8",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-06-08T10:15:32+00:00",
            "state": "BUSY"
        },
        "properties": {
            "cloud_init": "V1",
            "cpu_hot_plug": true,
            "cpu_hot_unplug": false,
            "description": "An image used for testing the Ansible Module",
            "disc_scsi_hot_plug": true,
            "disc_scsi_hot_unplug": false,
            "disc_virtio_hot_plug": true,
            "disc_virtio_hot_unplug": true,
            "image_aliases": [],
            "image_type": "CDROM",
            "licence_type": "LINUX",
            "location": "de/fra",
            "name": "debian-11.7.0-amd64-netinst-renamed.iso",
            "nic_hot_plug": true,
            "nic_hot_unplug": true,
            "public": false,
            "ram_hot_plug": true,
            "ram_hot_unplug": true,
            "size": 0.39
        },
        "type": "image"
    }
}

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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>image_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID of the image.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The resource name.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['absent', 'update']</td>
  </tr>
  </tbody>
</table>

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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>image_id<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID of the image.</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The resource name.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Human-readable description.</td>
  </tr>
  <tr>
  <td>cpu_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable CPU (no reboot required).</td>
  </tr>
  <tr>
  <td>cpu_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable CPU (no reboot required).</td>
  </tr>
  <tr>
  <td>ram_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable RAM (no reboot required).</td>
  </tr>
  <tr>
  <td>ram_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable RAM (no reboot required).</td>
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
  <td>disc_scsi_hot_plug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-plug capable SCSI drive (no reboot required).</td>
  </tr>
  <tr>
  <td>disc_scsi_hot_unplug<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Hot-unplug capable SCSI drive (no reboot required). Not supported with Windows VMs.</td>
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
  <td>licence_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The OS type of this image.</td>
  </tr>
  <tr>
  <td>cloud_init<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Cloud init compatibility.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
