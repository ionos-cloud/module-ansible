# s3key

This is a simple module that supports creating or removing S3Keys.

## Example Syntax


```yaml

  - name: Create an s3key
    s3key:
      user: <user_id/email>
  

  - name: Update an s3key
    s3key:
      user: <user_id/email>
      key_id: "00ca413c94eecc56857d
      active: False
      state: update
  

  - name: Remove an s3key
    s3key:
      user: <user_id/email>
      key_id: 00ca413c94eecc56857d
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "s3key": {
        "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>/s3keys/<ID>",
        "id": "<ID>",
        "metadata": {
            "created_date": "2023-05-31T13:49:52",
            "etag": "26c5aad97d5bb95cc0c1ed99addde9fe"
        },
        "properties": {
            "active": true,
            "secret_key": "<SECRET_KEY>"
        },
        "type": "s3key"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create an s3key
    s3key:
      user: <user_id/email>
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | active<br /><mark style="color:blue;">\<bool\></mark> | False | Denotes weather the S3 key is active. |
  | user<br /><mark style="color:blue;">\<str\></mark> | True | The ID or email of the user |
  | key_id<br /><mark style="color:blue;">\<str\></mark> | False | The ID of the S3 key. |
  | idempotency<br /><mark style="color:blue;">\<bool\></mark> | False | Flag that dictates respecting idempotency. If an s3key already exists, returns with already existing key instead of creating more.<br />Default: False<br />Options: [True, False] |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Remove an s3key
    s3key:
      user: <user_id/email>
      key_id: 00ca413c94eecc56857d
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | user<br /><mark style="color:blue;">\<str\></mark> | True | The ID or email of the user |
  | key_id<br /><mark style="color:blue;">\<str\></mark> | True | The ID of the S3 key. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update an s3key
    s3key:
      user: <user_id/email>
      key_id: "00ca413c94eecc56857d
      active: False
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | active<br /><mark style="color:blue;">\<bool\></mark> | False | Denotes weather the S3 key is active. |
  | user<br /><mark style="color:blue;">\<str\></mark> | True | The ID or email of the user |
  | key_id<br /><mark style="color:blue;">\<str\></mark> | True | The ID of the S3 key. |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update'] |

&nbsp;

&nbsp;
