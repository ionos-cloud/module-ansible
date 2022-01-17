# Snapshot

## Example Syntax

```yaml
    - name: Create snapshot
      snapshot:
        datacenter: production DC
        volume: master
        name: boot volume snapshot

    - name: Restore snapshot
      snapshot:
        datacenter: production DC
        volume: slave
        name: boot volume snapshot
        state: restore
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | **yes**/no | string |  | The datacenter in which the volume resides. Required for `state='present'` or `state='restore'` to create or restore a snapshot. |
| volume | **yes**/no | string |  | The volume to create or restore the snapshot. Required for `state='present'` or `state='restore'`. |
| name | **yes**/no | string |  | The name of the snapshot. Required for `state='update'` or `state='absent'` to update or remove a snapshot. |
| description | no | string |  | The description of the snapshot. |
| licence\_type | no | string |  | The licence type for the volume. This is used when updating the snapshot: LINUX, WINDOWS, UNKNOWN, OTHER, WINDOWS2016 |
| cpu\_hot\_plug | no | boolean |  | Indicates the volume is capable of CPU hot plug \(no reboot required\). |
| cpu\_hot\_unplug | no | boolean |  | Indicates the volume is capable of CPU hot unplug \(no reboot required\). |
| ram\_hot\_plug | no | boolean |  | Indicates the volume is capable of memory hot plug. |
| ram\_hot\_unplug | no | boolean |  | Indicates the volume is capable of memory hot unplug. |
| nic\_hot\_plug | no | boolean |  | Indicates the volume is capable of NIC hot plug. |
| nic\_hot\_unplug | no | boolean |  | Indicates the volume is capable of NIC hot unplug. |
| disc\_virtio\_hot\_plug | no | boolean |  | Indicates the volume is capable of VirtIO drive hot plug. |
| disc\_virtio\_hot\_unplug | no | boolean |  | Indicates the volume is capable of VirtIO drive hot unplug. |
| disc\_scsi\_hot\_plug | no | boolean |  | Indicates the volume is capable of SCSI drive hot plug. |
| disc\_scsi\_hot\_unplug | no | boolean |  | Indicates the volume is capable of SCSI drive hot unplug. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environment variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the resource to be created before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, restore, update |

