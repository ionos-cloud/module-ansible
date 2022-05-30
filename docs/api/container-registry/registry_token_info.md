# registry_token_info

This is a simple module that supports listing existing Registry Tokens

## Example Syntax


```yaml

    - name: List Registry Tokens
        registry_token_info:
        register: registry_tokens_response


    - name: Show Registry Tokens
        debug:
            var: registry_tokens_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| registry_id | True | str |  | The ID of an existing Registry. |
| api_url | False | str |  | The Ionos API base URL. |
| token | True | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |