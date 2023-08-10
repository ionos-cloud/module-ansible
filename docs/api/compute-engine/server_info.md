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
| datacenter<br /><span class="blue-span">str</span> | True | The ID or name of the datacenter. |
| upgrade_needed<br /><span class="blue-span">bool</span> | False | Filter servers that can or that cannot be upgraded. |
| filters<br /><span class="blue-span">dict</span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth<br /><span class="blue-span">int</span> | False | The depth used when retrieving the items.<br />Default: 1 |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><span class="blue-span">str</span> | False | The Ionos API certificate fingerprint. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
