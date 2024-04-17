The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/01__minimal_example` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# The following host and connection specs are mandatory as the IONOS Cloud
# Ansible module is 'proxied' via localhost
- hosts: localhost
  connection: local
  gather_facts: false

  vars_files:
    - ../vars.yml

  vars:
    - datacenter_name: Ansible Tutorials - Minimal Functional Test
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
    # See https://docs.ionos.com/ansible/api/compute-engine/datacenter for
    # more information
    - name: Create the datacenter '{{ datacenter_name }}' in {{ location }}
      ionoscloudsdk.ionoscloud.datacenter:
        name: "{{ datacenter_name }}"
        location: "{{ location }}"
        state: present
      register: datacenter_response

    

    # See https://docs.ionos.com/ansible/api/compute-engine/server for more
    # information
    - name: Create the server '{{ server_name }}' --- this may take a while, please don't interrupt this operation...)
      ionoscloudsdk.ionoscloud.server:
        # quite a bit longer than just 'datacenter_name', to be sure, but it shows
        # you how you can get the name from the register variable returned above
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "{{ server_name }}"
        cores: "1"
        ram: "1024"
        cpu_family: "{{ datacenter_response.datacenter.properties.cpu_architecture[0].cpu_family }}"
        assign_public_ip: true
        disk_type: HDD
        volume_size: "5"
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"
        # if you don't want to perform any first-boot tasks using cloud-init,
        # simply remove the following line
        user_data: "{{ lookup('file', 'cloud-init.txt') | string | b64encode }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_server_response


    - name: Print the newly-provisioned server's public IP address
      ansible.builtin.debug:
        msg:
          - "The server's IP address is {{ create_server_response.machines[0].entities.nics['items'][0].properties.ips[0] }}"
          - "(Please note this _will_ change across VM _power-cycles / hard-resets_)"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "The server is now created, and may be inspected. Press <Enter> when you are ready for it to be (forcibly) shutdown. (This may take a while...)"
      when: pause_between_operations


    - name: Stop '{{ server_name }}'
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_name }}"
        instance_ids:
          - "{{ server_name }}"

        state: stopped
        wait_timeout: "{{ wait_timeout }}"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "The server is now stopped. Press <Enter> when you are ready for it to be powered back on. (This may take a while...)"
      when: pause_between_operations
        
        
    - name: Start '{{ server_name }}'
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_name }}"
        instance_ids:
          - "{{ server_name }}"

        state: running
        wait_timeout: "{{ wait_timeout }}"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "End of example. Press <Enter> when you are ready for the contents of '{{ datacenter_name }}' to be deleted..."
      when: pause_between_operations


    - name: Remove the server
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_name }}"
        instance_ids:
          - "{{ server_name }}"

        state: absent
        wait_timeout: "{{ wait_timeout }}"


    # This will remove all servers, volumes, and other objects contained therein
    - name: Delete the datacenter '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.datacenter:
        datacenter: "{{ datacenter_response.datacenter.id }}"    # can delete by name or id
        state: absent

```
{% endcode %}