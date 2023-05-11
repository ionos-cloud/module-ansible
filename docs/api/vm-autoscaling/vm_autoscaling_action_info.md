# vm_autoscaling_action_info

This is a simple module that supports listing existing VM Autoscaling Group Actions

## Example Syntax


```yaml

    - name: List VM Autoscaling Group Actions
        vm_autoscaling_action_info:
            vm_autoscaling_group: "{{ vm_autoscaling_group_response.vm_autoscaling_group.id }}"
        register: vm_autoscaling_actions_response

    - name: Show VM Autoscaling Group Actions
        debug:
            var: vm_autoscaling_actions_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| vm_autoscaling_group | False | str |  | The ID or name of an existing VM Autoscaling Group. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
