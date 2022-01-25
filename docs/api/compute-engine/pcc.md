# Private cross connect

## Example Syntax

```yaml
    - name: Create pcc
      pcc:
        name: "{{ name }}"
        description: "{{ description }}"

    - name: Update pcc
      pcc:
        pcc_id: "{{pcc.id}}"
        name: "{{ new_name }}"
        description: "{{ new_description }}"
        state: update

    - name: Remove pcc
      pcc:
        pcc_id: "{{pcc.id}}"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| pcc\_id | **yes**/no | string |  | The ID of the pcc. Required for state = 'update' or state = 'absent'. |
| name | **yes**/no | string |  | The name of the pcc. Required only for state = 'present'. |
| description | no | string |  | The description of the pcc. |

