The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/08__a_quick_introduction_to_managed_kubernetes` sub-directory.

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
    # Method 2: Using the Cloud API (https://api.ionos.com/docs/cloud/v6/),
    # the ansible.builtin.uri module, Bearer Authorization and json_query
    - name: Get information about the LANs in '{{ datacenter_name }}'
      ansible.builtin.uri:
        url: "https://api.ionos.com/cloudapi/v6/datacenters/7b5a9a9e-a2b1-438a-8746-967d4cad4612/?pretty=true&depth=2&offset=0&limit=1000"
        method: GET
        return_content: true
        headers:
          Authorization: "Bearer {{ lookup('ansible.builtin.env', 'IONOS_TOKEN', default='') }}"
      no_log: true
      register: api__get_dc_response


    - name: Debug
      ansible.builtin.debug:
        var: api__get_dc_response.json.properties.cpuArchitecture[0].cpuFamily

```
{% endcode %}