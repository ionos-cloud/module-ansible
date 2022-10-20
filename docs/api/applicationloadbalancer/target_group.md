# target_group

This is a simple module that supports creating or removing Target Groups.

## Example Syntax


```yaml

  - name: Create Target Group
    target_group:
      name: "{{ name }}"
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
      name: "{{ name }} - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      state: update
    register: target_group_response_update
  

  - name: Remove Target Group
    target_group:
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      wait_timeout: 2000
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Target Group
    target_group:
      name: "{{ name }}"
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
  | name | True | str |  | The name of the Target Group. |
  | algorithm | True | str |  | Balancing algorithm. |
  | protocol | True | str |  | Balancing protocol. |
  | health_check | False | dict |  | Health check properties for target group. |
  | http_health_check | False | dict |  | HTTP health check properties for target group. |
  | targets | False | list |  | An array of items in the collection. |
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
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      wait_timeout: 2000
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Target Group. |
  | target_group_id | False | str |  | The ID of the Target Group. |
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
      name: "{{ name }} - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group_id: "{{ target_group_response.target_group.id }}"
      wait: true
      state: update
    register: target_group_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the Target Group. |
  | algorithm | False | str |  | Balancing algorithm. |
  | protocol | False | str |  | Balancing protocol. |
  | health_check | False | dict |  | Health check properties for target group. |
  | http_health_check | False | dict |  | HTTP health check properties for target group. |
  | targets | False | list |  | An array of items in the collection. |
  | target_group_id | False | str |  | The ID of the Target Group. |
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
