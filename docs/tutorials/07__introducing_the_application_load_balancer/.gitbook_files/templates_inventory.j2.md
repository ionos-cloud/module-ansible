The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/07__introducing_the_application_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```j2
---
gateways:
  hosts:
    {{ server_config['jumpbox'].name }}:


app-servers:
  hosts:
{% for server in server_config['app_server'] %}
    {{ server.name }}:
{% endfor %}

all:
  vars:
    ansible_ssh_common_args: "-F ssh_config"

```
{% endcode %}