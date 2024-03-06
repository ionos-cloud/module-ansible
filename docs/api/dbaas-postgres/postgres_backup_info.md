# postgres_backup_info

This is a simple module that supports listing existing Postgres Cluster backups

## Example Syntax


```yaml
name: List Postgres Cluster Backups
ionoscloudsdk.ionoscloud.postgres_backup_info: null
register: postgres_backup_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "postgres_backups": [
        {
            "type": "backup",
            "id": "06b53b38-398a-4fc6-8eed-a8f3d4847a76-4oymiqu-12",
            "metadata": {
                "created_date": "2023-08-09T14:55:33+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "id": null,
                "cluster_id": "06b53b38-398a-4fc6-8eed-a8f3d4847a76",
                "version": "12",
                "is_active": true,
                "earliest_recovery_target_time": "2023-08-09T15:07:48+00:00"
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
  <td>postgres_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing Postgres Cluster.</td>
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
