# share_info

This is a simple module that supports listing Shares.

## Example Syntax


```yaml

    - name: Get all Shares of a group
      share_info:
        group: "AnsibleIonosGroup"
      register: share_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "shares": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/0e191818-5dd6-4248-b226-a0c863c71d03/shares/82ad5ad2-7f10-4c2f-ad22-6ae36575f730",
            "id": "82ad5ad2-7f10-4c2f-ad22-6ae36575f730",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/groups/0e191818-5dd6-4248-b226-a0c863c71d03/shares/b22cf038-aa2a-4806-a2c1-2a4e3507c37a",
            "id": "b22cf038-aa2a-4806-a2c1-2a4e3507c37a",
            "properties": {
                "edit_privilege": true,
                "share_privilege": true
            },
            "type": "resource"
        }
    ],
    "failed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| group | True | str |  | The name or ID of the group. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
