# Group

## Example Syntax

```text
    - name: Create group
      group:
        name: guests
        create_datacenter: true
        create_snapshot: true
        reserve_ip: true
        access_activity_log: false

    - name: Update group
      group:
        name: guests
        create_datacenter: false
        users:
          - john.smith@test.com
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes** | string |  | The name of the group. |
| create\_datacenter | no | boolean |  | Indicates if the group is allowed to create virtual data centers. |
| create\_snapshot | no | boolean |  | Indicates if the group is allowed to create snapshots. |
| reserve\_ip | no | boolean |  | Indicates if the group is allowed to reserve IP addresses. |
| access\_activity\_log | no | boolean |  | Indicates if the group is allowed to access the activity log. |
| users | no | list |  | A list of \(non-administrator\) user IDs or emails to associate with the group. Set to empty list \(`[]`\) to remove all users from the group. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

