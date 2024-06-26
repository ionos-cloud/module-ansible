# vm_autoscaling_group_info

This is a simple module that supports listing existing VM Autoscaling Groups

## Example Syntax


```yaml

name: List VM Autoscaling Groups
ionoscloudsdk.ionoscloud.vm_autoscaling_group_info: null
register: vm_autoscaling_groups_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "result": [
        {
            "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66",
            "type": "autoscaling-group",
            "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66",
            "metadata": {
                "created_by": "<USER_EMAIL>",
                "created_by_user_id": "<USER_ID>",
                "created_date": "2023-10-30T13:53:50.863223+00:00",
                "etag": "TefQ2rgppiLzKV2Rq9hUFgP3iRM8qsMKTkTgkVcCEro=",
                "last_modified_by": "<USER_EMAIL>",
                "last_modified_by_user_id": "<USER_ID>",
                "last_modified_date": "2023-10-30T13:56:15.276450+00:00",
                "state": "AVAILABLE"
            },
            "properties": {
                "datacenter": {
                    "id": "8b8b9122-b8ef-4966-a36a-2e9cf8609121",
                    "type": "datacenter",
                    "href": "https://api.public.production.k8s.fra2.profitbricks.net/cloudapi/v6/datacenters/8b8b9122-b8ef-4966-a36a-2e9cf8609121"
                },
                "location": "us/las",
                "max_replica_count": 5,
                "min_replica_count": 1,
                "name": "AnsibleVMAutoscalingGroup",
                "policy": {
                    "metric": "INSTANCE_CPU_UTILIZATION_AVERAGE",
                    "range": "PT24H",
                    "scale_in_action": {
                        "amount": 1.0,
                        "amount_type": "ABSOLUTE",
                        "cooldown_period": "PT5M",
                        "termination_policy": "RANDOM",
                        "delete_volumes": true
                    },
                    "scale_in_threshold": 33.0,
                    "scale_out_action": {
                        "amount": 1.0,
                        "amount_type": "ABSOLUTE",
                        "cooldown_period": "PT5M"
                    },
                    "scale_out_threshold": 77.0,
                    "unit": "PER_HOUR"
                },
                "replica_configuration": {
                    "availability_zone": "AUTO",
                    "cores": 2,
                    "cpu_family": "INTEL_XEON",
                    "nics": [
                        {
                            "lan": 1,
                            "name": "SDK_TEST_NIC1",
                            "dhcp": true,
                            "firewall_active": null,
                            "firewall_type": null,
                            "flow_logs": [],
                            "firewall_rules": [],
                            "target_group": null
                        },
                        {
                            "lan": 1,
                            "name": "SDK_TEST_NIC2",
                            "dhcp": false,
                            "firewall_active": null,
                            "firewall_type": null,
                            "flow_logs": [],
                            "firewall_rules": [],
                            "target_group": null
                        }
                    ],
                    "ram": 1024,
                    "volumes": [
                        {
                            "image": "b6d8c6f2-febc-11ed-86e8-2e7f0689c849",
                            "image_alias": null,
                            "name": "SDK_TEST_VOLUME",
                            "size": 50,
                            "ssh_keys": [],
                            "type": "HDD",
                            "user_data": null,
                            "bus": "IDE",
                            "backupunit_id": null,
                            "boot_order": "AUTO",
                            "image_password": null
                        }
                    ]
                }
            },
            "entities": {
                "actions": {
                    "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions",
                    "type": "collection",
                    "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/actions"
                },
                "servers": {
                    "id": "cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/servers",
                    "type": "collection",
                    "href": "https://api.ionos.com/autoscaling/groups/cd7407bc-54ff-4dcb-bf0e-6c2f7fa45c66/servers"
                }
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
