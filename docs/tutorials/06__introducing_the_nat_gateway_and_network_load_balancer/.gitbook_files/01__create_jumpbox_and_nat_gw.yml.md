The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/06__introducing_the_nat_gateway_and_network_load_balancer` sub-directory.

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
    # Provision the jumpbox, heavily borrowed from 03__jumpbox_with_internal_server
    - name: Retrieve Cube templates
      ionoscloudsdk.ionoscloud.cube_template_info:
        filters: "{ 'properties.name': '{{ server_config['jumpbox'].cube_size }}' }"
      register: template_list


    - name: Provision a minimal Cube Jumpbox
      ionoscloudsdk.ionoscloud.cube_server:
        datacenter: "{{ datacenter_name }}"
        name: "{{ server_config['jumpbox'].name }}"
        template_uuid: "{{ template_list.cube_templates[0].id }}"
        disk_type: DAS
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"
        assign_public_ip: true

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
    # Reserve a block of two IP addresses (one for the NAT gateway, one for
    # the NLB). See https://docs.ionos.com/ansible/api/compute-engine/ipblock
    - name: Create an IP Block for our datacenter
      ionoscloudsdk.ionoscloud.ipblock:
        name: "IP Block for {{ datacenter_name }}"
        location: "{{ location }}"
        size: "{{ ip_block.size }}"
        state: present
      register: ip_block_response




    # =======================================================================
    # Create (and, where necessary, transfer) the required temporary files
    - name: Create a temporary ssh-key-pair so we can connect to the 'internal server' via the jumpbox
      ansible.builtin.shell:
        cmd: ssh-keygen -t rsa -b 4096 -f temporary_id_rsa -N "" || true


    - name: Create a local ssh_config file
      ansible.builtin.template:
        src: templates/ssh_config.j2
        dest: ssh_config


    - name: Create a local / 'nested' Ansible inventory.yml file
      ansible.builtin.template:
        src: templates/inventory.j2
        dest: inventory.yml


    - name: Delete any pre-existing ssh_known_hosts_tmp file
      ansible.builtin.shell: rm -f ssh_known_hosts_tmp


    - name: Copy temporary ssh private key to the jumpbox
      ansible.builtin.shell: scp -F ssh_config temporary_id_rsa jumpbox:/root/.ssh/id_rsa




    # =======================================================================
    # Create the NAT Gateway --- see https://docs.ionos.com/ansible/api/nat-gateway/nat_gateway
    - name: Create a NAT Gateway --- this can take a little while (typically between 3 and 8 minutes), so please don't interrupt this operation...
      ionoscloudsdk.ionoscloud.nat_gateway:
        datacenter: "{{ datacenter_name }}"    # can be either the name or the UUID of the datacenter
        name: "{{ nat_gateway.name }}"
        public_ips: 
          - "{{ ip_block_response.ipblock.properties.ips[0] }}"
        lans:
          - id: "{{ create_second_lan_response.lan.id }}"
            gateway_ips: "{{ nat_gateway.ip }}"

        wait: true
        wait_timeout: "{{ vnf_wait_timeout }}"
      register: nat_gateway_response


    # See https://docs.ionos.com/ansible/api/nat-gateway/nat_gateway_rule
    - name: Create an SNAT gateway rule
      ionoscloudsdk.ionoscloud.nat_gateway_rule:
        datacenter: "{{ datacenter_name }}"                         # can be either the name or the UUID of the datacenter
        nat_gateway: "{{ nat_gateway_response.nat_gateway.id }}"    # can be either the name or the UUID of the gateway
        name: "SNAT Default Rule"
        type: "SNAT"
        protocol: "ALL"
        source_subnet: "{{ lan.address }}"
        public_ip: "{{ ip_block_response.ipblock.properties.ips[0] }}"

        wait: true
        wait_timeout: "{{ vnf_wait_timeout }}"

```
{% endcode %}