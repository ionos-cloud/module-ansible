# user_info

This is a simple module that supports listing Users.

## Example Syntax


```yaml

    - name: Get all Users of a group
      user_info:
        group: "AnsibleIonosGroup"
      register: user_list_response

    - name: Get all Users
      user_info:
      register: all_user_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "users": [
        {
            "entities": {
                "groups": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/groups",
                    "id": "<USER_ID>/groups",
                    "items": null,
                    "type": "collection"
                },
                "owns": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/owns",
                    "id": "<USER_ID>/owns",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
            "id": "<USER_ID>",
            "metadata": {
                "created_date": "2023-02-09T16:26:34+00:00",
                "etag": "37a6259cc0c1dae299a7866489dff0bd",
                "last_login": null
            },
            "properties": {
                "active": true,
                "administrator": false,
                "email": "<EMAIL>",
                "firstname": "John",
                "force_sec_auth": false,
                "lastname": "Doe",
                "s3_canonical_user_id": "<s3_canonical_user_id>",
                "sec_auth_active": false
            },
            "type": "user"
        },
        {
            "entities": {
                "groups": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/groups",
                    "id": "<USER_ID>/groups",
                    "items": null,
                    "type": "collection"
                },
                "owns": {
                    "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/owns",
                    "id": "<USER_ID>/owns",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
            "id": "<USER_ID>",
            "metadata": {
                "created_date": "2023-08-03T14:07:59+00:00",
                "etag": "37a6259cc0c1dae299a7866489dff0bd",
                "last_login": null
            },
            "properties": {
                "active": true,
                "administrator": false,
                "email": "<EMAIL>",
                "firstname": "John1",
                "force_sec_auth": false,
                "lastname": "Doe",
                "s3_canonical_user_id": "<s3_canonical_user_id>",
                "sec_auth_active": false
            },
            "type": "user"
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
| group | False | str |  | The name or ID of the group. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
