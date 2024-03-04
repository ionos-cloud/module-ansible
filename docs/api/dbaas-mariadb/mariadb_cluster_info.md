# mariadb_cluster_info

This is a simple module that supports listing existing MariaDB Clusters

## Example Syntax


```yaml

    - name: List MariaDB Clusters
        mariadb_cluster_info:
        register: mariadb_clusters_response

    - name: Show MariaDB Clusters
        debug:
            var: mariadb_clusters_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "mariadb_clusters": [
        {
            "id": "7182ab85-3671-45e5-b2bb-e943c4479e03",
            "metadata": {
                "created_date": "2024-02-27T16:02:55+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "last_modified_date": "2024-02-27T16:02:55+00:00",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "state": "AVAILABLE"
            },
            "properties": {
                "display_name": "MariaDB-cluster",
                "mariadb_version": "10.6",
                "dns_name": "<CLUSTER_DNS>",
                "instances": 1,
                "ram": 4,
                "cores": 4,
                "storage_size": 10,
                "connections": [
                    {
                        "datacenter_id": "3e223566-5a98-495a-9e4c-2c5fc71c057b",
                        "lan_id": "2",
                        "cidr": "<CIDR"
                    }
                ],
                "maintenance_window": {
                    "time": "14:17:42",
                    "day_of_the_week": "Tuesday"
                }
            }
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
