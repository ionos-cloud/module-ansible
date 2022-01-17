# IpBlock

## Example Syntax

```yaml
    - name: Create ipblock
      ipblock:
        name:  "{{ name }}"
        location: "{{ location }}"
        size: 2
        state: present

    - name: Update ipblock
      ipblock:
        name: "{{ name }}"
        location: "{{ location }}"
        state: update

    - name: Remove ipblock
      ipblock:
        name: "{{ name }}"
        state: absent
      register: delete_result
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes** | string |  | The name of the IPBlock. |
| location | no | string | us/las | The IPBlock location: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr |
| size | no | integer | 1 | The number of IP addresses to allocate in the IPBlock. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicates desired state of the resource: **present**, absent |

