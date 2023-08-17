# registry_token

This is a module that supports creating, updating or destroying Registry Tokens

## Example Syntax


```yaml
- name: Create Registry Token
    registry_token:
        registry: RegistryName
        name: test_registry_token
        scopes:
            - actions: 
                    - pull
                      push
                      delete
                name: repo1
                type: repositry
        status: enabled
        expiry_date: 2022-06-24T17:04:10+03:00
    register: registry_token_response
  
- name: Update Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        scopes:
            - actions: 
                    - pull
                name: repo2
                type: repositry
        status: disbled
        expiry_date: 2022-07-24T17:04:10+03:00
    register: updated_registry_token_response
  
- name: Delete Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "registry_token": {
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
                "password": "<PASSWORD>",
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
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Registry Token
    registry_token:
        registry: RegistryName
        name: test_registry_token
        scopes:
            - actions: 
                    - pull
                      push
                      delete
                name: repo1
                type: repositry
        status: enabled
        expiry_date: 2022-06-24T17:04:10+03:00
    register: registry_token_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | scopes | False | list |  | List of scopes for the token |
  | expiry_date | False | str |  | The expiry date for the token in iso format |
  | status | False | str |  | The status of the token |
  | name | True | str |  | The name of your token. |
  | registry | True | str |  | The ID or name of an existing Registry. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | registry_token | True | str |  | The ID or name of an existing token. |
  | registry | True | str |  | The ID or name of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update Registry Token
    registry_token:
        registry: RegistryName
        registry_token: test_registry_token
        scopes:
            - actions: 
                    - pull
                name: repo2
                type: repositry
        status: disbled
        expiry_date: 2022-07-24T17:04:10+03:00
    register: updated_registry_token_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | scopes | False | list |  | List of scopes for the token |
  | expiry_date | False | str |  | The expiry date for the token in iso format |
  | status | False | str |  | The status of the token |
  | name | False | str |  | The name of your token. |
  | registry_token | True | str |  | The ID or name of an existing token. |
  | registry | True | str |  | The ID or name of an existing Registry. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
