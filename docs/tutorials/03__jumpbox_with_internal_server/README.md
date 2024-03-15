# 3. Provision a Jumpbox and an Internal Server

# Overview
In this example, we will see how one might provision an 'internal server' (i.e. one that isn't directly connected to the Internet) along with a [Jumpbox (aka Jump Box aka Jump server)](https://en.wikipedia.org/wiki/Jump_server) that can be used to log into this 'semi-isolated' VM via SSH, and which can also be used, e.g., to run additional Ansible Playbooks _on the VM_ to perform additional, post-provisioning tasks. (In order to install additional packages, etc., on the new VM, it would, of course, need some kind of _outgoing_ network connectivity — we will look at how this can be done using our [NAT Gateway](https://docs.ionos.com/cloud/early-access/nat-gateway/overview) in Part 6 of this series.)




## Before you begin
This example also introduces a few new modules, techniques and 'code snippets' that you might find interesting, including:

1. how the `ionoscloudsdk.ionoscloud.cube_template` and `cube_server` modules can be used to provision a [Cube Server](https://docs.ionos.com/cloud/compute/cloud-cubes/cloud-cubes) given its desired 'size' name;
2. pointers to and/or examples of how files can be created 'on the fly' (e.g. via `ansible.builtin.shell` + HEREDOCs, via the `copy` module, and via Jinja templates); and
3. how `ssh_config` and Ansible inventory files can be automatically generated and then used, together, to allow you to ssh into, and run Ansible playbooks on a server that isn't directly connected to the Internet.



### What's in this example?
This example includes and/or depends on the following files:

| File                | Description                                                                                                          |
| ---                 | ---                                                                                                                  |
| `main.yml`                        | This is the example's main Ansible file; it communicates via `localhost` and our Ansible Module with the IONOS Cloud [Cloud API](https://api.ionos.com/docs/cloud/) in order to provision our virtual resources   |
| `configure-internal-server.yml`   | This playbook is run _on the internal VM_ via the jumpbox (see `ansible_ssh_common_args` in `inventory.yml` and/or `ssh_config` _after_ running `main.yml`)   |
| `cloud-init.txt`                  | This file contains the [cloud-init data](https://docs.ionos.com/cloud/compute-engine/virtual-servers/how-tos/boot-cloud-init) that will be used to tailor the internal server when it's being provisioned    |
| `templates/ssh_config.j2`         | A simple [Jinja template](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html), in this case, to dynamically create the `ssh_config` file mentioned above     |
| `../vars.yml`                     | This file is common to all of our Ansible examples and contains a set of more generally-used variable definitions    |




## Usage

1. To provision this infrastructure, simply run the following command:
   ```
   ansible-playbook main.yml
   ```
2. Optionally, look at the contents of the dynamically-created files (in particular, `ssh_config` and `inventory.yml`)
3. To ssh into the VMs, type the following _from the same directory in another shell_ (where `${DESIRED_SERVER}` is either `jumpbox` or `internal`):
   ```
   ssh -F ssh_config ${DESIRED_SERVER}
   ```
4. To configure the internal server via the jumpbox, you can then run the following command (also from a secondary shell):
   ```
   ansible-playbook -i inventory.yml configure-internal-server.yml
   ```
5. Once you have finished exploring this example, press `<Enter>` in the shell from Step 1 to let the `main.yml` playbook delete the provisioned resources.




## Summary
In this tutorial, we saw examples of:

1. how to use the `ionoscloudsdk.ionoscloud.cube_template` and `cube_server` modules to provision a Cube Server;
2. how the `ansible.builtin.shell` module and the `ssh-keygen` command can be used to generate a temporary SSH key-pair;
3. how the `ansible.builtin.template` module, and the `ansible.builtin.shell` module and the `cat` command can be used to dynamically create files based upon the contents of register variables
4. how we can use the above to configure a jumpbox that can, in turn, be used to access and configure an 'internal server' that is otherwise inaccessible from the Internet




## Source files
The source files for this tutorial can be downloaded from its [Github repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git`, and changing into the `module-ansible/docs/tutorials/03__jumpbox_with_internal_server` sub-directory.
