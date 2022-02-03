# Postgres Backup Info

## Example Syntax

```yaml
  - name: List Postgres Cluster Backups
    ionoscloudsdk.ionoscloud.postgres_cluster_info:
      postgres_cluster: {{ postgres_cluster.id }}
    register: postgres_clusters_response

  - name: Show Postgres Cluster Backups
    debug:
      var: postgres_clusters_response.result
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| postgres_cluster | no | string |  | Either a UUID or a display name of the Postgres cluster. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
