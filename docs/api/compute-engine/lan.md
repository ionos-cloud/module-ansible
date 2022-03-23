# lan

This module allows you to create or remove a LAN.

## Example Syntax


```yaml
# Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  
# Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  
# Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
<<<<<<< HEAD
    - name: Create public LAN
      lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        state: present

    - name: Update LAN
      lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        ip_failover:
            - ip: "158.222.102.93"
              nic_uuid: "{{ nic.id }}"
            - ip: "158.222.102.94"
              nic_uuid: "{{ nic.id }}"
        state: update
=======
  # Create a LAN
- name: Create private LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: false
    state: present
  
>>>>>>> 00db8fa... feat: generate docs (#61)
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | name | True | str |  | The name or ID of the LAN. |
  | pcc_id | False | str |  | The ID of the PCC. |
  | ip_failover | False | list |  | The IP failover group. |
  | public | False | bool | False | If true, the LAN will have public Internet access. |
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
  # Remove a LAN
- name: Remove LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | name | True | str |  | The name or ID of the LAN. |
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
  # Update a LAN
- name: Update LAN
  lan:
    datacenter: Virtual Datacenter
    name: nameoflan
    public: true
    ip_failover:
          208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
          208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
    state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter name or UUID in which to operate. |
  | name | True | str |  | The name or ID of the LAN. |
  | pcc_id | False | str |  | The ID of the PCC. |
  | ip_failover | False | list |  | The IP failover group. |
  | public | False | bool | False | If true, the LAN will have public Internet access. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | True | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | True | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
