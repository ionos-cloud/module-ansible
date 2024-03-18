The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/03__jumpbox_with_internal_server` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```bash
#!/bin/bash
dd if=/dev/zero of=/swapfile bs=1M count=512
chmod 0600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile    none    swap    sw    0    0' >> /etc/fstab

```
{% endcode %}