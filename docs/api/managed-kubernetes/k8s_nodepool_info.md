# k8s_nodepool_info

This is a simple module that supports listing k8s nodepools.

## Example Syntax


```yaml

name: List Nodepools
ionoscloudsdk.ionoscloud.k8s_nodepool_info:
  k8s_cluster: ''
register: k8s_nodepool_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "nodepools": [
        {
            "href": "https://api.ionos.com/cloudapi/v6/k8s/75214458-7d67-4c86-9213-df8b4fa6dc2a/nodepools/448a6330-7a67-4dde-ba92-84c2ea8fdbe2",
            "id": "448a6330-7a67-4dde-ba92-84c2ea8fdbe2",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T13:09:54+00:00",
                "etag": "60bcdb02bec2a0cd6c7908b7afd152f9",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T13:09:54+00:00",
                "state": "DEPLOYING"
            },
            "properties": {
                "annotations": {
                    "ann1": "value1",
                    "ann2": "value2"
                },
                "auto_scaling": {
                    "max_node_count": 3,
                    "min_node_count": 1
                },
                "availability_zone": "AUTO",
                "available_upgrade_versions": [],
                "cores_count": 1,
                "cpu_family": "INTEL_SKYLAKE",
                "datacenter_id": "2318e3c3-5114-4b2a-a1b6-8b26657c78a3",
                "k8s_version": "1.25.11",
                "labels": {
                    "color": "red",
                    "foo": "bar",
                    "size": "10"
                },
                "lans": [
                    {
                        "datacenter_id": null,
                        "dhcp": false,
                        "id": 1,
                        "routes": null
                    }
                ],
                "maintenance_window": {
                    "day_of_the_week": "Saturday",
                    "time": "03:47:54Z"
                },
                "name": "my-nodepool-26",
                "node_count": 2,
                "public_ips": [
                    "<IP1>",
                    "<IP2>",
                    "<IP3>",
                    "<IP4>"
                ],
                "ram_size": 2048,
                "storage_size": 100,
                "storage_type": "HDD"
            },
            "type": "nodepool"
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/managed-kubernetes).

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
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
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
