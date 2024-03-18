The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/09__a_quick_introduction_to_dbaas` sub-directory.

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




    # =======================================================================
    # Provision the jumpbox, heavily borrowed from 3__jumpbox_with_internal_server
    - name: Retrieve Cube templates
      ionoscloudsdk.ionoscloud.cube_template:
        state: present
      register: template_list


    - name: Retrieve Template ID for '{{ server_config['jumpbox'].cube_size }}'
      set_fact:
        desired_template_uuid: "{{ item.id }}"
      when: item.properties.name == server_config['jumpbox'].cube_size
      with_items:
        - "{{ template_list.template['items'] }}"


    - name: Provision a minimal Cube Jumpbox
      ionoscloudsdk.ionoscloud.cube_server:
        datacenter: "{{ datacenter_name }}"
        name: "{{ server_config['jumpbox'].name }}"
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
        datacenter: "{{ datacenter_name }}"
        name: "{{ lan.name }}"
        public: false
      register: create_second_lan_response


    - name: Create a second NIC for the Jumpbox
      ionoscloudsdk.ionoscloud.nic:
        datacenter: "{{ datacenter_name }}"
        name: "{{ server_config['jumpbox'].name }}.eth1"
        server: "{{ server_config['jumpbox'].name }}"
        lan: "{{ create_second_lan_response.lan.id }}"
        ips:
          - "{{ server_config['jumpbox'].ip }}"
        dhcp: true

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"




    # =======================================================================
    # Create (and, where necessary, transfer) the required temporary files
    - name: Create a temporary ssh-key-pair so we can connect to the 'internal server' via the jumpbox
      ansible.builtin.shell:
        cmd: ssh-keygen -t rsa -b 4096 -f temporary_id_rsa -N "" || true


    - name: Create a local ssh_config file
      ansible.builtin.template:
        src: templates/ssh_config.j2
        dest: ssh_config


    - name: Delete any pre-existing ssh_known_hosts_tmp file
      ansible.builtin.shell: rm -f ssh_known_hosts_tmp


    - name: Copy temporary ssh private key to the jumpbox
      ansible.builtin.shell: scp -F ssh_config temporary_id_rsa jumpbox:/root/.ssh/id_rsa
      when: false


    - name: Add an Ansible host entry for the jumpbox
      ansible.builtin.add_host:
        hostname: "jumpbox"
        ansible_host: "{{ create_cube_response['machines'][0]['entities']['nics']['items'][0]['properties']['ips'][0] }}"
        remote_user: root
        group: vms-to-be-configured




    # =======================================================================
    # Reserve a one IP address block for the NLB
    - name: Create an IP Block for our datacenter
      ionoscloudsdk.ionoscloud.ipblock:
        name: "IP Block for {{ datacenter_name }}"
        location: "{{ location }}"
        size: "{{ ip_block.size }}"
        state: present
      register: ip_block_response
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS




    # =======================================================================
    # see https://docs.ionos.com/ansible/api/network-load-balancer/network_load_balancer
    - name: Create Network Load Balancer --- this can take quite a while (typically between 3 and 6 minutes), so please don't interrupt this operation...
      ionoscloudsdk.ionoscloud.network_load_balancer:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ nlb.name }}"
        listener_lan: "{{ create_cube_response.machines[0]['entities']['nics']['items'][0]['properties']['lan'] }}"
        ips:
          - "{{ ip_block_response.ipblock.properties.ips[0] }}"
        target_lan: "{{ create_second_lan_response.lan.id }}"
        lb_private_ips:
          - "{{ nlb.ip }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_nlb_response
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS




    # see https://docs.ionos.com/ansible/api/network-load-balancer/network_load_balancer_rule
    - name: Create Network Load Balancer Forwarding Rule for psql
      ionoscloudsdk.ionoscloud.network_load_balancer_rule:
        name: "NLB PSQL connections"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        listener_ip: "{{ ip_block_response.ipblock.properties.ips[0] }}"
        listener_port: "5432"
        targets:
          - ip: "{{ dbaas_config.postgres_cluster.ip }}"
            port: "5432"
            weight: "100"
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ create_nlb_response.network_load_balancer.id }}"
        wait: true
      register: nlb_forwarding_rule_response_psql
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS


    - name: Create Network Load Balancer Forwarding Rule for mongo
      ionoscloudsdk.ionoscloud.network_load_balancer_rule:
        name: "NLB MONGO connections"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        listener_ip: "{{ ip_block_response.ipblock.properties.ips[0] }}"
        listener_port: "27017"
        targets:
          - ip: "{{ dbaas_config.mongodb_cluster.ip }}"
            port: "27017"
            weight: "100"
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ create_nlb_response.network_load_balancer.id }}"
        wait: true
      register: nlb_forwarding_rule_response_mongo
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS






# =======================================================================
# And in our second play, go ahead and configure the jumpbox (which was
# added, dynamically, to our inventory above using the add_host module)
- hosts: vms-to-be-configured
  gather_facts: false


  tasks:
    - name: Set ansible_ssh_common_args
      set_fact:
        ansible_ssh_common_args: "-F ssh_config"


    - name: Update repositories cache and upgrade the system
      ansible.builtin.apt:
        upgrade: dist
        update_cache: yes
        cache_valid_time: 3600


    - name: Install required packages
      ansible.builtin.package:
        name:
          - gnupg
          - postgresql-client-common
          - postgresql-client
        state: present


    - name: Add the MongoDB 6.0 signing key
      ansible.builtin.apt_key:
        url: https://www.mongodb.org/static/pgp/server-6.0.asc
        state: present


    - name: Add the MongoDB 6.0 Linux repository
      ansible.builtin.apt_repository:
        repo: deb [arch=amd64] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse
        filename: mongodb-org-6.0
        state: present


    - name: Install MongoSH
      ansible.builtin.apt:
        name:
          - mongodb-mongosh
        update_cache: yes
        state: present

```
{% endcode %}