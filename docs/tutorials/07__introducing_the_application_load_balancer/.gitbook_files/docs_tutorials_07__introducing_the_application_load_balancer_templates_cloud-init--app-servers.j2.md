The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/07__introducing_the_application_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```j2
#!/bin/bash
dd if=/dev/zero of=/swapfile bs=1M count=2048
chmod 0600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile    none    swap    sw    0    0' >> /etc/fstab


ip route add default via {{ nat_gateway.ip }}

```
{% endcode %}