# Ansible Module

Version: **profitbricks-module-ansible v1.1.0**

## Table of Contents

* [Description](#description)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Usage](#usage)
    * [Authentication](#authentication)
    * [Ansible Playbooks](#ansible-playbooks)
    * [Execute a Playbook](#execute-a-playbook)
    * [Wait for Requests](#wait-for-requests)
    * [Wait for Services](#wait-for-services)
    * [Incrementing Servers](#incrementing-servers)
    * [SSH Key Authentication](#ssh-key-authentication)
* [Reference](#reference)
    * [profitbricks](#profitbricks)
    * [profitbricks_datacenter](#profitbricks_datacenter)
    * [profitbricks_lan](#profitbricks_lan)
    * [profitbricks_nic](#profitbricks_nic)
    * [profitbricks_volume](#profitbricks_volume)
    * [profitbricks\_firewall\_rule](#profitbricks_firewall_rule)
    * [profitbricks_ipblock](#profitbricks_ipblock)
    * [profitbricks_snapshot](#profitbricks_snapshot)
    * [profitbricks_user](#profitbricks_user)
    * [profitbricks_group](#profitbricks_group)
    * [profitbricks_share](#profitbricks_share)
* [Examples](#examples)
* [Support](#support)
* [Testing](#testing)
* [Contributing](#contributing)

## Description

Ansible is an IT automation tool that allows users to configure, deploy, and orchestrate advanced tasks such as continuous deployments or zero downtime rolling updates. The ProfitBricks module for Ansible leverages the ProfitBricks Cloud API.

## Getting Started

The ProfitBricks module for Ansible has a couple of requirements:

* ProfitBricks account
* Python
* [Ansible](https://www.ansible.com/)
* [ProfitBricks SDK for Python](https://devops.profitbricks.com/libraries/python/)

Before you begin you will need to have signed-up for a ProfitBricks account. The credentials you establish during sign-up will be used to authenticate against the ProfitBricks Cloud API.

Ansible must also be installed before the ProfitBricks module can be used. Please review the official [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html) for more information on installing Ansible.

Lastly, the ProfitBricks module requires the ProfitBricks SDK for Python to be installed. This can easily be accomplished with Python PyPI.

    pip install profitbricks

## Installation

1. The ProfitBricks module for Ansible must first be downloaded from GitHub. This can be accomplished a few different ways such as downloading and extracting the archive using `curl` or cloning the GitHub repository locally.

    Download and extract with `curl`:

        mkdir -p profitbricks-module-ansible && curl -L https://github.com/profitbricks/profitbricks-module-ansible/tarball/master | tar zx -C profitbricks-module-ansible/ --strip-components=1

    Clone the GitHub repository locally:

        git clone https://github.com/profitbricks/profitbricks-module-ansible/

2. Ansible must be made aware of the new module path. This too can be accomplished a few different ways depending on your requirements and environment.

    * Ansible configuration file: `ansible.cfg`
    * Environment variable: `ANSIBLE_LIBRARY`
    * Command line parameter: `ansible-playbook --module-path [path]`

    2a. The preferred method is to update the Ansible configuration with the module path. To include the path globally for all users, edit the `/etc/ansible/ansible.cfg` file and add `library = /path/to/module/profitbricks` under the **[default]** section. For example:

        [default]
        library = /path/to/profitbricks-module-ansible/profitbricks

    Note that the Ansible configuration file is read from several locations in the following order:

    * `ANSIBLE_CONFIG` environment variable path
    * `ansible.cfg` from the current directory
    * `.ansible.cfg` in the user home directory
    * `/etc/ansible/ansible.cfg`

    2b. The module path can also be set using an environment variable. This variable will be lost once the terminal session is closed:

        export ANSIBLE_LIBRARY=/path/to/profitbricks-module-ansible/profitbricks

    2c. The module path can be overridden with an `ansible-playbook` command line parameter:

        ansible-playbook --module-path /path/to/profitbricks-module-ansible/profitbricks playbook.yml

## Usage

### Authentication

Credentials can be supplied within a Playbook with the following parameters:

* **subscription_user**
* **subscription_password**

However, the module can also inherit the credentials from environment variables:

* `PROFITBRICKS_USERNAME`
* `PROFITBRICKS_PASSWORD`

Storing credentials in environment variables is useful if you plan to store your PlayBooks using version control.

### Ansible Playbooks

Ansible leverages YAML manifest files called Playbooks. The Playbook will describe the infrastructure to build and is processed from top down. Here is a simple Playbook that will provision two identical servers:

`example.yml`:

    ---
    - hosts: localhost
      connection: local
      gather_facts: false
    
      tasks:
        - name: Provision a set of instances
          profitbricks:
              datacenter: Example
              name: server%02d
              auto_increment: true
              count: 2
              cores: 4
              ram: 4096
              image: 25cfc4fd-fe2f-11e6-afc5-525400f64d8d
              image_password: secretpassword
              location: us/las
              assign_public_ip: true
              remove_boot_volume: true
              state: present
          register: profitbricks

### Execute a Playbook

If your credentials are not already defined:

    export PROFITBRICKS_USERNAME=username
    export PROFITBRICKS_PASSWORD=password

The `ansible-playbook` command will execute the above Playbook.

    ansible-playbook example.yml

### Wait for Requests

When a request to create a resource such as a server is submitted to the ProfitBricks Cloud API, that request is accepted immediately while the provisioning occurs on the backend. This means the request can appear finished while provisioning is still occurring.

Sometimes requests must be told to wait until they finish before continuing to provision dependent resources. For example, a server must finish provisioning before a data volume can be created and attached to the server.

The ProfitBricks module includes two resource parameters to address this scenario:

* **wait** (default: true)
* **wait_timeout** (default: 600 seconds)

By default, the module will wait until a resource is finished provisioning before continuing to process further resources defined in the Playbook.

### Wait for Services

There may be occasions where additional waiting is required. For example, a server may be finished provisioning and shown as available, but IP allocation and network access is still pending. The built-in Ansible module **wait_for** can be invoked to monitor SSH connectivity.

    - name: Wait for SSH connectivity
      wait_for:
          port: 22
          host: "{{ item.public_ip }}"
          search_regex: OpenSSH
          delay: 10
      with_items: "{{ profitbricks.machines }}"

### Incrementing Servers

The **profitbricks** module will provision a number of identical and fully operational servers based on the **count** parameter. A **count** parameter of 10 will provision ten servers with system volumes and network connectivity.

The server **name** parameter with a value of `server%02d` will appended the name with the incremental count. For example, server01, server02, server03, and so forth.

The **auto_increment** parameter can be set to `false` to disable this feature and provision a single server.

### SSH Key Authentication

The ProfitBricks module sets server authentication using the **image_password** and **ssh_keys** parameters. Previous examples have demonstrated the administrative user password being set with the **image_password** parameter. The following example demonstrates two public SSH keys being supplied with two different methods.

1. Set the public key as a string in the Playbook.
2. Load the public key into a variable from a local file.

`example.yml`:

    ---
    - hosts: localhost
      connection: local
      gather_facts: false

      vars:
          ssh_public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

      tasks:
        - name: Provision a server
          profitbricks:
              datacenter: Example
              name: server%02d
              assign_public_ip: true
              image: 25cfc4fd-fe2f-11e6-afc5-525400f64d8d
              ssh_keys:
                  - "{{ ssh_public_key }}"
                  - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDPCNA2YgJ...user@hostname"
              state: present

## Reference

### profitbricks

#### Example Syntax

    - profitbricks:
          datacenter: Example
          name: server%02d
          cores: 2
          ram: 4096
          volume_size: 50
          cpu_family: INTEL_XEON
          image: a3eae284-a2fe-11e4-b187-5f1f641608c8
          count: 5
          assign_public_ip: true

#### Parameter Reference

The following parameters are supported:
                      
| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| auto_increment | no | boolean | true | Whether or not to increment created servers. |
| count | no | integer | 1 | The number of servers to create. |
| name | **yes** | string | | The name of the server(s). |
| image | **yes** | string | | The image alias or UUID for creating the server. |
| image_password | no | string | | Password set for the administrative user. |
| ssh_keys | no | list | none | List of public SSH keys allowing access to the server. |
| datacenter | no | string | none | The datacenter where the server is located. |
| cores | no | integer | 2 | The number of CPU cores to allocate to the server. |
| ram | no | integer | 2048 | The amount of memory to allocate to the server. |
| cpu_family | no | string | AMD_OPTERON | The CPU family type of the server: **AMD_OPTERON**, INTEL_XEON |
| availability_zone | no | string | AUTO | The availability zone assigned to the server: **AUTO**, ZONE\_1, ZONE\_2 |
| volume_size | no | integer | 10 | The size in GB of the boot volume. |
| disk_type | no | string | HDD | The type of disk the volume will use: **HDD**, SSD |
| volume\_availability\_zone | no | string | AUTO | The storage availability zone assigned to the volume: **AUTO**, ZONE\_1, ZONE\_2, ZONE\_3 |
| bus | no | string | VIRTIO | The bus type for the volume: **VIRTIO**, IDE |
| instance_ids | no | list | | List of instance IDs used only with `state='absent'` during deletes. |
| location | no | string | us/las | The datacenter location used only if the module creates a default datacenter: us/las, us/ewr, de/fra, de/fkb |
| assign\_public\_ip | no | boolean | false | This will assign the server to the public LAN. The LAN is created if no LAN exists with public Internet access. |
| lan | no | integer | 1 | The LAN ID of the server. |
| nat | no | boolean | false | The private IP address has outbound access to the Internet. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the instance to be in state 'running' before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| remove\_boot\_volume | no | boolean | true | Remove the boot volume of the server being deleted. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, running, stopped, update |

### profitbricks_datacenter

#### Example Syntax

    - profitbricks_datacenter:
          name: Example DC
          description: test datacenter
          location: us/las

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| name | **yes** | string | | The name of the datacenter. |
| location | no | string | us/las | The datacenter location: us/las, us/ewr, de/fra, de/fkb |
| description | no | string | | The description of the datacenter. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_lan

#### Example Syntax

    - name: Create public LAN
      profitbricks_lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        state: present

    - name: Update LAN
      profitbricks_lan:
        datacenter: Virtual Datacenter
        name: nameoflan
        public: true
        ip_failover:
           208.94.38.167: 1de3e6ae-da16-4dc7-845c-092e8a19fded
           208.94.38.168: 8f01cbd3-bec4-46b7-b085-78bb9ea0c77c
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| datacenter | **yes** | string | | The datacenter in which to operate. |
| name | **yes** | string | | The name of the LAN. |
| public | no | boolean | true | If true, the LAN will have public Internet access. |
| ip_failover | no | dict | | The IP failover group dictionary where its keys represent IP addresses and values represent NIC UUIDs. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_nic

#### Example Syntax

    - name: Create private NIC
      profitbricks_nic:
          datacenter: Example
          server: "{{ item.id }}"
          lan: 2
          state: present
      register: private_nic
      with_items: "{{ profitbricks.machines }}"

    - name: Update NIC
      profitbricks_nic:
        datacenter: Example
        server: "{{ item.id }}"
        name: 7341c2454f
        lan: 1
        ips:
          - 158.222.103.23
          - 158.222.103.24
        dhcp: false
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| datacenter | **yes** | string | | The datacenter in which to operate. |
| server | **yes** | string | | The server name or UUID. |
| name | **yes** | string | | The name or UUID of the NIC. Only required on deletes. |
| lan | **yes** | integer | | The LAN to connect the NIC. The LAN will be created if it does not exist. Only required on creates. |
| dhcp | no | boolean | | Indicates if the NIC is using DHCP or not. |
| nat | no | boolean | | Allow the private IP address outbound Internet access. |
| firewall_active | no | boolean | | Indicates if the firewall is active. |
| ips | no | list | | A list of IPs to be assigned to the NIC. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_volume

#### Example Syntax

    - name: Create data volume
      profitbricks_volume:
          datacenter: Example
          server: "{{ item.id }}"
          name: "{{ item.properties.name }}-data%02d"
          size: 20
          disk_type: SSD
          licence_type: OTHER
          state: present
      with_items: "{{ profitbricks.machines }}"

    - name: Update volumes
      profitbricks_volume:
        datacenter: Tardis One
        instance_ids:
          - vol01
          - vol02
        size: 50
        bus: IDE
        wait_timeout: 500
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| datacenter | **yes** | string | | The datacenter in which to create the volume. |
| server | no | string | | The server on which to attach the volume. |
| name | **yes** | string | | The name of the volume. You can enumerate the names using auto_increment. |
| size | no | integer | 10 | The size of the volume in GB. |
| bus | no | string | VIRTIO | The bus type of the volume: **VIRTIO**, IDE |
| image | no | string | | The image alias, image UUID, or snapshot UUID for the volume. |
| image_password | no | string | | Password set for the administrative user. |
| ssh_keys | no | list | | Public SSH keys allowing access to the server. |
| disk_type | no | string | HDD | The disk type of the volume: **HDD**, SSD |
| licence_type | no | string | UNKNOWN | The licence type for the volume. This is used when the image is non-standard: LINUX, WINDOWS, **UNKNOWN**, OTHER, WINDOWS2016 |
| availability_zone | no | string | AUTO | The storage availability zone assigned to the volume: **AUTO**, ZONE\_1, ZONE\_2, ZONE\_3 |
| count | no | integer | 1 | The number of volumes to create. |
| auto_increment | no | boolean | true | Whether or not to increment created servers. |
| instance_ids | no | list | | List of instance UUIDs only used when `state='absent'` or `state='update'` to remove or update volumes. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the resource to be created before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks\_firewall\_rule

#### Example Syntax

    - name: Allow SSH access
      profitbricks_firewall_rule:
          datacenter: Example
          server: server01
          nic: nic01
          name: Allow SSH
          protocol: TCP
          source_ip: 0.0.0.0
          port_range_start: 22
          port_range_end: 22
          state: present
      with_items: "{{ private_nic.results }}"

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| datacenter | **yes** | string | | The datacenter name or UUID in which to operate. |
| server | **yes** | string | | The server name or UUID. |
| nic | **yes** | string | | The NIC name or UUID. |
| name | **yes** | string | | The name or UUID of the firewall rule. |
| protocol | no | string | | The protocol of the firewall rule: TCP, UDP, ICMP, ANY |
| source_mac | no | string | | Only traffic originating from the MAC address is allowed. No value allows all source MAC addresses. |
| source_ip | no | string | | Only traffic originating from the IPv4 address is allowed. No value allows all source IPs. |
| target_ip | no | string | | In case the target NIC has multiple IP addresses, only traffic directed to the IP address of the NIC is allowed. No value allows all target IPs. |
| port\_range\_start | integer | string | | Defines the start range of the allowed port if protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534 |
| port\_range\_end | integer | string | | Defines the end range of the allowed port if the protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534 |
| icmp_type | no | integer | | Defines the allowed type if the protocol ICMP is chosen. No value allows all types: 0 to 254 |
| icmp_code | no | integer | | Defines the allowed code if protocol ICMP is chosen. No value allows all codes: 0 to 254 |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_ipblock

#### Example Syntax

    - name: Create IPBlock
      profitbricks_ipblock:
        name: spare
        location: us/ewr
        size: 2

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| name | **yes** | string | | The name of the IPBlock. |
| location | no | string | us/las | The IPBlock location: us/las, us/ewr, de/fra, de/fkb |
| size | no | integer | 1 | The number of IP addresses to allocate in the IPBlock. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicates desired state of the resource: **present**, absent |

### profitbricks_snapshot

#### Example Syntax

    - name: Create snapshot
      profitbricks_snapshot:
        datacenter: production DC
        volume: master
        name: boot volume snapshot

    - name: Restore snapshot
      profitbricks_snapshot:
        datacenter: production DC
        volume: slave
        name: boot volume snapshot
        state: restore

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| datacenter | **yes** | string | | The datacenter in which the volume resides. |
| volume | **yes** | string | | The server on which to attach the volume. |
| name | no | string | | The name of the snapshot. |
| description | no | string | | The description of the snapshot. |
| licence_type | no | string | | The licence type for the volume. This is used when updating the snapshot: LINUX, WINDOWS, UNKNOWN, OTHER, WINDOWS2016 |
| cpu_hot_plug | no | boolean | | Indicates the volume is capable of CPU hot plug (no reboot required). |
| cpu_hot_unplug | no | boolean | | Indicates the volume is capable of CPU hot unplug (no reboot required). |
| ram_hot_plug | no | boolean | | Indicates the volume is capable of memory hot plug. |
| ram_hot_unplug | no | boolean | | Indicates the volume is capable of memory hot unplug. |
| nic_hot_plug | no | boolean | | Indicates the volume is capable of NIC hot plug. |
| nic_hot_unplug | no | boolean | | Indicates the volume is capable of NIC hot unplug. |
| disc_virtio_hot_plug | no | boolean | | Indicates the volume is capable of VirtIO drive hot plug. |
| disc_virtio_hot_unplug | no | boolean | | Indicates the volume is capable of VirtIO drive hot unplug. |
| disc_scsi_hot_plug | no | boolean | | Indicates the volume is capable of SCSI drive hot plug. |
| disc_scsi_hot_unplug | no | boolean | | Indicates the volume is capable of SCSI drive hot unplug. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environment variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environment variable. |
| wait | no | boolean | true | Wait for the resource to be created before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, restore, update |

### profitbricks_user

#### Example Syntax

    - name: Create user
      profitbricks_user:
        firstname: John
        lastname: Doe
        email: john.doe@example.com
        password: secretpassword123
        administrator: true

    - name: Update user
      profitbricks_user:
        firstname: John
        lastname: Doe
        email: john.doe@example.com
        administrator: false
        groups:
          - Developers
          - Testers
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| firstname | **yes** | string | | The user's first name. |
| lastname | **yes** | string | | The user's last name. |
| email | **yes** | string | | The user's email. |
| password | **yes** | string | | A password for the user. |
| administrator | no | boolean | | Indicates if the user has administrative rights. |
| force_sec_auth | no | boolean | | Indicates if secure (two-factor) authentication should be forced for the user. |
| groups | no | list | | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list (`[]`) to remove the user from all groups. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_group

#### Example Syntax

    - name: Create group
      profitbricks_group:
        name: guests
        create_datacenter: true
        create_snapshot: true
        reserve_ip: true
        access_activity_log: false

    - name: Update group
      profitbricks_group:
        name: guests
        create_datacenter: false
        users:
          - john.smith@test.com
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| name | **yes** | string | | The name of the group. |
| create_datacenter | no | boolean | | Indicates if the group is allowed to create virtual data centers. |
| create_snapshot | no | boolean | | Indicates if the group is allowed to create snapshots. |
| reserve_ip | no | boolean | | Indicates if the group is allowed to reserve IP addresses. |
| access_activity_log | no | boolean | | Indicates if the group is allowed to access the activity log. |
| users | no | list | | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list (`[]`) to remove all users from the group. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

### profitbricks_share

#### Example Syntax

    - name: Create shares
      profitbricks_share:
        group: Demo
        edit_privilege: true
        share_privilege: true
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
          - ba7efccb-a761-11e7-90a7-525400f64d8d
        state: present

    - name: Update shares
      profitbricks_share:
        group: Demo
        edit_privilege: false
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        state: update

#### Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| --- | :-: | --- | --- | --- |
| group | **yes** | string | | The name or ID of the group. |
| resource_ids | **yes**  | list | | A list of resource IDs to add, update or remove as shares. |
| edit_privilege | no | boolean | | Indicates that the group has permission to edit privileges on the resource. |
| share_privilege | no | boolean | | Indicates that the group has permission to share the resource. |
| subscription_user | no | string | | The ProfitBricks username. Overrides the PROFITBRICKS_USERNAME environement variable. |
| subscription_password | no | string | | The ProfitBricks password. Overrides the PROFITBRICKS_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

## Examples

The following example will provision two servers both connected to public and private LANs. The two servers will have an attached data volume and each NIC will have firewall rules assigned.

    ---
    - hosts: localhost
      connection: local
      gather_facts: false

      vars:
          datacenter: Example
          location: us/las
          image: ubuntu:latest
          image_password: secretpassword
          timeout: 900
        
      tasks:
        - name: Provision a set of instances
          profitbricks:
              datacenter: "{{ datacenter }}"
              name: server%02d
              auto_increment: true
              cores: 4
              ram: 4096
              availability_zone: ZONE_1
              volume_availability_zone: ZONE_3
              volume_size: 10
              cpu_family: AMD_OPTERON
              disk_type: HDD
              image: "{{ image }}"
              image_password: "{{ image_password }}"
              location: "{{ location }}"
              count: 2
              assign_public_ip: true
              remove_boot_volume: true
              wait: true
              wait_timeout: "{{ timeout }}"
              state: present
          register: profitbricks
    
        - debug: msg="{{profitbricks.machines}}"
    
        - name: Public SSH firewall rule
          profitbricks_firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              nic: "{{ item.nic.id }}"
              name: Allow SSH
              protocol: TCP
              source_ip: 0.0.0.0
              port_range_start: 22
              port_range_end: 22
              state: present
          with_items: "{{ profitbricks.machines }}"
    
        - name: Create private NIC
          profitbricks_nic:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              lan: 2
              state: present
          register: private_nic
          with_items: "{{ profitbricks.machines }}"
    
        - name: Create SSH firewall rule
          profitbricks_firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.item.id }}"
              nic: "{{ item.id }}"
              name: Allow SSH
              protocol: TCP
              source_ip: 0.0.0.0
              port_range_start: 22
              port_range_end: 22
              state: present
          with_items: "{{ private_nic.results }}"
    
        - name: Create ping firewall rule
          profitbricks_firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.item.id }}"
              nic: "{{ item.id }}"
              name: Allow Ping
              protocol: ICMP
              source_ip: 0.0.0.0
              icmp_type: 8
              icmp_code: 0
              state: present
          with_items: "{{ private_nic.results }}"
    
        - name: Create data volume
          profitbricks_volume:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              name: "{{ item.properties.name }}-data%02d"
              size: 50
              disk_type: SSD
              licence_type: OTHER
              wait_timeout: "{{ timeout }}"
              state: present
          with_items: "{{ profitbricks.machines }}"
    
## Support

You are welcome to contact us with questions or comments using the **Community** section of the [ProfitBricks DevOps Central](https://devops.profitbricks.com/). Please report any feature requests or issues using GitHub issue tracker.

* [ProfitBricks REST API](https://devops.profitbricks.com/api/rest/) documentation.
* Ask a question or discuss at [ProfitBricks DevOps Central](https://devops.profitbricks.com/community/).
* Report an [issue here](https://github.com/profitbricks/profitbricks-module-ansible/issues).
* More examples are located in the [GitHub repository](https://github.com/profitbricks/profitbricks-module-ansible/tree/master/examples) `examples` directory.

## Testing

Set your ProfitBricks user credentials.

    export PROFITBRICKS_USERNAME=username
    export PROFITBRICKS_PASSWORD=password

Change into the `tests` directory and execute the Playbooks.

    cd tests
    ansible-playbook server.yml

Note: The ProfitBricks public image UUIDs change periodically due to updates. Therefore, it is recommended to use image aliases.

## Contributing

1. Fork the repository ([https://github.com/profitbricks/profitbricks-module-ansible/fork](https://github.com/profitbricks/profitbricks-module-ansible/fork))
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
