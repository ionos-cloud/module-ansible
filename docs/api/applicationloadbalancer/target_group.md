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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:#003d8f">str</span> | True | The target group name. |
  | algorithm<br /><span style="color:#003d8f">str</span> | True | The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target. |
  | protocol<br /><span style="color:#003d8f">str</span> | True | The forwarding protocol. Only the value 'HTTP' is allowed. |
  | health_check<br /><span style="color:#003d8f">dict</span> | False | Health check properties for target group. |
  | http_health_check<br /><span style="color:#003d8f">dict</span> | False | HTTP health check properties for target group. |
  | targets<br /><span style="color:#003d8f">list</span> | False | Array of items in the collection. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:#003d8f">str</span> | False | The target group name. |
  | target_group<br /><span style="color:#003d8f">str</span> | True | The ID or name of the Target Group. |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span style="color:#003d8f">str</span> | False | The target group name. |
  | algorithm<br /><span style="color:#003d8f">str</span> | False | The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target. |
  | protocol<br /><span style="color:#003d8f">str</span> | False | The forwarding protocol. Only the value 'HTTP' is allowed. |
  | health_check<br /><span style="color:#003d8f">dict</span> | False | Health check properties for target group. |
  | http_health_check<br /><span style="color:#003d8f">dict</span> | False | HTTP health check properties for target group. |
  | targets<br /><span style="color:#003d8f">list</span> | False | Array of items in the collection. |
  | target_group<br /><span style="color:#003d8f">str</span> | True | The ID or name of the Target Group. |
  | do_not_replace<br /><span style="color:#003d8f">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
