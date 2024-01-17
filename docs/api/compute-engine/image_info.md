# image_info

This is a simple module that supports listing images.

## Example Syntax


```yaml

    - name: Get all images
      image_info:
      register: image_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "images": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/a4418461-cd77-11e9-b88c-525400f64d8d",
            "id": "a4418461-cd77-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T11:48:55+00:00",
                "etag": "bc19e06c9ae75b7e61d47d91f04f643b",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T11:48:55+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "de/fkb",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/0e4d57f9-cd78-11e9-b88c-525400f64d8d",
            "id": "0e4d57f9-cd78-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T11:51:53+00:00",
                "etag": "ca643281fd2a5b68002bc00ac0ecd920",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T11:51:53+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "de/txl",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/9fc889b9-cd78-11e9-b88c-525400f64d8d",
            "id": "9fc889b9-cd78-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T11:55:57+00:00",
                "etag": "a3fa5ae5293940160c650ff3841673f6",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T11:55:57+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "gb/lhr",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/4fae71cb-cd79-11e9-b88c-525400f64d8d",
            "id": "4fae71cb-cd79-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T12:00:52+00:00",
                "etag": "6550d7bc4bc0e5d157374e008924d3a3",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T12:00:52+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "us/las",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/358651ed-cd7a-11e9-b88c-525400f64d8d",
            "id": "358651ed-cd7a-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T12:07:17+00:00",
                "etag": "33ac6431c7325b8e86960226dcfcc2f1",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T12:07:17+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "us/ewr",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/2e581ea0-cd77-11e9-b88c-525400f64d8d",
            "id": "2e581ea0-cd77-11e9-b88c-525400f64d8d",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2019-09-02T11:45:37+00:00",
                "etag": "50edcfde37a8daf2a555b64156ed3c7b",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2019-09-02T11:45:37+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "de/fra",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/1816b163-ae4c-11eb-9cb6-9aa29238f122",
            "id": "1816b163-ae4c-11eb-9cb6-9aa29238f122",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2021-05-06T09:19:00+00:00",
                "etag": "66678c219449dd7c88fa18dcb004fd84",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2021-05-06T09:19:00+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "es/vit",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/images/5318c3f1-602d-11ed-a67c-fe6d461d20e1",
            "id": "5318c3f1-602d-11ed-a67c-fe6d461d20e1",
            "metadata": {
                "created_by": "System",
                "created_by_user_id": "[UNKNOWN]",
                "created_date": "2022-11-09T12:52:10+00:00",
                "etag": "566e3004fce9911f258a31752700d27c",
                "last_modified_by": "System",
                "last_modified_by_user_id": "[UNKNOWN]",
                "last_modified_date": "2022-11-09T12:52:10+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cloud_init": "NONE",
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": null,
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image_aliases": [
                    "debian:10_iso"
                ],
                "image_type": "CDROM",
                "licence_type": "LINUX",
                "location": "fr/par",
                "name": "debian-10.0.0-amd64-netinst.iso",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "public": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "size": 0.33
            },
            "type": "image"
        }
    ],
    "failed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
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
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
  </tbody>
</table>
