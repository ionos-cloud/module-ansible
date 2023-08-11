# server_info

This is a simple module that supports listing servers.

## Example Syntax


```yaml

    - name: Get all servers for given datacenter
      server_info:
        datacenter: AnsibleDatacenter
      register: server_list_response

    - name: Get only the servers that need to be upgraded
      server_info:
        datacenter: AnsibleDatacenter
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

| Name | Required | Description |
| :--- | :---: | :--- |
| datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the datacenter. |
| upgrade_needed<br /><mark style="color:blue;">\<bool\></mark> | False | Filter servers that can or that cannot be upgraded. |
| filters<br /><mark style="color:blue;">\<dict\></mark> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth<br /><mark style="color:blue;">\<int\></mark> | False | The depth used when retrieving the items.<br />Default: 1 |
| api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
| username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
