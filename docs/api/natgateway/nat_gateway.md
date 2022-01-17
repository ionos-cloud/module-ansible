# NAT Gateway

## Example Syntax

```yaml

    - name: Create NAT Gateway
      nat_gateway:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ name }}"
        public_ips: "{{ ipblock_response_create.ipblock.properties.ips }}"
        lans:
          - id: "{{ lan_response.lan.id }}"
            gateway_ips: "10.11.2.5/24"
        wait: true
      register: nat_gateway_response

    - name: Update NAT Gateway
      nat_gateway:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ name }} - UPDATED"
        public_ips: "{{ ipblock_response_update.ipblock.properties.ips }}"
        nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
        wait: true
        state: update
      register: nat_gateway_response_update

    - name: Remove NAT Gateway
      nat_gateway:
       nat_gateway_id: "{{ nat_gateway_response.nat_gateway.id }}"
       datacenter_id: "{{ datacenter_response.datacenter.id }}"
       wait: true
       wait_timeout: 2000
       state: absent
    
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes** | string |  | The name of the NAT Gateway. |
| datacenter_id | **yes** | string | | The ID of the datacenter |
| nat_gateway_id | **yes**/no | string |  | The ID of the NAT Gateway. Required when state = 'update' or state = 'absent'. |
| lans | no | string |  | Collection of LANs connected to the NAT gateway. IPs must contain valid subnet mask. If user will not provide any IP then system will generate an IP with /24 subnet. |
| public_ips | **yes**/no | string |  | Collection of public IP addresses of the NAT gateway. Should be customer reserved IP addresses in that location. Required only for state = 'present'. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

