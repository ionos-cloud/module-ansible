# Table of contents

* [Introduction](README.md)
* [Changelog](changelog.md)

## Usage

* [Authentication](usage/authentication.md)
* [Using proxies](usage/http\_proxy.md)
* [Ansible Playbooks](usage/ansibleplaybooks.md)
* [Wait for Services](usage/waitforservices.md)
* [Incrementing servers](usage/incrementingservers.md)
* [Check Mode and Diff](usage/check_mode_and_diff.md)
* [SSH Key Authentication](usage/sshkeyauthentication.md)
* [Return values](usage/returnvalues.md)
* [Testing](usage/testing.md)
* [Declarative Changes](usage/declarative_changes.md)

## Tutorials
* [Tutorials introduction](tutorials/README.md)
* [Minimal example](tutorials/01__minimal_example/README.md)
    * [cloud-init.txt.md](tutorials/01__minimal_example/.gitbook_files/cloud-init.txt.md)
    * [main.yml.md](tutorials/01__minimal_example/.gitbook_files/main.yml.md)
* [Server with multiple NICs and storage volumes](tutorials/02__server_with_multiple_nics_and_storage_volumes/README.md)
    * [main.yml.md](tutorials/02__server_with_multiple_nics_and_storage_volumes/.gitbook_files/main.yml.md)
* [Jumpbox with internal server](tutorials/03__jumpbox_with_internal_server/README.md)
    * [cloud-init.txt.md](tutorials/03__jumpbox_with_internal_server/.gitbook_files/cloud-init.txt.md)
    * [configure-internal-server.yml.md](tutorials/03__jumpbox_with_internal_server/.gitbook_files/configure-internal-server.yml.md)
    * [main.yml.md](tutorials/03__jumpbox_with_internal_server/.gitbook_files/main.yml.md)
    * [templates_ssh_config.j2.md](tutorials/03__jumpbox_with_internal_server/.gitbook_files/templates_ssh_config.j2.md)
* [Working with existing resources](tutorials/04__working_with_existing_resources/README.md)
    * [part-1.yml.md](tutorials/04__working_with_existing_resources/.gitbook_files/part-1.yml.md)
    * [part-2.yml.md](tutorials/04__working_with_existing_resources/.gitbook_files/part-2.yml.md)
    * [part-3.yml.md](tutorials/04__working_with_existing_resources/.gitbook_files/part-3.yml.md)
    * [vars.yml.md](tutorials/04__working_with_existing_resources/.gitbook_files/vars.yml.md)
* [Introducing roles](tutorials/05__introducing_roles/README.md)
    * [part-1.yml.md](tutorials/05__introducing_roles/.gitbook_files/part-1.yml.md)
    * [part-2.yml.md](tutorials/05__introducing_roles/.gitbook_files/part-2.yml.md)
    * [part-3.yml.md](tutorials/05__introducing_roles/.gitbook_files/part-3.yml.md)
    * [roles_common_base-server_meta_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_common_base-server_meta_main.yml.md)
    * [roles_common_base-server_tasks_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_common_base-server_tasks_main.yml.md)
    * [roles_common_fail2ban_meta_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_common_fail2ban_meta_main.yml.md)
    * [roles_common_fail2ban_tasks_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_common_fail2ban_tasks_main.yml.md)
    * [roles_docker-server_meta_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_docker-server_meta_main.yml.md)
    * [roles_docker-server_tasks_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_docker-server_tasks_main.yml.md)
    * [roles_docker-server_vars_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_docker-server_vars_main.yml.md)
    * [roles_nfs-client_meta_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-client_meta_main.yml.md)
    * [roles_nfs-client_tasks_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-client_tasks_main.yml.md)
    * [roles_nfs-client_vars_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-client_vars_main.yml.md)
    * [roles_nfs-server_meta_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-server_meta_main.yml.md)
    * [roles_nfs-server_tasks_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-server_tasks_main.yml.md)
    * [roles_nfs-server_vars_main.yml.md](tutorials/05__introducing_roles/.gitbook_files/roles_nfs-server_vars_main.yml.md)
    * [templates_ssh_config.j2.md](tutorials/05__introducing_roles/.gitbook_files/templates_ssh_config.j2.md)
    * [vars.yml.md](tutorials/05__introducing_roles/.gitbook_files/vars.yml.md)
* [Introducing the NAT Gateway and Network Load Balancer](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/README.md)
    * [01__create_jumpbox_and_nat_gw.yml.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/01__create_jumpbox_and_nat_gw.yml.md)
    * [02__create_app_servers_and_nlb.yml.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/02__create_app_servers_and_nlb.yml.md)
    * [03__configure_app_servers.yml.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/03__configure_app_servers.yml.md)
    * [04__clean_up.yml.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/04__clean_up.yml.md)
    * [nginx-config.patch.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/nginx-config.patch.md)
    * [templates_cloud-init--app-servers.j2.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/templates_cloud-init--app-servers.j2.md)
    * [templates_index.html.j2.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/templates_index.html.j2.md)
    * [templates_inventory.j2.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/templates_inventory.j2.md)
    * [templates_ssh_config.j2.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/templates_ssh_config.j2.md)
    * [vars.yml.md](tutorials/06__introducing_the_nat_gateway_and_network_load_balancer/.gitbook_files/vars.yml.md)
