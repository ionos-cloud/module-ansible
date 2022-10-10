# server

Create, update, destroy, update, start, stop, and reboot a Ionos virtual machine. When the virtual machine is created it can optionally wait for it to be 'running' before returning. The CUBE functionality of the server module is DEPRECATED. Please use the new cube_server module for operations with CUBE servers.

## Example Syntax


```yaml
# Provisioning example. This will create three servers and enumerate their names.
    - server:
        datacenter: Tardis One
        name: web%02d.stackpointcloud.com
        cores: 4
        ram: 2048
        volume_size: 50
        cpu_family: INTEL_XEON
        image: ubuntu:latest
        location: us/las
        count: 3
        assign_public_ip: true
  
# Update Virtual machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - web001.stackpointcloud.com
        - web002.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update
  # Rename virtual machine
    - server:
        datacenter: Tardis One
        instance_ids: web001.stackpointcloud.com
        name: web101.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update

# Removing Virtual machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: absent
  
# Starting Virtual Machines.
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: running
  
# Stopping Virtual Machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: stopped
  
```
&nbsp;

&nbsp;

# state: **running**
```yaml
  # Starting Virtual Machines.
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: running
  
```
### Available parameters for state **running**:
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
# state: **stopped**
```yaml
  # Stopping Virtual Machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - 'web001.stackpointcloud.com'
        - 'web002.stackpointcloud.com'
        - 'web003.stackpointcloud.com'
        wait_timeout: 500
        state: stopped
  
```
### Available parameters for state **stopped**:
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
# state: **resume**
```yaml
  
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
  # Removing Virtual machines
    - server:
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
  # Provisioning example. This will create three servers and enumerate their names.
    - server:
        datacenter: Tardis One
        name: web%02d.stackpointcloud.com
        cores: 4
        ram: 2048
        volume_size: 50
        cpu_family: INTEL_XEON
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
  | volume_availability_zone | False | str |  | The storage availability zone assigned to the volume. |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | cores | False | int | 2 | The number of CPU cores to allocate to the virtual machine. |
  | ram | False | int | 2048 | The amount of memory to allocate to the virtual machine. |
  | cpu_family | False | str | AMD_OPTERON | The amount of memory to allocate to the virtual machine. |
  | availability_zone | False | str | AUTO | The availability zone assigned to the server. |
  | volume_size | False | int | 10 | The size in GB of the boot volume. |
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
  | type | False | str | ENTERPRISE | The type of the virtual machine. |
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
  # Update Virtual machines
    - server:
        datacenter: Tardis One
        instance_ids:
        - web001.stackpointcloud.com
        - web002.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update
  # Rename virtual machine
    - server:
        datacenter: Tardis One
        instance_ids: web001.stackpointcloud.com
        name: web101.stackpointcloud.com
        cores: 4
        ram: 4096
        cpu_family: INTEL_XEON
        availability_zone: ZONE_1
        state: update

```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the virtual machine. |
  | datacenter | True | str |  | The datacenter to provision this virtual machine. |
  | cores | False | int | 2 | The number of CPU cores to allocate to the virtual machine. |
  | ram | False | int | 2048 | The amount of memory to allocate to the virtual machine. |
  | instance_ids | False | list |  | list of instance ids. Should only contain one ID if renaming in update state |
  | boot_volume | False | str |  | The volume used for boot. |
  | boot_cdrom | False | str |  | The CDROM used for boot. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
