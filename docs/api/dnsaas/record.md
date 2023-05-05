# record

This is a simple module that supports creating or removing records. This module has a dependency on ionoscloud-dnsaas &gt;= 1.0.0

## Example Syntax


```yaml

    - name: Create Record
    record:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ record_name }}"
      type: "{{ record_type }}"
      content: "{{ record_content }}"
      enabled: "{{ record_enabled }}"
      ttl: "{{ record_ttl }}"
      priority: "{{ record_priority }}"
    register: record_response
  

  - name: Update Record
    record:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ record_name_update }}"
      type: "{{ record_type_update }}"
      content: "{{ record_content_update }}"
      enabled: "{{ record_enabled_update }}"
      ttl: "{{ record_ttl_update }}"
      priority: "{{ record_priority_update }}"
    register: record_response_update
  
# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Delete Record
    record:
      zone: "{{ zone_response.zone.id }}"
      record: "{{ record_response_update.record.id }}"
      wait: true
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
    - name: Create Record
    record:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ record_name }}"
      type: "{{ record_type }}"
      content: "{{ record_content }}"
      enabled: "{{ record_enabled }}"
      ttl: "{{ record_ttl }}"
      priority: "{{ record_priority }}"
    register: record_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | zone | True | str |  | The ID or name of the zone. |
  | name | True | str |  | The name of the record. |
  | content | True | str |  | The content of the record. |
  | type | True | str |  | Holds supported DNS resource record types. In the DNS context a record is a DNS resource record. The options are: ['A', 'AAAA', 'CNAME', 'ALIAS', 'MX', 'NS', 'SRV', 'TXT', 'CAA', 'SSHFP', 'TLSA', 'SMIMEA', 'DS', 'HTTPS', 'SVCB', 'OPENPGPKEY', 'CERT', 'URI', 'RP', 'LOC'] |
  | ttl | False | int |  | Time to live for the record, recommended 3600. |
  | priority | False | int |  | Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI record types and ignored for all other types. |
  | enabled | False | bool |  | When true - the record is visible for lookup. |
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
  # Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Delete Record
    record:
      zone: "{{ zone_response.zone.id }}"
      record: "{{ record_response_update.record.id }}"
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | zone | True | str |  | The ID or name of the zone. |
  | record | True | str |  | The ID or name of the record. |
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
  
  - name: Update Record
    record:
      zone: "{{ zone_response.zone.id }}"
      name: "{{ record_name_update }}"
      type: "{{ record_type_update }}"
      content: "{{ record_content_update }}"
      enabled: "{{ record_enabled_update }}"
      ttl: "{{ record_ttl_update }}"
      priority: "{{ record_priority_update }}"
    register: record_response_update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | zone | True | str |  | The ID or name of the zone. |
  | name | False | str |  | The name of the record. |
  | content | False | str |  | The content of the record. |
  | type | False | str |  | Holds supported DNS resource record types. In the DNS context a record is a DNS resource record. The options are: ['A', 'AAAA', 'CNAME', 'ALIAS', 'MX', 'NS', 'SRV', 'TXT', 'CAA', 'SSHFP', 'TLSA', 'SMIMEA', 'DS', 'HTTPS', 'SVCB', 'OPENPGPKEY', 'CERT', 'URI', 'RP', 'LOC'] |
  | ttl | False | int |  | Time to live for the record, recommended 3600. |
  | priority | False | int |  | Priority value is between 0 and 65535. Priority is mandatory for MX, SRV and URI record types and ignored for all other types. |
  | enabled | False | bool |  | When true - the record is visible for lookup. |
  | record | True | str |  | The ID or name of the record. |
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
