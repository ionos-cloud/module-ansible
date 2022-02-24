# Share

## Example Syntax

```text
    - name: Create shares
      ionoscloudsdk.ionoscloud.share:
        group: Demo
        edit_privilege: true
        share_privilege: true
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
          - ba7efccb-a761-11e7-90a7-525400f64d8d
        state: present

    - name: Update shares
      ionoscloudsdk.ionoscloud.share:
        group: Demo
        edit_privilege: false
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| group | **yes** | string |  | The name or ID of the group. |
| resource\_ids | **yes** | list |  | A list of resource IDs to add, update or remove as shares. |
| edit\_privilege | no | boolean |  | Indicates that the group has permission to edit privileges on the resource. |
| share\_privilege | no | boolean |  | Indicates that the group has permission to share the resource. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

