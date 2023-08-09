# nic_flowlog_info

This is a simple module that supports listing Flowlogs.

## Example Syntax


```yaml

    - name: Get all Flowlogs for a NIC
      nic_flowlog_info:
        datacenter: "AnsibleDatacenter"
        server: "AnsibleServer"
        nic: "AnsibleNic"
      register: flowlog_list_response

```


&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | True | str |  | The ID or name of the datacenter. |
| server | True | str |  | The ID or name of the Server. |
| nic | True | str |  | The ID or name of an existing NIC. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
