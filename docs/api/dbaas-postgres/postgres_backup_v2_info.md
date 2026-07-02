# postgres_backup_v2_info

This is a simple module that supports listing existing Postgres Cluster backups using the DBaaS PostgreSQL v2 API. There is no per-cluster backups endpoint, so when I(postgres_cluster) is provided the account-wide backup list is filtered by cluster id server-side via the API's filter parameter.

## Example Syntax


```yaml

name: List Postgres Cluster Backups (all)
ionoscloudsdk.ionoscloud.postgres_backup_v2_info:
  location: ''
register: postgres_backup_response

```


&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-postgres).

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
  <td>postgres_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The ID or name of an existing Postgres Cluster. If set, only backups belonging to this cluster are returned.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The location (region) whose regional endpoint will be queried. Possible options are: &quot;de/fra&quot;, &quot;de/txl&quot;, &quot;es/vit&quot;, &quot;fr/par&quot;, &quot;gb/lhr&quot;, &quot;gb/bhx&quot;, &quot;us/ewr&quot;, &quot;us/las&quot;, &quot;us/mci&quot;. If not set, the endpoint will be the one corresponding to &quot;de/txl&quot;. The api_url, if set, overrides this.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of properties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
