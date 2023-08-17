# s3key_info

This is a simple module that supports listing S3Keys.

## Example Syntax


```yaml

    - name: List S3Keys for user
      s3key_info:
        user: <user_id/email>
        register: s3key_info_response

    - name: Show S3Keys
      debug:
        var: s3key_info_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "s3keys": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/s3keys/<ID>",
            "id": "<ID>",
            "metadata": {
                "created_date": "2023-08-03T14:09:10",
                "etag": "f245addf606d4e505be3ce87c622bf75"
            },
            "properties": {
                "active": true,
                "secret_key": "<SECRET_KEY>"
            },
            "type": "s3key"
        },
        {
            "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/s3keys/<ID>",
            "id": "<ID>",
            "metadata": {
                "created_date": "2023-08-03T14:09:11",
                "etag": "0c24df8cd19a7e35da34e4f4370f305a"
            },
            "properties": {
                "active": true,
                "secret_key": "<SECRET_KEY>"
            },
            "type": "s3key"
        }
    ],
    "failed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| user | True | str |  | The ID or email of the user |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
