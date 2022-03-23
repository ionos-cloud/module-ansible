# SSH Key Authentication

The Ionos module sets server authentication using the **image\_password** and **ssh\_keys** parameters. Previous examples have demonstrated the administrative user password being set with the **image\_password** parameter. The following example demonstrates two public SSH keys being supplied with two different methods.

1. Set the public key as a string in the Playbook.
2. Load the public key into a variable from a local file.

`example.yml`:

```yaml
  - hosts: localhost 
    connection: local 
    gather_facts: false

    vars: 
        ssh_public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

  tasks:
  - name: Provision a server
   ionoscloudsdk.ionoscloud.server:
      datacenter: Example
      name: server%02d
      assign_public_ip: true
      image: 25cfc4fd-fe2f-11e6-afc5-525400f64d8d
      ssh_keys:
          - "{{ ssh_public_key }}"
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDPCNA2YgJ...user@hostname"
      state: present
```

