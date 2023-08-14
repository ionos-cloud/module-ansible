# nat_gateway

This is a simple module that supports creating or removing NATGateways. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Create NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: NATGatewayName
      public_ips:
        - <ip1>
        - <ip2>
      lans:
        - id: 1
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  

  - name: Update NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: "NATGatewayName - UPDATED"
      public_ips:
        - <ip1>
        - <ip2>
      nat_gateway: NATGatewayName
      wait: true
      state: update
    register: nat_gateway_response_update
  

  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway: NATGatewayName
      datacenter: DatacenterName
      wait: true
      wait_timeout: 2000
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "action": "create",
    "nat_gateway": {
        "entities": {
            "flowlogs": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0/flowlogs",
                "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0/flowlogs",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "rules": {
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0/rules",
                "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0/rules",
                "items": null,
                "type": "collection"
            }
        },
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/0406692b-b25f-4a58-8b41-e3b2d761447c/natgateways/abcc8593-a4a9-4ea0-b63c-04f95f395aa0",
        "id": "abcc8593-a4a9-4ea0-b63c-04f95f395aa0",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T11:46:08+00:00",
            "etag": "f64f5fbd951032447f9e9a9b0d7ab1a2",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T11:46:08+00:00",
            "state": "AVAILABLE"
        },
        "properties": {
            "lans": [],
            "name": "AnsibleAutoTestNAT",
            "public_ips": [
                "<IP1>",
                "<IP2>"
            ]
        },
        "type": "natgateway"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: NATGatewayName
      public_ips:
        - <ip1>
        - <ip2>
      lans:
        - id: 1
          gateway_ips: "10.11.2.5/24"
      wait: true
    register: nat_gateway_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | Name of the NAT Gateway. |
  | public_ips | True | list |  | Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location. |
  | lans | False | list |  | Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Remove NAT Gateway
    nat_gateway:
      nat_gateway: NATGatewayName
      datacenter: DatacenterName
      wait: true
      wait_timeout: 2000
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | Name of the NAT Gateway. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | nat_gateway | True | str |  | The ID or name of the NAT Gateway. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update NAT Gateway
    nat_gateway:
      datacenter: DatacenterName
      name: "NATGatewayName - UPDATED"
      public_ips:
        - <ip1>
        - <ip2>
      nat_gateway: NATGatewayName
      wait: true
      state: update
    register: nat_gateway_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | Name of the NAT Gateway. |
  | public_ips | False | list |  | Collection of public IP addresses of the NAT Gateway. Should be customer reserved IP addresses in that location. |
  | lans | False | list |  | Collection of LANs connected to the NAT Gateway. IPs must contain a valid subnet mask. If no IP is provided, the system will generate an IP with /24 subnet. |
  | datacenter | True | str |  | The ID or name of the datacenter. |
  | nat_gateway | True | str |  | The ID or name of the NAT Gateway. |
  | allow_replace | False | bool | False | Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
