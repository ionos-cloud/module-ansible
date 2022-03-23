# datacenter

This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers. This module has a dependency on ionos-cloud &gt;= 6.0.0

## Example Syntax


```yaml
# Create a Datacenter
  - name: Create datacenter
    datacenter:
      name: "Example DC"
      description: "description"
      location: de/fra
    register: datacenter_response
  
# Update a datacenter description
  - name: Update datacenter
    datacenter:
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  
# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
<<<<<<< HEAD
    - name: Create datacenter
      datacenter:
        name: "{{ datacenter }}"
        description: "{{ description }}"
        location: de/fra
      register: datacenter_response

    - name: Update datacenter
      datacenter:
        id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ datacenter }}"
        description: "{{ description }} - RENAMED"
        state: update
      register: updated_datacenter

    - name: Debug - Show Updated Datacenter
      debug:
        msg: "{{ updated_datacenter }}"

    - name: Remove datacenter
      datacenter:
        id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ datacenter }}"
        state: absent
      register: deleted_datacenter
=======
  # Create a Datacenter
  - name: Create datacenter
    datacenter:
      name: "Example DC"
      description: "description"
      location: de/fra
    register: datacenter_response
  
>>>>>>> 00db8fa... feat: generate docs (#61)
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the virtual datacenter. |
  | description | False | str |  | The description of the virtual datacenter. |
  | location | True | str | us/las | The datacenter location. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual datacenter. |
  | id | False | str |  | The ID of the virtual datacenter. |
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
  # Update a datacenter description
  - name: Update datacenter
    datacenter:
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual datacenter. |
  | id | False | str |  | The ID of the virtual datacenter. |
  | description | False | str |  | The description of the virtual datacenter. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
