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
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "machines": [
        {
            "entities": {
                "cdroms": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/cdroms",
                    "id": "595d4dcb-8872-4b70-b757-071106809c11/cdroms",
                    "items": [],
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "nics": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/nics",
                    "id": "595d4dcb-8872-4b70-b757-071106809c11/nics",
                    "items": [
                        {
                            "entities": {
                                "firewallrules": {
                                    "links": null,
                                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/nics/f3d10c9a-f27f-4c0e-911e-57116bfd6b5f/firewallrules",
                                    "id": "f3d10c9a-f27f-4c0e-911e-57116bfd6b5f/firewallrules",
                                    "items": null,
                                    "limit": null,
                                    "offset": null,
                                    "type": "collection"
                                },
                                "flowlogs": {
                                    "links": null,
                                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/nics/f3d10c9a-f27f-4c0e-911e-57116bfd6b5f/flowlogs",
                                    "id": "f3d10c9a-f27f-4c0e-911e-57116bfd6b5f/flowlogs",
                                    "items": null,
                                    "limit": null,
                                    "offset": null,
                                    "type": "collection"
                                }
                            },
                            "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/nics/f3d10c9a-f27f-4c0e-911e-57116bfd6b5f",
                            "id": "f3d10c9a-f27f-4c0e-911e-57116bfd6b5f",
                            "metadata": {
                                "created_by": "<USER_EMAIL>",
                                "created_by_user_id": "<USER_ID>",
                                "created_date": "2023-06-06T13:38:37+00:00",
                                "etag": "b5741a67e66f02d91468c1f1420c1fcf",
                                "last_modified_by": "<USER_EMAIL>",
                                "last_modified_by_user_id": "<USER_ID>",
                                "last_modified_date": "2023-06-06T13:38:37+00:00",
                                "state": "AVAILABLE"
                            },
                            "properties": {
                                "device_number": null,
                                "dhcp": true,
                                "firewall_active": false,
                                "firewall_type": "INGRESS",
                                "ips": [
                                    "<IP>"
                                ],
                                "lan": 1,
                                "mac": "02:01:ed:b1:3d:98",
                                "name": "90aaee2d0c",
                                "pci_slot": 6
                            },
                            "type": "nic"
                        }
                    ],
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11/volumes",
                    "id": "595d4dcb-8872-4b70-b757-071106809c11/volumes",
                    "items": [
                        {
                            "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/volumes/52f55625-5fa3-4d9c-b244-6db1609c5918",
                            "id": "52f55625-5fa3-4d9c-b244-6db1609c5918",
                            "metadata": {
                                "created_by": "<USER_EMAIL>",
                                "created_by_user_id": "<USER_ID>",
                                "created_date": "2023-06-06T13:38:37+00:00",
                                "etag": "b5741a67e66f02d91468c1f1420c1fcf",
                                "last_modified_by": "<USER_EMAIL>",
                                "last_modified_by_user_id": "<USER_ID>",
                                "last_modified_date": "2023-06-06T13:38:37+00:00",
                                "state": "AVAILABLE"
                            },
                            "properties": {
                                "availability_zone": "AUTO",
                                "backupunit_id": null,
                                "boot_order": "AUTO",
                                "boot_server": "595d4dcb-8872-4b70-b757-071106809c11",
                                "bus": "VIRTIO",
                                "cpu_hot_plug": true,
                                "device_number": 1,
                                "disc_virtio_hot_plug": true,
                                "disc_virtio_hot_unplug": true,
                                "image": "48150141-a6b9-11ed-9e9f-e60bb43016ef",
                                "image_alias": null,
                                "image_password": null,
                                "licence_type": "LINUX",
                                "name": "ada2931874",
                                "nic_hot_plug": true,
                                "nic_hot_unplug": true,
                                "pci_slot": 5,
                                "ram_hot_plug": true,
                                "size": 30.0,
                                "ssh_keys": null,
                                "type": "DAS",
                                "user_data": null
                            },
                            "type": "volume"
                        }
                    ],
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/servers/595d4dcb-8872-4b70-b757-071106809c11",
            "id": "595d4dcb-8872-4b70-b757-071106809c11",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-06-06T13:38:37+00:00",
                "etag": "b5741a67e66f02d91468c1f1420c1fcf",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-06-06T13:38:37+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "availability_zone": "AUTO",
                "boot_cdrom": null,
                "boot_volume": {
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/fb6c7a8d-ab0a-434d-9507-7bb83835751a/volumes/52f55625-5fa3-4d9c-b244-6db1609c5918",
                    "id": "52f55625-5fa3-4d9c-b244-6db1609c5918",
                    "type": "volume"
                },
                "cores": 1,
                "cpu_family": "AMD_EPYC",
                "name": "AnsibleAutoTestCompute 01",
                "ram": 1024,
                "template_uuid": "15c6dd2f-02d2-4987-b439-9a58dd59ecc3",
                "type": "CUBE",
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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><span class="blue-span">list</span> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['resume', 'suspend', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><span class="blue-span">list</span> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['resume', 'suspend', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span class="blue-span">str</span> | False | The name of the  resource. |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><span class="blue-span">list</span> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['resume', 'suspend', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span class="blue-span">str</span> | True | The name of the  resource. |
  | assign_public_ip<br /><span class="blue-span">bool</span> | False | This will assign the machine to the public LAN. If no LAN exists with public Internet access it is created.<br />Default: False<br />Options: [True, False] |
  | image<br /><span class="blue-span">str</span> | True | The image alias or ID for creating the virtual machine. |
  | image_password<br /><span class="blue-span">str</span> | False | Password set for the administrative user. |
  | ssh_keys<br /><span class="blue-span">list</span> | False | Public SSH keys allowing access to the virtual machine.<br />Default:  |
  | user_data<br /><span class="blue-span">str</span> | False | The cloud-init configuration for the volume as base64 encoded string. |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter to provision this virtual machine. |
  | availability_zone<br /><span class="blue-span">str</span> | False | The availability zone in which the server should be provisioned.<br />Default: AUTO<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2'] |
  | bus<br /><span class="blue-span">str</span> | False | The bus type for the volume.<br />Default: VIRTIO<br />Options: ['IDE', 'VIRTIO'] |
  | count<br /><span class="blue-span">int</span> | False | The number of virtual machines to create.<br />Default: 1 |
  | location<br /><span class="blue-span">str</span> | False | The datacenter location. Use only if you want to create the Datacenter or else this value is ignored.<br />Default: us/las<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'] |
  | lan<br /><span class="blue-span">str</span> | False | The ID or name of the LAN you wish to add the servers to (can be a string or a number). |
  | nat<br /><span class="blue-span">bool</span> | False | Boolean value indicating if the private IP address has outbound access to the public Internet.<br />Default: False<br />Options: [True, False] |
  | remove_boot_volume<br /><span class="blue-span">bool</span> | False | Remove the bootVolume of the virtual machine you're destroying.<br />Default: True<br />Options: [True, False] |
  | disk_type<br /><span class="blue-span">str</span> | False | The disk type for the volume.<br />Default: HDD<br />Options: ['HDD', 'SSD', 'SSD Standard', 'SSD Premium', 'DAS'] |
  | nic_ips<br /><span class="blue-span">list</span> | False | The list of IPS for the NIC. |
  | template_uuid<br /><span class="blue-span">str</span> | False | The ID of the template for creating a CUBE server; the available templates for CUBE servers can be found on the templates resource. |
  | boot_volume<br /><span class="blue-span">str</span> | False | The volume used for boot. |
  | boot_cdrom<br /><span class="blue-span">str</span> | False | The CDROM used for boot. |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['resume', 'suspend', 'absent', 'present', 'update'] |

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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | name<br /><span class="blue-span">str</span> | False | The name of the  resource. |
  | datacenter<br /><span class="blue-span">str</span> | True | The datacenter to provision this virtual machine. |
  | instance_ids<br /><span class="blue-span">list</span> | False | list of instance ids. Should only contain one ID if renaming in update state<br />Default:  |
  | boot_volume<br /><span class="blue-span">str</span> | False | The volume used for boot. |
  | boot_cdrom<br /><span class="blue-span">str</span> | False | The CDROM used for boot. |
  | do_not_replace<br /><span class="blue-span">bool</span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
  | username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span class="blue-span">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span class="blue-span">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span class="blue-span">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['resume', 'suspend', 'absent', 'present', 'update'] |

&nbsp;

&nbsp;
