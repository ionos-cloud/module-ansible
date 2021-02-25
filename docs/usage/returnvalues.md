# Return values

## create

For create operations, the module returns a dict containing:

| Name | Value | Description |
| :--- | :--- | :--- |
| action | always **create** | The name of the current action |
| change | `True` or `False` | If the task made changes within the resources |
| failed | `True` or `False` | If the task failed |
| resource | The current resource | The key contains the resource name and the value is a dictionary containing the current resource. |

Example for datacenter resource:

```text
{
    "action": "create",
    "changed": false,
    "datacenter": {
        "entities": {},
        "href": "https://api.ionos.com/cloudapi/v5/datacenters/3f0a326d-5a51-4a4e-bd9c-a4c8d9df06f7",
        "id": "3f0a326d-5a51-4a4e-bd9c-a4c8d9df06f7",
        "metadata": {},
        "properties": {
            "description": null,
            "features": [
                "SSD"
            ],
            "location": "de/fra",
            "name": "ANSIBLE TEST",
            "sec_auth_protection": false,
            "version": 6
        },
        "type": "datacenter"
    },
    "failed": false
}
```

## update

For update operations, the module returns a dict containing:

| Name | Value | Description |
| :--- | :--- | :--- |
| action | always **update** | The name of the current action |
| change | `True` or `False` | If the task made changes within the resources |
| failed | `True` or `False` | If the task failed |
| resource | The current resource | The key contains the resource name and the value is a dictionary containing the current resource. |

Example for datacenter resource:

```text
{
    "action": "update",
    "changed": true,
    "datacenter": {
        "entities": {},
        "href": "https://api.ionos.com/cloudapi/v5/datacenters/3f0a326d-5a51-4a4e-bd9c-a4c8d9df06f7",
        "id": "3f0a326d-5a51-4a4e-bd9c-a4c8d9df06f7",
        "metadata": {},
        "properties": {
            "description": "Ansible test description 2 - RENAMED",
            "features": [
                "SSD"
            ],
            "location": "de/fra",
            "name": "ANSIBLE TEST",
            "sec_auth_protection": false,
            "version": 6
        },
        "type": "datacenter"
    },
    "failed": false
}
```

## delete

For delete operations, the module returns a dict containing:

| Name | Value | Description |
| :--- | :--- | :--- |
| action | always **delete** | The name of the current action |
| change | `True` or `False` | If the task made changes within the resources |
| failed | `True` or `False` | If the task failed |
| id | The id of the resource |  |

Example for datacenter resource:

```text
{
    "action": "delete",
    "changed": true,
    "failed": false,
    "id": "a8ddad52-bc71-439d-9f56-fc2c103af8f2"
}
```

