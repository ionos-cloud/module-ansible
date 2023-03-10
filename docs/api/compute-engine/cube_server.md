# cube_server

Create, update, destroy, update, resume, suspend, and reboot a Ionos CUBE virtual machine. When the virtual machine is created it can optionally wait for it to be 'running' before returning.

## Example Syntax


```yaml
# Provisioning example. This will create three CUBE servers and enumerate their names.
    - cube_server:
        datacenter: Tardis One
        name: web%02d.stackpointcloud.com
        template_id: <template_id>
        image: ubuntu:latest
        location: us/las
        count: 3
        assign_public_ip: true
  
# Update CUBE Virtual machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - web001.stackpointcloud.com
        - web002.stackpointcloud.com
        availability_zone: ZONE_1
        state: update
  # Rename CUBE Virtual machine
    - cube_server:
        datacenter: Tardis One
        instance_ids: web001.stackpointcloud.com
        name: web101.stackpointcloud.com
        availability_zone: ZONE_1
        state: update

# Removing CUBE Virtual machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: absent
  
# Starting CUBE Virtual Machines.
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: resume
  
# Suspending CUBE Virtual Machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: suspend
  
```
&nbsp;

&nbsp;

# state: **resume**
```yaml
  # Starting CUBE Virtual Machines.
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: resume
  
```
### Available parameters for state **resume**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | instance_ids | False | list |  | list of instance ids. Should only contain one ID if renaming in update state |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **suspend**
```yaml
  # Suspending CUBE Virtual Machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: suspend
  
```
### Available parameters for state **suspend**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | instance_ids | False | list |  | list of instance ids. Should only contain one ID if renaming in update state |
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
  # Removing CUBE Virtual machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual machine. |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | instance_ids | False | list |  | list of instance ids. Should only contain one ID if renaming in update state |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **present**
```yaml
  # Provisioning example. This will create three CUBE servers and enumerate their names.
    - cube_server:
        datacenter: Tardis One
        name: web%02d.stackpointcloud.com
        template_id: <template_id>
        image: ubuntu:latest
        location: us/las
        count: 3
        assign_public_ip: true
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the virtual machine. |
  | assign_public_ip | False | bool | False | This will assign the machine to the public LAN. If no LAN exists with public Internet access it is created. |
  | image | True | str |  | The image alias or ID for creating the virtual machine. |
  | image_password | False | str |  | Password set for the administrative user. |
  | ssh_keys | False | list |  | Public SSH keys allowing access to the virtual machine. |
  | user_data | False | str |  | The cloud-init configuration for the volume as base64 encoded string. |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | availability_zone | False | str | AUTO | The availability zone assigned to the server. |
  | bus | False | str | VIRTIO | The bus type for the volume. |
  | count | False | int | 1 | The number of virtual machines to create. |
  | location | False | str | us/las | The datacenter location. Use only if you want to create the Datacenter or else this value is ignored. |
  | lan | False | str |  | The ID or name of the LAN you wish to add the servers to (can be a string or a number). |
  | nat | False | bool | False | Boolean value indicating if the private IP address has outbound access to the public Internet. |
  | remove_boot_volume | False | bool | True | Remove the bootVolume of the virtual machine you're destroying. |
  | disk_type | False | str | HDD | The disk type for the volume. |
  | nic_ips | False | list |  | The list of IPS for the NIC. |
  | template_uuid | False | str |  | The template used when crating a CUBE server. |
  | boot_volume | False | str |  | The volume used for boot. |
  | boot_cdrom | False | str |  | The CDROM used for boot. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
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
  # Update CUBE Virtual machines
    - cube_server:
        datacenter: Tardis One
        instance_ids:
        - web001.stackpointcloud.com
        - web002.stackpointcloud.com
        availability_zone: ZONE_1
        state: update
  # Rename CUBE Virtual machine
    - cube_server:
        datacenter: Tardis One
        instance_ids: web001.stackpointcloud.com
        name: web101.stackpointcloud.com
        availability_zone: ZONE_1
        state: update

```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual machine. |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | instance_ids | False | list |  | list of instance ids. Should only contain one ID if renaming in update state |
  | boot_volume | False | str |  | The volume used for boot. |
  | boot_cdrom | False | str |  | The CDROM used for boot. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
