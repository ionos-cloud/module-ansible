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
| filters<br /><span class="blue-span">dict</span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| registry<br /><span class="blue-span">str</span> | True | The ID or name of an existing Registry. |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
