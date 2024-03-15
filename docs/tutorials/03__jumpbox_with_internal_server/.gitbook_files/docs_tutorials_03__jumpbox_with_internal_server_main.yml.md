The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/03__jumpbox_with_internal_server` sub-directory.

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
    - datacenter_name: Getting Started - Ansible - Jumpbox with Internal Server
    - jumpbox_name:    Jumpbox
    - cube_size:       CUBES XS
    - int_server_name: Example internal server




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




    - name: Create a temporary ssh-key-pair so we can connect to the 'internal server' via the jumpbox
      ansible.builtin.shell:
        cmd: ssh-keygen -t rsa -b 4096 -f temporary_id_rsa -N "" || true




    # =======================================================================
    # See https://docs.ionos.com/ansible/api/compute-engine/cube_template
    - name: Retrieve Cube templates
      ionoscloudsdk.ionoscloud.cube_template:
        state: present
      register: template_list


    # Iterate over the list of templates returned above and set the 'desired_
    # template_uuid' fact based upon the specified 'search criterium'
    - name: Retrieve Template ID for '{{ cube_size }}'
      set_fact:
        desired_template_uuid: "{{ item.id }}"
      when: item.properties.name == cube_size
      with_items:
        - "{{ template_list.template['items'] }}"




    # See https://docs.ionos.com/ansible/api/compute-engine/cube_server
    - name: Provision a minimal Cube Jumpbox
      ionoscloudsdk.ionoscloud.cube_server:
        datacenter: "{{ datacenter_name }}"
        name: "{{ jumpbox_name }}"
        template_uuid: "{{ desired_template_uuid }}"
        disk_type: DAS
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"
        assign_public_ip: true
        remove_boot_volume: true

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_cube_response


    - name: Create a second, internal LAN within '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.lan:
        datacenter: "{{ datacenter_response.datacenter.properties.name }}"
        name: "internal"
        public: false
      register: create_second_lan_response


    - name: Create a second NIC for the Jumpbox
      ionoscloudsdk.ionoscloud.nic:
        datacenter: "{{ datacenter_name }}"
        name: "{{ jumpbox_name }}.eth1"
        server: "{{ jumpbox_name }}"
        lan: "{{ create_second_lan_response.lan.id }}"
        ips:
          - 192.168.16.16
        dhcp: true

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"




    - name: Create the server '{{ int_server_name }}'
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_name }}"
        name: "{{ int_server_name }}"
        cores: "1"
        ram: "1024"
        cpu_family: "{{ cpu_family }}"
        disk_type: HDD
        volume_size: "5"
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"
          - "{{ lookup('file', 'temporary_id_rsa.pub') }}"
        lan: "{{ create_second_lan_response.lan.id }}"
        nic_ips:
          - 192.168.16.17
        user_data: "{{ lookup('file', 'cloud-init.txt') | string | b64encode }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_server_response




    # Create a 'local' ssh_config' file for the hosts in this example using the
    # ansible.builtin.template module and a very simple Jinja template file
    - name: Create a local ssh_config file
      ansible.builtin.template:
        src: templates/ssh_config.j2
        dest: ssh_config


    # There are several ways we could 'create' this file (including by using
    # the ansible.builtin.blockinfile or .copy modules, or just by creating a
    # simple, static .yml file), but we've opted for the following to show
    # how one can use HEREDOCs with the ansible.builtin.shell module
    - name: Create a local / 'nested' Ansible inventory.yml file
      ansible.builtin.shell:
        cmd: |
          (cat <<EOF
          ---
          gateways:
            hosts:
              jumpbox:


          internal_hosts:
            hosts:
              internal:


          all:
            vars:
              ansible_ssh_common_args: "-F ssh_config"
          EOF
          ) > inventory.yml


    - name: Delete any pre-existing ssh_known_hosts_tmp file
      ansible.builtin.shell: rm -f ssh_known_hosts_tmp


    # While one would, ordinarily, use, e.g., ansible.builtin.copy, in _this_ case
    # --- i.e. because we're using 'hosts: localhost, connection: local' rather
    # than connecting to the remote hosts --- it's arguably simpler to just scp
    # the file in question over to the jumpbox
    - name: Copy temporary ssh private key to the jumpbox
      ansible.builtin.shell: scp -F ssh_config temporary_id_rsa jumpbox:/root/.ssh/id_rsa




    # =======================================================================
    - name: Provisioning done, print next steps
      ansible.builtin.debug:
        msg:
          - "Both servers successfully provisioned. To connect to the jumpbox, run:"
          - "    ssh -F ssh_config jumpbox"
          - "To connect to the internal server _via_ the jumpbox, use the command:"
          - "    ssh -F ssh_config internal"
          - "And to run the configure-internal-server.yml on the _internal_ server, run:"
          - "    ansible-playbook -i inventory.yml configure-internal-server.yml"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "End of example. Press <Enter> when you are ready for the contents of {{ datacenter_name }} to be deleted..."


    - name: Delete the datacenter '{{ datacenter_name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        id: "{{ datacenter_response.datacenter.id }}"
        state: absent


    - name: And delete any 'temporary' or run-time files that might cause problems between iterations
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      with_items:
        - ssh_known_hosts_tmp

```
{% endcode %}