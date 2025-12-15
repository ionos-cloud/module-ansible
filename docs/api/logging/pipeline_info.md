# pipeline_info

This is a simple module that supports listing existing Pipelines

## Example Syntax


```yaml

name: List Pipelines
ionoscloudsdk.ionoscloud.pipeline_info: null
register: pipelines_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "pipelines": [
        {
            "id": "f30a1c8f-334d-4238-b259-b0a761a87352",
            "type": "Pipeline",
            "metadata": {
                "created_date": "2023-10-17T15:19:14+00:00",
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_by_user_uuid": "<USER_UUID>",
                "last_modified_date": "2023-10-17T15:19:14+00:00",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_by_user_uuid": "<USER_UUID>",
                "status": "AVAILABLE"
            },
            "properties": {
                "name": "ansiblepipelinetest123",
                "logs": [
                    {
                        "public": true,
                        "source": "kubernetes",
                        "tag": "tag",
                        "protocol": "http",
                        "labels": null,
                        "destinations": [
                            {
                                "type": "loki",
                                "retention_in_days": 7
                            }
                        ]
                    }
                ],
                "tcp_address": "",
                "http_address": "<HTTP_ADDRESS>",
                "grafana_address": "<GRAFANA_ADDRESS>"
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/logging).

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
  <td>Filter that can be used to list only objects which have a certain set of properties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
