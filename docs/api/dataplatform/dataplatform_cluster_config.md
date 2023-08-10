# dataplatform_cluster_config

This is a simple module that supports getting config of DataPlatform clusters

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml

  - name: Get DataPlatform config
  dataplatform_cluster_config:
    dataplatform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
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
  
  - name: Get DataPlatform config
  dataplatform_cluster_config:
    dataplatform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | cluster<br /><span style="color:#003d8f">str</span> | True | The name or the ID of the Data Platform cluster. |
  | config_file<br /><span style="color:#003d8f">str</span> | True | The name of the file in which to save the config. |
  | api_url<br /><span style="color:#003d8f">str</span> | False | The Ionos API base URL. |
  | username<br /><span style="color:#003d8f">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:#003d8f">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:#003d8f">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | state<br /><span style="color:#003d8f">str</span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present'] |

&nbsp;

&nbsp;
