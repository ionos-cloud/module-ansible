import importlib
import os
import yaml

from plugins.module_utils.common_ionos_options import transform_options_for_ducumentation


MODULES_DIR = os.path.join('plugins', 'modules')


def update_descriptions(module_name):
    # Fixing module info imports
    with open(os.path.join(MODULES_DIR, module_name) + '.py', 'r') as module_file_read:
        initial_module = module_file_read.read()
    with open(os.path.join(MODULES_DIR, module_name) + '.py', 'w') as plugin_file_write:
        plugin_file_write.write(initial_module.replace('ansible_collections.ionoscloudsdk.ionoscloud.plugins', '.'))

    try:
        module = importlib.import_module('plugins.modules.' + module_name)
    finally:
        # Revert module changess
        with open(os.path.join(MODULES_DIR, module_name) + '.py', 'w') as plugin_file_write:
            plugin_file_write.write(initial_module)
    
    # print(transform_options_for_ducumentation(module.OPTIONS, module.STATES))

    existing_examples = module.EXAMPLES
    try:
        new_examples = '\n'.join(module.EXAMPLE_PER_STATE.values()).strip(' ')
    except AttributeError:
        new_examples = existing_examples

    existing_doc = yaml.safe_load(module.DOCUMENTATION)['options']
    if isinstance(existing_doc, dict):
        existing_doc = transform_options_for_ducumentation(yaml.safe_load(module.DOCUMENTATION)['options'], module.STATES)
    new_doc = transform_options_for_ducumentation(module.OPTIONS, module.STATES)

    if (
        existing_doc != new_doc
        or existing_examples != new_examples
    ):
        print('Updating Galaxy DOCUMENTATION for {}'.format(module_name))
        with open(os.path.join(MODULES_DIR, module_name + '.py'), 'r') as f:
            module_content = f.read()
        with open(os.path.join(MODULES_DIR, module_name + '.py'), 'w') as f:
            f.write(module_content.replace(existing_doc, new_doc).replace(existing_examples, new_examples))
    

modules_to_generate = [
    'application_load_balancer_flowlog_info',
    'application_load_balancer_flowlog',
    'application_load_balancer_forwardingrule_info',
    'application_load_balancer_forwardingrule',
    'application_load_balancer_info',
    'application_load_balancer',
    'backupunit_info',
    'target_group_info',
    'target_group',
    'cube_server',
    'cube_template_info',
    'datacenter_info',
    'datacenter',
    'firewall_rule_info',
    'firewall_rule',
    'image_info',
    'image',
    'ipblock_info',
    'ipblock',
    'lan_info',
    'lan',
    'nic_flowlog_info',
    'nic_flowlog',
    'nic_info',
    'nic',
    'pcc_info',
    'pcc',
    'server_info',
    'server',
    'snapshot_info',
    'snapshot',
    'volume_info',
    'volume',
    'registry',
    'registry_info',
    'registry_token',
    'registry_token_info',
    'registry_repository',
    'registry_repository_info',
    'registry_artifact_info',
    'registry_vulnerability_info',
    'postgres_cluster',
    'postgres_backup_info',
    'postgres_cluster_info',
    'mongo_cluster_info',
    'mongo_cluster_template_info',
    'mongo_cluster',
    'mongo_cluster_user',
    'mongo_cluster_user_info',
    'backupunit',
    'k8s_cluster_info',
    'k8s_cluster',
    'k8s_config',
    'k8s_nodepool_info',
    'k8s_nodepool',
    'nat_gateway_flowlog_info',
    'nat_gateway_flowlog',
    'nat_gateway_rule_info',
    'nat_gateway_rule',
    'nat_gateway_info',
    'nat_gateway',
    'network_load_balancer_flowlog_info',
    'network_load_balancer_flowlog',
    'network_load_balancer_rule_info',
    'network_load_balancer_rule',
    'network_load_balancer_info',
    'network_load_balancer',
    'group_info',
    'group',
    's3key_info',
    's3key',
    'share_info',
    'share',
    'user_info',
    'user',
    'vcpu_server',
    'certificate',
    'certificate_info',
    'pipeline',
    'pipeline_info',
    'vm_autoscaling_group',
    'vm_autoscaling_group_info',
    'vm_autoscaling_action_info',
    'vm_autoscaling_server_info',
    'dns_zone',
    'dns_zone_info',
    'dns_record',
    'dns_record_info',
    'dns_secondary_zone',
    'dns_secondary_zone_info',
    'mariadb_cluster',
    'mariadb_cluster_info',
    'mariadb_backup_info',
]

for module in modules_to_generate:
    update_descriptions(module)
