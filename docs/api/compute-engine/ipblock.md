# ipblock

This module allows you to create or remove an IPBlock.

## Example Syntax


```yaml
# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  
# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
    state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name or ID of the IPBlock. |
  | location | True | str | us/las | The IP Block location. |
  | size | False | int | 1 | The number of IP addresses to allocate in the IPBlock. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    name: staging
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name or ID of the IPBlock. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
