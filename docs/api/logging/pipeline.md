# pipeline

This is a module that supports creating, updating or destroying Pipelines

## Example Syntax


```yaml

name: Create Pipeline
ionoscloudsdk.ionoscloud.pipeline:
  name: 'ansiblepipelinetest'
  logs: '[{'source': 'kubernetes', 'tag': 'tag', 'protocol': 'http', 'destinations': [{'type': 'loki', 'retention_in_days': 7}]}]'
  wait: true
  wait_timeout: 1200
register: pipeline_response


name: Update pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  name: 'ansiblepipeNEW'
  logs: '[{'source': 'docker', 'tag': 'differenttag', 'protocol': 'tcp', 'labels': ['1'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}, {'source': 'kubernetes', 'tag': 'updatedtag', 'protocol': 'http', 'labels': ['2'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}]'
  state: update
register: updated_pipeline_response


name: Delete pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  wait: true
  state: absent


name: Renew Pipeline key
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  state: renew

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "update",
    "pipeline": {
        "id": "f30a1c8f-334d-4238-b259-b0a761a87352",
        "type": "Pipeline",
        "metadata": {
            "created_date": "2023-10-17T15:19:14+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_by_user_uuid": "<USER_UUID>",
            "last_modified_date": "2023-10-17T15:21:02+00:00",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_by_user_uuid": "<USER_UUID>",
            "status": "AVAILABLE"
        },
        "properties": {
            "name": "ansiblepipelinetest123UPDATED",
            "logs": [
                {
                    "public": false,
                    "source": "docker",
                    "tag": "differenttag",
                    "protocol": "tcp",
                    "labels": [
                        "new_label"
                    ],
                    "destinations": [
                        {
                            "type": "loki",
                            "retention_in_days": 14
                        }
                    ]
                },
                {
                    "public": false,
                    "source": "kubernetes",
                    "tag": "updatedtag",
                    "protocol": "http",
                    "labels": [
                        "label"
                    ],
                    "destinations": [
                        {
                            "type": "loki",
                            "retention_in_days": 14
                        }
                    ]
                }
            ],
            "tcp_address": "",
            "http_address": "<HTTP_ADDRESS>",
            "grafana_address": "<GRAFANA_ADDRESS>"
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/logging).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create Pipeline
ionoscloudsdk.ionoscloud.pipeline:
  name: 'ansiblepipelinetest'
  logs: '[{'source': 'kubernetes', 'tag': 'tag', 'protocol': 'http', 'destinations': [{'type': 'loki', 'retention_in_days': 7}]}]'
  wait: true
  wait_timeout: 1200
register: pipeline_response

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the pipeline. Must be not more that 20 characters long.</td>
  </tr>
  <tr>
  <td>logs<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>The information of the log pipelines</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  wait: true
  state: absent

```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>pipeline<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Pipeline.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  name: 'ansiblepipeNEW'
  logs: '[{'source': 'docker', 'tag': 'differenttag', 'protocol': 'tcp', 'labels': ['1'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}, {'source': 'kubernetes', 'tag': 'updatedtag', 'protocol': 'http', 'labels': ['2'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}]'
  state: update
register: updated_pipeline_response

```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the pipeline. Must be not more that 20 characters long.</td>
  </tr>
  <tr>
  <td>logs<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>The information of the log pipelines</td>
  </tr>
  <tr>
  <td>pipeline<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Pipeline.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **renew**
```yaml
  
name: Renew Pipeline key
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  state: renew

```
### Available parameters for state **renew**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>pipeline<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Pipeline.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update', 'renew']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
