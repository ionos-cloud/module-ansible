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
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "machines": [
        {
            "entities": {
                "cdroms": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/cdroms",
                    "id": "78ce195d-147b-48d8-a20e-57104b99badd/cdroms",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "nics": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/nics",
                    "id": "78ce195d-147b-48d8-a20e-57104b99badd/nics",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd/volumes",
                    "id": "78ce195d-147b-48d8-a20e-57104b99badd/volumes",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/servers/78ce195d-147b-48d8-a20e-57104b99badd",
            "id": "78ce195d-147b-48d8-a20e-57104b99badd",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-29T09:17:01+00:00",
                "etag": "f9b2094caee723ec45475a17c223ddd2",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-05-29T09:17:01+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "boot_cdrom": null,
                "boot_volume": {
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/f6e15460-e5eb-451a-9da7-08c9da65a179/volumes/4e9d988c-d4d8-4de1-a325-7f1a7b0ea77f",
                    "id": "4e9d988c-d4d8-4de1-a325-7f1a7b0ea77f",
                    "type": "volume"
                },
                "cores": 1,
                "cpu_family": "INTEL_SKYLAKE",
                "name": "AnsibleAutoTestCompute",
                "ram": 2048,
                "template_uuid": null,
                "type": "ENTERPRISE",
                "vm_state": "RUNNING"
            },
            "type": "server"
        }
    ],
    "action": "create"
}

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><mark style="color:blue;">\<list\></mark> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><mark style="color:blue;">\<list\></mark> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | False | The name of the  resource. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><mark style="color:blue;">\<list\></mark> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | True | The name of the  resource. |
  | assign_public_ip<br /><mark style="color:blue;">\<bool\></mark> | False | This will assign the machine to the public LAN. If no LAN exists with public Internet access it is created.<br />Default: False<br />Options: [True, False] |
  | image<br /><mark style="color:blue;">\<str\></mark> | True | The image alias or ID for creating the virtual machine. |
  | image_password<br /><mark style="color:blue;">\<str\></mark> | False | Password set for the administrative user. |
  | ssh_keys<br /><mark style="color:blue;">\<list\></mark> | False | Public SSH keys allowing access to the virtual machine.<br />Default:  |
  | user_data<br /><mark style="color:blue;">\<str\></mark> | False | The cloud-init configuration for the volume as base64 encoded string. |
  | volume_availability_zone<br /><mark style="color:blue;">\<str\></mark> | False | The storage availability zone assigned to the volume.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3'] |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The datacenter to provision this virtual machine. |
  | cores<br /><mark style="color:blue;">\<int\></mark> | False | The total number of cores for the enterprise server.<br />Default: 2 |
  | ram<br /><mark style="color:blue;">\<int\></mark> | False | The memory size for the enterprise server in MB, such as 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. If you set the RAM size more than 240GB, then ramHotPlug will be set to FALSE and can not be set to TRUE unless RAM size not set to less than 240GB.<br />Default: 2048 |
  | cpu_family<br /><mark style="color:blue;">\<str\></mark> | False | CPU architecture on which server gets provisioned; not all CPU architectures are available in all datacenter regions; available CPU architectures can be retrieved from the datacenter resource; must not be provided for CUBE and VCPU servers.<br />Default: AMD_OPTERON<br />Options: ['AMD_OPTERON', 'INTEL_XEON', 'INTEL_SKYLAKE'] |
  | availability_zone<br /><mark style="color:blue;">\<str\></mark> | False | The availability zone in which the server should be provisioned.<br />Default: AUTO<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2'] |
  | volume_size<br /><mark style="color:blue;">\<int\></mark> | False | The size in GB of the boot volume.<br />Default: 10 |
  | bus<br /><mark style="color:blue;">\<str\></mark> | False | The bus type for the volume.<br />Default: VIRTIO<br />Options: ['IDE', 'VIRTIO'] |
  | count<br /><mark style="color:blue;">\<int\></mark> | False | The number of virtual machines to create.<br />Default: 1 |
  | location<br /><mark style="color:blue;">\<str\></mark> | False | The datacenter location. Use only if you want to create the Datacenter or else this value is ignored.<br />Default: us/las<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'] |
  | lan<br /><mark style="color:blue;">\<str\></mark> | False | The ID or name of the LAN you wish to add the servers to (can be a string or a number). |
  | nat<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean value indicating if the private IP address has outbound access to the public Internet.<br />Default: False<br />Options: [True, False] |
  | remove_boot_volume<br /><mark style="color:blue;">\<bool\></mark> | False | Remove the bootVolume of the virtual machine you're destroying.<br />Default: True<br />Options: [True, False] |
  | disk_type<br /><mark style="color:blue;">\<str\></mark> | False | The disk type for the volume.<br />Default: HDD<br />Options: ['HDD', 'SSD', 'SSD Standard', 'SSD Premium', 'DAS'] |
  | nic_ips<br /><mark style="color:blue;">\<list\></mark> | False | The list of IPS for the NIC. |
  | boot_volume<br /><mark style="color:blue;">\<str\></mark> | False | The volume used for boot. |
  | boot_cdrom<br /><mark style="color:blue;">\<str\></mark> | False | The CDROM used for boot. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><mark style="color:blue;">\<str\></mark> | False | The name of the  resource. |
  | datacenter<br /><mark style="color:blue;">\<str\></mark> | True | The datacenter to provision this virtual machine. |
  | cores<br /><mark style="color:blue;">\<int\></mark> | False | The total number of cores for the enterprise server.<br />Default: 2 |
  | ram<br /><mark style="color:blue;">\<int\></mark> | False | The memory size for the enterprise server in MB, such as 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. If you set the RAM size more than 240GB, then ramHotPlug will be set to FALSE and can not be set to TRUE unless RAM size not set to less than 240GB.<br />Default: 2048 |
  | instance_ids<br /><mark style="color:blue;">\<list\></mark> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | boot_volume<br /><mark style="color:blue;">\<str\></mark> | False | The volume used for boot. |
  | boot_cdrom<br /><mark style="color:blue;">\<str\></mark> | False | The CDROM used for boot. |
  | do_not_replace<br /><mark style="color:blue;">\<bool\></mark> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos API certificate fingerprint. |
  | username<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><mark style="color:blue;">\<str\></mark> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><mark style="color:blue;">\<bool\></mark> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><mark style="color:blue;">\<int\></mark> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><mark style="color:blue;">\<str\></mark> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update'] |

&nbsp;

&nbsp;
