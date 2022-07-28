# data_platform_cluster_config

This is a simple module that supports getting config of DataPlatform clusters

## Example Syntax


```yaml

  - name: Get DataPlatform config
  data_platform_cluster_config:
    data_platform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Get DataPlatform config
  data_platform_cluster_config:
    data_platform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | data_platform_cluster_id | True | str |  | The ID of the Data Platform cluster. |
  | config_file | True | str |  | The name of the file in which to save the config. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
