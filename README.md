# ProfitBricks Ansible Module

The path to the ProfitBricks Ansible module can be specified in several ways.

* `ANSIBLE_LIBRARY` environment variables:
`export ANSIBLE_LIBRARY=/path/to/profitbricks-ansible-module/lib`
* `ansible-playbook --module-path` command line parameter:
  `ansible-playbook --module-path /path/to/profitbricks-ansible-module/lib`
* `ansible.cfg` configuration file

Example `ansible.cfg`:

```
[default]
library = /path/to/profitbricks-ansible-module/lib
```

The Ansible configuration file is read in the following order:

* `ANSIBLE_CONFIG` environment variable path
* `ansible.cfg` from the current directory
* `.ansible.cfg` in the user home directory
* `/etc/ansible/ansible.cfg`

Ansible Playbook

The module supports the following environment variables.

* PROFITBRICKS_USERNAME
* PROFITBRICKS_PASSWORD

`export PROFITBRICKS_USERNAME=user@domain.com`
`export PROFITBRICKS_PASSWORD=password`
