# dataplatform_nodepool_info

This is a simple module that supports listing existing DataPlatform Nodepools

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

    - name: List DataPlatform Nodepools
        dataplatform_nodepool_info:
            cluster: ClusterName
        register: dataplatform_nodepools_response


    - name: Show DataPlatform Clusters
        debug:
            var: dataplatform_nodepools_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "6fcf85d2-d503-41e7-9f08-cbfa9ac6be80",
            "type": "nodepool",
            "href": "https://api.ionos.com/dataplatform/clusters/fe6a5792-7473-4067-ba83-6d135582e623/nodepools/6fcf85d2-d503-41e7-9f08-cbfa9ac6be80",
            "metadata": {
                "e_tag": null,
                "created_date": "2023-05-29T14:06:54+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_in_contract_number": "31909592",
                "last_modified_date": "2023-05-29T14:10:32+00:00",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "current_data_platform_version": "22.11",
                "current_data_platform_revision": 1,
                "available_upgrade_versions": [],
                "state": "AVAILABLE"
            },
            "properties": {
                "name": "my-nodepool",
                "data_platform_version": null,
                "datacenter_id": "f68205d8-8334-43b0-9f64-b06babcf5bd6",
                "node_count": 2,
                "cpu_family": "INTEL_SKYLAKE",
                "cores_count": 1,
                "ram_size": 2048,
                "availability_zone": "AUTO",
                "storage_type": "HDD",
                "storage_size": 100,
                "maintenance_window": {
                    "time": "12:02:00",
                    "day_of_the_week": "Wednesday"
                },
                "labels": {
                    "color": "blue",
                    "size": "11"
                },
                "annotations": {
                    "ann1": "updatedvalue1",
                    "ann2": "updatedvalue2"
                }
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;

&nbsp;
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| filters | False | dict |  | Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name' |
| cluster | True | str |  | The ID of the Data Platform cluster. |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
