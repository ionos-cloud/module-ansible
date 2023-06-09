# target_group

This is a simple module that supports creating or removing Target Groups.

## Example Syntax


```yaml

  - name: Create Target Group
    target_group:
      name: "AnsibleAutoTestCompute"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      targets:
        - ip: "22.231.2.2"
          port: 8080
          weight: 123
          health_check_enabled: true
          maintenance_enabled: false
      health_check:
        check_timeout: 2000
        check_interval: 1000
        retries: 3
      http_health_check:
        path: "./"
        method: "GET"
        match_type: "STATUS_CODE"
        response: 200
        regex: false
        negate: false
      wait: true
    register: target_group_response
  

  - name: Update Target Group
    target_group:
      name: "AnsibleAutoTestCompute - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group: "AnsibleAutoTestCompute"
      wait: true
      state: update
    register: target_group_response_update
  

  - name: Remove Target Group
    target_group:
      target_group: "AnsibleAutoTestCompute - UPDATED"
      wait: true
      wait_timeout: 2000
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "target_group": {
        "href": "https://api.ionos.com/cloudapi/v6/targetgroups/5f757b12-776b-4ac0-befb-56499db09baf",
        "id": "5f757b12-776b-4ac0-befb-56499db09baf",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-06-06T10:01:58+00:00",
            "etag": "8f3a5c9d9ddd3ef6312b02d3bc9c319e",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-06-06T10:01:58+00:00",
            "state": "BUSY"
        },
        "properties": {
            "algorithm": "ROUND_ROBIN",
            "health_check": {
                "check_interval": 1000,
                "check_timeout": 2000,
                "retries": 3
            },
            "http_health_check": {
                "match_type": "STATUS_CODE",
                "method": "GET",
                "negate": false,
                "path": "./",
                "regex": false,
                "response": "200"
            },
            "name": "AnsibleAutoTestALB",
            "protocol": "HTTP",
            "targets": [
                {
                    "health_check_enabled": true,
                    "ip": "<IP>",
                    "maintenance_enabled": null,
                    "port": 8080,
                    "weight": 123
                }
            ]
        },
        "type": "target-group"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Target Group
    target_group:
      name: "AnsibleAutoTestCompute"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      targets:
        - ip: "22.231.2.2"
          port: 8080
          weight: 123
          health_check_enabled: true
          maintenance_enabled: false
      health_check:
        check_timeout: 2000
        check_interval: 1000
        retries: 3
      http_health_check:
        path: "./"
        method: "GET"
        match_type: "STATUS_CODE"
        response: 200
        regex: false
        negate: false
      wait: true
    register: target_group_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The target group name. |
  | algorithm | True | str |  | The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target. |
  | protocol | True | str |  | The forwarding protocol. Only the value 'HTTP' is allowed. |
  | health_check | False | dict |  | Health check properties for target group. |
  | http_health_check | False | dict |  | HTTP health check properties for target group. |
  | targets | False | list |  | Array of items in the collection. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
  
  - name: Remove Target Group
    target_group:
      target_group: "AnsibleAutoTestCompute - UPDATED"
      wait: true
      wait_timeout: 2000
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The target group name. |
  | target_group | True | str |  | The ID or name of the Target Group. |
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
  
  - name: Update Target Group
    target_group:
      name: "AnsibleAutoTestCompute - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group: "AnsibleAutoTestCompute"
      wait: true
      state: update
    register: target_group_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The target group name. |
  | algorithm | False | str |  | The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target. |
  | protocol | False | str |  | The forwarding protocol. Only the value 'HTTP' is allowed. |
  | health_check | False | dict |  | Health check properties for target group. |
  | http_health_check | False | dict |  | HTTP health check properties for target group. |
  | targets | False | list |  | Array of items in the collection. |
  | target_group | True | str |  | The ID or name of the Target Group. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
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
