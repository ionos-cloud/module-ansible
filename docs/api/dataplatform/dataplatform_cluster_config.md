# dataplatform_cluster_config

This is a simple module that supports getting config of DataPlatform clusters

⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.

## Example Syntax


```yaml
name: Get kubeconfig by ID
ionoscloudsdk.ionoscloud.dataplatform_cluster_config:
  cluster: ''
  config_file: config.yaml

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

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dataplatform).
&nbsp;

&nbsp;

# state: **present**
```yaml
  name: Get kubeconfig by ID
ionoscloudsdk.ionoscloud.dataplatform_cluster_config:
  cluster: ''
  config_file: config.yaml

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
  <td>cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name or the ID of the Data Platform cluster.</td>
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
