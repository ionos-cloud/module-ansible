The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```j2
Host *
User root
StrictHostKeyChecking accept-new
UserKnownHostsFile ssh_known_hosts_tmp

Host example-server
Hostname {{ create_server_response['machines'][0]['entities']['nics']['items'][0]['properties']['ips'][0] }}

```
{% endcode %}