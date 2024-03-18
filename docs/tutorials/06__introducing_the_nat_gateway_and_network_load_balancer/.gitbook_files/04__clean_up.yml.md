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


    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "About to delete '{{ datacenter.name }}'' and all of its contents. Press <Enter> to proceed..."
      when: pause_between_operations



    - name: Delete the datacenter '{{ datacenter.name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        id: "{{ datacenter.id }}"
        state: absent


    - name: Delete the IP Block corresponding to this example
      ionoscloudsdk.ionoscloud.ipblock:
        name: "IP Block for {{ datacenter_name }}"
        state: absent


    - name: And finally delete any 'temporary' or run-time files
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      with_items:
        - ssh_config
        - ssh_known_hosts_tmp
        - temporary_id_rsa
        - temporary_id_rsa.pub
        - inventory.yml
        - cloud-init--app-servers.txt

```
{% endcode %}