# nic_flowlog_info

This is a simple module that supports listing Flowlogs.

## Example Syntax


```yaml
name: List NIC Flowlogs
ionoscloudsdk.ionoscloud.nic_flowlog_info:
  datacenter: 'AnsibleAutoTestCompute'
  server: 'AnsibleAutoTestCompute'
  nic: 'AnsibleAutoTestCompute'
register: nic_flowlog_list_response

```


&nbsp;

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
  <td>datacenter<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the datacenter.</td>
  </tr>
  <tr>
  <td>server<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the Server.</td>
  </tr>
  <tr>
  <td>nic<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing NIC.</td>
  </tr>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
