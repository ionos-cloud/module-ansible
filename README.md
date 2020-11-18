# Ansible Module

Version: **ionos-cloud-module-ansible v2.2.0**

API Version: **Ionos Cloud Cloud API v5**

## Table of Contents

- [Description](#description)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
  - [Authentication](#authentication)
  - [Ansible Playbooks](#ansible-playbooks)
  - [Execute a Playbook](#execute-a-playbook)
  - [Wait for Requests](#wait-for-requests)
  - [Wait for Services](#wait-for-services)
  - [Incrementing Servers](#incrementing-servers)
  - [SSH Key Authentication](#ssh-key-authentication)
- [Reference](#reference)
  - [server](#server)
  - [datacenter](#datacenter)
  - [lan](#lan)
  - [nic](#nic)
  - [volume](#volume)
  - [firewall_rule](#rule)
  - [ipblock](#ipblock)
  - [snapshot](#snapshot)
  - [user](#user)
  - [group](#group)
  - [share](#share)
  - [pcc](#pcc)
  - [s3key](#s3key)
  - [k8s_cluster](#k8s_cluster)
  - [k8s_nodepool](#k8s_nodepool)
  - [k8s_config](#k8s_config)
  - [backupunit](#backupunit)
- [Examples](#examples)
- [Support](#support)
- [Testing](#testing)
- [Contributing](#contributing)

## Description

Ansible is an IT automation tool that allows users to configure, deploy, and orchestrate advanced tasks such as continuous deployments or zero downtime rolling updates. The Ionos module for Ansible leverages the Ionos Cloud API.

## Getting Started

The Ionos module for Ansible has a couple of requirements:

- Ionos Cloud account
- Python
- [Ansible](https://www.ansible.com/)
- [Ionos SDK for Python](https://pypi.org/project/ionossdk/)

Before you begin you will need to have signed-up for a Ionos account. The credentials you establish during sign-up will be used to authenticate against the Ionos Cloud API.

Ansible must also be installed before the Ionos module can be used. Please review the official [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html) for more information on installing Ansible.

Lastly, the Ionos module requires the Ionos SDK for Python to be installed. This can easily be accomplished with Python PyPI.

    pip install ionossdk

## Installation

1.  The Ionos module for Ansible must first be downloaded from GitHub. This can be accomplished a few different ways such as downloading and extracting the archive using `curl` or cloning the GitHub repository locally.

    Download and extract with `curl`:

        mkdir -p ionos-module-ansible && curl -L https://github.com/ionos-cloud/sdk-ansible/tarball/master | tar zx -C ionos-module-ansible/ --strip-components=1

    Clone the GitHub repository locally:

        git clone https://github.com/ionos-cloud/sdk-ansible

2.  Ansible must be made aware of the new module path. This too can be accomplished a few different ways depending on your requirements and environment.

    - Ansible configuration file: `ansible.cfg`
    - Environment variable: `ANSIBLE_LIBRARY`
    - Command line parameter: `ansible-playbook --module-path [path]`

    2a. The preferred method is to update the Ansible configuration with the module path. To include the path globally for all users, edit the `/etc/ansible/ansible.cfg` file and add `library = /path/to/module/ionos_cloud` under the **[default]** section. For example:

        [default]
        library = /path/to/ionos-module-ansible/ionos_cloud

    Note that the Ansible configuration file is read from several locations in the following order:

    - `ANSIBLE_CONFIG` environment variable path
    - `ansible.cfg` from the current directory
    - `.ansible.cfg` in the user home directory
    - `/etc/ansible/ansible.cfg`

    2b. The module path can also be set using an environment variable. This variable will be lost once the terminal session is closed:

        export ANSIBLE_LIBRARY=/path/to/ionos-module-ansible/ionos_cloud

    2c. The module path can be overridden with an `ansible-playbook` command line parameter:

        ansible-playbook --module-path /path/to/ionos-module-ansible/ionos_cloud playbook.yml

## Usage

### Authentication

Credentials can be supplied within a Playbook with the following parameters:

- **username** (**subscription_user** is a legacy alias)
- **password** (**subscription_password** is a legacy alias)

However, the module can also inherit the credentials from environment variables:

- `IONOS_USERNAME`
- `IONOS_PASSWORD`

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
          server:
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
          register: ionos

### Execute a Playbook

If your credentials are not already defined:

    export IONOS_USERNAME=username
    export IONOS_PASSWORD=password

The `ansible-playbook` command will execute the above Playbook.

    ansible-playbook example.yml

### Wait for Services

There may be occasions where additional waiting is required. For example, a server may be finished provisioning and shown as available, but IP allocation and network access is still pending. The built-in Ansible module **wait_for** can be invoked to monitor SSH connectivity.

    - name: Wait for SSH connectivity
      wait_for:
          port: 22
          host: "{{ item.public_ip }}"
          search_regex: OpenSSH
          delay: 10
      with_items: "{{ ionos.machines }}"

### Incrementing Servers

The **servers** module will provision a number of identical and fully operational servers based on the **count** parameter. A **count** parameter of 10 will provision ten servers with system volumes and network connectivity.

The server **name** parameter with a value of `server%02d` will appended the name with the incremental count. For example, server01, server02, server03, and so forth.

The **auto_increment** parameter can be set to `false` to disable this feature and provision a single server.

### SSH Key Authentication

The Ionos module sets server authentication using the **image_password** and **ssh_keys** parameters. Previous examples have demonstrated the administrative user password being set with the **image_password** parameter. The following example demonstrates two public SSH keys being supplied with two different methods.

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
          server:
              datacenter: Example
              name: server%02d
              assign_public_ip: true
              image: 25cfc4fd-fe2f-11e6-afc5-525400f64d8d
              ssh_keys:
                  - "{{ ssh_public_key }}"
                  - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDPCNA2YgJ...user@hostname"
              state: present

## Documentation for API Endpoints
All URIs are relative to https://api.ionos.com/cloudapi/v5

### server

#### Example

    - server:
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

| Name                     |  Required  | Type             | Default     | Description                                                                                                                  |
| ------------------------ | :--------: | ---------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| auto_increment           |     no     | boolean          | true        | Whether or not to increment created servers.                                                                                 |
| count                    |     no     | integer          | 1           | The number of servers to create.                                                                                             |
| name                     | **yes**/no | string           |             | The name of the server(s). Required only for `state='present'`.                                                              |
| image                    | **yes**/no | string           |             | The image alias or UUID for creating the server. Required only for `state='present'`.                                        |
| image_password           |     no     | string           |             | Password set for the administrative user.                                                                                    |
| ssh_keys                 |     no     | list             | none        | List of public SSH keys allowing access to the server.                                                                       |
| datacenter               |  **yes**   | string           | none        | The datacenter where the server is located.                                                                                  |
| cores                    |     no     | integer          | 2           | The number of CPU cores to allocate to the server.                                                                           |
| ram                      |     no     | integer          | 2048        | The amount of memory to allocate to the server.                                                                              |
| cpu_family               |     no     | string           | AMD_OPTERON | The CPU family type of the server: **AMD_OPTERON**, INTEL_XEON, INTEL_SKYLAKE                                                |
| availability_zone        |     no     | string           | AUTO        | The availability zone assigned to the server: **AUTO**, ZONE_1, ZONE_2                                                       |
| volume_size              |     no     | integer          | 10          | The size in GB of the boot volume.                                                                                           |
| disk_type                |     no     | string           | HDD         | The type of disk the volume will use: **HDD**, SSD                                                                           |
| volume_availability_zone |     no     | string           | AUTO        | The storage availability zone assigned to the volume: **AUTO**, ZONE_1, ZONE_2, ZONE_3                                       |
| bus                      |     no     | string           | VIRTIO      | The bus type for the volume: **VIRTIO**, IDE                                                                                 |
| instance_ids             | **yes**/no | list             |             | List of instance IDs or names. **Not required** for `state='present'`.                                                       |
| location                 |     no     | string           | us/las      | The datacenter location used only if the module creates a default datacenter: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr |
| assign_public_ip         |     no     | boolean          | false       | This will assign the server to the public LAN. The LAN is created if no LAN exists with public Internet access.              |
| lan                      |     no     | string / integer | 1           | The LAN ID / Name for the server.                                                                                            |
| nat                      |     no     | boolean          | false       | The private IP address has outbound access to the Internet.                                                                  |
| api_url                  |     no     | string           |             | The Ionos API base URL.                                                                                               |
| username                 |     no     | string           |             | The Ionos username. Overrides the IONOS_USERNAME environment variable.                                         |
| password                 |     no     | string           |             | The Ionos password. Overrides the IONOS_PASSWORD environment variable.                                         |
| wait                     |     no     | boolean          | true        | Wait for the instance to be in state 'running' before continuing.                                                            |
| wait_timeout             |     no     | integer          | 600         | The number of seconds until the wait ends.                                                                                   |
| remove_boot_volume       |     no     | boolean          | true        | Remove the boot volume of the server being deleted.                                                                          |
| state                    |     no     | string           | present     | Indicate desired state of the resource: **present**, absent, running, stopped, update                                        |


### datacenter

#### Example Syntax

    - datacenter:
          name: Example DC
          description: test datacenter
          location: us/las

#### Parameter Reference

The following parameters are supported:

| Name         | Required | Type    | Default | Description                                                                           |
| ------------ | :------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| name         | **yes**  | string  |         | The name of the datacenter.                                                           |
| location     |    no    | string  | us/las  | The datacenter location: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr               |
| description  |    no    | string  |         | The description of the datacenter.                                                    |
| api_url      |    no    | string  |         | The Ionos API base URL.                                                        |
| username     |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable. |
| password     |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable. |
| wait         |    no    | boolean | true    | Wait for the operation to complete before continuing.                                 |
| wait_timeout |    no    | integer | 600     | The number of seconds until the wait ends.                                            |
| state        |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                   |

### lan

#### Example Syntax

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

#### Parameter Reference

The following parameters are supported:

| Name         | Required | Type    | Default | Description                                                                                            |
| ------------ | :------: | ------- | ------- | ------------------------------------------------------------------------------------------------------ |
| datacenter   | **yes**  | string  |         | The datacenter in which to operate.                                                                    |
| name         | **yes**  | string  |         | The name of the LAN.                                                                                   |
| public       |    no    | boolean | true    | If true, the LAN will have public Internet access.                                                     |
| ip_failover  |    no    | list    |         | The IP failover list of group dictionaries containing IP addresses and NIC UUIDs. |
| api_url      |    no    | string  |         | The Ionos API base URL.                                                                         |
| username     |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable.                  |
| password     |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable.                  |
| wait         |    no    | boolean | true    | Wait for the operation to complete before continuing.                                                  |
| wait_timeout |    no    | integer | 600     | The number of seconds until the wait ends.                                                             |
| state        |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                                    |

### nic

#### Example Syntax

    - name: Create private NIC
      nic:
          datacenter: Example
          server: "{{ item.id }}"
          lan: 2
          state: present
      register: private_nic
      with_items: "{{ ionos.machines }}"

    - name: Update NIC
      nic:
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

| Name            | Required | Type    | Default | Description                                                                                         |
| --------------- | :------: | ------- | ------- | --------------------------------------------------------------------------------------------------- |
| datacenter      | **yes**  | string  |         | The datacenter in which to operate.                                                                 |
| server          | **yes**  | string  |         | The server name or UUID.                                                                            |
| name            | **yes**  | string  |         | The name or UUID of the NIC. Only required on deletes.                                              |
| lan             | **yes**  | integer |         | The LAN to connect the NIC. The LAN will be created if it does not exist. Only required on creates. |
| dhcp            |    no    | boolean |         | Indicates if the NIC is using DHCP or not.                                                          |
| nat             |    no    | boolean |         | Allow the private IP address outbound Internet access.                                              |
| firewall_active |    no    | boolean |         | Indicates if the firewall is active.                                                                |
| ips             |    no    | list    |         | A list of IPs to be assigned to the NIC.                                                            |
| api_url         |    no    | string  |         | The Ionos API base URL.                                                                      |
| username        |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable.               |
| password        |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable.               |
| wait            |    no    | boolean | true    | Wait for the operation to complete before continuing.                                               |
| wait_timeout    |    no    | integer | 600     | The number of seconds until the wait ends.                                                          |
| state           |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                                 |

### volume

#### Example Syntax

    - name: Create data volume
      volume:
          datacenter: Example
          server: "{{ item.id }}"
          name: "{{ item.properties.name }}-data%02d"
          size: 20
          disk_type: SSD
          licence_type: OTHER
          state: present
      with_items: "{{ ionos.machines }}"

    - name: Update volumes
      volume:
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

| Name              |  Required  | Type    | Default | Description                                                                                                                   |
| ----------------- | :--------: | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| datacenter        |  **yes**   | string  |         | The datacenter in which to create the volume.                                                                                 |
| server            |     no     | string  |         | The server on which to attach the volume.                                                                                     |
| name              | **yes**/no | string  |         | The name of the volume. You can enumerate the names using auto_increment.                                                     |
| size              |     no     | integer | 10      | The size of the volume in GB.                                                                                                 |
| bus               |     no     | string  | VIRTIO  | The bus type of the volume: **VIRTIO**, IDE                                                                                   |
| image             |     no     | string  |         | The image alias, image UUID, or snapshot UUID for the volume.                                                                 |
| image_password    |     no     | string  |         | Password set for the administrative user.                                                                                     |
| ssh_keys          |     no     | list    |         | Public SSH keys allowing access to the server.                                                                                |
| disk_type         |     no     | string  | HDD     | The disk type of the volume: **HDD**, SSD                                                                                     |
| licence_type      |     no     | string  | UNKNOWN | The licence type for the volume. This is used when the image is non-standard: LINUX, WINDOWS, **UNKNOWN**, OTHER, WINDOWS2016 |
| availability_zone |     no     | string  | AUTO    | The storage availability zone assigned to the volume: **AUTO**, ZONE_1, ZONE_2, ZONE_3                                        |
| count             |     no     | integer | 1       | The number of volumes to create.                                                                                              |
| auto_increment    |     no     | boolean | true    | Whether or not to increment created servers.                                                                                  |
| instance_ids      | **yes**/no | list    |         | List of instance UUIDs or names. Required for `state='absent'` or `state='update'` to remove or update volumes.               |
| api_url           |     no     | string  |         | The Ionos API base URL.                                                                                                |
| username          |     no     | string  |         | The Ionos username. Overrides the IONOS_USERNAME environment variable.                                          |
| password          |     no     | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environment variable.                                          |
| wait              |     no     | boolean | true    | Wait for the resource to be created before continuing.                                                                        |
| wait_timeout      |     no     | integer | 600     | The number of seconds until the wait ends.                                                                                    |
| state             |     no     | string  | present | Indicate desired state of the resource: **present**, absent, update                                                           |

### firewall_rule

#### Example Syntax

    - name: Allow SSH access
      firewall_rule:
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

| Name             | Required | Type    | Default | Description                                                                                                                                      |
| ---------------- | :------: | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| datacenter       | **yes**  | string  |         | The datacenter name or UUID in which to operate.                                                                                                 |
| server           | **yes**  | string  |         | The server name or UUID.                                                                                                                         |
| nic              | **yes**  | string  |         | The NIC name or UUID.                                                                                                                            |
| name             | **yes**  | string  |         | The name or UUID of the firewall rule.                                                                                                           |
| protocol         |    no    | string  |         | The protocol of the firewall rule: TCP, UDP, ICMP, ANY                                                                                           |
| source_mac       |    no    | string  |         | Only traffic originating from the MAC address is allowed. No value allows all source MAC addresses.                                              |
| source_ip        |    no    | string  |         | Only traffic originating from the IPv4 address is allowed. No value allows all source IPs.                                                       |
| target_ip        |    no    | string  |         | In case the target NIC has multiple IP addresses, only traffic directed to the IP address of the NIC is allowed. No value allows all target IPs. |
| port_range_start | integer  | string  |         | Defines the start range of the allowed port if protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534                   |
| port_range_end   | integer  | string  |         | Defines the end range of the allowed port if the protocol TCP or UDP is chosen. Leave value empty to allow all ports: 1 to 65534                 |
| icmp_type        |    no    | integer |         | Defines the allowed type if the protocol ICMP is chosen. No value allows all types: 0 to 254                                                     |
| icmp_code        |    no    | integer |         | Defines the allowed code if protocol ICMP is chosen. No value allows all codes: 0 to 254                                                         |
| api_url          |    no    | string  |         | The Ionos API base URL.                                                                                                                   |
| username         |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environment variable.                                                             |
| password         |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environment variable.                                                             |
| wait             |    no    | boolean | true    | Wait for the operation to complete before continuing.                                                                                            |
| wait_timeout     |    no    | integer | 600     | The number of seconds until the wait ends.                                                                                                       |
| state            |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                                                                              |

### ipblock

#### Example Syntax

    - name: Create IPBlock
      ipblock:
        name: spare
        location: us/ewr
        size: 2

#### Parameter Reference

The following parameters are supported:

| Name         | Required | Type    | Default | Description                                                                           |
| ------------ | :------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| name         | **yes**  | string  |         | The name of the IPBlock.                                                              |
| location     |    no    | string  | us/las  | The IPBlock location: us/las, us/ewr, de/fra, de/fkb, de/txl, gb/lhr                  |
| size         |    no    | integer | 1       | The number of IP addresses to allocate in the IPBlock.                                |
| api_url      |    no    | string  |         | The Ionos API base URL.                                                        |
| username     |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable. |
| password     |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable. |
| wait         |    no    | boolean | true    | Wait for the operation to complete before continuing.                                 |
| wait_timeout |    no    | integer | 600     | The number of seconds until the wait ends.                                            |
| state        |    no    | string  | present | Indicates desired state of the resource: **present**, absent                          |

### snapshot

#### Example Syntax

    - name: Create snapshot
      snapshot:
        datacenter: production DC
        volume: master
        name: boot volume snapshot

    - name: Restore snapshot
      snapshot:
        datacenter: production DC
        volume: slave
        name: boot volume snapshot
        state: restore

#### Parameter Reference

The following parameters are supported:

| Name                   |  Required  | Type    | Default | Description                                                                                                                      |
| ---------------------- | :--------: | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| datacenter             | **yes**/no | string  |         | The datacenter in which the volume resides. Required for `state='present'` or `state='restore'` to create or restore a snapshot. |
| volume                 | **yes**/no | string  |         | The volume to create or restore the snapshot. Required for `state='present'` or `state='restore'`.                               |
| name                   | **yes**/no | string  |         | The name of the snapshot. Required for `state='update'` or `state='absent'` to update or remove a snapshot.                      |
| description            |     no     | string  |         | The description of the snapshot.                                                                                                 |
| licence_type           |     no     | string  |         | The licence type for the volume. This is used when updating the snapshot: LINUX, WINDOWS, UNKNOWN, OTHER, WINDOWS2016            |
| cpu_hot_plug           |     no     | boolean |         | Indicates the volume is capable of CPU hot plug (no reboot required).                                                            |
| cpu_hot_unplug         |     no     | boolean |         | Indicates the volume is capable of CPU hot unplug (no reboot required).                                                          |
| ram_hot_plug           |     no     | boolean |         | Indicates the volume is capable of memory hot plug.                                                                              |
| ram_hot_unplug         |     no     | boolean |         | Indicates the volume is capable of memory hot unplug.                                                                            |
| nic_hot_plug           |     no     | boolean |         | Indicates the volume is capable of NIC hot plug.                                                                                 |
| nic_hot_unplug         |     no     | boolean |         | Indicates the volume is capable of NIC hot unplug.                                                                               |
| disc_virtio_hot_plug   |     no     | boolean |         | Indicates the volume is capable of VirtIO drive hot plug.                                                                        |
| disc_virtio_hot_unplug |     no     | boolean |         | Indicates the volume is capable of VirtIO drive hot unplug.                                                                      |
| disc_scsi_hot_plug     |     no     | boolean |         | Indicates the volume is capable of SCSI drive hot plug.                                                                          |
| disc_scsi_hot_unplug   |     no     | boolean |         | Indicates the volume is capable of SCSI drive hot unplug.                                                                        |
| api_url                |     no     | string  |         | The Ionos API base URL.                                                                                                   |
| username               |     no     | string  |         | The Ionos username. Overrides the IONOS_USERNAME environment variable.                                             |
| password               |     no     | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environment variable.                                             |
| wait                   |     no     | boolean | true    | Wait for the resource to be created before continuing.                                                                           |
| wait_timeout           |     no     | integer | 600     | The number of seconds until the wait ends.                                                                                       |
| state                  |     no     | string  | present | Indicate desired state of the resource: **present**, absent, restore, update                                                     |

### user

#### Example Syntax

    - name: Create user
      user:
        firstname: John
        lastname: Doe
        email: john.doe@example.com
        user_password: secretpassword123
        administrator: true

    - name: Update user
      user:
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

| Name           |  Required  | Type    | Default | Description                                                                                                                                  |
| -------------- | :--------: | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| firstname      | **yes**/no | string  |         | The user's first name. Required for `state='present'` only.                                                                                  |
| lastname       | **yes**/no | string  |         | The user's last name. Required for `state='present'` only.                                                                                   |
| email          |  **yes**   | string  |         | The user's email.                                                                                                                            |
| user_password  | **yes**/no | string  |         | A password for the user. Required for `state='present'` only.                                                                                |
| administrator  |     no     | boolean |         | Indicates if the user has administrative rights.                                                                                             |
| force_sec_auth |     no     | boolean |         | Indicates if secure (two-factor) authentication should be forced for the user.                                                               |
| groups         |     no     | list    |         | A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list (`[]`) to remove the user from all groups. |
| api_url        |     no     | string  |         | The Ionos API base URL.                                                                                                               |
| username       |     no     | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable.                                                        |
| password       |     no     | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable.                                                        |
| wait           |     no     | boolean | true    | Wait for the operation to complete before continuing.                                                                                        |
| wait_timeout   |     no     | integer | 600     | The number of seconds until the wait ends.                                                                                                   |
| state          |     no     | string  | present | Indicate desired state of the resource: **present**, absent, update                                                                          |

### group

#### Example Syntax

    - name: Create group
      group:
        name: guests
        create_datacenter: true
        create_snapshot: true
        reserve_ip: true
        access_activity_log: false

    - name: Update group
      group:
        name: guests
        create_datacenter: false
        users:
          - john.smith@test.com
        state: update

#### Parameter Reference

The following parameters are supported:

| Name                | Required | Type    | Default | Description                                                                                                                                |
| ------------------- | :------: | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| name                | **yes**  | string  |         | The name of the group.                                                                                                                     |
| create_datacenter   |    no    | boolean |         | Indicates if the group is allowed to create virtual data centers.                                                                          |
| create_snapshot     |    no    | boolean |         | Indicates if the group is allowed to create snapshots.                                                                                     |
| reserve_ip          |    no    | boolean |         | Indicates if the group is allowed to reserve IP addresses.                                                                                 |
| access_activity_log |    no    | boolean |         | Indicates if the group is allowed to access the activity log.                                                                              |
| users               |    no    | list    |         | A list of (non-administrator) user IDs or emails to associate with the group. Set to empty list (`[]`) to remove all users from the group. |
| api_url             |    no    | string  |         | The Ionos API base URL.                                                                                                             |
| username            |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable.                                                      |
| password            |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable.                                                      |
| wait                |    no    | boolean | true    | Wait for the operation to complete before continuing.                                                                                      |
| wait_timeout        |    no    | integer | 600     | The number of seconds until the wait ends.                                                                                                 |
| state               |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                                                                        |

### share

#### Example Syntax

    - name: Create shares
      share:
        group: Demo
        edit_privilege: true
        share_privilege: true
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
          - ba7efccb-a761-11e7-90a7-525400f64d8d
        state: present

    - name: Update shares
      share:
        group: Demo
        edit_privilege: false
        resource_ids:
          - b50ba74e-b585-44d6-9b6e-68941b2ce98e
        state: update

#### Parameter Reference

The following parameters are supported:

| Name            | Required | Type    | Default | Description                                                                           |
| --------------- | :------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| group           | **yes**  | string  |         | The name or ID of the group.                                                          |
| resource_ids    | **yes**  | list    |         | A list of resource IDs to add, update or remove as shares.                            |
| edit_privilege  |    no    | boolean |         | Indicates that the group has permission to edit privileges on the resource.           |
| share_privilege |    no    | boolean |         | Indicates that the group has permission to share the resource.                        |
| api_url         |    no    | string  |         | The Ionos API base URL.                                                        |
| username        |    no    | string  |         | The Ionos username. Overrides the IONOS_USERNAME environement variable. |
| password        |    no    | string  |         | The Ionos password. Overrides the IONOS_PASSWORD environement variable. |
| wait            |    no    | boolean | true    | Wait for the operation to complete before continuing.                                 |
| wait_timeout    |    no    | integer | 600     | The number of seconds until the wait ends.                                            |
| state           |    no    | string  | present | Indicate desired state of the resource: **present**, absent, update                   |

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
          server:
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
          register: ionos

        - debug: msg="{{ionos.machines}}"

        - name: Public SSH firewall rule
          firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              nic: "{{ item.nic.id }}"
              name: Allow SSH
              protocol: TCP
              source_ip: 0.0.0.0
              port_range_start: 22
              port_range_end: 22
              state: present
          with_items: "{{ ionos.machines }}"

        - name: Create private NIC
          nic:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              lan: 2
              state: present
          register: private_nic
          with_items: "{{ ionos.machines }}"

        - name: Create SSH firewall rule
          firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.item.id }}"
              nic: "{{ item.nic.id }}"
              name: Allow SSH
              protocol: TCP
              source_ip: 0.0.0.0
              port_range_start: 22
              port_range_end: 22
              state: present
          with_items: "{{ private_nic.results }}"

        - name: Create ping firewall rule
          firewall_rule:
              datacenter: "{{ datacenter }}"
              server: "{{ item.item.id }}"
              nic: "{{ item.nic.id }}"
              name: Allow Ping
              protocol: ICMP
              source_ip: 0.0.0.0
              icmp_type: 8
              icmp_code: 0
              state: present
          with_items: "{{ private_nic.results }}"

        - name: Create data volume
          volume:
              datacenter: "{{ datacenter }}"
              server: "{{ item.id }}"
              name: "{{ item.properties.name }}-data%02d"
              size: 50
              disk_type: SSD
              licence_type: OTHER
              wait_timeout: "{{ timeout }}"
              state: present
          with_items: "{{ ionos.machines }}"
          
### s3key

#### Example Syntax

    - name: Create an s3key
      s3key:
        user_id: "{{ user_id }}"

    - name: Update an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        active: False
        state: update

    - name: Remove an s3key
      s3key:
        user_id: "{{ user_id }}"
        key_id: "00ca413c94eecc56857d"
        state: absent

#### Parameter Reference

The following parameters are supported:

| Name         | Required | Type    | Default | Description                                                                           |
| ------------ | :------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| user_id      | **yes**  | string  |         | The unique ID of the user.                                                           |
| key_id       | **yes**  | string  |         | The ID of the key. Required only for state = 'update' or state = 'absent'               |
| active       |    no    | boolean |         | State of the key.                                                  |


### k8s_cluster

#### Example Syntax

    - name: Create k8s cluster
      k8s_cluster:
        name: "{{ cluster_name }}"

    - name: Delete k8s cluster
      k8s_cluster:
        k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
        state: absent

    - name: Update k8s cluster
      k8s_cluster:
        k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
        maintenance_window:
          day: 'Tuesday'
          time: '13:03:00'
        k8s_version: 1.17.8
        state: update
        

#### Parameter Reference

The following parameters are supported:

| Name               | Required   | Type    | Default | Description                                                                           |
| ------------------ | :--------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| cluster_name       | **yes**/no | string  |         | The name of the cluster. Required only for state = 'present'                                                           |
| k8s_cluster_id     | **yes**    | string  |         | The ID of the cluster. Required only for state = 'update' or state = 'absent'               |
| k8s_version        |    no      | string  |         | The kubernetes version in which the cluster is running.                                                  |
| maintenance_window |    no      |  dict   |         | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'.                                                          |



### k8s_nodepool

#### Example Syntax

    - name: Create k8s cluster nodepool
      k8s_nodepools:
        cluster_name: "{{ name }}"
        k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
        datacenter_id: "4d495548-e330-434d-83a9-251bfa645875"
        node_count: "1"
        cpu_family: "AMD_OPTERON"
        cores_count: "1"
        ram_size: "2048"
        availability_zone: "AUTO"
        storage_type: "SSD"
        storage_size: "100"

    - name: Delete k8s cluster nodepool
      k8s_nodepools:
        k8s_cluster_id: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
        nodepool_id: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
        state: absent

    - name: Update k8s cluster nodepool
      k8s_nodepools:
        cluster_name: "{{ name }}"
        k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
        nodepool_id: "6e9efcc6-649a-4514-bee5-6165b614c89e"
        node_count: 1
        cores_count: "1"
        maintenance_window:
          day: 'Tuesday'
          time: '13:03:00'
        auto_scaling:
          min_node_count: 1
          max_node_count: 3
        state: update


#### Parameter Reference

The following parameters are supported:

| Name               | Required   | Type    | Default | Description                                                                                                                                          |
| ------------------ | :--------: | ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| nodepool_name      | **yes**    | string  |         | The name of the nodepool. Required only for state = 'present'                                                                                        |
| k8s_cluster_id     | **yes**    | string  |         | The ID of the cluster.                                                                                                                               |
| nodepool_id        | **yes**/no | string  |         | The ID of the nodepool. Required for state = 'update' or state = 'absent'                                                                            |
| datacenter_id      | **yes**/no | string  |         | The ID of the datacenter. Required only for state = 'present'                                                                                        |
| node_count         | **yes**/no |  int    |         | The number of nodes in the nodepool. Required only for state = 'present'                                                                             |
| cpu_family         | **yes**/no | string  |         | A valid CPU family name. Required only for state = 'update' or state = 'absent'                                                                      |
| cores_count        | **yes**/no | string  |         | The number of cores. Required only for state = 'present'                                                                                             |
| ram_size           | **yes**/no | string  |         | RAM size for node, minimum size 2048MB is recommended. Required only for state = 'present'                                                           |
| availability_zone  | **yes**/no | string  |         | The availability zone in which the server should exist. Required only for state = 'present'                                                          |
| storage_type       | **yes**/no | string  |         | Hardware type of the volume. Required only for state = 'present'                                                                                     |
| storage_size       | **yes**/no | string  |         | The size of the volume in GB. The size should be greater than 10GB. Required only for state = 'present'                                              |
| maintenance_window |    no      |  dict   |         | The day and time for the maintenance. Contains 'dayOfTheWeek' and 'time'.                                                                            |
| auto_scaling       |    no      |  dict   |         | The minimum and maximum number of worker nodes that the managed node group can scale in. Contains 'min_node_count' and 'max_node_count'.             |



### k8s_config

#### Example Syntax

    - name: Get k8s config
      k8s_config:
        k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
        config_file: 'config.yaml'
        state: present

#### Parameter Reference

The following parameters are supported:

| Name               | Required   | Type    | Default | Description                                                                           |
| ------------------ | :--------: | ------- | ------- | ------------------------------------------------------------------------------------- |
| k8s_cluster_id     | **yes**    | string  |         | The ID of the cluster.                                                          |
| config_file        | **yes**    | string  |         | The name of the file that will contain the configuration of the cluster.                                                  |
          
### backupunit

#### Example Syntax

    - name: Create backupunit
      backupunit:
        backupunit_email: "{{ email }}"
        backupunit_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a backupunit
      backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        backupunit_email: "{{ updated_email }}"
        backupunit_password:  "{{ updated_password }}"
        state: update

    - name: Remove backupunit
      backupunit:
        backupunit_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        state: absent
        
#### Parameter Reference

The following parameters are supported:

| Name                  | Required    | Type    | Default | Description                                                                                                                                     |
| ----------------------| :---------: | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| name                  | **yes**/no  | string  |         | The resource name (only alphanumeric characters are acceptable). Only required when state = 'present'.                                          |
| backupunit_email      | **yes**/no  | string  |         | The email associated with the backup unit. This email does not have to be the same as the user's email.  Only required when state = 'present'.  |
| backupunit_password   | **yes**/no  | string  |         | The password associated to that resource.  Only required when state = 'present'.                                                                |
| backupunit_id         | **yes**/no  | string  |         | The ID of the backupunit.  Required when state = 'update' or state = 'absent'.                                                                  |

### pcc

#### Example Syntax

    - name: Create pcc
      pcc:
        name: "{{ name }}"
        description: "{{ description }}"

    - name: Update pcc
      pcc:
        pcc_id: "49e73efd-e1ea-11ea-aaf5-5254001a8838"
        name: "{{ new_name }}"
        description: "{{ new_description }}"
        state: update

    - name: Remove pcc
      pcc:
        pcc_id: "2851af0b-e1ea-11ea-aaf5-5254001a8838"
        state: absent
        
#### Parameter Reference

The following parameters are supported:

| Name            | Required    | Type    | Default | Description                                                                           |
| --------------- | :------:    | ------- | ------- | ------------------------------------------------------------------------------------- |
| pcc_id          | **yes**/no  | string  |         | The ID of the pcc. Required for state = 'update' or state = 'absent'.                  |
| name            | **yes**/no  | string  |         | The name of the pcc. Required only for state = 'present'.                              |
| description     |    no       | string  |         | The description of the pcc.                                                           |


## Support

You are welcome to contact us with questions or comments using the **Community** section of the [Ionos DevOps Central](https://devops.ionos.com/). Please report any feature requests or issues using GitHub issue tracker.

- [Ionos API](https://devops.ionos.com/api/cloud/v4/) documentation.
- Ask a question or discuss at [Ionos DevOps Central](https://devops.ionos.com/community/).
- Report an [issue here](https://github.com/ionos-cloud/sdk-ansible/issues).

## Testing

Set your Ionos user credentials.

    export IONOS_USERNAME=username
    export IONOS_PASSWORD=password

Change into the `tests` directory and execute the Playbooks.

    cd tests
    ansible-playbook server.yml

Note: The Ionos public image UUIDs change periodically due to updates. Therefore, it is recommended to use image aliases.

## Contributing

1. Fork the repository ([https://github.com/ionos-cloud/sdk-ansible/fork](https://github.com/ionos-cloud/sdk-ansible/fork))
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
