# Server

## Example

```text
    - name: Provision a server
      server:
         datacenter: "{{ datacenter }}"
         name: "{{ name }} %02d"
         auto_increment: true
         cores: 1
         ram: 1024
         availability_zone: ZONE_1
         volume_availability_zone: ZONE_3
         volume_size: 5
         cpu_family: AMD_OPTERON
         disk_type: HDD
         image: "{{ image }}"
         image_password: "{{ password }}"
         ssh_keys:
            - "{{ ssh_public_key }}"
         location: "{{ location }}"
         count: 1
         assign_public_ip: true
         remove_boot_volume: true
         wait: true
         wait_timeout: "{{ timeout }}"
         state: present

    - name: Update server
      server:
         datacenter: "{{ datacenter }}"
         instance_ids:
           - "{{ name }} 01"
         cores: 2
         ram: 2048
         wait_timeout: "{{ timeout }}"
         state: update

    - name: Stop server
      server:
         datacenter: "{{ datacenter }}"
         instance_ids:
           - "{{ name }} 01"
         wait_timeout: "{{ timeout }}"
         state: stopped

    - name: Start server
      server:
         datacenter: "{{ datacenter }}"
         instance_ids:
           - "{{ name }} 01"
         wait_timeout: "{{ timeout }}"
         state: running
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| auto\_increment | no | boolean | true | Whether or not to increment created servers. |
| count | no | integer | 1 | The number of servers to create. |
| name | **yes**/no | string |  | The name of the server\(s\). Required only for `state='present'`. |
| image | **yes**/no | string |  | The image alias or UUID for creating the server. Required only for `state='present'`. |
| image\_password | no | string |  | Password set for the administrative user. |
| ssh\_keys | no | list | none | List of public SSH keys allowing access to the server. |
| datacenter | **yes** | string | none | The datacenter where the server is located. |
| cores | no | integer | 2 | The number of CPU cores to allocate to the server. |
| ram | no | integer | 2048 | The amount of memory to allocate to the server. |
| cpu\_family | no | string | AMD\_OPTERON | The CPU family type of the server: **AMD\_OPTERON**, INTEL\_XEON, INTEL\_SKYLAKE |
| availability\_zone | no | string | AUTO | The availability zone assigned to the server: **AUTO**, ZONE\_1, ZONE\_2 |
| volume\_size | no | integer | 10 | The size in GB of the boot volume. |
| disk\_type | no | string | HDD | The type of disk the volume will use: **HDD**, SSD |
| volume\_availability\_zone | no | string | AUTO | The storage availability zone assigned to the volume: **AUTO**, ZONE\_1, ZONE\_2, ZONE\_3 |
| bus | no | string | VIRTIO | The bus type for the volume: **VIRTIO**, IDE |
| instance\_ids | **yes**/no | list |  | List of instance IDs or names. **Not required** for `state='present'`. |
| location | no | string | us/las | The datacenter location used only if the module creates a default datacenter: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr |
| assign\_public\_ip | no | boolean | false | This will assign the server to the public LAN. The LAN is created if no LAN exists with public Internet access. |
| lan | no | string / integer | 1 | The LAN ID / Name for the server. |
| nat | no | boolean | false | The private IP address has outbound access to the Internet. |
| nic\_ips | no | list | false | List of IPs to be set in the included NIC of the server. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environment variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the instance to be in state 'running' before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| remove\_boot\_volume | no | boolean | true | Remove the boot volume of the server being deleted. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, running, stopped, update |

\_\_

