# 4. How to Work with Existing Resources

## Overview
Thus far, all of our examples have consisted of a single Ansible playbook (at least as far as the provisioning tasks were concerned). While fine in _simple_ situations, this approach doesn't scale well with the complexity of the problem you're trying to solve (where, e.g., you might need to split your code over multiple, separate playbooks), or if you're wanting to modify pre-existing resources. (In the latter case, in particular, since they might've been provisioned completely independently of any Ansible playbooks, there might never have been any outputs that could've been saved into a register variable.)

In this example, we will look at three ways in which we can work with pre-existing resources:

1. by using an external tool (in this case, `ionosctl`) to look up the required information, and the `ansible.builtin.shell` and `set_fact` modules to process its output;
2. by using the `ansible.builtin.uri` module and the `community.general.json_query` filter to obtain this information via our [Cloud API](https://api.ionos.com/docs/cloud/v6/); and
3. through the use of `ionoscloudsdk.ionoscloud.*_info` modules (which can be thought of as something of an abstraction of Method 2, wrapped into an Ansible module).




## Before you begin
This example also introduces a few new modules, techniques and 'code snippets' that you might find interesting, including:

1. how the output of 'external' command-line tools can be used within Ansible with help of the `ansible.builtin.shell` module;
2. how the `ansible.builtin.uri` module can be used to 'import' data from arbitrary APIs, and more concretely, from our [Cloud API](https://api.ionos.com/docs/cloud/v6/)
3. how the `community.general.json_query` filter can be used to filter JSON documents and create new objects which can then be used by subsequent tasks; and
4. how the `ionoscloudsdk.ionoscloud.*_info` family of modules can be used to obtain 'read-only' information in a more consistent way (and in a way that resembles [Terraform's Data Sources](https://developer.hashicorp.com/terraform/language/data-sources), for those who are already familiar with Terraform).



### What's in this example?
This example includes and/or depends on the following files:

| File            | Description                                                                                            |
| ---             | ---                                                                                                    |
| `part-1.yml`    | This playbook provisions a single server and an internal LAN (that is not yet connected to any VM) within a new VDC; it is used to create the 'pre-existing resources' that will be used in the subsequent playbooks    |
| `part-2.yml`    | This playbook shows the three different ways to work with existing resources that are mentioned above; it retrieves information about the VDC, LANs and servers created in Part 1, and uses some of this information to add a second NIC to the server    |
| `part-3.yml`    | This playbook cleans up all of the resources provisioned in Parts 1 and 2, and should be run once you're done with the earlier parts    |
| `vars.yml`      | This file contains the variable definitions common to `part-1.yml`, `part-2.yml` and `part-3.yml`    |
| `../vars.yml`   | This file is common to all of our Ansible examples and contains a set of more generally-used variable definitions     |




## Usage
1. To provision our 'starting' infrastructure, run the following command:
   ```
   ansible-playbook part-1.yml
   ```
2. To execute the 'meat' of this example, run the following command (possilby after enabling `verbose_debugging` — see below):
   ```
   ansible-playbook part-2.yml
   ```
3. Examine the outputs of the previous step; if you'd like to make changes to `part-2.yml`, you can delete the resources that were provisioned in Step 2, and re-run said playbook
4. Execute the following to delete the resources provisioned in the previous steps:
   ```
   ansible-playbook part-3.yml
   ```

To see additional 'debugging' information — in particular, the results of the API call, and the raw and filtered output of the `ionoscloudsdk.ionoscloud.server_info` module — you can set `verbose_debugging` to `true` in `../vars.yml`



### Troubleshooting tips
- As `part-2.yml` depends on having a working installation of `ionosctl`, if the `Retrieve information about '{{ datacenter_name }}' via ionosctl` task fails, you might want to make sure the following command returns the expected information: `ionosctl datacenter list`. (If it doesn't, please refer to [docs.ionos.com/cli-ionosctl](https://docs.ionos.com/cli-ionosctl).)
- If calls to the `ansible.builtin.uri` module throw authentication errors despite, e.g., having a valid `IONOS_TOKEN` environment variable, you might want to remove any entries for the 'machine' `api.ionos.com` from your `~/.netrc` file (as the `uri` module will try to use the authentication information contained there over our explicit use of the `Authorization` header variable).
   - If you still experience problems with the `uri` module, the output of the following 'direct API' call might be helpful:
     ```
     curl -X GET "https://api.ionos.com/cloudapi/v6/datacenters/?pretty=true&depth=0" \
       -H "accept: application/json" \
       -H "Authorization: Bearer ${IONOS_TOKEN}"
     ```




## Summary
In this tutorial, we saw three different ways in which we can work with previously-provisioned resources:

1. using the `ansible.builtin.shell` module and the output of an 'external' command-line tool;
2. using the `ansible.builtin.uri` module together with the `community.general.json_query` filter; and
3. using the `ionoscloudsdk.ionoscloud.*_info` family of 'data source' modules




## Source files
The source files for this tutorial can be downloaded from its [Github repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs), or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git`, and changing into the `module-ansible/docs/tutorials/04__working_with_existing_resources` sub-directory.
