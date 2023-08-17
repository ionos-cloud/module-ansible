# List of changes that were introduced with the declarative tasks update (7.0.0)

## object identification
Module parameters have been changed to receive either the name or the id so instead of using multiple parameters for object identification we now use a single parameter specifying the type of the object

Example: for `datacenter`, instead of using `id` and `name` to identify the datacenter we now use a new parameter (`datacenter`) which can receive either of them

This change happens for many other parameters used for identification, not only for the resource created by the module

Example: for `nic` apart from the `nic` parameter used to identify the nic, `datacenter`, `server` and `lan` will the used to identify the other resources

> **_NOTE:_** In order for this to work, ansible now asumes unique names for objects, will fail when multiple objects with the same names are found

## the way states will work for the modules

```yaml
    present:
        looks for the object:
            does not exist -> create
            exists -> update

    update:
        updates the object if no unchangeable properties are modified
        replaces if they are -> create new object, removes the old one
        `do_not_replace` can be set to true so the module will fail if this happens to avoid losing resources

    absent:
        looks for the object:
            does not exist -> OK
            exists -> delete
```

### the do_not_replace parameter

Defaults to `false`


if `false` will allow the replace behavior to occur

if `true` and a resource would be replaced it will throw an error instead

## list of parameters that when changed or set trigger resource replacement

| module | replace if changed | replace if set |
| :--- | :--- | :--- |
| backupunit | name | - |
| certificate | certificate_file, certificate_chain_file | private_key_file |
| cube_server | template_uuid, availability_zone | - |
| datacenter | location | - |
| dataplatform_cluster | datacenter | - |
| dataplatform_nodepool | name, cpu_family, cores_count, ram_size, availability_zone, storage_type, storage_size | - |
| ipblock | size, location | - |
| k8s_nodepool | name, cpu_family, cores_count, ram_size, availability_zone, storage_type, storage_size, datacenter | - |
| mongo_cluster | mongo_db_version, location | - |
| postgres_cluster | connections, backup_location, location, synchronization_mode, storage_type | - |
| registry_token | name | - |
| registry | name, location | - |
| volume | backupunit, size, disk_type, availability_zone, licence_type, user_data | - |



## list of parameters that were renamed, removed or added

application_load_balancer:
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer

application_load_balancer_flowlog
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer
- flowlog_id -> flowlog

application_load_balancer_forwardingrule
- datacenter_id -> datacenter
- application_load_balancer_id -> application_load_balancer
- forwarding_rule_id -> forwarding_rule

backupunit
- backupunit_id -> backupunit

certificate
- certificate_id -> certificate

datacenter
- removed id
- added datacenter

dataplatform_cluster
- datacenter_id -> datacenter

firewall_rule
- added firewall_rule

group
- added group

ipblock
- added ipblock

k8s_cluster
- k8s_cluster_id -> k8s_cluster

k8s_nodepool
- removed nodepool_id
- added k8s_nodepool
- k8s_cluster_id -> k8s_cluster
- datacenter_id -> datacenter
- lan_ids -> lans
- nodepool_name -> name

lan
- added lan
- pcc_id -> pcc

mongo_cluster_user
- mongo_cluster_id -> mongo_cluster

nat_gateway
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter

nat_gateway_flowlog
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter
- flowlog_id -> flowlog

nat_gateway_rule
- nat_gateway_id -> nat_gateway
- datacenter_id -> datacenter
- nat_gateway_rule_id -> nat_gateway_rule

network_load_balancer
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter

network_load_balancer_flowlog
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter
- flowlog_id -> flowlog

network_load_balancer_flowlog
- network_load_balancer_id -> network_load_balancer
- datacenter_id -> datacenter
- forwarding_rule_id -> forwarding_rule

nic
- removed id
- added nic

nic_flowlog
- datacenter_id -> datacenter
- server_id -> server
- nic_id -> nic
- flowlog_id -> flowlog

pcc
- pcc_id -> pcc

registry
- registry_id -> registry

registry_token
- removed token_id
- added registry_token
- registry_id -> registry

registry_token_info
- registry_id -> registry

s3_key
- user_id -> user

s3_key_info
- user_id -> user

server
- remove template_uuid and type, use cube_server

snapshot
- added snapshot

target_group
- target_group_id -> target_group

user
- removed s3_canonical_user_id
- added user

volume
- backupunit_id -> backupunit
