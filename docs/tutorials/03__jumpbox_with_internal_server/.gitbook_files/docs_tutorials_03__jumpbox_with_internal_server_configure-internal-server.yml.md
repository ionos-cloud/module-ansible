The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/03__jumpbox_with_internal_server` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# Unlike main.yml (which communicates with the IONOS Cloud Ansible module via
# localhost), _this_ playbook is run on the internal server (i.e. the VM that
# has _no_ connection to the Internet) via the jumpbox). Given said lack of
# Internet access, we're not able to, e.g., install or update any software, so
# instead, we will just dump some host information to a file on the internal
# server, and copy it back to our 'local' computer
- hosts: internal

  tasks:
    - name: Log information of interest
      ansible.builtin.blockinfile:
        path: "/tmp/internal-server-hostinfo"
        create: yes
        marker: ""
        block: |
          fqdn: {{ ansible_facts.fqdn }}
          distribution: {{ ansible_distribution_file_variety }} {{ ansible_distribution }} {{ ansible_distribution_version }} {{ ansible_distribution_release }}
          kernel_version: {{ ansible_kernel }} {{ ansible_kernel_version }}
          interfaces: {{ ansible_interfaces }}


    - name: And copy them back to our localhost
      ansible.builtin.fetch:
        src: /tmp/internal-server-hostinfo
        dest: "internal-server-hostinfo.txt"
        flat: yes


```
{% endcode %}