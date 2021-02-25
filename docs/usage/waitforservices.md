# Wait for Services

There may be occasions where additional waiting is required. For example, a server may be finished provisioning and shown as available, but IP allocation and network access is still pending. The built-in Ansible module **wait\_for** can be invoked to monitor SSH connectivity.

```text
  - name: Wait for SSH connectivity
    wait_for:
      port: 22
      host: "{{ item.public_ip }}"
      search_regex: OpenSSH
      delay: 10
    with_items: ""
```

