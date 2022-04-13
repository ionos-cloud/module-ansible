# volume_info

This is a simple module that supports listing volumes.

## Example Syntax


```yaml

    - name: Get all volumes for given datacenter
      volume_info:
        datacenter: "{{ datacenter }}"
      register: volume_list_response

    - name: Show all volumes for the datacenter
      debug:
        var: volume_list_response

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | True | str |  | The ID or name of the datacenter. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
