# S3key

## Example Syntax

```text
    - name: Create an s3key
      s3key:
        user_id: "{{ user_id }}"

    - name: Update an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        active: False
        state: update

    - name: Remove an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        state: absent
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| user\_id | **yes** | string |  | The unique ID of the user. |
| key\_id | **yes** | string |  | The ID of the key. Required only for state = 'update' or state = 'absent' |
| active | no | boolean |  | State of the key. |

