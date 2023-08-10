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

| Name | Required | Description |
| :--- | :---: | :--- |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
