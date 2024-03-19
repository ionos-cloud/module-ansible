The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/04__working_with_existing_resources` sub-directory.

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


    - name: Create a second LAN within '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.lan:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "internal"
        public: false


    - name: Create the server '{{ server_name }}' --- this may take a while, please don't interrupt this operation...)
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "{{ server_name }}"
        cores: "1"
        ram: "1024"
        cpu_family: "{{ cpu_family }}"
        assign_public_ip: true
        disk_type: HDD
        volume_size: "5"
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      # previously we have saved the output of this task in the following 
      # register variable, but since _this_ installment is all about using
      # pre-existing resources, we'll skip this step, and show how one can
      # use an `_info` module in part-2.yml
      ##register: create_server_response
    

```
{% endcode %}