* [Introducing the Application Load Balancer](tutorials/07__introducing_the_application_load_balancer/README.md)
    * [01__create_jumpbox_and_nat_gw.yml.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/01__create_jumpbox_and_nat_gw.yml.md)
    * [02__create_app_servers_and_alb.yml.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/02__create_app_servers_and_alb.yml.md)
    * [03__configure_app_servers.yml.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/03__configure_app_servers.yml.md)
    * [04__clean_up.yml.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/04__clean_up.yml.md)
    * [templates_cloud-init--app-servers.j2.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/templates_cloud-init--app-servers.j2.md)
    * [templates_index.html.j2.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/templates_index.html.j2.md)
    * [templates_inventory.j2.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/templates_inventory.j2.md)
    * [templates_ssh_config.j2.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/templates_ssh_config.j2.md)
    * [vars.yml.md](tutorials/07__introducing_the_application_load_balancer/.gitbook_files/vars.yml.md)
* [A quick introduction to DBaaS](tutorials/09__a_quick_introduction_to_dbaas/README.md)
    * [01__create_jumpbox_and_nlb.yml.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/01__create_jumpbox_and_nlb.yml.md)
    * [02a__create_postgres_cluster.yml.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/02a__create_postgres_cluster.yml.md)
    * [02b__create_mongodb_cluster.yml.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/02b__create_mongodb_cluster.yml.md)
    * [03__clean_up.yml.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/03__clean_up.yml.md)
    * [templates_ssh_config.j2.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/templates_ssh_config.j2.md)
    * [vars.yml.md](tutorials/09__a_quick_introduction_to_dbaas/.gitbook_files/vars.yml.md)

## API
* Application Load Balancer
  * Modules
    * [Flowlog](api/applicationloadbalancer/application_load_balancer_flowlog.md)
    * [Application Load Balancer Forwarding Rule](api/applicationloadbalancer/application_load_balancer_forwardingrule.md)
    * [Application Load Balancer](api/applicationloadbalancer/application_load_balancer.md)
    * [Target Group](api/applicationloadbalancer/target_group.md)
  * Info Modules
    * [Flowlogs](api/applicationloadbalancer/application_load_balancer_flowlog_info.md)
    * [Application Load Balancer Forwarding Rules](api/applicationloadbalancer/application_load_balancer_forwardingrule_info.md)
    * [Application Load Balancers](api/applicationloadbalancer/application_load_balancer_info.md)
    * [Target Groups](api/applicationloadbalancer/target_group_info.md)
* Compute Engine
  * Modules
    * [CUBE Server](api/compute-engine/cube_server.md)
    * [Datacenter](api/compute-engine/datacenter.md)
    * [Firewall Rule](api/compute-engine/firewall_rule.md)
    * [Image](api/compute-engine/image.md)
    * [IP Block](api/compute-engine/ipblock.md)
    * [LAN](api/compute-engine/lan.md)
    * [Flowlog](api/compute-engine/nic_flowlog.md)
    * [NIC](api/compute-engine/nic.md)
    * [PCC](api/compute-engine/pcc.md)
    * [Server](api/compute-engine/server.md)
    * [Snapshot](api/compute-engine/snapshot.md)
    * [Volume](api/compute-engine/volume.md)
    * [VCPU Server](api/compute-engine/vcpu_server.md)
  * Info Modules
    * [CUBE templates](api/compute-engine/cube_template_info.md)
    * [Datacenters](api/compute-engine/datacenter_info.md)
    * [Firewall Rules](api/compute-engine/firewall_rule_info.md)
    * [Images](api/compute-engine/image_info.md)
    * [IpBlocks](api/compute-engine/ipblock_info.md)
    * [Lans](api/compute-engine/lan_info.md)
    * [Flowlogs](api/compute-engine/nic_flowlog_info.md)
    * [NICs](api/compute-engine/nic_info.md)
    * [PCCs](api/compute-engine/pcc_info.md)
    * [Servers](api/compute-engine/server_info.md)
    * [Snapshots](api/compute-engine/snapshot_info.md)
    * [Volumes](api/compute-engine/volume_info.md)
* Container Registry
  * Modules
    * [Registry](api/container-registry/registry.md)
    * [Registry Token](api/container-registry/registry_token.md)
    * [Repository](api/container-registry/registry_repository.md)
  * Info Modules
    * [Registries](api/container-registry/registry_info.md)
    * [Registry Tokens](api/container-registry/registry_token_info.md)
    * [Artifacts](api/container-registry/registry_artifact_info.md)
    * [Repositories](api/container-registry/registry_repository_info.md)
    * [Vulnerabilities](api/container-registry/registry_vulnerability_info.md)
* DBaaS Postgres
  * Modules
    * [Postgres Cluster](api/dbaas-postgres/postgres_cluster.md)
  * Info Modules
    * [Postgres Cluster Backups](api/dbaas-postgres/postgres_backup_info.md)
    * [Postgres Clusters](api/dbaas-postgres/postgres_cluster_info.md)
