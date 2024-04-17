# 1. A Minimal Example

## Overview
We begin our look at the IONOS Cloud Ansible Module with a minimal example that creates, and then deletes a Virtual Data Center (VDC) containing one server. It also shows you how the Ansible Module can be used to shut off a VM and power it back on.



## Before you begin
If you're looking at this example whilst also learning about Ansible, then the following notes / hints might prove helpful:

1. Read through the table below, which describes the files that make up this example.
2. At a minimum, go through `main.yml` and `../vars.yml` to get a feeling for how everything fits together. What do you expect to happen?
3. Follow the steps outlined in the 'Usage' section below to actually provision your VM.
4. Look at what was created in the DCD, at a minimum, and possibly using an API tool like the rather excellent [IonosCTL](https://docs.ionos.com/cli-ionosctl) command-line tool.
5. Go back through `main.yml` to compare what the various stanzas _say_ with what they _do_.
6. Once you have a general understanding of what this example does (and _how_ it does what it does), feel free to make whatever changes you want to, knowing that you can always just do a `git diff`, `git revert` or `git pull` if you 'break something' along the way. (That said, the scope for modification is a _bit_ limited due to the minimal nature of this example — if you want to start playing around with multiple storage volumes or NICs, you might want to wait until the next example.)



### What's in this example?
Even though this example is quite minimal, it includes and/or depends upon the following files:

| File                | Description                                                                                                          |
| ---                 | ---                                                                                                                  |
| `main.yml`          | As its name suggests, this is the example's main (and only) Ansible file                                             |
| `../vars.yml`       | This file is common to all of our Ansible examples and contains a set of more generally-used variable definitions    |
| `cloud-init.txt`    | This file contains the [cloud-init data](https://docs.ionos.com/cloud/compute-engine/virtual-servers/how-tos/boot-cloud-init) that will be used to tailor the new server while it's being provisioned    |




## Usage
> **Note:** As with all other 'executable' examples in this repository, an 'End User Licence Agreement'-like statement will be displayed, which must be accepted before the tasks proper can be executed.
>
> Please note that, while potentially quite minimal, you will incur charges for the resources based upon how long you keep them provisioned; for more information on the actual costs, you can follow the links displayed in the 'EULA' text. (But also, as a rough guide, a single-core VM with 1GB of RAM and 10GB of HDD storage would cost about 4.5 (Euro)cents per hour, as of April 2024.)

To provision this infrastructure:

1. make sure that you have a working installation of Ansible and the IONOS Cloud Ansible module as described in the '[Before you begin](../README.md#before-you-begin)' section of this series' introduction, and that your `IONOS_TOKEN` environment variable is set; and
2. run the following command on your Ansible host:
   ```
   ansible-playbook main.yml
   ```

If you let it run until it completes successfully, you shouldn't _need_ to do anything else, however we still recommend that you confirm (via the DCD or `ionosctl`) that the server and its containing data center have been deleted as expected; if the playbook failed with errors, then you will _definitely_ want to do this.


Should you have any problems running this playbook, you might want to refer to the section entitled '[A few good to knows](../README.md#a-few-good-to-knows)' for some troubleshooting tips.




## Summary
Although quite limited in its scope, this example illustrates several things (at least to the beginner) including:

1. how to provision IONOS Cloud Data Centers and Servers, and to change the state of the latter;
2. how to read in the contents of files and environment variables (in `../vars.yml`);
3. how to prompt for user input (and evaluate composite conditionals); and
4. how to use the results of previous tasks (i.e. register variables) — e.g., `datacenter_response` and `create_server_response`




## Source files
The source files for this tutorial can be downloaded from its [Github repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/01__minimal_example` sub-directory.
