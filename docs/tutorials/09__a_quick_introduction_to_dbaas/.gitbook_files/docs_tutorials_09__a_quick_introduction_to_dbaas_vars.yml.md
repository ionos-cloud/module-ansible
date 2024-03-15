The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/09__a_quick_introduction_to_dbaas` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS: false


datacenter_name: Getting Started - Ansible - Introducing DBaaS

ip_block:         { 'size': '1' }

lan:              { 'name': 'Internal LAN', 'address': '192.168.8.0/24',  'gw_ip': '192.168.8.1' }

nlb:              { 'name': 'NLB', 'ip': '192.168.8.248' }

server_config:    { 'jumpbox': { 'name': 'jumpbox',
                                 'cube_size': 'CUBES XS',
                                 'ip': '192.168.8.8' } }

dbaas_config:     { 'postgres_cluster': { 'ram': '2048',    # must be 2048 or greater
                                 'cores': '1',
                                 'volume_size': '10240',    # in MB, must be 2048 or greater
                                 'storage_type': 'HDD',
                                 'ip': '192.168.8.16' },
                    'mongodb_cluster':  { 'template': 'MongoDB Playground',
                                 'version': '6.0',
                                 'ip': '192.168.8.17' } }

```
{% endcode %}