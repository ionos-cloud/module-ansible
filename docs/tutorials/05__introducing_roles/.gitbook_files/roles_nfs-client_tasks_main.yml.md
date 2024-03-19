The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# ==============================================================================
- name: About to execute tasks file for role 'nfs-client'
  ansible.builtin.meta: noop




- name: Install the NFS client
  ansible.builtin.package:
    name:
      - nfs-common
    state: present


- name: Install autofs
  ansible.builtin.package:
    name:
      - autofs
    state: present


- name: Add an entry to /etc/auto.master
  ansible.builtin.lineinfile:
    path: /etc/auto.master
    line: '/-   /etc/auto.nfs'


- name: Create / add an entry to /etc/auto.nfs
  ansible.builtin.lineinfile:
    path: /etc/auto.nfs
    line: "{{ nfs_mount_point }}    {{ nfs_server_path }}"
    create: yes
  when: nfs_server_path | length > 0


- name: Restart the automounter service so these changes can take effect
  ansible.builtin.service:
    name: autofs
    state: restarted
```
{% endcode %}