The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/08__a_quick_introduction_to_managed_kubernetes` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
datacenter_name: Getting Started - Ansible - Introducing mk8s

lan:              { 'name': 'Internal LAN', 'address': '192.168.8.0/24' }

server_config:    { 'jumpbox': { 'name': 'jumpbox',
                                 'cube_size': 'CUBES XS',
                                 'ip': '192.168.8.8' } }

k8s_config:       { 'cluster_name': 'getting-started--ansible--cluster', 
                    'nodepool_config': { 'node_count': '2',
                                 'auto_scaling2': { 'min': '1', 'max': '3' },
                                 'node_spec': { 'ram': '2048',    # must be 2048 or greater
                                                'cores': '1',
                                                'volume_size': '10',
                                                'storage_type': 'HDD' } } }

# k8s_config.nodepool_config.node_spec.cores
```
{% endcode %}