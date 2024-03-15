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
    # See https://docs.ionos.com/ansible/api/compute-engine/cube_template
    - name: Retrieve cluster templates
      ionoscloudsdk.ionoscloud.mongo_cluster_template_info:
      register: template_list


    # Iterate over the list of templates returned above and set the 'desired_
    # template_uuid' fact based upon the specified 'search criterium'
    # 'mongodb_cluster':  { 'cluster_template': 'MongoDB Playground',
    - name: Retrieve Template ID for '{{ dbaas_config.mongodb_cluster.template }}'
      set_fact:
        desired_template_uuid: "{{ item.id }}"
      when: item.properties.name == dbaas_config.mongodb_cluster.template
      with_items:
        - "{{ template_list['result'] }}"




    # =======================================================================
    # See https://docs.ionos.com/ansible/api/dbaas-mongo/mongo_cluster_template_info
    - name: Create MongoDB Cluster
      ionoscloudsdk.ionoscloud.mongo_cluster:
        mongo_db_version: "{{ dbaas_config.mongodb_cluster.version }}"
        instances: 1
        template_id: "{{ desired_template_uuid }}"
        location: "{{ location }}"
        connections:
          - cidr_list: 
              - "{{ dbaas_config.mongodb_cluster.ip }}/24"
            datacenter: "{{ datacenter.id }}"
            lan: "{{ internal_lan.id }}"
        display_name: "MongoDB Cluster for {{ datacenter_name }}"
        wait: true
      register: mongodb_cluster_response    


    - name: Extract MongoDB Cluster hostname
      ansible.builtin.set_fact:
        cluster_hostname: "{{ mongodb_cluster_response.mongo_cluster.properties.connection_string | regex_replace('^(.*)://(.*)$', '\\2') }}"


    - name: Create Cluster User
      ionoscloudsdk.ionoscloud.mongo_cluster_user:
        mongo_cluster_id: "{{ mongodb_cluster_response.mongo_cluster.id }}"
        mongo_username: dbadmin
        mongo_password: "{{ default_password }}"
        user_roles:
          - role: readWrite
            database: test
      register: mongo_user_response




    # =======================================================================
    # Note that, instead of {{ dbaas_config.mongodb_cluster.ip }} in the SSH
    # command below, one _could_ try to use the hostname contained in
    # {{ mongodb_cluster_response.mongo_cluster.properties.connection_string }}
    # but given that this uses the mongodb+srv protocol, one would need to
    # first query the corresponding SRV record, then the hostname returned
    # by said query. E.g.
    # $ dig +short _mongodb._tcp.m-hq5v594hxxxxxxxx.mongodb.gb-lhr.ionos.com srv
    # 10 1 27017 r1.m-hq5v594hxxxxxxxx.mongodb.gb-lhr.ionos.com.
    # $ dig +short r1.m-hq5v594hxxxxxxxx.mongodb.gb-lhr.ionos.com
    # 192.168.8.17
    - name: Print usage information
      ansible.builtin.debug:
        msg:
          - "The MongoDB cluster {{ cluster_hostname }} has been created"
          - "To access it, use one of the following commands:"
          - "    From the jumpbox:"
          - "        mongosh {{ mongodb_cluster_response.mongo_cluster.properties.connection_string }} --username dbadmin"
          - "    Externally via the jumpbox:"
          - "        In one shell:     ssh -L 27017:{{ dbaas_config.mongodb_cluster.ip }}:27017 root@{{ jumpbox_ip }}"
          - "        In another shell: mongosh 'mongodb://dbadmin@localhost?tls=true&tlsAllowInvalidHostnames=true'"
          - "{% if ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS %}    Externally via the NLB:{% endif %}"
          - "{% if ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS %}        mongosh 'mongodb://dbadmin@{{ ip_block[0] }}?tls=true&tlsAllowInvalidHostnames=true'{% endif %}"

```
{% endcode %}