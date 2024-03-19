# Getting Started with the IONOS Cloud Ansible Module

> **Warning**
>
> The notes and code-snippets included in this repository are provided _without warranty_, as examples of how to perform certain tasks or operations using our Configuration Management tools and/or to help replicate and diagnose potential issues more quickly.
>
> While every effort has been made to ensure that the information and/or code contained herein is current and works as intended, it has not been through any formal or rigorous testing process, and therefore should be used at your own discretion.
>
> For _definitive_ information and documentation, please see [docs.ionos.com/ansible](https://docs.ionos.com/ansible)




## Overview
In this series, we will introduce the [IONOS Cloud Ansible Module](https://docs.ionos.com/ansible), and show how it can be used to provision many of our more commonly-used Compute resources and Managed Services in combinations that are at least _representative_ of 'real-world' deployments.

Beyond providing prototypical examples, we will also introduce a few more general conventions and patterns which can be used to make your code more readable and reusable, and where there are a few different ways of performing the same task, we will try to introduce them, via comments, directly in the source files.




### Intended audience
The examples and code-snippets contained in this repository are intended for people who are not necessarily familiar with IONOS Cloud's product offerings and/or our Ansible module, but are wanting to learn how to provision and configure such resources in a scriptable way. A certain familiarity with Linux (or other UNIX-like operating systems) is assumed, and _some_ experience with Ansible or other scripting and/or programming languages would also help.

For some of the more 'advanced' topics — including our Managed Kubernetes and Database offerings — it is assumed that you are already familiar with the underlying software; in these cases, we will not be introducing basic concepts — rather, we will focus on IONOS Cloud-specific configuration and optimisation options.

A secondary use for these tutorials is to provide 'known-working' reference implementations, especially for Managed Services that have _practical_ dependencies on other types of resources. For this use case, the relevant examples can be provisioned and configured using Ansible, but then inspected and, potentially, 'tweaked' interactively via the Data Center Designer (DCD) or the API to get a better understanding of how these products might be used in 'production environments'.



### What's in this collection?
This collection consists of the following tutorials — while each one typically focuses on one, or at most two complementary types of resources, some of them also introduce 'better practices' and/or techniques that can help make your code more modular, and while they are basically independent, they trace out a certain 'trajectory' in terms of complexity and 'real-world applicability':


| File                                                      | Description |
| ---                                                       | ---         |
| [`01__minimal_example`](01__minimal_example)              | A very minimal example that creates a one-server datacenter and shows: (a) how to retrieve a few pieces of information 'programmatically'; and (b) how to change the VM's state, before cleaning up after itself    |
| [`02__server_with_multiple_nics_and_storage_volumes`](02__server_with_multiple_nics_and_storage_volumes)    | This example builds upon the first one by showing you how to create and attach secondary NICs and storage volumes to a server   |
| [`03__jumpbox_with_internal_server`](03__jumpbox_with_internal_server)    | This example introduces the Cube server, and shows you how an SSH ['jump server / jump box'](https://en.wikipedia.org/wiki/Jump_server) can be used to provide shell access, and apply Ansible Playbooks to an otherwise inaccessible VM; it also shows how one can 'bridge' IaaS-level provisioning and VM-level configuration    |
| [`04__working_with_existing_resources`](04__working_with_existing_resources)    | This example shows how `info` modules, external tools (in this case, `ionosctl`), and the [ansible.builtin.uri](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html) module can be used to obtain information about, and work with pre-existing resources    |
| [`05__introducing_roles`](05__introducing_roles)              | In this example, we briefly look at [Ansible Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html), and how they can be used to make your Ansible code more modular and reusable    |
| [`06__introducing_the_nat_gateway_and_network_load_balancer`](06__introducing_the_nat_gateway_and_network_load_balancer)    | In this example, we introduce the NAT Gateway and Network Load Balancer, and see how they can be used to implement source and destination NAT, respectively    |
| [`07__introducing_the_application_load_balancer`](07__introducing_the_application_load_balancer)    | In this example, we introduce the Application Load Balancer and see how it can be used to implement _Layer 7_ load balancing with rule-based forwarders    |
| [`09__a_quick_introduction_to_dbaas`](09__a_quick_introduction_to_dbaas)    | In this example, we introduce our Managed PostgreSQL and MongoDB Services, and show how they can be accessed from servers in different locations   |




## Before you begin
In order to use the examples in this tutorial series, you will need a working installation of [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html) and our [Ansible module](https://docs.ionos.com/ansible/#installation); if you have [git](https://git-scm.com) installed as well, that will make it easier to download and manage these examples' source and configuration files.

While the recommended way to explore our APIs, SDKs and Confirguration Management Tools is to install the necessary software components as described in their respective documentation, a quick-and-easy way to get started is to use the [IONOS Cloud API / SDK 'Sandpit'](https://hub.docker.com/r/metzionos/ionos-cloud-api-sandpit) Docker container, assuming you have access to a machine with a working installation of [Docker Engine](https://docs.docker.com/engine/) or [Docker Desktop](https://docs.docker.com/desktop/) that's capable of running amd64-based Linux images.

If you do, then just follow the instructions over at the image's [Docker Hub page](https://hub.docker.com/r/metzionos/ionos-cloud-api-sandpit) to spin up a 'sandpit environment' that you can use to explore our [Ansible module](https://docs.ionos.com/ansible) and [Terraform provider](https://docs.ionos.com/terraform-provider/), along with some other command line utilities...

> **Note:** Upon trying to 'apply' any of the examples in this repository, an 'End User Licence Agreement'-like statement will be displayed, which must also be accepted before the tasks proper can be executed.
>
> Also note that, while potentially quite minimal, you will incur charges for the resources based upon how long you keep them provisioned; for more information on the actual costs, you can follow the links displayed in the 'EULA' text. (But also, as a rough guide, a single-core VM with 1GB of RAM and 10GB of HDD storage would cost about 4.5 (Euro)cents per hour, as of September 2023.)
>
> **While every effort has been made to ensure each example 'cleans up' after itself, this cannot be guaranteed — particularly if an error is thrown, e.g., when trying out custom changes or otherwise experimenting with the provided files. To avoid any unexpected charges, we strongly recommend that you review your resources in the DCD, and manually delete anything that was missed by the Ansible Playbooks.** 



### Important note about token- vs password-based authentication
Although most of our Configuration Management tools, Software Development Kits (SDKs) and APIs support both password- and token-based authentication, the use of tokens is generally preferred. While far from exhaustive, reasons for using tokens over passwords include that they can provide more finely-grained _per application_ credentials that can expire and/or be invalidated independently of each other, and in contrast to passwords, should a _token_ be compromised, the chances that it will leak information which can be used to compromise other services are also significantly reduced.

Accordingly, whenever the code included in this repository makes lower-level calls to our Cloud API, it assumes that the `IONOS_TOKEN` environment variable contains a valid token, and will _not_ fallback to using the `IONOS_USERNAME` and `IONOS_PASSWORD` environment variables.

For information on how to create a token that can be used for IONOS Cloud API calls, see our [Authentication API](https://api.ionos.com/docs/authentication/v1/#tag/tokens) documentation or [ionosctl / Authentication / Login](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/login) and [TokenGenerate](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate).



### A few good-to-knows
In addition to the above disclaimers, the following notes might help you troubleshoot problems commonly encountered when getting started:

- If you get any `couldn't resolve module/action ... This often indicates a misspelling, missing collection, or incorrect module path` error messages, make sure you've downloaded and 'setup' the IONOS Cloud Ansible module; see [this page](https://docs.ionos.com/ansible/#installation) for the definitive information, however two ways of doing this are:
  - to run `ansible-galaxy collection install ionoscloudsdk.ionoscloud` as _yourself_ (i.e. without calling `sudo` or otherwise running this as `root`) — under Linux, this will install said module under `~/.ansible/collections/ansible_collections`; or
  - to clone the module into the location of your choosing using the command `git clone https://github.com/ionos-cloud/module-ansible`, and to inform Ansible of this location, either through the use of the `ANSIBLE_LIBRARY` environment variable or via a command-line argument (e.g., `ansible-playbook --module-path ${MODULE_PATH} ...`)
- If you get a `name 'certificate_manager_sdk_version' is not defined` error message when working with the Application Load Balancer, make sure you have the module installed (this can be done by running the command `pip install ionoscloud-cert-manager`)
- You will need to set the `IONOS_TOKEN` environment variable before running any of the playbooks contained in this subdirectory. For information on how to create a token, see the section above.
- Should you wish to 'invoke' IONOS Cloud modules _without_ having to use their fully qualified collection name (FQCN) every time, you can use the [`collections`](https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html#simplifying-module-names-with-the-collections-keyword) keyword and the `ionoscloudsdk.ionoscloud` 'namespace'. (Whilst convenient, this _could_, in theory, lead to 'namespace collisions' with other third-party modules, hence the advice to use FQCNs in any production code.)




## Glossary
The following key terms are used throughout this series of tutorials:

| Term                   | Description                                          |
| ---                    | ---                                                  |
| DCD                    | [Data Center Designer](https://docs.ionos.com/cloud/getting-started/data-center-designer), a unique graphical tool for creating and managing Virtual Data Centers (VDC) in the cloud; configuration is intuitive and straightforward with a JavaScript-based graphical user interface.   |
| VDC                    | A Virtual Data Center is a collection of cloud resources used for creating an enterprise-grade IT infrastructure. VDC resources include the processors, memory, disk space, and networks from which virtual machines are built.    |




## Source files
The source files for all of the examples in this tutorial series can be downloaded from [github.com/ionos-cloud/module-ansible/tree/master/docs/tutorials](https://github.com/ionos-cloud/module-ansible/tree/master/docs), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials` sub-directory.
