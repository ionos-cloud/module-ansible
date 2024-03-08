# k8s_config

This is a simple module that supports getting the config of K8s clusters This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml
name: Get k8s config
ionoscloudsdk.ionoscloud.k8s_config:
  k8s_cluster: ''
  config_file: config.yaml
  state: present

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

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/managed-kubernetes).
&nbsp;

&nbsp;

# state: **present**
```yaml
  name: Get k8s config
ionoscloudsdk.ionoscloud.k8s_config:
  k8s_cluster: ''
  config_file: config.yaml
  state: present

```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>config_file<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the file in which to save the config.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
