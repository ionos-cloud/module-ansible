# snapshot_info

This is a simple module that supports listing Snapshots.

## Example Syntax


```yaml

name: List Snapshots
ionoscloudsdk.ionoscloud.snapshot_info: null
register: snapshot_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "snapshots": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/snapshots/1f18a6ff-6365-4704-88d8-75cd9387aab7",
            "id": "1f18a6ff-6365-4704-88d8-75cd9387aab7",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T11:49:41+00:00",
                "etag": "6d66d25257bbcc92d4f4980309d7a073",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T11:49:41+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "cpu_hot_plug": true,
                "cpu_hot_unplug": false,
                "description": "Ansible test snapshot",
                "disc_scsi_hot_plug": false,
                "disc_scsi_hot_unplug": false,
                "disc_virtio_hot_plug": true,
                "disc_virtio_hot_unplug": true,
                "licence_type": "UNKNOWN",
                "location": "gb/lhr",
                "name": "AnsibleAutoTestCompute",
                "nic_hot_plug": true,
                "nic_hot_unplug": true,
                "ram_hot_plug": true,
                "ram_hot_unplug": false,
                "sec_auth_protection": false,
                "size": 10.0
            },
            "type": "snapshot"
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
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of properties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
