# Firewall rule

## Example Syntax

```text
    - name: Allow SSH access
      firewall_rule:
          datacenter: Example
          server: server01
          nic: nic01
          name: Allow SSH
          protocol: TCP
          source_ip: 0.0.0.0
          port_range_start: 22
          port_range_end: 22
          state: present
      with_items: "{{ private_nic.results }}"
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| datacenter | **yes** | string |  | The datacenter name or UUID in which to operate. |
| server | **yes** | string |  | The server name or UUID. |
| nic | **yes** | string |  | The NIC name or UUID. |
| name | **yes** | string |  | The name or UUID of the firewall rule. |
| protocol | no | string |  | The protocol of the firewall rule: TCP, UDP, ICMP, ANY |
| source\_mac | no | string |  | Only traffic originating from the MAC address is allowed. No value allows all source MAC addresses. |
| source\_ip | no | string |  | Only traffic originating from the IPv4 address is allowed. No value allows all source IPs. |
| target\_ip | no | string |  | In case the target NIC has multiple IP addresses, only traffic directed to the IP address of the NIC is allowed. No value allows all target IPs. |
| port\_range\_start | integer | string |  | Defines the start range of the allowed port if protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534 |
| port\_range\_end | integer | string |  | Defines the end range of the allowed port if the protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534 |
| icmp\_type | no | integer |  | Defines the allowed type if the protocol ICMP is chosen. No value allows all types: 0 to 254 |
| icmp\_code | no | integer |  | Defines the allowed code if protocol ICMP is chosen. No value allows all codes: 0 to 254 |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environment variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

