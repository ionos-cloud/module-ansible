The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/07__introducing_the_application_load_balancer` sub-directory.

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
    - name: Get information about the datacenter '{{ datacenter_name }}'
      ionoscloudsdk.ionoscloud.datacenter_info:
        filters: { 'properties.name': '{{ datacenter_name }}' }
      register: datacenter_info_response


    - name: Wait for user confirmation
      ansible.builtin.pause:
        prompt: "About to delete '{{ datacenter_info_response.datacenters[0].properties.name }}' and all of its contents. Press <Enter> to proceed..."




    - name: Delete the datacenter '{{ datacenter_name }}' and everything contained therein
      ionoscloudsdk.ionoscloud.datacenter:
        datacenter: "{{ datacenter_name }}"
        state: absent


    - name: Delete the IP Block corresponding to this example
      ionoscloudsdk.ionoscloud.ipblock:
        ipblock: "IP Block for {{ datacenter_name }}"
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