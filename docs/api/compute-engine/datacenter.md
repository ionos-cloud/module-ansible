# Datacenter

## Example Syntax

```yaml
    - name: Create datacenter
      datacenter:
        name: "{{ datacenter }}"
        description: "{{ description }}"
        location: de/fra
      register: datacenter_response

    - name: Update datacenter
      datacenter:
        id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ datacenter }}"
        description: "{{ description }} - RENAMED"
        state: update
      register: updated_datacenter

    - name: Debug - Show Updated Datacenter
      debug:
        msg: "{{ updated_datacenter }}"

    - name: Remove datacenter
      datacenter:
        id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ datacenter }}"
        state: absent
      register: deleted_datacenter
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes** | string |  | The name of the datacenter. |
| location | no | string | us/las | The datacenter location: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr |
| description | no | string |  | The description of the datacenter. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

