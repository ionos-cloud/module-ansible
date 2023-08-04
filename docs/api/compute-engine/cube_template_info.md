# cube_template_info

This is a simple module that supports retrieving one or more Cube templates

## Example Syntax


```yaml

    - name: List templates
      cube_template:
        state: present
      register: template_list

    - name: Get template by template id
      cube_template:
        template_id: 9ab6545c-b138-4a86-b6ca-0d872a2b0953
      register: template_response
  
```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| template_id | False | str |  | The ID of the template. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
