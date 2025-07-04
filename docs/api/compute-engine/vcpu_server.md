# vcpu_server

Create, update, destroy, update, start, stop, and reboot a Ionos virtual machine. When the virtual machine is created it can optionally wait for it to be 'running' before returning.

## Example Syntax


```yaml

name: Provision two servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  cores: 1
  ram: 1024
  availability_zone: ZONE_1
  lan: 'AnsibleAutoTestCompute'
  volume_availability_zone: ZONE_3
  volume_size: 20
  disk_type: SSD Standard
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  location: de/txl
  user_data: ''
  count: 2
  remove_boot_volume: true
  wait: true
  wait_timeout: '500'
  state: present
register: server_create_result


name: Update servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  - 'AnsibleAutoTestCompute 02'
  cores: 2
  ram: 2048
  wait_timeout: '500'
  state: update


name: Remove servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  remove_boot_volume: true
  wait_timeout: '500'
  state: absent


name: Start servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: '500'
  state: running


name: Stop servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: '500'
  state: stopped

```


### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

&nbsp;

# state: **running**
```yaml
  
name: Start servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: '500'
  state: running

```
### Available parameters for state **running**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter to provision this virtual machine.</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **stopped**
```yaml
  
name: Stop servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  wait_timeout: '500'
  state: stopped

```
### Available parameters for state **stopped**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter to provision this virtual machine.</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Remove servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute'
  - 'AnsibleAutoTestCompute 02'
  remove_boot_volume: true
  wait_timeout: '500'
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the virtual machine.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter to provision this virtual machine.</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **present**
```yaml
  
name: Provision two servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute %02d'
  cores: 1
  ram: 1024
  availability_zone: ZONE_1
  lan: 'AnsibleAutoTestCompute'
  volume_availability_zone: ZONE_3
  volume_size: 20
  disk_type: SSD Standard
  image: 'ubuntu:latest'
  image_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  location: de/txl
  user_data: ''
  count: 2
  remove_boot_volume: true
  wait: true
  wait_timeout: '500'
  state: present
register: server_create_result

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the virtual machine.</td>
  </tr>
  <tr>
  <td>assign_public_ip<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>This will assign the machine to the public LAN. If no LAN exists with public Internet access it is created.<br />Default: False<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>image<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The image alias or ID for creating the virtual machine.</td>
  </tr>
  <tr>
  <td>image_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Password set for the administrative user.</td>
  </tr>
  <tr>
  <td>ssh_keys<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Public SSH keys allowing access to the virtual machine.<br />Default: </td>
  </tr>
  <tr>
  <td>user_data<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The cloud-init configuration for the volume as base64 encoded string.</td>
  </tr>
  <tr>
  <td>volume_availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The storage availability zone assigned to the volume.<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3']</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter to provision this virtual machine.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of CPU cores to allocate to the virtual machine.<br />Default: 2</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory to allocate to the virtual machine.<br />Default: 2048</td>
  </tr>
  <tr>
  <td>availability_zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The availability zone assigned to the server.<br />Default: AUTO<br />Options: ['AUTO', 'ZONE_1', 'ZONE_2', 'ZONE_3']</td>
  </tr>
  <tr>
  <td>volume_size<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The size in GB of the boot volume.<br />Default: 10</td>
  </tr>
  <tr>
  <td>bus<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The bus type for the volume.<br />Default: VIRTIO<br />Options: ['IDE', 'VIRTIO']</td>
  </tr>
  <tr>
  <td>count<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of virtual machines to create.<br />Default: 1</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The datacenter location. Use only if you want to create the Datacenter or else this value is ignored.<br />Default: us/las<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr']</td>
  </tr>
  <tr>
  <td>lan<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of the LAN you wish to add the servers to (can be a string or a number).</td>
  </tr>
  <tr>
  <td>nat<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean value indicating if the private IP address has outbound access to the public Internet.<br />Default: False<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>remove_boot_volume<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Remove the bootVolume of the virtual machine you're destroying.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>disk_type<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The disk type for the volume.<br />Default: HDD<br />Options: ['HDD', 'SSD', 'SSD Standard', 'SSD Premium', 'DAS']</td>
  </tr>
  <tr>
  <td>nic_ips<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The list of IPS for the NIC.</td>
  </tr>
  <tr>
  <td>boot_volume<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The volume used for boot.</td>
  </tr>
  <tr>
  <td>boot_cdrom<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The CDROM used for boot.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update servers
ionoscloudsdk.ionoscloud.vcpu_server:
  datacenter: 'AnsibleAutoTestCompute'
  instance_ids:
  - 'AnsibleAutoTestCompute 01'
  - 'AnsibleAutoTestCompute 02'
  cores: 2
  ram: 2048
  wait_timeout: '500'
  state: update

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the virtual machine.</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The datacenter to provision this virtual machine.</td>
  </tr>
  <tr>
  <td>cores<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The number of CPU cores to allocate to the virtual machine.<br />Default: 2</td>
  </tr>
  <tr>
  <td>ram<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The amount of memory to allocate to the virtual machine.<br />Default: 2048</td>
  </tr>
  <tr>
  <td>instance_ids<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>list of instance ids. Should only contain one ID if renaming in update state<br />Default: </td>
  </tr>
  <tr>
  <td>boot_volume<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The volume used for boot.</td>
  </tr>
  <tr>
  <td>boot_cdrom<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The CDROM used for boot.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['running', 'stopped', 'absent', 'present', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
