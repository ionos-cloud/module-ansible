# 5. An Introduction to Ansible Roles

## Overview
In this example, we will take a quick digression to look at [Ansible Roles](https://docs.ansible.com/ansible/latest//playbook_guide/playbooks_reuse_roles.html) and how they can be used to make your code more reusable.

As roles are a core feature of Ansible — i.e. they are completely independent of the IONOS Core Ansible Module — we won't go into any explanation of their structure or how to create them (though a few useful references are mentioned at the bottom of this document); rather, this is more about providing an example that you can look at and (potentially) use as a starting point for some of your own sample projects.




## Before you begin
 If you're not already familiar with the concepts of roles, you might want to look at the [Ansible Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html) section of the official documentation before continuing with the rest of this tutorial.

 


### What's in this example?
This example includes and/or depends on the following files:

| File             | Description                                                                                            |
| ---              | ---                                                                                                    |
| `part-1.yml`     | This playbook provisions a single server and creates a few temporary files that are used by the subsequent playbooks    |
| `part-2.yml`     | This playbook runs _on_ the newly-provisioned server and applies a few roles to this VM    |
| `part-3.yml`     | This playbook cleans up all of the resources provisioned in Part 1, and should be run, once you're done with the earlier parts    |
| `vars.yml`       | This file contains the variable definitions common to `part-1.yml`, `part-2.yml` and `part-3.yml`    |
| `../vars.yml`    | This file is common to all of our Ansible examples and contains a set of more generally-used variable definitions     |
| `templates/ssh_config.j2`    | A simple Jinja template, in this case, to dynamically create the `ssh_config` file mentioned above     |
| `roles/`         | A set simple, unofficial but usable roles that will be used in this example, and which you cold look at and/or edit    |




## Usage
1. To provision our 'starting' infrastructure, run the following command:
   ```
   ansible-playbook part-1.yml
   ```
2. To execute the 'meat' of this example, run the following command (possibly after enabling `verbose_debugging` — see below):
   ```
   ansible-playbook part-2.yml
   ```
3. Optionally, examine the outputs of the previous step; if you'd like to make changes to `part-2.yml`, you can delete the resources that were provisioned in Step 2, and re-run said playbook
4. Execute the following to delete the resources provisioned in the previous steps:
   ```
   ansible-playbook part-3.yml
   ```




## Resources and references
- Ansible Documentation. Using Ansible playbooks / Working with playbooks / Roles. Available from [docs.ansible.com/ansible/latest//playbook_guide/playbooks_reuse_roles.html](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
- Ansible Documentation. Galaxy User Guide / Installing roles from Galaxy. Available from [docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-roles-from-galaxy](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-roles-from-galaxy)
- Red Hat, Enable Sysadmin (April 2021). 8 Steps to developing an Ansible Role in Linux. Retrieved from [https://www.redhat.com/sysadmin/developing-ansible-role](redhat.com/sysadmin/developing-ansible-role) on 17 May 2023.