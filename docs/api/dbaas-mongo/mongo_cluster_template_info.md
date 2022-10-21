# mongo_cluster_template_info

This is a simple module that supports listing existing Mongo Cluster Templates

## Example Syntax


```yaml

    - name: List Mongo Cluster Templates
        mongo_cluster_templates_info:
        register: mongo_cluster_templates_response


    - name: Show Mongo Cluster Templates
        debug:
            var: mongo_cluster_templates_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| api_url | False | str |  | The Ionos API base URL. |
| username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
