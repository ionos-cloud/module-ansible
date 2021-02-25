# Ansible Playbooks

## Ansible Playbooks

Ansible leverages YAML manifest files called Playbooks. The Playbook will describe the infrastructure to build and is processed from top down. Here is a simple Playbook that will provision two identical servers:

`example.yml`:

```text
      - hosts: localhost
      connection: local
      gather_facts: false

      tasks:
      - name: Provision a set of instances
          server:
              datacenter: Example
              name: server%02d
              auto_increment: true
              count: 2
              cores: 4
              ram: 4096
              image: 25cfc4fd-fe2f-11e6-afc5-525400f64d8d
              image_password: secretpassword
              location: us/las
              assign_public_ip: true
              remove_boot_volume: true
              state: present
          register: ionos
```

## Execute a Playbook

If your credentials are not already defined:

```text
export IONOS_USERNAME=username
export IONOS_PASSWORD=password
```

The `ansible-playbook` command will execute the above Playbook.

```text
ansible-playbook example.yml
```

