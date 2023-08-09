# datacenter

This is a simple module that supports creating or removing datacenters. A datacenter is required before you can create servers. This module has a dependency on ionoscloud &gt;= 6.0.2

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
      datacenter: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  
# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      datacenter: "Example DC"
      state: absent
  
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

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a Datacenter
  - name: Create datacenter
    datacenter:
      name: "Example DC"
      description: "description"
      location: de/fra
    register: datacenter_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of the  resource. |
  | description | False | str |  | A description for the datacenter, such as staging, production. |
  | location | True | str |  | The physical location where the datacenter will be created. This will be where all of your servers live. Property cannot be modified after datacenter creation (disallowed in update requests). |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
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
  # Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      datacenter: "Example DC"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | datacenter | True | str |  | The ID or name of the virtual datacenter. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
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
  # Update a datacenter description
  - name: Update datacenter
    datacenter:
      datacenter: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of the  resource. |
  | description | False | str |  | A description for the datacenter, such as staging, production. |
  | location | False | str |  | The physical location where the datacenter will be created. This will be where all of your servers live. Property cannot be modified after datacenter creation (disallowed in update requests). |
  | datacenter | True | str |  | The ID or name of the virtual datacenter. |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
