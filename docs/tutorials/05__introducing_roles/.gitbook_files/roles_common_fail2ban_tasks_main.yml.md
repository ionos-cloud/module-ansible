The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# ==============================================================================
- name: About to execute tasks file for role 'fail2ban'
  ansible.builtin.meta: noop



- name: Install fail2ban
  ansible.builtin.package:
    name:
      - fail2ban
    state: present
```
{% endcode %}