The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# Unlike main.yml (which communicates with the IONOS Cloud Ansible module via
# localhost), _this_ playbook is run on / within the VM
- hosts: example-server


  vars:
    # roles that will be applied iterately at the _end_ of this play --- note
    # that 'common/base-server' is explicitly applied below (e.g. to update
    # the system's packages), while the nfs-server and -client roles are also
    # applied explicitly due to their role-specific parameters
    roles_to_apply:
      - common/fail2ban
      - docker-server




  tasks:
    # Perform some basic / preparatory tasks
    - name: Update repositories cache and upgrade the system
      ansible.builtin.apt:
        upgrade: dist
        update_cache: yes
        cache_valid_time: 3600


    - name: Gather the package facts
      ansible.builtin.package_facts:
        manager: auto




    # An example of the simplest way to include a role
    - name: Apply the common 'base-server' role
      include_role:
        name: common/base-server




    # Examples of how variables can be passed to included roles
    - name: Apply the 'nfs-server' role
      include_role:
        name: nfs-server
      vars:
        - export_root: /export
        - export_specifier: "127.0.0.1(ro,sync,no_subtree_check,no_root_squash)"


    - name: Apply the 'nfs-client' role
      include_role:
        name: nfs-client
      vars:
        nfs_mount_point: /mnt
        nfs_server_path: "127.0.0.1:/export"




    # And finally, an example of how one might apply a list of roles
    - name: And apply the remaining roles to target system
      include_role:
        name: "{{ role }}"
      with_items: "{{ roles_to_apply }}"
      loop_control:
        loop_var: role

```
{% endcode %}