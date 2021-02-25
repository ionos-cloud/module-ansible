# Testing

Set your IONOS user credentials.

```text
export IONOS_USERNAME=username
export IONOS_PASSWORD=password
```

Change into the `tests` directory and execute the Playbooks.

```text
cd tests
ansible-playbook server-test.yml
```

Note: The IONOS public image UUIDs change periodically due to updates. Therefore, it is recommended to use image aliases.

