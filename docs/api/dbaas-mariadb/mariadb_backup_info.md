# mariadb_backup_info

This is a simple module that supports listing existing MariaDB Cluster backups

## Example Syntax


```yaml

    - name: List MariaDB Cluster Backups
        mariadb_cluster_backup_info:
            mariadb_cluster: backuptest-04
        register: mariadb_backups_response

    - name: Show MariaDB Cluster Backups
        debug:
            var: mariadb_backups_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "mariadb_backups": [
        {
            "id": "745d661a-4b9a-4970-94c5-8aab9062ea35",
            "properties": {
                "cluster_id": "745d661a-4b9a-4970-94c5-8aab9062ea35",
                "earliest_recovery_target_time": "2024-03-19T14:35:39+00:00",
                "size": 1,
                "base_backups": [
                    {
                        "created": "2024-03-19T14:35:39+00:00",
                        "size": 1
                    }
                ]
            }
        }
    ],
    "failed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-mariadb).

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
  <td>mariadb_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing MariaDB Cluster.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location from which to retrieve clusters and backups. Different service endpoints are used based on location, possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;.</td>
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
