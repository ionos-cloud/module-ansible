# Cube template

## Example Syntax

```yaml
    - name: List templates
      cube_template:
        state: present
      register: template_list

    - name: Get template by template id
      cube_template:
        template_id: "{{ template_list.template['items'][0]['id'] }}"
      register: template_response

```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| template_id | no | string |  | The UUID of the template. If missing, the module will return all available templates.  |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| state | no | string | present | Indicate desired state of the resource: only **present** available. |

