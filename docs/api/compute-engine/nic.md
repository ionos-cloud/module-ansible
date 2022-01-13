# Nic

## Example Syntax

```text
    - name: Create private NIC
      nic:
          datacenter: Example
          server: "{{ item.id }}"
          lan: 2
          state: present
      register: private_nic
      with_items: "{{ ionos.machines }}"

    - name: Update NIC
      nic:
        datacenter: Example
        server: "{{ item.id }}"
        name: 7341c2454f
        lan: 1
        ips:
          - 158.222.103.23
          - 158.222.103.24
        dhcp: false
        state: update
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | **yes** | string |  | The datacenter in which to operate. |
| server | **yes** | string |  | The server name or UUID. |
| name | no | string |  | The name of the NIC. |
| id | **yes** | string |  | The id of the NIC. |
| lan | **yes** | integer |  | The LAN to connect the NIC. The LAN will be created if it does not exist. Only required on creates. |
| dhcp | no | boolean |  | Indicates if the NIC is using DHCP or not. |
| nat | no | boolean |  | Allow the private IP address outbound Internet access. |
| firewall\_active | no | boolean |  | Indicates if the firewall is active. |
| ips | no | list |  | A list of IPs to be assigned to the NIC. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

