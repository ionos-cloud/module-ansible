# s3key_info

This is a simple module that supports listing S3Keys.

## Example Syntax


```yaml

    - name: List S3Keys for user
      s3key_info:
        user_id: "{{ user_id }}"
        register: s3key_info_response

    - name: Show S3Keys
      debug:
        var: s3key_info_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| user_id | True | str |  | The ID of the user |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
