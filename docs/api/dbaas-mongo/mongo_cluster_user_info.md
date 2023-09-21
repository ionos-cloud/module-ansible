# mongo_cluster_user_info

This is a simple module that supports listing existing Mongo Clusters

## Example Syntax


```yaml

    - name: List Mongo Clusters
        mongo_cluster_info:
        register: mongo_clusters_response


    - name: Show Mongo Clusters
        debug:
            var: mongo_clusters_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "type": "user",
            "metadata": {
                "created_date": "2023-05-30T14:20:09+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>"
            },
            "properties": {
                "username": "testuser",
                "password": null,
                "roles": [
                    {
                        "role": "read",
                        "database": "test"
                    }
                ]
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
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name'</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
