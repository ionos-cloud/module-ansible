# Ansible Playbooks

## Ansible Playbooks

Ansible leverages YAML manifest files called Playbooks. The Playbook will describe the infrastructure to build and is processed from top down. Here is a simple Playbook that will provision two identical servers:

`example.yml`:

```yaml
      - hosts: localhost
      connection: local
      gather_facts: false

      tasks:
      - name: Provision a set of instances
          ionoscloudsdk.ionoscloud.server:
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

> :warning: If you are using names instead of UUIDs to reference objects and they contain field marked with no_log (such as passwords), they may not work, so please use UUIDs instead in those cases!

**NOT WORKING**:
```yaml
      - hosts: localhost
      connection: local
      gather_facts: false

      tasks:
      - name: Create Cluster
        ionoscloudsdk.ionoscloud.postgres_cluster:
          display_name: test
          db_password: test
        register: cluster_response

      - name: Delete Cluster
      ionoscloudsdk.ionoscloud.postgres_cluster:
          postgres_cluster: "{{ cluster_response.postgres_cluster.properties.display_name }}"
          state: absent
```

In this case you should use the UUID of the cluster as the above example will not work:

**WORKING**:
```yaml
      - hosts: localhost
      connection: local
      gather_facts: false

      tasks:
      - name: Create Cluster
          ionoscloudsdk.ionoscloud.postgres_cluster:
              display_name: test
              db_password: test
          register: cluster_response

      - name: Delete Cluster
          ionoscloudsdk.ionoscloud.postgres_cluster:
              postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
              state: absent
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

