The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# ==============================================================================
- name: About to execute tasks file for role 'nfs-server'
  ansible.builtin.meta: noop




- name: Install and setup an NFS server
  ansible.builtin.package:
    name:
      - nfs-kernel-server
    state: present


- name: Create the host-share directory
  ansible.builtin.file:
    path: "{{ export_root }}"
    state: directory
    mode: '1777'


- name: Create entry in /etc/exports
  ansible.builtin.lineinfile:
    path: /etc/exports
    line: "{{ export_root }}    {{ export_specifier }}"


- name: Copying the contents of {{ export_preload_path }} to nfs_server:/{{ export_root }}
  ansible.builtin.copy:
    src: "{{ export_preload_path }}"
    dest: "{{ export_root }}"
  when: export_preload_path | length > 0


- name: Tell nfs-server to reload its config
  ansible.builtin.service:
    name: nfs-server
    state: reloaded
```
{% endcode %}