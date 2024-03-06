# mongo_cluster_info

This is a simple module that supports listing existing the users in a Mongo Cluster

## Example Syntax


```yaml
name: List Mongo Clusters
ionoscloudsdk.ionoscloud.mongo_cluster_info: null
register: mongo_clusters_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "type": "cluster",
            "id": "3fdd2940-f9b4-425d-b52b-4199a84188d2",
            "metadata": {
                "created_date": "2023-05-30T13:43:20+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": "AVAILABLE",
                "health": "HEALTHY"
            },
            "properties": {
                "display_name": "AnsibleTestMongoDBCluster",
                "mongo_db_version": "5.0",
                "location": "de/fra",
                "instances": 3,
                "connections": [
                    {
                        "datacenter_id": "6b36f398-2089-414b-a57f-85f7b88aee5b",
                        "lan_id": "1",
                        "cidr_list": [
                            "<CIDR1>",
                            "<CIDR2>",
                            "<CIDR3>"
                        ]
                    }
                ],
                "maintenance_window": {
                    "time": "14:13:28",
                    "day_of_the_week": "Thursday"
                },
                "template_id": "6b78ea06-ee0e-4689-998c-fc9c46e781f6",
                "connection_string": "<CONNECTION_STRING>"
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
