## 5.0.1 (21 December, 2020)

#### Features:
- **IPFailover** now supports dynamically generated IPs
- On **server creation** it is possible to specify an IP for the server's included NIC
- Added an option to **rename network interfaces** (Update NIC operation)

#### Bug fixes:
- Fixed the return value of start/stop machine

#### Enhancements:
- Changed the return values for the tasks. [Here](README.md#return-values) you can find the more details about the new templates.

#### Misc:
- Rebranded the module from **profitbricks** to **ionos-cloud**
- Changed the python package to **ionoscloud** instead of **profitbricks**
- The **datacenter** and **nic** modules now have both _name_ and _id_ parameters, instead of just _name_


<br>

### Migration steps from [Profitbricks Module](https://github.com/ionos-enterprise/profitbricks-module-ansible) to [Ionos Cloud Module](https://github.com/ionos-cloud/sdk-ansible):
- install [ionoscloud python package](https://pypi.org/project/ionoscloud) using `pip install ionoscloud`
- set the `IONOS_USERNAME` and `IONOS_PASSWORD` environment variables (instead of `PROFITBRICKS_USERNAME` and `PROFITBRICKS_PASSWORD`)
- adapt the playbooks by:
    - using the return values decribed [here](README.md#return-values)
    - changing the module names in playbooks (using find and replace), eliminating the `profitbricks_` prefix:

        | profitbricks module           | ionos-cloud module            |
        |-------------------------------|-------------------------------|
        | profitbricks_backupunit       | backupunit                    |
        | profitbricks_datacenter       | datacenter                    |
        | profitbricks_firewall_rule    | firewall_rule                 |
        | profitbricks_group            | group                         |
        | profitbricks_ipblock          | ipblock                       |
        | profitbricks_k8s_cluster      | k8s_cluster                   |
        | profitbricks_k8s_config       | k8s_config                    |
        | profitbricks_k8s_nodepool     | k8s_nodepool                  |
        | profitbricks_lan              | lan                           |
        | profitbricks_nic              | nic                           |
        | profitbricks_pcc              | pcc                           |
        | profitbricks_s3key            | s3key                         |
        | profitbricks_share            | share                         |
        | profitbricks_snapshot         | snapshot                      |
        | profitbricks_user             | user                          |
        | profitbricks_volume           | volume                        |
        | profitbricks                  | server                        |
