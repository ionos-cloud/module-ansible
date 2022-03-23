# s3key

This is a simple module that supports creating or removing S3Keys.

## Example Syntax


```yaml

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
&nbsp;

&nbsp;

# state: **present**
```yaml
<<<<<<< HEAD
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
=======
  
  - name: Create an s3key
    s3key:
      user_id: "{{ user_id }}"
  
>>>>>>> 00db8fa... feat: generate docs (#61)
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | active | False | bool |  | Denotes weather the S3 key is active. |
  | user_id | True | str |  | The ID of the user |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | idempotency | False | bool | False | If a key already exists, don't create any more on further requests. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Remove an s3key
    s3key:
      user_id: "{{ user_id }}"
      key_id: "00ca413c94eecc56857d"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | user_id | True | str |  | The ID of the user |
  | key_id | True | str |  | The ID of the S3 key. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update an s3key
    s3key:
      user_id: "{{ user_id }}"
      key_id: "00ca413c94eecc56857d"
      active: False
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | active | False | bool |  | Denotes weather the S3 key is active. |
  | user_id | True | str |  | The ID of the user |
  | key_id | True | str |  | The ID of the S3 key. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
