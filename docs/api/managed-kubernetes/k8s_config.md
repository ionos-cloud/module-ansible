# k8s_config

This is a simple module that supports getting the config of K8s clusters This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

  - name: Get k8s config
  k8s_config:
    k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
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
    k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | k8s_cluster | True | str |  | The ID or name of the K8s cluster. |
  | config_file | True | str |  | The name of the file in which to save the config. |
  | api_url | False | str |  | The Ionos API base URL. |
  | certificate_fingerprint | False | str |  | The Ionos API certificate fingerprint. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
