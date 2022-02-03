# Lan

## Example Syntax

```yaml
    - name: Create public LAN
      ionoscloudsdk.ionoscloud.lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        state: present

    - name: Update LAN
      ionoscloudsdk.ionoscloud.lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        ip_failover:
            - ip: "158.222.102.93"
              nic_uuid: "{{ nic.id }}"
            - ip: "158.222.102.94"
              nic_uuid: "{{ nic.id }}"
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | **yes** | string |  | The datacenter in which to operate. |
| name | **yes** | string |  | The name of the LAN. |
| public | no | boolean | true | If true, the LAN will have public Internet access. |
| ip\_failover | no | list |  | The IP failover list of group dictionaries containing IP addresses and NIC UUIDs. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

