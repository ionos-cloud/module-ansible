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
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| filters<br /><mark style="color:blue;">\<dict\></mark> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| registry<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of an existing Registry. |
| api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
| username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
