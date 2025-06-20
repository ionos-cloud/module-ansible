# k8s_cluster

This is a simple module that supports creating or removing K8s Clusters. This module has a dependency on ionoscloud &gt;= 6.0.2

## Example Syntax


```yaml

name: Create k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  cluster_name: my-cluster-
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
register: cluster_response


name: Update k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  cluster_name: my_cluster
  k8s_cluster: ''
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  state: update
register: cluster


name: Delete k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  k8s_cluster: ''
  state: absent
  wait: false

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "cluster": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/k8s/b08b63ff-8bee-4091-ad5f-f8296eedd93b",
        "id": "b08b63ff-8bee-4091-ad5f-f8296eedd93b",
        "metadata": {
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>",
            "created_date": "2023-05-31T09:42:32+00:00",
            "etag": "28a43faaa371c59d79d86aca2d6f7792",
            "last_modified_by": "<USER_EMAIL>",
            "last_modified_by_user_id": "<USER_ID>",
            "last_modified_date": "2023-05-31T09:42:32+00:00",
            "state": "DEPLOYING"
        },
        "properties": {
            "api_subnet_allow_list": null,
            "available_upgrade_versions": null,
            "k8s_version": null,
            "maintenance_window": {
                "day_of_the_week": "Wednesday",
                "time": "12:02:00Z"
            },
            "name": "my-cluster-4",
            "s3_buckets": null,
            "viable_node_pool_versions": null
        },
        "type": "k8s"
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/managed-kubernetes).
&nbsp;

&nbsp;

# state: **present**
```yaml
  
name: Create k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  cluster_name: my-cluster-
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
register: cluster_response

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
  <td>cluster_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>k8s_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Kubernetes version that the cluster is running. This limits which Kubernetes versions can run in a cluster's node pools. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>The maintenance window is used to update the control plane and the K8s version of the cluster. If no value is specified, it is chosen dynamically, so there is no fixed default value.</td>
  </tr>
  <tr>
  <td>api_subnet_allow_list<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Access to the K8s API server is restricted to these CIDRs. Intra-cluster traffic is not affected by this restriction. If no AllowList is specified, access is not limited. If an IP is specified without a subnet mask, the default value is 32 for IPv4 and 128 for IPv6.</td>
  </tr>
  <tr>
  <td>s3_buckets_param<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of Object storage buckets configured for K8s usage. At the moment, it contains only one bucket that is used to store K8s API audit logs.</td>
  </tr>
  <tr>
  <td>public<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>The indicator whether the cluster is public or private. Note that the status FALSE is still in the beta phase.</td>
  </tr>
  <tr>
  <td>location<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>This attribute is mandatory if the cluster is private and optional if the cluster is public. The location must be enabled for your contract, or you must have a data center at that location. This property is not adjustable.</td>
  </tr>
  <tr>
  <td>nat_gateway_ip<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The nat gateway IP of the cluster if the cluster is private. This property is immutable. Must be a reserved IP in the same location as the cluster's location. This attribute is mandatory if the cluster is private.</td>
  </tr>
  <tr>
  <td>node_subnet<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The node subnet of the cluster, if the cluster is private. This property is optional and immutable. Must be a valid CIDR notation for an IPv4 network prefix of 16 bits length.</td>
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
name: Delete k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  k8s_cluster: ''
  state: absent
  wait: false

```
### Available parameters for state **absent**:
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  
name: Update k8s cluster
ionoscloudsdk.ionoscloud.k8s_cluster:
  cluster_name: my_cluster
  k8s_cluster: ''
  maintenance_window:
    day_of_the_week: Wednesday
    time: '12:02:00'
  state: update
register: cluster

```
### Available parameters for state **update**:
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
  <td>cluster_name<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>k8s_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the K8s cluster.</td>
  </tr>
  <tr>
  <td>k8s_version<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Kubernetes version that the cluster is running. This limits which Kubernetes versions can run in a cluster's node pools. Also, not all Kubernetes versions are suitable upgrade targets for all earlier versions.</td>
  </tr>
  <tr>
  <td>maintenance_window<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">True</td>
  <td>The maintenance window is used to update the control plane and the K8s version of the cluster. If no value is specified, it is chosen dynamically, so there is no fixed default value.</td>
  </tr>
  <tr>
  <td>api_subnet_allow_list<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>Access to the K8s API server is restricted to these CIDRs. Intra-cluster traffic is not affected by this restriction. If no AllowList is specified, access is not limited. If an IP is specified without a subnet mask, the default value is 32 for IPv4 and 128 for IPv6.</td>
  </tr>
  <tr>
  <td>s3_buckets_param<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>List of Object storage buckets configured for K8s usage. At the moment, it contains only one bucket that is used to store K8s API audit logs.</td>
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
  <td>How long before wait gives up, in seconds.<br />Default: 3600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
