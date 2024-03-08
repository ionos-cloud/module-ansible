# volume_info

This is a simple module that supports listing volumes.

## Example Syntax


```yaml
name: List Volumes
ionoscloudsdk.ionoscloud.volume_info:
  datacenter: 'AnsibleAutoTestCompute'
register: volume_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "action": "info",
    "changed": false,
    "servers": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/volumes/0d3e108d-8f58-47c7-a3fb-705a2979083b",
            "id": "0d3e108d-8f58-47c7-a3fb-705a2979083b",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-06-06T11:37:52+00:00",
                "etag": "72761afffbe760fe1207ef4397b2df9f",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-06-06T11:37:52+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "backupunit_id": null,
                "boot_order": "NONE",
                "boot_server": null,
                "bus": null,
                "cpu_hot_plug": true,
                "device_number": null,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image": "01abcc20-a6b9-11ed-9e9f-e60bb43016ef",
                "image_alias": null,
                "image_password": null,
                "licence_type": "UNKNOWN",
                "name": "AnsibleAutoTestCompute 02",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "pci_slot": null,
                "ram_hot_plug": true,
                "size": 20.0,
                "ssh_keys": null,
                "type": "SSD Premium",
                "user_data": null
            },
            "type": "volume"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/volumes/81472d47-f6b1-4fe5-a345-d2e03db68fea",
            "id": "81472d47-f6b1-4fe5-a345-d2e03db68fea",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-06-06T11:35:19+00:00",
                "etag": "42ade3221dbec89ee4873048af14028b",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-06-06T11:35:19+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "backupunit_id": null,
                "boot_order": "NONE",
                "boot_server": null,
                "bus": null,
                "cpu_hot_plug": true,
                "device_number": null,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "image": "01abcc20-a6b9-11ed-9e9f-e60bb43016ef",
                "image_alias": null,
                "image_password": null,
                "licence_type": "UNKNOWN",
                "name": "AnsibleAutoTestCompute 01",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "pci_slot": null,
                "ram_hot_plug": true,
                "size": 20.0,
                "ssh_keys": null,
                "type": "SSD Premium",
                "user_data": null
            },
            "type": "volume"
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).

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
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of the server.</td>
  </tr>
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
