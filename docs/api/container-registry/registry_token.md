# registry_token

This is a module that supports creating, updating or destroying Registry Tokens

## Example Syntax


```yaml
- name: Create Registry Token
    registry_token:
        registry_id: "{{ registry_id }}"
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
        registry_id: "{{ registry_id }}"
        name: test_registry_token
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
        registry_id: "{{ registry_id }}"
        name: test_registry_token
        state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Registry Token
    registry_token:
        registry_id: "{{ registry_id }}"
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
  | registry_id | True | str |  | The ID of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | True | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete Registry Token
    registry_token:
        registry_id: "{{ registry_id }}"
        name: test_registry_token
        state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of your token. |
  | token_id | False | str |  | The ID of an existing token. |
  | registry_id | True | str |  | The ID of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | True | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update Registry Token
    registry_token:
        registry_id: "{{ registry_id }}"
        name: test_registry_token
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
  | token_id | False | str |  | The ID of an existing token. |
  | registry_id | True | str |  | The ID of an existing Registry. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | True | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
