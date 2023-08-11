# volume_info

This is a simple module that supports listing volumes.

## Example Syntax


```yaml

    - name: Get all volumes for given datacenter
      volume_info:
        datacenter: "AnsibleDatacenter"
      register: volume_list_response
      
    - name: Get all volumes for given server
      volume_info:
        datacenter: "AnsibleDatacenter"
        server: "AnsibleServerName"
      register: volume_list_server_response

    - name: Show all volumes for the datacenter
      debug:
        var: volume_list_response

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The ID or name of the datacenter. |
| server<br /><mark style="color:blue;">\<str\></mark> | False | The ID or name of the server. |
| filters<br /><mark style="color:blue;">\<dict\></mark> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth<br /><mark style="color:blue;">\<int\></mark> | False | The depth used when retrieving the items.<br />Default: 1 |
| api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
| username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