* DBaaS Mongo
  * Modules
    * [Mongo Cluster](api/dbaas-mongo/mongo_cluster.md)
    * [Mongo Cluster User](api/dbaas-mongo/mongo_cluster_user.md)
  * Info Modules
    * [Mongo Cluster Users](api/dbaas-mongo/mongo_cluster_info.md)
    * [Mongo Cluster Templates](api/dbaas-mongo/mongo_cluster_template_info.md)
    * [Mongo Clusters](api/dbaas-mongo/mongo_cluster_user_info.md)
* Dbaas Mariadb
  * Modules
    * [MariaDB Cluster](api/dbaas-mariadb/mariadb_cluster.md)
  * Info Modules
    * [MariaDB Clusters](api/dbaas-mariadb/mariadb_cluster_info.md)
    * [MariaDB Cluster Backups](api/dbaas-mariadb/mariadb_backup_info.md)
* Managed Backup
  * Modules
    * [Backup Unit](api/managed-backup/backupunit.md)
  * Info Modules
    * [Backupunits](api/managed-backup/backupunit_info.md)
* Managed Kubernetes
  * Modules
    * [K8s Cluster](api/managed-kubernetes/k8s_cluster.md)
    * [K8s config](api/managed-kubernetes/k8s_config.md)
    * [K8s Nodepool](api/managed-kubernetes/k8s_nodepool.md)
  * Info Modules
    * [K8s Clusters](api/managed-kubernetes/k8s_cluster_info.md)
    * [K8s Nodepools](api/managed-kubernetes/k8s_nodepool_info.md)
* NAT Gateway
  * Modules
    * [Flowlog](api/natgateway/nat_gateway_flowlog.md)
    * [NAT Gateway rule](api/natgateway/nat_gateway_rule.md)
    * [NAT Gateway](api/natgateway/nat_gateway.md)
  * Info Modules
    * [Flowlogs](api/natgateway/nat_gateway_flowlog_info.md)
    * [NAT Gateway rules](api/natgateway/nat_gateway_rule_info.md)
    * [NAT Gateways](api/natgateway/nat_gateway_info.md)
* Network Load Balancer
  * Modules
    * [Flowlog](api/networkloadbalancer/network_load_balancer_flowlog.md)
    * [Network Loadbalancer forwarding rule](api/networkloadbalancer/network_load_balancer_rule.md)
    * [Network Loadbalancer](api/networkloadbalancer/network_load_balancer.md)
  * Info Modules
    * [Network Loadbalancers Flowlogs](api/networkloadbalancer/network_load_balancer_flowlog_info.md)
    * [Network Loadbalancer forwarding rules](api/networkloadbalancer/network_load_balancer_rule_info.md)
    * [Network Loadbalancers](api/networkloadbalancer/network_load_balancer_info.md)
* User Management
  * Modules
    * [Group](api/user-management/group.md)
    * [S3 Key](api/user-management/s3key.md)
    * [Share](api/user-management/share.md)
    * [User](api/user-management/user.md)
  * Info Modules
    * [Groups](api/user-management/group_info.md)
    * [S3 Keys](api/user-management/s3key_info.md)
    * [Shares](api/user-management/share_info.md)
    * [Users](api/user-management/user_info.md)
* Data Platform
  * Modules
    * [Data Platform Cluster](api/dataplatform/dataplatform_cluster.md)
    * [DataPlatform Cluster Config](api/dataplatform/dataplatform_cluster_config.md)
    * [Data Platform Nodepool](api/dataplatform/dataplatform_nodepool.md)
  * Info Modules
    * [DataPlatform Clusters](api/dataplatform/dataplatform_cluster_info.md)
    * [DataPlatform Nodepools](api/dataplatform/dataplatform_nodepool_info.md)
* Certificate Manager
  * Modules
    * [Certificate](api/certificate/certificate.md)
  * Info Modules
    * [Certificates](api/certificate/certificate_info.md)
* Logging
  * Modules
    * [Pipeline](api/logging/pipeline.md)
  * Info Modules
    * [Pipelines](api/logging/pipeline_info.md)
* Vm Autoscaling
  * Modules
    * [VM Autoscaling Group](api/vm-autoscaling/vm_autoscaling_group.md)
  * Info Modules
    * [VM Autoscaling Groups](api/vm-autoscaling/vm_autoscaling_group_info.md)
    * [VM Autoscaling Group Actions](api/vm-autoscaling/vm_autoscaling_action_info.md)
    * [VM Autoscaling Group Servers](api/vm-autoscaling/vm_autoscaling_server_info.md)
* Dns
  * Modules
    * [Zone](api/dns/dns_zone.md)
    * [Record](api/dns/dns_record.md)
    * [Secondary Zone](api/dns/dns_secondary_zone.md)
  * Info Modules
    * [DNS Zones](api/dns/dns_zone_info.md)
    * [DNS Records](api/dns/dns_record_info.md)
    * [DNS Secondary Zones](api/dns/dns_secondary_zone_info.md)
