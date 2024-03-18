The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# ==============================================================================
- name: About to execute tasks file for 'common/base server' role
  ansible.builtin.meta: noop




- name: Update repositories cache and upgrade the system
  ansible.builtin.apt:
    upgrade: dist
    update_cache: yes
    cache_valid_time: 3600




- name: Install some more-or-less essential packages
  ansible.builtin.package:
    name:
      - sudo
      - curl
      - wget
      - git
      - screen
      - nmap
      - traceroute
    state: present
```
{% endcode %}