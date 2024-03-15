The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/04__working_with_existing_resources` sub-directory.

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
    # Method 1: Using ansible.builtin.shell, something like `ionosctl` and
    # set_fact to create a new object containing the attributes of interest
    - name: Retrieve information about '{{ datacenter_name }}' via ionosctl
      ansible.builtin.shell: ionosctl datacenter list | grep '{{ datacenter_name }}' | cut -d' ' -f1
      register: ionosctl_datacenter_response


    - name: Print contents of 'ionosctl_datacenter_response'
      ansible.builtin.debug:
        var: ionosctl_datacenter_response
      when: verbose_debugging


    - name: Set ionosctl-derived fact
      ansible.builtin.set_fact:
        datacenter: { 'name': "{{ datacenter_name }}", 'id': "{{ ionosctl_datacenter_response.stdout }}" }




    # =======================================================================
    # Method 2: Using the Cloud API (https://api.ionos.com/docs/cloud/v6/),
    # the ansible.builtin.uri module, Bearer Authorization and json_query
    - name: Get information about the LANs in '{{ datacenter_name }}'
      ansible.builtin.uri:
        url: "https://api.ionos.com/cloudapi/v6/datacenters/{{ datacenter.id }}/lans?pretty=true&depth=2&offset=0&limit=1000"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_lans_response


    # See https://docs.ansible.com/ansible/latest/collections/community/general/docsite/filter_guide_selecting_json_data.html
    # for insights into how `json_query` can be used. Note that, since the
    # reserved characters in 'content' are actually escaped, we first need
    # to pass it through `from_json` before we can perform the query
    - name: Set a couple of LAN-related facts based on the above
      ansible.builtin.set_fact:
        all_lans: "{{ api__get_lans_response.content | from_json | json_query('items[*].{id: id, properties: properties}') }}"
        secondary_lan: "{{ (api__get_lans_response.content | from_json | json_query(query))[0] }}"
      vars:
        query: "items[?properties.name=='internal'].{id: id, properties: properties}"


    # Add a second NIC to the server by name
    - name: Add a second NIC to the server
      ionoscloudsdk.ionoscloud.nic:
        datacenter: "{{ datacenter_name }}"
        name: "{{ server_name }}.eth1"
        server: "{{ server_name }}"
        lan: "{{ secondary_lan.id }}"
        ips:
          - 192.168.16.16
        dhcp: true

        state: present
        wait: true
        wait_timeout: "{{ wait_timeout }}"




    # =======================================================================
    # Method 3: Using one of the supported `_info` modules --- in this case,
    # `ionoscloudsdk.ionoscloud.server_info` --- to retrieve information 
    # _all_ of the servers contained in the Data Center 'datacenter_name'
    - name: Get information about the server '{{ server_name }}'
      ionoscloudsdk.ionoscloud.server_info:
        datacenter: "{{ datacenter_name }}"
        depth: 5
      register: get_server_response


    # And retrieve the desired 'server information object' by iterating over
    # 'get_server_response.servers' and comparing 'item.properties.name' to
    # the value of 'server_name'. (Note that, as server names do _not_ have
    # to be unique, this approach cannot be used in _every_ conceivable
    #  situation, however as long as server names are unique, it will work
    - name: Retrieve information for the server '{{ server_name }}' by manually iterating through 'get_server_response'
      ansible.builtin.set_fact:
        desired_server_info__iter: "{{ item }}"
      when: item.properties.name == server_name
      with_items: "{{ get_server_response.servers }}"


    # Alternatively, we can create a list of 'server information objects'
    # whose 'properties.name' value matches 'server_name'; in _this_ case,
    # if there are multiple servers with the same name, information about
    # _all_ of them will be returned
    - name: Retrieve information for the server '{{ server_name }}' using `json_query`
      ansible.builtin.set_fact:
        desired_server_info__query: "{{ get_server_response | json_query(query) }}"
      vars:
        query: "servers[?properties.name=='{{ server_name }}']"




    - name: Print the contents of 'api__get_lans_response'
      ansible.builtin.debug:
        var: api__get_lans_response
      when: verbose_debugging


    - name: Print the contents of 'desired_server_info__iter'
      ansible.builtin.debug:
        var: desired_server_info__iter
      when: verbose_debugging


    - name: Print the contents of 'desired_server_info__query'
      ansible.builtin.debug:
        var: desired_server_info__query
      when: verbose_debugging

```
{% endcode %}