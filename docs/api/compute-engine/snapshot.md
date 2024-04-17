# snapshot

This module allows you to create or remove a snapshot.

## Example Syntax


```yaml

name: Create snapshot
ionoscloudsdk.ionoscloud.snapshot:
  datacenter: 'AnsibleAutoTestCompute'
  volume: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  description: Ansible test snapshot
  wait_timeout: 600
register: result


name: Update snapshot
ionoscloudsdk.ionoscloud.snapshot:
  snapshot: 'AnsibleAutoTestCompute'
  description: Ansible test snapshot - RENAME
  state: update


name: Restore snapshot
ionoscloudsdk.ionoscloud.snapshot:
  datacenter: 'AnsibleAutoTestCompute'
  volume: 'AnsibleAutoTestCompute'
  snapshot: 'AnsibleAutoTestCompute'
  state: restore


name: Delete snapshot
ionoscloudsdk.ionoscloud.snapshot:
  snapshot: 'AnsibleAutoTestCompute'
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
    "action": "create",
    "snapshot": {
        "href": "https://api.ionos.com/cloudapi/v6/snapshots/c77c9be7-fb6d-4747-ac3d-a8489d8499d1",
        "id": "c77c9be7-fb6d-4747-ac3d-a8489d8499d1",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-29T12:57:58+00:00",
            "etag": "f47933bc5bead5ca05821105dc943e9f",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-29T12:57:58+00:00",
            "state": "BUSY"
        },
        "properties": {
            "cpu_hot_plug": false,
            "cpu_hot_unplug": false,
            "description": "Ansible test snapshot",
            "disc_scsi_hot_plug": false,
            "disc_scsi_hot_unplug": false,
            "disc_virtio_hot_plug": false,
            "disc_virtio_hot_unplug": false,
            "licence_type": "UNKNOWN",
            "location": "gb/lhr",
            "name": "AnsibleAutoTestCompute",
            "nic_hot_plug": false,
            "nic_hot_unplug": false,
            "ram_hot_plug": false,
            "ram_hot_unplug": false,
            "sec_auth_protection": false,
            "size": 10.0
        },
        "type": "snapshot"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create snapshot
ionoscloudsdk.ionoscloud.snapshot:
  datacenter: 'AnsibleAutoTestCompute'
  volume: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  description: Ansible test snapshot
  wait_timeout: 600
register: result

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
  <td>The datacenter in which the volumes reside.</td>
  </tr>
  <tr>
  <td>volume<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or UUID of the volume.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Human-readable description.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete snapshot
ionoscloudsdk.ionoscloud.snapshot:
  snapshot: 'AnsibleAutoTestCompute'
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
  <td>snapshot<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing snapshot.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update snapshot
ionoscloudsdk.ionoscloud.snapshot:
  snapshot: 'AnsibleAutoTestCompute'
  description: Ansible test snapshot - RENAME
  state: update

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
  <td>snapshot<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing snapshot.</td>
  </tr>
  <tr>
  <td>licence_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>OS type of this snapshot<br />Options: ['UNKNOWN', 'WINDOWS', 'WINDOWS2016', 'WINDOWS2022', 'RHEL', 'LINUX', 'OTHER']</td>
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
  <td>Is capable of SCSI drive hot unplug (no reboot required). This works only for non-Windows virtual Machines.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **restore**
```yaml
  
name: Restore snapshot
ionoscloudsdk.ionoscloud.snapshot:
  datacenter: 'AnsibleAutoTestCompute'
  volume: 'AnsibleAutoTestCompute'
  snapshot: 'AnsibleAutoTestCompute'
  state: restore

```
### Available parameters for state **restore**:
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
  <td>The datacenter in which the volumes reside.</td>
  </tr>
  <tr>
  <td>volume<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or UUID of the volume.</td>
  </tr>
  <tr>
  <td>snapshot<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing snapshot.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'restore']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
