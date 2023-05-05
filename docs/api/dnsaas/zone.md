# zone

This is a simple module that supports creating or removing zones. This module has a dependency on ionoscloud-dnsaas &gt;= 1.0.0

## Example Syntax


```yaml

  - name: Create Zone
    zone:
      name: "{{ zone_name }}"
      description: "{{ zone_description }}"
      enabled: "{{ zone_enabled }}"
    register: zone_response
  

  - name: Update Zone
    zone:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ zone_name_update }}"
      description: "{{ zone_description_update }}"
      enabled: "{{ zone_enabled_update }}"
      state: update
    register: updated_zone_response
  

  - name: Delete Zone
    zone:
      zone: "{{ zone_response.zone.properties.zone_name }}"
      wait: true
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Zone
    zone:
      name: "{{ zone_name }}"
      description: "{{ zone_description }}"
      enabled: "{{ zone_enabled }}"
    register: zone_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the zone. |
  | description | False | str |  | The description of the zone. |
  | enabled | False | bool |  | Whether the zone is enabled. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
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
  
  - name: Delete Zone
    zone:
      zone: "{{ zone_response.zone.properties.zone_name }}"
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | zone | True | str |  | The ID or name of the zone. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Zone
    zone:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ zone_name_update }}"
      description: "{{ zone_description_update }}"
      enabled: "{{ zone_enabled_update }}"
      state: update
    register: updated_zone_response
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the zone. |
  | description | False | str |  | The description of the zone. |
  | enabled | False | bool |  | Whether the zone is enabled. |
  | zone | True | str |  | The ID or name of the zone. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
