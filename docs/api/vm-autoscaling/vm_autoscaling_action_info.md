# vm_autoscaling_action_info

This is a simple module that supports listing existing VM Autoscaling Group Actions

## Example Syntax


```yaml

name: List VM Autoscaling Group Actions
ionoscloudsdk.ionoscloud.vm_autoscaling_action_info:
  vm_autoscaling_group: ''
register: vm_autoscaling_actions_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "4293fe77-1fc5-42e9-aff4-2ed8341c1b0e",
            "type": "autoscaling-action",
            "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions/4293fe77-1fc5-42e9-aff4-2ed8341c1b0e",
            "metadata": {
                "created_date": "2023-10-30T13:53:50.864025+00:00",
                "etag": "gwd8DcnJt7zZJhhm+3Q3yDZ2u/kRCsheLOxHXYOTVbc=",
                "last_modified_date": "2023-10-30T13:54:57.443808+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "action_status": "SUCCESSFUL",
                "action_type": "SCALE_OUT"
            }
        }
    ],
    "failed": false,
    "changed": false
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/vm-autoscaling).

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
  <td>vm_autoscaling_group<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing VM Autoscaling Group.</td>
  </tr>
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
