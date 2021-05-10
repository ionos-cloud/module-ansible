# Cube server

## Example Syntax

```text
    - name: Create Cube Server
      cube_server:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ name }}"
        template_uuid: "15c6dd2f-02d2-4987-b439-9a58dd59ecc3"
        volume_type: "DAS"
        wait: true
      register: cube_server_response

    - name: Update Cube Server
      cube_server:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        cube_server_id: "{{ cube_server_response.cube_server.id }}"
        name: "{{ name }} - UPDATED"
        wait: true
        state: update
      register: cube_server_response_update

    - name: Suspend Cube Server
      cube_server:
       cube_server_id: "{{ cube_server_response.cube_server.id }}"
       datacenter_id: "{{ datacenter_response.datacenter.id }}"
       wait: true
       state: suspend

    - name: Resume Cube Server
      cube_server:
       cube_server_id: "{{ cube_server_response.cube_server.id }}"
       datacenter_id: "{{ datacenter_response.datacenter.id }}"
       wait: true
       state: resume

    - name: Remove Cube Server
      cube_server:
       cube_server_id: "{{ cube_server_response.cube_server.id }}"
       datacenter_id: "{{ datacenter_response.datacenter.id }}"
       wait: true
       state: absent
    
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the server. Required only for state = 'present'. |
| template_uuid | **yes**/no | string |  | The UUID of the template for creating a CUBE server; the available templates for CUBE servers can be found on the templates resource. Required only for state = 'present'. |
| cores |  **yes**/no  | string |  | The total number of cores for the server. Required only for state = 'present'. |
| ram |  **yes**/no  | string |  | The amount of memory for the server in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB. Required only for state = 'present'. |
| availability_zone |  **yes**/no  | string |  | The availability zone in which the server should exist. Accepted values: "AUTO", "ZONE_1", "ZONE_2". Required only for state = 'present'. |
| vm_state |  **yes**/no  | string |  | Status of the virtual Machine. Values: "NOSTATE", "RUNNING", "BLOCKED", "PAUSED", "SHUTDOWN", "SHUTOFF", "CRASHED". Required only for state = 'present'. |
| boot_cdrom |  **yes**/no  | string |  | The boot CDROM. Required only for state = 'present'. |
| boot_volume |  **yes**/no  | string |  | The volume to boot. Required only for state = 'present'. |
| cpu_family |  **yes**/no  | string |  | CPU architecture on which server gets provisioned; not all CPU architectures are available in all datacenter regions; available CPU architectures can be retrieved from the datacenter resource. Required only for state = 'present'. |
| volume_size |  **yes**/no  | string |  | The size of the volume. Required only for state = 'present'. |
| volume_type |  **yes**/no  | string |  | The type of the volume. Accepted values: "HDD", "SSD", "SSD Standard", "SSD Premium", "DAS". Required only for state = 'present'. |
| datacenter_id | **yes** | string |  | The ID of the datacenter. |
| cube_server_id | **yes**/no | string |  | The ID of the CUBE server. Required when state = 'update',  state = 'absent',  state = 'resume',  state = 'suspend'. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update, suspend, resume |

