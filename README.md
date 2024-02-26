[![Ansible Galaxy](https://img.shields.io/badge/galaxy-ionoscloudsdk.ionoscloud-660198.svg?style=flat)](https://galaxy.ansible.com/ionoscloudsdk/ionoscloud)
[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=alert_status)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=bugs)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=security_rating)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=ansible-module&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=ansible-module)
[![Workflow status](https://github.com/ionos-cloud/module-ansible/workflows/CI/badge.svg?branch=master)](https://github.com/ionos-cloud/module-ansible/actions/workflows/CI.yml)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")

# Ansible Module for IONOS Cloud


## Overview

Ansible is an IT automation tool that allows you to configure, deploy, and orchestrate advanced tasks, such as continuous deployments or zero downtime rolling updates. The IONOS module for Ansible leverages the IONOS Cloud API.

## Getting Started

Source code and in-depth documentation about installation and use are available [here](https://docs.ionos.com/ansible/). The module is also available on [Ansible Galaxy](https://galaxy.ansible.com/ionoscloudsdk/ionoscloud).

The IONOS module for Ansible requires the following:

* IONOS Cloud account
* Python >= 3.5
* [Ansible](https://www.ansible.com/)
* [IONOS Cloud **Compute Engine** Python SDK](https://pypi.org/project/ionoscloud/) >= 6.1.6
* [IONOS Cloud **DBaaS PostgreSQL** Python SDK](https://pypi.org/project/ionoscloud-dbaas-postgres/) >= 1.1.1
* [IONOS Cloud **DBaaS MongoDB** Python SDK](https://pypi.org/project/ionoscloud-dbaas-mongo/) >= 1.2.2
* [IONOS Cloud **Container Registry** Python SDK](https://pypi.org/project/ionoscloud-container-registry/) >= 1.0.0
* [IONOS Cloud **Data Platform** Python SDK](https://pypi.org/project/ionoscloud-dataplatform/) >= 1.0.0
* [IONOS Cloud **Certificate Manager** Python SDK](https://pypi.org/project/ionoscloud-cert-manager/) >= 1.0.0

> **_NOTE:_**  The Ansible module does not support Python 2. It only supports Python >= 3.5.

Before you begin you will need an IONOS account. The credentials from your registration will be used to authenticate against the IONOS Cloud API.

Ansible must also be installed before the IONOS module can be used. Please review the official [Ansible Documentation](http://docs.ansible.com/ansible/intro_installation.html) for more information on installing Ansible.

The IONOS module requires some IONOS SDKs for Python to be installed. This can easily be accomplished with Python PyPI:

```text
pip install ionoscloud
pip install ionoscloud-dbaas-postgres
pip install ionoscloud-dbaas-mongo
pip install ionoscloud-container-registry
pip install ionoscloud-dataplatform
pip install ionoscloud-cert-manager
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

   ```text
   mkdir -p ionos-module-ansible && curl -L https://github.com/ionos-cloud/module-ansible/tarball/master | tar zx -C ionos-module-ansible/ --strip-components=1
   ```

   Clone the GitHub repository locally:

   ```text
   git clone https://github.com/ionos-cloud/module-ansible
   ```

2. Install the collection with ansible-galaxy.

  ```bash
  ansible-galaxy collection build .
  ansible-galaxy collection install ionoscloudsdk-ionoscloud-<module_version>.tar.gz
  ```

## FAQ

1. How can I open a bug/feature request?

Bugs & feature requests can be open on the repository issues: [https://github.com/ionos-cloud/module-ansible/issues/new/choose](https://github.com/ionos-cloud/module-ansible/issues/new/choose)

1. Can I contribute to the Ansible Module?

Sure! Our repository is public, feel free to fork it and file a PR for one of the issues opened in the issues list. We will review it and work together to get it released.

