# registry_token_info

This is a simple module that supports listing existing Registry Tokens

## Example Syntax


```yaml

    - name: List Registry Tokens
        registry_token_info:
            registry: "RegistryName"
        register: registry_tokens_response


    - name: Show Registry Tokens
        debug:
            var: registry_tokens_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "href": "",
            "id": "1e9f63b6-ff23-41ab-8f7e-57dd1008d6b5",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-29T13:51:29+00:00",
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "last_modified_date": null,
                "state": "enabled"
            },
            "properties": {
                "credentials": {
                    "password": "",
                    "username": "testRegistryToken"
                },
                "expiry_date": null,
                "name": "testRegistryToken",
                "scopes": [
                    {
                        "actions": [
                            "pull",
                            "push"
                        ],
                        "name": "nume",
                        "type": "repo"
                    }
                ],
                "status": "enabled"
            },
            "type": "token"
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| registry | True | str |  | The ID or name of an existing Registry. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
