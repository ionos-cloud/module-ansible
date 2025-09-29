import importlib
import os
import yaml
import chevron


MODULES_DIR = os.path.join('plugins', 'modules')


def find_examples_in_test_file(filename, module_reference, left_states, state_examples, test_vars):
    with open(filename, 'r') as f:
        test_file = yaml.load(f.read(), Loader=yaml.SafeLoader)
        for task in test_file[0]['tasks']:
            if (
                module_reference in task.keys()
                and task.get(module_reference, {}).get('state', 'present') in left_states
            ):
                state_examples[task.get(module_reference, {}).get('state', 'present')] = '\n' + chevron.render(
                    yaml.dump(task, default_flow_style=False, sort_keys=False),
                    test_vars,
                )
                left_states.remove(task.get(module_reference, {}).get('state', 'present'))


def find_info_examples_in_test_file(filename, module_reference, left_states, state_examples, test_vars):
    with open(filename, 'r') as f:
        test_file = yaml.load(f.read(), Loader=yaml.SafeLoader)
        for task in test_file[0]['tasks']:
            if module_reference in task.keys() and 'info' in left_states:
                    state_examples['info'] = '\n' + chevron.render(
                        yaml.dump(task, default_flow_style=False, sort_keys=False),
                        test_vars,
                    )
                    left_states.remove('info')


def get_examples_from_tests(module_name, module):
    tests_dir = os.path.join('tests', module.DOC_DIRECTORY)

    if module_name.endswith('_info'):
        example_extract_method = find_info_examples_in_test_file
    else:
        example_extract_method = find_examples_in_test_file

    state_examples = {}
    left_states = list(module.STATES)
    module_reference = 'ionoscloudsdk.ionoscloud.' + module_name
    files_to_check = []

    with open(os.path.join(tests_dir, 'vars.yml')) as f:
        test_vars = yaml.load(f.read(), Loader=yaml.SafeLoader)

    with open(os.path.join(tests_dir, 'all-tests.yml')) as f:
        files_to_check.extend([
            test.get('import_playbook') for test in yaml.load(f.read(), Loader=yaml.SafeLoader)
            if test.get('import_playbook') is not None
        ])

    if module_name.endswith('_info'):
        files_to_check.sort(key=lambda x:(x and module_name[:-5] in x), reverse=True)
    else:
        files_to_check.sort(key=lambda x:(x and module_name in x), reverse=True)

    try:
        for filename in files_to_check:
            if filename:
                example_extract_method(
                    os.path.join(tests_dir, filename), module_reference,
                    left_states, state_examples, test_vars,
                )
                if len(left_states) == 0:
                    return state_examples
    except Exception as e:
        print(e)
        raise KeyError
    return state_examples


def update_module(module_name, to_change):
    with open(os.path.join(MODULES_DIR, module_name + '.py'), 'r') as f:
        module_content = f.read()

    for old_line, new_line in to_change:
        module_content = module_content.replace(old_line, new_line, 1)

    with open(os.path.join(MODULES_DIR, module_name + '.py'), 'w') as f:
        f.write(module_content)


def update_examples(module_name):
    module = importlib.import_module('plugins.modules.' + module_name)
    
    state_examples = get_examples_from_tests(module_name, module)
    to_change = []

    if module_name.endswith('_info'):
        if state_examples.get('info') and state_examples.get('info') != module.EXAMPLES:
                to_change.append([module.EXAMPLES, state_examples.get('info')])
    else:
        for state in module.STATES:
            if state_examples.get(state) and state_examples.get(state) != module.EXAMPLE_PER_STATE.get(state):
                to_change.append([module.EXAMPLE_PER_STATE.get(state), state_examples.get(state)])

    if len(to_change)> 0:
        print('Updating examples in {}...\n'.format(module_name))
        update_module(module_name, to_change)


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
    # 'image_info',
    # 'image',
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
    # 'registry_vulnerability_info',
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
    'auto_certificate',
    'auto_certificate_info',
    'certificate_provider',
    'certificate_provider_info',
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
]

for module in modules_to_generate:
    update_examples(module)
