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
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
