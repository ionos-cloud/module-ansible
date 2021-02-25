# Volume

## Example Syntax

```text
    - name: Create datacenter
      datacenter:
          name: "{{ datacenter }}"
          location: "{{ location }}"

    - name: Create volumes
      volume:
        datacenter: "{{ datacenter }}"
        name: "{{ name }} %02d"
        count: 2
        size: 2
        availability_zone: ZONE_3
        auto_increment: yes
        wait_timeout: 600
        wait: true
        state: present

    - name: Update volumes
      volume:
        datacenter: "{{ datacenter }}"
        instance_ids:
          - "{{ name }} 01"
          - "{{ name }} 02"
        size: 5
        wait_timeout: 600
        wait: true
        state: update

    - name: Delete volumes
      volume:
        datacenter: "{{ datacenter }}"
        instance_ids:
          - "{{ name }} 01"
          - "{{ name }} 02"
        wait_timeout: 600
        state: absent

    - name: Remove datacenter
      datacenter:
        name: "{{ datacenter }}"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | **yes** | string |  | The datacenter in which to create the volume. |
| server | no | string |  | The server on which to attach the volume. |
| name | **yes**/no | string |  | The name of the volume. You can enumerate the names using auto\_increment. |
| size | no | integer | 10 | The size of the volume in GB. |
| bus | no | string | VIRTIO | The bus type of the volume: **VIRTIO**, IDE |
| image | no | string |  | The image alias, image UUID, or snapshot UUID for the volume. |
| image\_password | no | string |  | Password set for the administrative user. |
| ssh\_keys | no | list |  | Public SSH keys allowing access to the server. |
| disk\_type | no | string | HDD | The disk type of the volume: **HDD**, SSD |
| licence\_type | no | string | UNKNOWN | The licence type for the volume. This is used when the image is non-standard: LINUX, WINDOWS, **UNKNOWN**, OTHER, WINDOWS2016 |
| availability\_zone | no | string | AUTO | The storage availability zone assigned to the volume: **AUTO**, ZONE\_1, ZONE\_2, ZONE\_3 |
| count | no | integer | 1 | The number of volumes to create. |
| auto\_increment | no | boolean | true | Whether or not to increment created servers. |
| instance\_ids | **yes**/no | list |  | List of instance UUIDs or names. Required for `state='absent'` or `state='update'` to remove or update volumes. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environment variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the resource to be created before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

