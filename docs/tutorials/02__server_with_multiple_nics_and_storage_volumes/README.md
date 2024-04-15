# 2. Provision a Server with Multiple NICs and Storage Volumes

## Overview
In this installment, we will add a second NIC and volume to our basic server — whilst still rather trivial, this playbook might be useful as an example of how to do this using the output of a previous task (since it's not currently possible to pass arrays of NICs, etc. to `ionoscloudsdk.ionoscloud.server`).




## Before you begin
Continuing with the thought of learning about Ansible _and_ the IONOS Cloud module at the same time, you might find the following notes / hints helpful:

1. At a minimum, go through `main.yml` and `../vars.yml` to get a feeling for how everything fits together. What do you expect to happen?
2. Follow the steps outlined in the 'Usage' section below to actually provision your VM.
3. Look at what has been created using the DCD, at a minimum, and possibly using an API tool like [IonosCTL](https://docs.ionos.com/cli-ionosctl).
4. Go back through `main.yml` to compare what the various stanzas _say_ with what they _do_.
5. If you're not already familiar with Ansible's [registered variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#registering-variables), then you might want to set `verbose_debugging` to true (see `../vars.yml`) and re-run this playbook to see what each task is outputting upon completion.

For 'extra marks', you could:

1. use, e.g., [jsonpathfinder.com](https://jsonpathfinder.com) and/or
Ansible's [Playbook Debugger](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_debugger.html) to see how — and, in some cases, _why_ — the playbook references the nested variables that it does; and
2. expand this example to create a second server that's connected to the same LANs as the first using the contents of registered variables _as succinctly as possible_ — when and where can you use dot notation to access [nested variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#referencing-nested-variables), and where do you need to use bracket notation?



### What's in this Example?
Even though this example is still quite minimal, it includes and/or depends upon the following files:

| File                | Description                                                                                                          |
| ---                 | ---                                                                                                                  |
| `main.yml`          | This is the example's main (and only) Ansible file                                                                   |
| `../vars.yml`       | This file is common to all of our Ansible examples and contains a set of more generally-used variable definitions    |




## Usage
> **Note:** As with all other 'executable' examples in this repository, an 'End User Licence Agreement'-like statement will be displayed, which must also be accepted before the tasks proper can be executed.
>
> Please note that, while potentially quite minimal, you will incur charges for the resources based upon how long you keep them provisioned; for more information on the actual costs, you can follow the links displayed in the 'EULA' text. (But also, as a rough guide, a single-core VM with 1GB of RAM and 10GB of HDD storage would cost about 4.5 (Euro)cents per hour, as of April 2024.)


To provision this infrastructure:

1. make sure that your `IONOS_TOKEN` environment variable has been set; and
2. run the following command on your Ansible host:
   ```
   ansible-playbook main.yml
   ```

If you let it run until it completes successfully, you shouldn't _need_ to do anything else, however we still recommend that you confirm (via the DCD or `ionosctl`) that the server and its containing Virtual Data Center (VDC) have been deleted as expected; if the playbook failed with errors, then you will definitely want to do this.


> From this point on, we will assume that you have a working environment, and are aware of the costs associated with provisioning resources (albeit temporarily) and the importance of making sure all example resources have been completely unprovisioned afterwards; if you haven't already done so, we suggest you visit, e.g., [cloud.ionos.com/prices](https://cloud.ionos.com/prices) or [cloud.ionos.de/preise](https://cloud.ionos.de/preise), depending on where your contract is based.




## Summary
In this tutorial, we saw examples of:

1. how to use the `ionoscloudsdk.ionoscloud.nic` and `volume` modules to provision additional network interfaces and storage volumes; and
2. how one can access slightly more complicated nested attributes that one will often see when working with register variables.




## Source Files
The source files for this tutorial can be downloaded from its [Github repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/02__server_with_multiple_nics_and_storage_volumes` sub-directory.
