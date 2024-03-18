The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/06__introducing_the_nat_gateway_and_network_load_balancer` sub-directory.

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
    - name: Get information about the LANs in '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.lan_info:
        datacenter: "{{ datacenter_name }}"
      register: lan_info_response


    - name: Set the fact 'public_lan' based on the above
      ansible.builtin.set_fact:
        public_lan: "{{ (lan_info_response | json_query(query))[0] }}"
      vars:
        query: "lans[?properties.name=='public']"


    - name: Set the fact 'secondary_lan' based on the above
      ansible.builtin.set_fact:
        secondary_lan: "{{ (lan_info_response | json_query(query))[0] }}"
      vars:
        query: "lans[?properties.name=='{{ lan.name }}']"




    # =======================================================================
    # Create the 'app servers' defined in 'server_config.app_server'
    - name: Create the cloud-init file for our app servers
      ansible.builtin.template:
        src: templates/cloud-init--app-servers.j2
        dest: cloud-init--app-servers.txt


    - name: Create the app servers specified in server_config.app_server
      ionoscloudsdk.ionoscloud.server:
        datacenter: "{{ datacenter_name }}"
        name: "{{ item.name }}"
        cores: "{{ item.cores }}"
        ram: "{{ item.ram }}"
        cpu_family: "{{ cpu_family }}"
        disk_type: HDD
        volume_size: "5"
        image: "{{ image_alias }}"
        image_password: "{{ default_password }}"
        ssh_keys:
          - "{{ ssh_public_key }}"
          - "{{ lookup('file', 'temporary_id_rsa.pub') }}"
        lan: "{{ secondary_lan.id }}"
        nic_ips:
          - "{{ item.ip }}"
        user_data: "{{ lookup('file', item.user_data_file) | string | b64encode }}"

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      with_items: "{{ server_config.app_server }}"
      register: create_app_server_response




    # =======================================================================
    # And finally create and minmally-configure a Network Load Balancer
    - name: Get information about our reserved IP Blocks
      ionoscloudsdk.ionoscloud.ipblock_info:
        filters: "{ 'properties.name': 'IP Block for {{ datacenter_name }}' }"
      register: ipblock_info_response


    - name: Set 'ip_block' based on the above
      ansible.builtin.set_fact:
        ip_block: "{{ ipblock_info_response.ipblocks[0].properties.ips }}"




    # see https://docs.ionos.com/ansible/api/network-load-balancer/network_load_balancer
    #   --> the example really needs the lb_private_ips, too
    - name: Create Network Load Balancer --- this can take quite a while (typically between 3 and 6 minutes), so please don't interrupt this operation...
      ionoscloudsdk.ionoscloud.network_load_balancer:
        datacenter: "{{ datacenter_name }}"
        name: "{{ nlb.name }}"
        listener_lan: "{{ public_lan.id }}"
        ips:
          - "{{ ip_block[1] }}"
        target_lan: "{{ secondary_lan.id }}"
        lb_private_ips:
          - "{{ nlb.ip }}"

        # state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"
      register: create_nlb_response


    # Before we can create a forwarding rule, we need the list of destination IPs
    # PRM: not quite sure why "{{ (create_app_server_response | json_query(query))[] }}"
    # won't work (when it does, e.g., on https://mixedanalytics.com/tools/jmespath-expression-tester/),
    - name: Set 'target_ips' based on 'create_app_server_response'
      ansible.builtin.set_fact:
        target_ips: "{{ create_app_server_response | json_query(query) }}"
      vars:
        query: "results[].machines[].entities.nics.items[].properties.ips"


    # we need two separate set_fact calls to guarantee the targets are initialised
    # as an empty list before they are used in the second call...
    - name: Create targets list
      ansible.builtin.set_fact:
        targets_ssh: []
        targets_http: []

    - name: Add new JSON Objects to 'targets'
      ansible.builtin.set_fact:
        targets_ssh: "{{ targets_ssh + 
                      [{ 'ip': item[0],
                          'port': '22',
                          'weight': '100' }] }}"
        targets_http: "{{ targets_http + 
                       [{ 'ip': item[0],
                          'port': '80',
                          'weight': '100' }] }}"
      loop: "{{ target_ips }}"


    - name: Print target objects
      ansible.builtin.debug:
        msg:
          - "targets_ssh: {{ targets_ssh }}"
          - "targets_http: {{ targets_http }}"
      when: verbose_debugging


    # see https://docs.ionos.com/ansible/api/network-load-balancer/network_load_balancer_rule
    - name: Create Network Load Balancer Forwarding Rule for tcp/ssh
      ionoscloudsdk.ionoscloud.network_load_balancer_rule:
        name: "NLB SSH connections"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        listener_ip: "{{ ip_block[1] }}"
        listener_port: "22"
        targets: "{{ targets_ssh }}"
        datacenter: "{{ datacenter_name }}"
        network_load_balancer: "{{ create_nlb_response.network_load_balancer.id }}"
        wait: true
      register: nlb_forwarding_rule_response_ssh


    - name: Create Network Load Balancer Forwarding Rule for tcp/http
      ionoscloudsdk.ionoscloud.network_load_balancer_rule:
        name: "NLB HTTP connections"
        algorithm: "ROUND_ROBIN"
        protocol: "TCP"
        listener_ip: "{{ ip_block[1] }}"
        listener_port: "80"
        targets: "{{ targets_http }}"
        datacenter: "{{ datacenter_name }}"
        network_load_balancer: "{{ create_nlb_response.network_load_balancer.id }}"
        wait: true
      register: nlb_forwarding_rule_response_http

```
{% endcode %}