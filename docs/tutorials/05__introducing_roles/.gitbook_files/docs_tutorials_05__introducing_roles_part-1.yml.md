The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
- hosts: localhost
  connection: local
  gather_facts: false

  vars_files:
    - ../vars.yml
    - vars.yml




  tasks:
    # =======================================================================
    - name: Display EULA
      ansible.builtin.pause:
        prompt: "{{ IONOS_UNSUPPORTED_EULA }}"
      register: INTERACTIVE_EULA_ACCEPTED
      when: IONOS_UNSUPPORTED_EULA_ACCEPTED != "yes"


    - name: Confirm acceptance of EULA
      ansible.builtin.assert:
        that:
          - IONOS_UNSUPPORTED_EULA_ACCEPTED == "yes" or INTERACTIVE_EULA_ACCEPTED.user_input == "yes"  




    # =======================================================================
    - name: Create the datacenter '{{ datacenter_name }}' in {{ location }}
      ionoscloudsdk.ionoscloud.datacenter:
        name: "{{ datacenter_name }}"
        location: "{{ location }}"
        state: present
      register: datacenter_response


    - name: Create the server '{{ server_name }}'
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "{{ server_name }}"
        cores: "1"
        ram: "1024"
        cpu_family: "{{ cpu_family }}"
        assign_public_ip: true
        disk_type: HDD
        volume_size: "10"
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"    
      register: create_server_response


    # Borrowed from 3__jumpbox_with_internal_server
    - name: Create a local ssh_config file
      ansible.builtin.template:
        src: templates/ssh_config.j2
        dest: ssh_config


    - name: Create a local / 'nested' Ansible inventory.yml file
      ansible.builtin.shell:
        cmd: |
          (cat <<EOF
          ---
          servers:
            hosts:
              example-server:


          all:
            vars:
              ansible_ssh_common_args: "-F ssh_config"
          EOF
          ) > inventory.yml


    - name: Delete any pre-existing ssh_known_hosts_tmp file
      ansible.builtin.shell: rm -f ssh_known_hosts_tmp

```
{% endcode %}