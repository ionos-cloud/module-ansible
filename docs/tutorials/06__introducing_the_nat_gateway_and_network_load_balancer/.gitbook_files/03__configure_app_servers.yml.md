The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/06__introducing_the_nat_gateway_and_network_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
- hosts: app-servers

  vars_files:
    - vars.yml


  tasks:
    # Apply some basic network configurations needed, since these VMs are
    # behind the NAT Gateway and don't have access to a 'full' DHCP server
    - name: Set our default route
      ansible.builtin.shell: "ip route add default via {{ nat_gateway.ip }} || true"


    # Arguably not the most robust solution, but while an approach based upon,
    # say, https://stackoverflow.com/a/67379573 would guarantee the resulting
    # file is always valid, assuming the level of indention doesn't change,
    # the following is simpler, and doesn't remove any comments that said file
    # might contain
    - name: Add our default route to /etc/netplan/50-cloud-init.yaml to make it persistent
      blockinfile:
        path: /etc/netplan/50-cloud-init.yaml
        insertbefore: "match:"
        block: |
          {% filter indent(width=12, first=true) %}
          routes:
            - to: default
              via: 192.168.8.1
          {% endfilter %}


    - name: Ensure 'DNS=212.227.123.16 212.227.123.17' is in the '[Resolve]' section of /etc/systemd/resolved.conf
      community.general.ini_file:
        path: /etc/systemd/resolved.conf
        section: Resolve
        option: DNS
        value: 212.227.123.16 212.227.123.17
        state: present


    - name: Restart the systemd-resolved service
      ansible.builtin.service:
        name: systemd-resolved
        state: restarted




    - name: Update repositories cache and upgrade the system
      ansible.builtin.apt:
        upgrade: dist
        update_cache: yes
        cache_valid_time: 3600


    - name: Install patch and nginx
      ansible.builtin.package:
        name:
          - patch
          - nginx
        state: present


    # Apply the changes mentioned in https://docs.nginx.com/nginx/admin-guide/load-balancer/using-proxy-protocol/
    - name: Patch the NGINX config files to support the Proxy Protocol
      ansible.posix.patch:
        src: nginx-config.patch
        basedir: /
        strip: 1
      when: nlb.proxy_protocol != "none"


    - name: And restart NGINX
      ansible.builtin.service:
        name: nginx
        state: restarted
      when: nlb.proxy_protocol != "none"


    - name: Need to recreate the NLB HTTP forwarding rule's targets
      ansible.builtin.debug:
        msg:
          - "NGINX has been configured to support (and expect) the PROXY protocol, however"
          - "until support is also added to the corresponding Ansible module, enabling it"
          - "there will need to be done manually, either via the DCD or an API PATCH call ---"
          - "please see https://docs.ionos.com/cloud/managed-services/network-load-balancer/configure-nlb#create-a-target"
          - "or https://api.ionos.com/docs/cloud/v6/#tag/Network-Load-Balancers/operation/datacentersNetworkloadbalancersForwardingrulesPatch"
          - "for more information"
      when: nlb.proxy_protocol != "none"


    - name: And create our per-host index.html files on the remote servers
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html

```
{% endcode %}