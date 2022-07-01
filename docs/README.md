# Introduction

## Overview

Ansible is an IT automation tool that allows you to configure, deploy, and orchestrate advanced tasks, such as continuous deployments or zero downtime rolling updates. The IONOS module for Ansible leverages the IONOS Cloud API.

## Getting Started

The module is also available on [Ansible Galaxy](https://galaxy.ansible.com/ionoscloudsdk/ionoscloud).

The IONOS module for Ansible requires the following:

* IONOS Cloud account
* Python >= 3.5
* [Ansible](https://www.ansible.com/)
* [IONOS SDK for Python](https://pypi.org/project/ionoscloud/) >= 6.0.2
* [IONOS DBaaS SDK for Python](https://pypi.org/project/ionoscloud-dbaas-postgres/) >= 1.0.2

> **_NOTE:_**  The Ansible module does not support Python 2. It only supports Python >= 3.5.

Before you begin you will need an IONOS account. The credentials from your registration will be used to authenticate against the IONOS Cloud API.

Ansible must also be installed before the IONOS module can be used. Please review the official [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html) for more information on installing Ansible.

The IONOS module requires the IONOS SDK for Python to be installed. This can easily be accomplished with Python PyPI:

```bash
pip install ionoscloud
pip install ionoscloud-dbaas-postgres
```

# Installation

## I. Using Ansible galaxy _(recommended)_

  Run the following command:

  ```bash
  ansible-galaxy collection install ionoscloudsdk.ionoscloud
  ```

## II. Downloading the module from GitHub

1. The IONOS module for Ansible must first be downloaded from GitHub. This can be accomplished a few different ways such as downloading and extracting the archive using `curl` or cloning the GitHub repository locally.

  Download and extract with `curl`:

  ```bash
  mkdir -p ionos-module-ansible && curl -L https://github.com/ionos-cloud/module-ansible/tarball/master | tar zx -C ionos-module-ansible/ --strip-components=1
  ```

  Clone the GitHub repository locally:

  ```bash
  git clone https://github.com/ionos-cloud/module-ansible
  ```

2. Ansible must be made aware of the new module path. This too can be accomplished a few different ways depending on your requirements and environment.

  * Ansible configuration file: `ansible.cfg`
  * Environment variable: `ANSIBLE_LIBRARY`
  * Command line parameter: `ansible-playbook --module-path [path]`

  2a. The preferred method is to update the Ansible configuration with the module path. To include the path globally for all users, edit the `/etc/ansible/ansible.cfg` file and add `library = /path/to/module/ionos_cloud` under the **\[default\]** section. For example:

  ```conf
  [default]
  library = /path/to/ionos-module-ansible/ionos_cloud
  ```

  Note that the Ansible configuration file is read from several locations in the following order:

  * `ANSIBLE_CONFIG` environment variable path
  * `ansible.cfg` from the current directory
  * `.ansible.cfg` in the user home directory
  * `/etc/ansible/ansible.cfg`

  2b. The module path can also be set using an environment variable. This variable will be lost once the terminal session is closed:

  ```bash
  export ANSIBLE_LIBRARY=/path/to/ionos-module-ansible/ionos_cloud
  ```

  2c. The module path can be overridden with an `ansible-playbook` command line parameter:

  ```bash
  ansible-playbook --module-path /path/to/ionos-module-ansible/ionos_cloud playbook.yml
  ```

## FAQ

1. How can I open a bug/feature request?

Bugs & feature requests can be open on the repository issues: [https://github.com/ionos-cloud/module-ansible/issues/new/choose](https://github.com/ionos-cloud/module-ansible/issues/new/choose)

2. Can I contribute to the Ansible Module?

Sure! Our repository is public, feel free to fork it and file a PR for one of the issues opened in the issues list. We will review it and work together to get it released.

