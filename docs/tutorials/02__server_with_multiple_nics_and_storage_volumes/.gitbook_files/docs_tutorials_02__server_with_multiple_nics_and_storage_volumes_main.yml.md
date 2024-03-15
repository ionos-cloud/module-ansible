The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/02__server_with_multiple_nics_and_storage_volumes` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
- hosts: localhost
  connection: local
  gather_facts: false

  vars_files:
    - ../vars.yml

  vars:
    - datacenter_name: Getting Started - Ansible - Server with multiple NICs and Storage Volumes
    - server_name:     Example server


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


    - name: Create the server '{{ server_name }}' --- this may take a while, please don't interrupt this operation...
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
      register: create_server_response


    - name: Print contents of 'create_server_response'
      ansible.builtin.debug:
        var: create_server_response
      when: verbose_debugging




    # =======================================================================
    # See https://docs.ionos.com/ansible/api/compute-engine/lan for more
    # information
    - name: Create a second LAN within '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.lan:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "internal"
        public: false
      register: create_second_lan_response


    - name: Print contents of 'create_second_lan_response'
      ansible.builtin.debug:
        var: create_second_lan_response
      when: verbose_debugging


    # See https://docs.ionos.com/ansible/api/compute-engine/nic for more
    # information
    - name: Create a second NIC for '{{ server_name }}' (this time with a 'static' IP address)
      ionoscloudsdk.ionoscloud.nic:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "{{ server_name }}.eth1"
        server: "{{ server_name }}"
        lan: "{{ create_second_lan_response.lan.id }}"
        ips:
          - 192.168.16.16
        dhcp: true

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_second_nic_response


    - name: Print contents of 'create_second_nic_response'
      ansible.builtin.debug:
        var: create_second_nic_response
      when: verbose_debugging




    # =======================================================================
    # See https://docs.ionos.com/ansible/api/compute-engine/volume for more
    # information
    - name: Create a second volume for '{{ server_name }}'
      ionoscloudsdk.ionoscloud.volume:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "{{ server_name }}.hdd1"
        server: "{{ server_name }}"
        size: 10
        disk_type: "HDD"
        licence_type: "OTHER"
      register: create_second_volume_response


    - name: Print contents of 'create_second_volume_response'
      ansible.builtin.debug:
        var: create_second_volume_response
      when: verbose_debugging




    # =======================================================================
    - name: Print some information about the created resources
      ansible.builtin.debug:
        msg:
          - "Server: [ {{ create_server_response.machines[0].id }} ]"
          # Unfortunately, due to how object-attributes are handled / expanded
          # within Jinja templates, we can't just write, e.g.,
          # {{ create_server_response.machines[0].entities.nics.items[0].properties.lan }}
          # or {{ create_server_response.machines[0].entities.volumes.id }}
          - "NIC_0:  [ {{ create_server_response['machines'][0]['entities']['nics']['items'][0]['properties']['lan'] }}, {{ create_server_response['machines'][0]['entities']['nics']['items'][0]['properties']['ips'][0] }} ]"
          - "NIC_1:  [ {{ create_second_nic_response.nic.properties.lan }}, {{ create_second_nic_response.nic.properties.ips[0] }} ]"
          - "Vol_0:  [ {{ create_server_response['machines'][0]['entities']['volumes']['items'][0]['id'] }} ]"
          - "Vol_1:  [ {{ create_second_volume_response.volumes[0].id }} ]"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "End of example. Press <Enter> when you are ready for the contents of '{{ datacenter_name }}'' to be deleted..."
      when: pause_between_operations


    # This will remove all servers, volumes, and other objects contained therein
    - name: Delete the datacenter '{{ datacenter_name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        datacenter: "{{ datacenter_name }}"
        state: absent

```
{% endcode %}