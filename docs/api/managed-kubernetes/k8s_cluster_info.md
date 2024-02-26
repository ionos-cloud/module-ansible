# k8s_cluster_info

This is a simple module that supports listing k8s clusters.

## Example Syntax


```yaml

    - name: Get all k8s clusters
      k8s_cluster_info:
      register: k8s_cluster_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "clusters": [
        {
            "entities": {
                "nodepools": {
                    "href": "https://api.ionos.com/cloudapi/v6/k8s/75214458-7d67-4c86-9213-df8b4fa6dc2a/nodepools",
                    "id": "75214458-7d67-4c86-9213-df8b4fa6dc2a/nodepools",
                    "items": null,
                    "type": "collection"
                }
            },
            "href": "https://api.ionos.com/cloudapi/v6/k8s/75214458-7d67-4c86-9213-df8b4fa6dc2a",
            "id": "75214458-7d67-4c86-9213-df8b4fa6dc2a",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-08-03T13:04:58+00:00",
                "etag": "12ef56686a1f54b5776f6067651a574a",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-08-03T13:04:58+00:00",
                "state": "ACTIVE"
            },
            "properties": {
                "api_subnet_allow_list": null,
                "available_upgrade_versions": [
                    "1.26.6",
                    "1.26.5",
                    "1.26.4"
                ],
                "k8s_version": "1.25.11",
                "maintenance_window": {
                    "day_of_the_week": "Thursday",
                    "time": "22:37:58Z"
                },
                "name": "my-cluster-4",
                "s3_buckets": null,
                "viable_node_pool_versions": [
                    "1.25.11",
                    "1.25.10",
                    "1.25.9",
                    "1.25.6",
                    "1.25.5",
                    "1.24.15",
                    "1.24.14",
                    "1.24.13",
                    "1.24.10",
                    "1.24.9",
                    "1.24.8",
                    "1.24.6"
                ]
            },
            "type": "k8s"
        }
    ],
    "failed": false
}

```

&nbsp;

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
