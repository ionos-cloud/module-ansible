The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/05__introducing_roles` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```yml
---
# ==============================================================================
- name: About to execute tasks file for role 'docker-server'
  ansible.builtin.meta: noop



- name: Make sure all the dependencies are installed
  ansible.builtin.package:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - gnupg
      - lsb-release
    state: present


- name: Add signing key
  ansible.builtin.apt_key:
    url: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"
    state: present


- name: Add repository into sources list
  ansible.builtin.apt_repository:
#    repo: "deb [arch={{ ansible_architecture }}] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} stable"
    repo: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} stable"
    state: present
    filename: docker


- name: Update the repositories cache
  ansible.builtin.apt:
    update_cache: yes


- name: Install Docker
  ansible.builtin.package:
    name:
      - containerd.io
      - docker-ce
      - docker-ce-cli
      - docker-compose-plugin
      - docker-compose
      - docker-registry
    state: present


# See https://docs.ansible.com/ansible/latest/collections/community/docker/docker_container_module.html#examples
- name: Create test containers
  community.docker.docker_container:
    name: "test-{{ test_image }}"
    image: "{{ test_image }}"
    auto_remove: true
    state: present
```
{% endcode %}