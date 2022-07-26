# registry_info

This is a simple module that supports listing existing Registries

## Example Syntax


```yaml

    - name: List Registries
        registry_info:
        register: registries_response


    - name: Show Registries
        debug:
            var: registries_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | True | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
