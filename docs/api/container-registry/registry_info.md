# registry_info

This is a simple module that supports listing existing Registries

⚠️ **Note:** Container Registry is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

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
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
