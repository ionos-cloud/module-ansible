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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>scopes<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of scopes for the token</td>
  </tr>
  <tr>
  <td>expiry_date<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The expiry date for the token in iso format</td>
  </tr>
  <tr>
  <td>status<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The status of the token</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of your token.</td>
  </tr>
  <tr>
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>registry_token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing token.</td>
  </tr>
  <tr>
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

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

<table data-full-width="true">
  <thead>
    <tr>
      <th width="20%">Name</th>
      <th width="15%" align="center">Required</th>
      <th width="65%">Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>scopes<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of scopes for the token</td>
  </tr>
  <tr>
  <td>expiry_date<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The expiry date for the token in iso format</td>
  </tr>
  <tr>
  <td>status<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The status of the token</td>
  </tr>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of your token.</td>
  </tr>
  <tr>
  <td>registry_token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing token.</td>
  </tr>
  <tr>
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
