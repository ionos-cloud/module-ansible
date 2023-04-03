# dataplatform_nodepool

This is a simple module that supports creating or removing Data Platform Nodepools. This module has a dependency on ionoscloud_dataplatform &gt;= 1.0.0

## Example Syntax


```yaml

  - name: Create Data Platform nodepool
    dataplatform_nodepool:
      name: "{{ name }}"
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: 1
      ram_size: 2048
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: 100
  

  - name: Update Data Platform nodepool
    dataplatform_nodepool:
      name: "{{ name }}"
      cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      node_count: 1
      cores_count: 1
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      state: update
  

  - name: Delete Data Platform nodepool
    dataplatform_nodepool:
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
&nbsp;

&nbsp;

# state: **present**
```yaml
  
  - name: Create Data Platform nodepool
    dataplatform_nodepool:
      name: "{{ name }}"
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      node_count: 1
      cpu_family: "AMD_OPTERON"
      cores_count: 1
      ram_size: 2048
      availability_zone: "AUTO"
      storage_type: "SSD"
      storage_size: 100
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | True | str |  | The name of your node pool. Must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | cluster | True | str |  | The name or ID of the Data Platform cluster. |
  | node_count | True | int |  | The number of nodes that make up the node pool. |
  | cpu_family | True | str |  | A valid CPU family name or `AUTO` if the platform shall choose the best fitting option.Available CPU architectures can be retrieved from the datacenter resource. |
  | cores_count | True | int |  | The number of cores for the node. |
  | ram_size | True | int |  | The RAM size for the node. Must be set in multiples of 1024 MB, with minimum size is of 2048 MB. |
  | availability_zone | True | str |  | The availability zone of the virtual datacenter region where the node pool resources should be provisioned. |
  | storage_type | True | str |  | The type of hardware for the volume. |
  | storage_size | True | int |  | The size of the volume in GB. The size should be greater than 10GB. |
  | maintenance_window | False | dict |  | The maintenance window is used for updating the software on the nodepool's nodes and for upgrading the nodepool's version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | labels | False | dict |  | Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) |
  | annotations | False | dict |  | Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  
  - name: Delete Data Platform nodepool
    dataplatform_nodepool:
      cluster: "a0a65f51-4d3c-438c-9543-39a3d7668af3"
      nodepool: "e3aa6101-436f-49fa-9a8c-0d6617e0a277"
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | cluster | True | str |  | The name or ID of the Data Platform cluster. |
  | nodepool | True | str |  | The name or ID of the Data Platform nodepool. |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
# state: **update**
```yaml
  
  - name: Update Data Platform nodepool
    dataplatform_nodepool:
      name: "{{ name }}"
      cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
      node_count: 1
      cores_count: 1
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

  | Name | Required | Type | Default | Description |
  | :--- | :---: | :--- | :--- | :--- |
  | name | False | str |  | The name of your node pool. Must be 63 characters or less and must be empty or begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between. |
  | cluster | True | str |  | The name or ID of the Data Platform cluster. |
  | nodepool | True | str |  | The name or ID of the Data Platform nodepool. |
  | node_count | False | int |  | The number of nodes that make up the node pool. |
  | maintenance_window | False | dict |  | The maintenance window is used for updating the software on the nodepool's nodes and for upgrading the nodepool's version. If no value is given, one is chosen dynamically, so there is no fixed default. |
  | labels | False | dict |  | Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) |
  | annotations | False | dict |  | Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) |
  | do_not_replace | False | bool | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a differentvalue to an immutable property. An error will be thrown instead |
  | api_url | False | str |  | The Ionos API base URL. |
  | username | False | str |  | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password | False | str |  | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token | False | str |  | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait | False | bool | True | Wait for the resource to be created before returning. |
  | wait_timeout | False | int | 600 | How long before wait gives up, in seconds. |
  | state | False | str | present | Indicate desired state of the resource. |

&nbsp;

&nbsp;
