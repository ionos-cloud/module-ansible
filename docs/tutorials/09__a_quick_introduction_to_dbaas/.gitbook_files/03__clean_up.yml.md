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
        url: "https://api.ionos.com/cloudapi/v6/datacenters?pretty=true&depth=1"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_datacenters_response

    
    - name: Extract the relevant entry from 'api__get_datacenters_response'
      ansible.builtin.set_fact:
        datacenter: "{{ api__get_datacenters_response.content | from_json | json_query(query) }}"
      vars:
        query: "items[?properties.name=='{{ datacenter_name }}'].{id: id, name: properties.name}"


    - name: Get information about the existing Postgres clusters
      ansible.builtin.uri:
        url: "https://api.ionos.com/databases/postgresql/clusters"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_postgres_clusters_response


    - name: Extract the relevant entry from 'api__get_postgres_clusters_response'
      ansible.builtin.set_fact:
        postgres_cluster: "{{ api__get_postgres_clusters_response.json | json_query(query) }}"
      vars:
        query: "items[?properties.displayName=='Postgres Cluster for {{ datacenter_name }}']"  #".{id: id, name: properties.name}"




    - name: Get information about the existing MongoDB clusters
      ansible.builtin.uri:
        url: "https://api.ionos.com/databases/mongodb/clusters"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_mongodb_clusters_response


    - name: Extract the relevant entry from 'api__get_mongodb_clusters_response'
      ansible.builtin.set_fact:
        mongodb_cluster: "{{ api__get_mongodb_clusters_response.json | json_query(query) }}"
      vars:
        query: "items[?properties.displayName=='MongoDB Cluster for {{ datacenter_name }}']"




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "About to delete '{{ datacenter_name }}' and all of its contents. Press <Enter> to proceed..."
      when: pause_between_operations


    - name: Delete Postgres Cluster
      ionoscloudsdk.ionoscloud.postgres_cluster:
        postgres_cluster: "{{ postgres_cluster[0].id }}"
        state: absent
        wait: true
      when: postgres_cluster | length > 0


    - name: Delete MongoDB Cluster
      ionoscloudsdk.ionoscloud.mongo_cluster:
        mongo_cluster: "{{ mongodb_cluster[0].id }}"
        state: absent
        wait: true
      when: mongodb_cluster | length > 0





    - name: Pause for an additional 15 seconds
      ansible.builtin.pause:
        seconds: 15
        

    - name: Delete the datacenter '{{ datacenter[0].name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        id: "{{ datacenter[0].id }}"
        state: absent
      when: datacenter | length > 0


    - name: Delete the IP Block corresponding to this example
      ionoscloudsdk.ionoscloud.ipblock:
        name: "IP Block for {{ datacenter_name }}"
        state: absent
      when: ENABLE_EXPLICITLY_UNSUPPORTED_CONFIGURATIONS


    - name: And finally delete any 'temporary' or run-time files
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      with_items:
        - ssh_config
        - ssh_known_hosts_tmp
        - temporary_id_rsa
        - temporary_id_rsa.pub

```
{% endcode %}