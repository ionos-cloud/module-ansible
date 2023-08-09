# k8s_nodepool_info

This is a simple module that supports listing k8s nodepools.

## Example Syntax


```yaml

    - name: Get all k8s nodepools in a cluster
      k8s_nodepool_info:
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

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| k8s_cluster | True | str |  | The ID or name of the K8s cluster. |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| depth | False | int | 1 | The depth used when retrieving the items. |
| api_url | False | str |  | The Ionos API base URL. |
| certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
