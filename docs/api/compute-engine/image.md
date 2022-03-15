# Image

## Example Syntax

```text
    - name: Update image
      ionoscloudsdk.ionoscloud.image:
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

    - name: Delete image
      ionoscloudsdk.ionoscloud.image:
        image_id: "916b10ea-be31-11eb-b909-c608708a73fa"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| image\_id | **yes**/no | string |  | The ID of the image. Only required when state = `update` |
| name | no | string |  | The resource name. |
| description | no | string |  | Human readable description. |
| cpu\_hot\_plug | no | boolean |  | Is capable of CPU hot plug \(no reboot required\). |
| cpu\_hot\_unplug | no | boolean |  | Is capable of CPU hot unplug \(no reboot required\). |
| ram\_hot\_plug | no | boolean |  | Is capable of memory hot plug \(no reboot required\). |
| ram\_hot\_unplug | no | boolean |  | Is capable of memory hot unplug \(no reboot required\). |
| nic\_hot\_plug | no | boolean |  | Is capable of nic hot plug \(no reboot required\). |
| nic\_hot\_unplug | no | boolean |  | Is capable of nic hot unplug \(no reboot required\). |
| disc\_scsi\_hot\_plug | no | boolean |  | Is capable of SCSI drive hot plug \(no reboot required\). |
| disc\_scsi\_hot\_unplug | no | boolean |  | Is capable of SCSI drive hot unplug \(no reboot required\). This works only for non-Windows virtual Machines.. |
| disc\_virtio\_hot\_plug | no | boolean |  | Is capable of Virt-IO drive hot plug \(no reboot required\). |
| disc\_virtio\_hot\_unplug | no | boolean |  | Is capable of Virt-IO drive hot unplug \(no reboot required\). This works only for non-Windows virtual Machines. |
| licence\_type | no | string |  | OS type of this Image. Accepted values: "UNKNOWN", "WINDOWS", "WINDOWS2016", "LINUX", "OTHER" |
| cloud\_init | no | string |  | Cloud init compatibility. Accepted values: "NONE", "V1" |

