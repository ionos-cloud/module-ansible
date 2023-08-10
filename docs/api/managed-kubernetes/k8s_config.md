# k8s_config

This is a simple module that supports getting config of K8s clusters This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Get k8s config
  k8s_config:
    k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "failed": false,
    "changed": true,
    "config": "<CONFIG_FILE_CONTENT>"
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Get k8s config
  k8s_config:
    k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | k8s_cluster_id<br /><span style="color:#003d8f">str</span> | True | The ID of the K8s cluster. |
  | config_file<br /><span style="color:#003d8f">str</span> | True | The name of the file in which to save the config. |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | certificate_fingerprint<br /><span style="color:#003d8f">str</span> | False | The Ionos API certificate fingerprint. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:#003d8f">bool</span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:#003d8f">int</span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present'] |

&nbsp;

&nbsp;
