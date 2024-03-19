The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/09__a_quick_introduction_to_dbaas` sub-directory.

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
    - name: Get information about the existing data centers
      ansible.builtin.uri:
        url: "https://api.ionos.com/cloudapi/v6/datacenters?pretty=true&depth=1&offset=0&limit=1000"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_datacenters_response


    - name: Extract the relevant entry from 'api__get_datacenters_response'
      ansible.builtin.set_fact:
        datacenter: "{{ (api__get_datacenters_response.content | from_json | json_query(query))[0] }}"
      vars:
        query: "items[?properties.name=='{{ datacenter_name }}'].{id: id, name: properties.name}"


    - name: Get information about the LANs in '{{ datacenter_name }}'
      ansible.builtin.uri:
        url: "https://api.ionos.com/cloudapi/v6/datacenters/{{ datacenter.id }}/lans?pretty=true&depth=2&offset=0&limit=1000"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      register: api__get_lans_response


    - name: Set the fact 'internal_lan' based on the above
      ansible.builtin.set_fact:
        internal_lan: "{{ (api__get_lans_response.content | from_json | json_query(query))[0] }}"
      vars:
        query: "items[?properties.name=='{{ lan.name }}'].{id: id, properties: properties}"


    - name: Get information about our reserved IP Blocks
      ansible.builtin.uri:
        url: "https://api.ionos.com/cloudapi/v6/ipblocks?pretty=true&depth=1&offset=0&limit=100"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      register: api__get_ip_blocks_response
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS


    - name: Set the fact 'ip_block' based on the above
      ansible.builtin.set_fact:
        ip_block: "{{ (api__get_ip_blocks_response.content | from_json | json_query(query))[0] }}"
      vars:
        query: "items[?properties.name=='IP Block for {{ datacenter_name }}'].properties.ips"
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS


    - name: Get information about the servers in our data center
      ionoscloudsdk.ionoscloud.server_info:
        datacenter: "{{ datacenter_name }}"
        depth: 5
      register: get_server_response


    - name: Retrieve the object describing the jumpbox
      ansible.builtin.set_fact:
        desired_server_info__query: "{{ get_server_response | json_query(query) }}"
      vars:
        query: "servers[?properties.name=='{{ server_config['jumpbox'].name }}']"


    - name: Retrieve the jumpbox's public IP
      ansible.builtin.set_fact:
        jumpbox_ip: "{{ (desired_server_info__query[0] | json_query(query))[0] }}"
      vars:
        query: "entities.nics.items[?properties.name!='{{ server_config['jumpbox'].name }}.eth1'].properties.ips[]"




    # =======================================================================
    # See https://docs.ionos.com/ansible/api/dbaas-postgres/postgres_cluster
    - name: Create Postgres Cluster
      ionoscloudsdk.ionoscloud.postgres_cluster:
        postgres_version: 12
        instances: 1
        cores: "{{ dbaas_config.postgres_cluster.cores }}"
        ram: "{{ dbaas_config.postgres_cluster.ram }}"
        storage_size: "{{ dbaas_config.postgres_cluster.volume_size }}"
        storage_type: "{{ dbaas_config.postgres_cluster.storage_type }}"
        location: "{{ location }}"
        connections:
          - cidr: "{{ dbaas_config.postgres_cluster.ip }}/24"
            datacenter: "{{ datacenter.id }}"
            lan: "{{ internal_lan.id }}"
        display_name: "Postgres Cluster for {{ datacenter_name }}"
        synchronization_mode: ASYNCHRONOUS
        db_username: dbadmin
        db_password: "{{ default_password }}"
        wait: true
      register: postgres_cluster_response    




    # =======================================================================
    - name: Print usage information
      ansible.builtin.debug:
        msg:
          - "To access your Postgres Cluster via, e.g., psql, use one of the following commands:"
          - "    From the jumpbox:"
          - "        psql -h {{ dbaas_config.postgres_cluster.ip }} -U dbadmin postgres"
          - "    Externally via the jumpbox:"
          - "        In one shell:     ssh -L 5432:{{ postgres_cluster_response.postgres_cluster.properties.dns_name }}:5432 root@{{ jumpbox_ip }}"
          - "        In another shell: psql -h localhost -U dbadmin postgres"
          - "{% if ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS %}    Externally via the NLB:{% endif %}"
          - "{% if ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS %}        psql -h {{ ip_block[0] }} -U dbadmin postgres{% endif %}"

```
{% endcode %}