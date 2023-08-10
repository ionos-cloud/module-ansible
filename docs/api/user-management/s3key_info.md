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
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| user<br /><span>\<str\></span> | True | The ID or email of the user |
| filters<br /><span>\<dict\></span> | False | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth<br /><span>\<int\></span> | False | The depth used when retrieving the items.<br />Default: 1 |
| api_url<br /><span>\<str\></span> | False | The Ionos API base URL. |
| certificate_fingerprint<br /><span>\<str\></span> | False | The Ionos API certificate fingerprint. |
| username<br /><span>\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span>\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span>\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
