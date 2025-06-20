# datacenter

This is a simple module that supports creating or removing datacenters. A datacenter is required before you can create servers. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

name: Create datacenter
ionoscloudsdk.ionoscloud.datacenter:
  name: 'AnsibleAutoTestCompute'
  description: 'Ansible Compute test description'
  location: 'gb/lhr'
  wait: true
register: datacenter_response


name: Update datacenter no change 1
ionoscloudsdk.ionoscloud.datacenter:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  description: 'Ansible Compute test description CHANGED'
  state: update
  allow_replace: false
register: datacenter_response_no_change2


name: Remove datacenter
ionoscloudsdk.ionoscloud.datacenter:
  datacenter: ''
  name: 'AnsibleAutoTestCompute'
  state: absent
  wait: true
register: deleted_datacenter

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": false,
    "failed": false,
    "action": "create",
    "datacenter": {
        "entities": {
            "lans": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/lans",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/lans",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "loadbalancers": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/loadbalancers",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/loadbalancers",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "natgateways": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/natgateways",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/natgateways",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "networkloadbalancers": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/networkloadbalancers",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/networkloadbalancers",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "servers": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/servers",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/servers",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            },
            "volumes": {
                "links": null,
                "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82/volumes",
                "id": "9683f0c0-e311-4194-bddc-a99bb2babf82/volumes",
                "items": null,
                "limit": null,
                "offset": null,
                "type": "collection"
            }
        },
        "href": "https://api.ionos.com/cloudapi/v6/datacenters/9683f0c0-e311-4194-bddc-a99bb2babf82",
        "id": "9683f0c0-e311-4194-bddc-a99bb2babf82",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-30T11:24:38+00:00",
            "etag": "f157640f8bc27aba358aed5cfbd74bf2",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-30T11:24:38+00:00",
            "state": "AVAILABLE"
        },
        "properties": {
            "cpu_architecture": [
                {
                    "cpu_family": "INTEL_SKYLAKE",
                    "max_cores": 4,
                    "max_ram": 20480,
                    "vendor": "GenuineIntel"
                }
            ],
            "description": "Ansible Compute test description",
            "features": [
                "cloud-init-private-image",
                "vm-autoscaling",
                "ssd",
                "vnf-nat",
                "k8s",
                "ssd-storage-zoning",
                "nic-hot-plug",
                "vnf-lb",
                "monitoring",
                "nic-hot-unplug",
                "pcc",
                "contract-identities",
                "disk-vio-hot-unplug",
                "disk-vio-hot-plug",
                "cloud-init",
                "flow-logs",
                "cpu-hot-plug",
                "core-vps",
                "k8s-cidr-s3-support",
                "private-loadbalancer",
                "mem-hot-plug",
                "vnf-alb"
            ],
            "location": "gb/lhr",
            "name": "AnsibleAutoTestCompute",
            "sec_auth_protection": false,
            "version": 2
        },
        "type": "datacenter"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).
&nbsp;

 **_NOTE:_**   **If you are using a versions 7.0.0 and up**: modules can replace resources if certain set parameters differ from the results found in the API!
## Parameters that can trigger a resource replacement:
  * location 
&nbsp;

# state: **present**
```yaml
  
name: Create datacenter
ionoscloudsdk.ionoscloud.datacenter:
  name: 'AnsibleAutoTestCompute'
  description: 'Ansible Compute test description'
  location: 'gb/lhr'
  wait: true
register: datacenter_response

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
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A description for the datacenter, such as staging, production.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The physical location where the datacenter will be created. This will be where all of your servers live. Property cannot be modified after datacenter creation (disallowed in update requests).<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr', 'es/vit', 'fr/par', 'us/mci']</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Remove datacenter
ionoscloudsdk.ionoscloud.datacenter:
  datacenter: ''
  name: 'AnsibleAutoTestCompute'
  state: absent
  wait: true
register: deleted_datacenter

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
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the virtual datacenter.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update datacenter no change 1
ionoscloudsdk.ionoscloud.datacenter:
  datacenter: 'AnsibleAutoTestCompute'
  name: 'AnsibleAutoTestCompute'
  description: 'Ansible Compute test description CHANGED'
  state: update
  allow_replace: false
register: datacenter_response_no_change2

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
  <td>The name of the  resource.</td>
  </tr>
  <tr>
  <td>description<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A description for the datacenter, such as staging, production.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The physical location where the datacenter will be created. This will be where all of your servers live. Property cannot be modified after datacenter creation (disallowed in update requests).<br />Options: ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr', 'es/vit', 'fr/par', 'us/mci']</td>
  </tr>
  <tr>
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the virtual datacenter.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indicating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
