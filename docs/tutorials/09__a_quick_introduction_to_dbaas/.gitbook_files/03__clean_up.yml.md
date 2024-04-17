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
    - name: Get information about 'Postgres Cluster for {{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.postgres_cluster_info:
        filters: "{ 'properties.display_name': 'Postgres Cluster for {{ datacenter_name }}' }"
      register: postgres_clusters_response


    - name: Get information about 'MongoDB Cluster for {{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.mongo_cluster_info:
        filters: "{ 'properties.display_name': 'MongoDB Cluster for {{ datacenter_name }}' }"
      register: mongo_clusters_response




    # =======================================================================
    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "About to delete '{{ datacenter_name }}' and all of its contents. Press <Enter> to proceed..."


    - name: Delete Postgres Cluster
      ionoscloudsdk.ionoscloud.postgres_cluster:
        postgres_cluster: "{{ postgres_clusters_response.postgres_clusters[0].id }}"
        state: absent

        wait: true
        wait_timeout: "{{ wait_timeout }}"
      when: postgres_clusters_response.postgres_clusters | length > 0


    - name: Delete MongoDB Cluster
      ionoscloudsdk.ionoscloud.mongo_cluster:
        mongo_cluster: "{{ mongo_clusters_response.mongo_clusters[0].id }}"
        state: absent

        wait: true
        wait_timeout: "{{ wait_timeout }}"
      when: mongo_clusters_response.mongo_clusters | length > 0




    - name: Pause for an additional 15 seconds
      ansible.builtin.pause:
        seconds: 15
        

    - name: Delete the datacenter '{{ datacenter_name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        datacenter: "{{ datacenter_name }}"
        state: absent


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