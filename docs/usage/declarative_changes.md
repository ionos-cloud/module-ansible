# Declarative Tasks Update (Version 7.0.0) - List of Major Changes

## Object Identification

With the introduction of the declarative tasks update (Version 7.0.0), module parameters have been revised to allow identification of objects using a single parameter that can accept either the name or the ID of the object. This replaces the need for multiple parameters previously used for object identification.

Example: Instead of using separate `id` and `name` parameters to identify a `datacenter`, a new parameter (`datacenter`) is now used, which accepts either the ID or the name of the datacenter.

This change applies to various other parameters used for identification, not limited to the resource created by the module.

Example: For `nic` identification, apart from the `nic` parameter, other resources like `datacenter`, `server`, and `lan` will be utilized.

> **_NOTE:_** For this mechanism to function properly, ansible now assumes unique names for objects. If multiple objects with the same names are found, the operation will fail.

## State Behavior for Modules

The update introduces changes in how states will work for the modules:

```yaml
    present:
        Looks for the object:
            - If it does not exist, create it.
            - If it already exists, it will function in the same way as the update state.

    update:
        - Updates the object if no unchangeable properties are modified.
        - Replaces the object if unchangeable properties are modified, creating a new object and removing the old one.
        - If `allow_replace` is set to false, the module will fail instead of replacing the object to avoid resource loss.

    absent:
        - Looks for the object:
            - If it does not exist, the operation is successful.
            - If it exists, delete it.
```

### The allow_replace parameter

Defaults to `false`

- If set to `true`, the replace behavior is allowed.
- If set to `false`, when a resource would be replaced, an error will be thrown instead.

## List of Parameters Triggering Resource Replacement

The following parameters, when changed or set, trigger resource replacement:

| Module                | Replace if Changed                                                                                 | Replace if Set   |
|:----------------------|:---------------------------------------------------------------------------------------------------|:-----------------|
| backupunit            | name                                                                                               | -                |
| certificate           | certificate_file, certificate_chain_file                                                           | private_key_file |
| cube_server           | template_uuid, availability_zone                                                                   | -                |
| datacenter            | location                                                                                           | -                |
| dataplatform_cluster  | datacenter                                                                                         | -                |
| dataplatform_nodepool | name, cpu_family, cores_count, ram_size, availability_zone, storage_type, storage_size             | -                |
| ipblock               | size, location                                                                                     | -                |
| k8s_nodepool          | name, cpu_family, cores_count, ram_size, availability_zone, storage_type, storage_size, datacenter | -                |
| mongo_cluster         | mongo_db_version, location                                                                         | -                |
| postgres_cluster      | connections, backup_location, location, synchronization_mode, storage_type                         | -                |
| registry_token        | name                                                                                               | -                |
| registry              | name, location                                                                                     | -                |
| volume                | image, size, disk_type, availability_zone, licence_type, user_data                                 | backupunit, image_password, ssh_keys                |

> **_NOTE:_** The following parameters used to have default values which have been removed to avoid triggering a replacement without a value being set by the user (the former default value is in paranthesis) :
- cube_server:
    - availability_zone ('AUTO')
- datacenter:
    - location ('us/las')
- ipblock:
    - size (1)
- volume: 
    - size (10)
    - ssh_keys ([])
    - disk_type ('HDD')
    - licence_type ('UNKNOWN')

## List of Parameter Changes

The update involves changes in parameter names, removal of parameters, and addition of new parameters for various modules. Here is the detailed list:

**application_load_balancer:**
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer

**application_load_balancer_flowlog:**
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer
- flowlog_id -> flowlog

**application_load_balancer_forwardingrule:**
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer
- forwarding_rule_id -> forwarding_rule

**backupunit:**
- backupunit_id -> backupunit

**certificate:**
- certificate_id -> certificate

**datacenter:**
- removed id
- added datacenter

**dataplatform_cluster:**
- datacenter_id -> datacenter

**firewall_rule:**
- added firewall_rule

**group:**
- added group

**ipblock:**
- added ipblock

**k8s_cluster:**
- k8s_cluster_id -> k8s_cluster

**k8s_nodepool:**
- removed nodepool_id
- added k8s_nodepool
- k8s_cluster_id -> k8s_cluster
- datacenter_id -> datacenter
- lan_ids -> lans
- nodepool_name -> name

**lan:**
- added lan
- pcc_id -> pcc

**mongo_cluster_user:**
- mongo_cluster_id -> mongo_cluster

**nat_gateway:**
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter

**nat_gateway_flowlog:**
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter
- flowlog_id -> flowlog

**nat_gateway_rule:**
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter
- nat_gateway_rule_id -> nat_gateway_rule

**network_load_balancer:**
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter

**network_load_balancer_flowlog:**
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter
- flowlog_id -> flowlog

**network_load_balancer_flowlog:**
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter
- forwarding_rule_id -> forwarding_rule

**nic:**
- removed id
- added nic

**nic_flowlog:**
- datacenter_id -> datacenter
- server_id -> server
- nic_id -> nic
- flowlog_id -> flowlog

**pcc:**
- pcc_id -> pcc

**registry:**
- registry_id -> registry

**registry_token:**
- removed token_id
- added registry_token
- registry_id -> registry

**registry_token_info:**
- registry_id -> registry

**s3_key:**
- user_id -> user

**s3_key_info:**
- user_id -> user

**server:**
- remove template_uuid and type, use cube_server

**snapshot:**
- added snapshot

**target_group:**
- target_group_id -> target_group

**user:**
- removed s3_canonical_user_id
- added user

**volume:**
- backupunit_id -> backupunit
