# cube_template

This is a simple module that supports retrieving one or more Cube templates

## Example Syntax


```yaml

    - name: List templates
      ionoscloudsdk.ionoscloud.cube_template:
        state: present
      register: template_list

    - name: Debug - Show Templates List
      debug:
        msg: "{{  template_list.template }}"

    - name: Get template by template id
      ionoscloudsdk.ionoscloud.cube_template:
        template_id: "{{ template_list.template['items'][0]['id'] }}"
      register: template_response

    - name: Debug - Show Template
      debug:
        msg: "{{ template_response.template }}"
  
```

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | template_id | False | str |  | The ID of the template. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | state | False | str | present | Indicate desired state of the resource. |
