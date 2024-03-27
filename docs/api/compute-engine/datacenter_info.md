# datacenter_info

This is a simple module that supports listing Datacenter.

## Example Syntax


```yaml

name: List Datacenters
ionoscloudsdk.ionoscloud.datacenter_info: null
register: datacenter_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "datacenters": [
        {
            "entities": {
                "lans": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/lans",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/lans",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "loadbalancers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/loadbalancers",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/loadbalancers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "natgateways": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/natgateways",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/natgateways",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "networkloadbalancers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/networkloadbalancers",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/networkloadbalancers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "servers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/servers",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/servers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513/volumes",
                    "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513/volumes",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/64d0766b-0fd0-458e-9bc9-33c885f2d513",
            "id": "64d0766b-0fd0-458e-9bc9-33c885f2d513",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2021-05-20T07:30:50+00:00",
                "etag": "e62eb402a429620cab4172c15dd6e27d",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2022-08-22T13:34:07+00:00",
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
                "description": "Datacenter created by an automated test.",
                "features": [
                    "cloud-init-private-image",
                    "vm-autoscaling",
                    "vnf-nat",
                    "ssd",
                    "k8s",
                    "ssd-storage-zoning",
                    "vnf-lb",
                    "nic-hot-plug",
                    "monitoring",
                    "pcc",
                    "nic-hot-unplug",
                    "contract-identities",
                    "disk-vio-hot-unplug",
                    "disk-vio-hot-plug",
                    "cloud-init",
                    "acronis-api-v2",
                    "flow-logs",
                    "cpu-hot-plug",
                    "core-vps",
                    "k8s-cidr-s3-support",
                    "vnf-alb",
                    "mem-hot-plug",
                    "private-loadbalancer"
                ],
                "location": "de/fra",
                "name": "SDK AUTO-TEST",
                "sec_auth_protection": false,
                "version": 16
            },
            "type": "datacenter"
        },
        {
            "entities": {
                "lans": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/lans",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/lans",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "loadbalancers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/loadbalancers",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/loadbalancers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "natgateways": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/natgateways",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/natgateways",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "networkloadbalancers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/networkloadbalancers",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/networkloadbalancers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "servers": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/servers",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/servers",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                },
                "volumes": {
                    "links": null,
                    "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26/volumes",
                    "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26/volumes",
                    "items": null,
                    "limit": null,
                    "offset": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/datacenters/328e0a22-a3de-4885-9aa3-ac4b8ca96d26",
            "id": "328e0a22-a3de-4885-9aa3-ac4b8ca96d26",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-05-10T14:32:33+00:00",
                "etag": "cec0304fe32078a996b2f991003ba35c",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-05-10T14:32:33+00:00",
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
                "description": null,
                "features": [
                    "cloud-init-private-image",
                    "vm-autoscaling",
                    "vnf-nat",
                    "ssd",
                    "k8s",
                    "ssd-storage-zoning",
                    "vnf-lb",
                    "nic-hot-plug",
                    "monitoring",
                    "pcc",
                    "nic-hot-unplug",
                    "contract-identities",
                    "disk-vio-hot-unplug",
                    "disk-vio-hot-plug",
                    "cloud-init",
                    "acronis-api-v2",
                    "flow-logs",
                    "cpu-hot-plug",
                    "core-vps",
                    "k8s-cidr-s3-support",
                    "vnf-alb",
                    "mem-hot-plug",
                    "private-loadbalancer"
                ],
                "location": "de/fra",
                "name": "AnsibleVMAutoscaling",
                "sec_auth_protection": false,
                "version": 2
            },
            "type": "datacenter"
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/compute-engine).

&nbsp;
### Available parameters:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
  </tbody>
</table>
