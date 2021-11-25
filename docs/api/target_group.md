# Target Group

## Example Syntax

```text
    - name: Create Target Group
      target_group:
        name: "{{ name }}"
        algorithm: "ROUND_ROBIN"
        protocol: "HTTP"
        targets:
          - ip: "22.231.2.2"
            port: 8080
            weight: 123
            health_check:
              check: true
              check_interval: 2000
              maintenance: true
        health_check:
          check_timeout: 2000
          connect_timeout: 5000
          target_timeout: 50000
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

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The resource name \(only alphanumeric characters are acceptable\). Only required when state = 'present'. |
| algorithm | **yes**/no | string |  |  Algorithm for the balancing. Accepted values: ROUND_ROBIN, LEAST_CONNECTION, RANDOM, SOURCE_IP.Only required when state = 'present'. |
| protocol | **yes**/no | string |  | Protocol of the balancing. Accepted value: HTTP. Only required when state = 'present'. |
| targets | no | List of dicts containing: properties, port, weight, health_check. |  | The list of targets. |
| health_check | **yes**/no | Dict containing: check_timeout, connect_timeout, target_timeout, retries. | | Health check properties for target group. |
| http_health_check | **yes**/no | Dict containing: path, method, match_type, response, regex, negate. |  | HTTP health check properties for target group. |
| target_group_id | **yes**/no | string |  | The ID of the target group.  Required when state = 'update' or state = 'absent'. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |
