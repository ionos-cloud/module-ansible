The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/06__introducing_the_nat_gateway_and_network_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```j2
Host nlb
User root
Hostname {{ ip_block_response.ipblock.properties.ips[1] }}
StrictHostKeyChecking no
UserKnownHostsFile /dev/null


Host *
User root
StrictHostKeyChecking accept-new
UserKnownHostsFile ssh_known_hosts_tmp
IdentityFile temporary_id_rsa

Host {{ server_config['jumpbox'].name }}
Hostname {{ create_cube_response['machines'][0]['entities']['nics']['items'][0]['properties']['ips'][0] }}

{% for server in server_config['app_server'] %}
Host {{ server.name }}
Hostname {{ server.ip }}
ProxyJump jumpbox

{% endfor %}
```
{% endcode %}