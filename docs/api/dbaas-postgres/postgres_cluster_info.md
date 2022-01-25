# Postgres Cluster Info

## Example Syntax

```yaml
  - name: List Postgres Clusters
      postgres_cluster_info:
      register: postgres_clusters_response


  - name: Show Postgres Clusters
      debug:
          var: postgres_clusters_response.result
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
