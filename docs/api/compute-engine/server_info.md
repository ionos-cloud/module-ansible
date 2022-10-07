# server_info

This is a simple module that supports listing servers.

## Example Syntax


```yaml

    - name: Get all servers for given datacenter
      server_info:
        datacenter: "{{ datacenter }}"
      register: server_list_response

    - name: Get only the servers that need to be upgraded
      server_info:
        datacenter: "{{ datacenter }}"
        upgrade_needed: true
      register: servers_list_upgrade_response

    - name: Show all servers for the created datacenter
      debug:
        var: server_list_response

    - name: Show servers that need an upgrade
      debug:
        var: servers_list_upgrade_response

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | True | str |  | The ID or name of the datacenter. |
| upgrade_needed | False | bool |  | Filter servers that can or that cannot be upgraded. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
