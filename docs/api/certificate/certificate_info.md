# certificate_info

This is a simple module that supports listing uploaded Certificates

## Example Syntax


```yaml

    - name: List Certificates
        certificate_info:
        register: certificates_response
    - name: Show Certificates
        debug:
            var: certificates_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "58da84bd-5dea-4838-9c43-391b7c75124a",
            "type": "certificate",
            "href": "https://api.ionos.com/certificatemanager/certificates/58da84bd-5dea-4838-9c43-391b7c75124a",
            "metadata": {
                "etag": null,
                "created_date": "2023-05-29T13:48:11Z",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-05-29T13:48:11Z",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "state": "AVAILABLE"
            },
            "properties": {
                "name": "test_certificate",
                "certificate": "<CERTIFICATE>",
                "certificate_chain": null
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
