The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/07__introducing_the_application_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
datacenter_name: Ansible Tutorials - Introducing the ALB

ip_block:         { 'size': '2' }

lan:              { 'name': 'Internal LAN', 'address': '192.168.8.0/24',  'gw_ip': '192.168.8.1' }

nat_gateway:      { 'name': 'NAT GW', 'ip': '192.168.8.1' }

alb:              { 'name': 'ALB', 'ip': '192.168.8.248' }

server_config:    { 'jumpbox': { 'name': 'jumpbox',
                                 'cube_size': 'CUBES XS',
                                 'ip': '192.168.8.8' },
                    'app_server': [ { 'name': 'app-server-1',
                                      'ram': '1024',
                                      'cores': '1',
                                      'volume_size': '5',
                                      'user_data_file': 'cloud-init--app-servers.txt',
                                      'ip': '192.168.8.16' },
                                     { 'name': 'app-server-2',
                                       'ram': '1024',
                                       'cores': '1',
                                       'volume_size': '5',
                                       'user_data_file': 'cloud-init--app-servers.txt',
                                       'ip': '192.168.8.17' } ] 
                  }

vnf_wait_timeout: 1800

ENABLE_PROXY_PROTOCOL: false

```
{% endcode %}