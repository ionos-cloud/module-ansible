import chevron
import copy
import importlib
import os
import yaml
from pathlib import Path


EXAMPLES_DIR = os.path.join('docs', 'returned_object_examples')
TEMPLATES_DIR = os.path.join('docs', 'templates')
MODULES_DIR = os.path.join('plugins', 'modules')

DIRECTORY_TO_NAME = {
    'applicationloadbalancer': 'Application Load Balancer',
    'certificate': 'Certificate Manager',
    'dbaas-postgres': 'DBaaS Postgres',
    'dbaas-mongo': 'DBaaS Mongo',
    'natgateway': 'NAT Gateway',
    'networkloadbalancer': 'Network Load Balancer',
    'dataplatform': 'Data Platform',
}


def generate_doc_file(module, module_name, states_parameters, template_file):
    with open(os.path.join(TEMPLATES_DIR, template_file), 'r') as template_file:
        target_directory = os.path.join('docs', os.path.join('api', module.DOC_DIRECTORY))
        Path(target_directory).mkdir(parents=True, exist_ok=True)
        target_filename = os.path.join(target_directory, module_name + '.md')
        
        try:
            with open(os.path.join(EXAMPLES_DIR, '{}.json'.format(module_name)), 'r') as example_file:
                return_example = example_file.read()
        except Exception:
            return_example = None
            print('!!! No return example found for {}\n'.format(module_name))
        try:
            immutable_options = module.IMMUTABLE_OPTIONS
        except AttributeError:
            immutable_options = None

        with open(target_filename, 'w') as target_file:
            target_file.write(chevron.render(
                template_file,
                {
                    'module_name': module_name,
                    'description': '\n\n'.join(yaml.safe_load(module.DOCUMENTATION)['description']),
                    'example': module.EXAMPLES,
                    'states_parameters': states_parameters,
                    'has_immutable_parameters': immutable_options is not None,
                    'immutable_parameters': immutable_options,
                    'return_example': return_example,
                },
            ))
            print('Generated docs for <{}> in {}'.format(module_name, target_filename))
    return target_filename


def generate_module_docs(module_name):
    # Fixing module info imports
    with open(os.path.join(MODULES_DIR, module_name) + '.py', 'r') as module_file_read:
        initial_module = module_file_read.read()
    with open(os.path.join(MODULES_DIR, module_name) + '.py', 'w') as plugin_file_write:
        plugin_file_write.write(initial_module.replace('ansible_collections.ionoscloudsdk.ionoscloud.plugins', '.'))

    module = importlib.import_module('plugins.modules.' + module_name)

    # Revert module changess
    with open(os.path.join(MODULES_DIR, module_name) + '.py', 'w') as plugin_file_write:
        plugin_file_write.write(initial_module)

    if module_name.endswith('_info'):
        def available_in_state(option):
            return state in option[1]['available']
        state_parameters = []
        for el in list(module.OPTIONS.items()):
            el[1]['name'] = el[0]
            el[1]['description'] = ''.join(el[1]['description'])
            el[1]['required'] = el[1].get('required', []) != []
            el[1]['hasDefault'] = (el[1].get('default') is not None)
            el[1]['hasChoices'] = (el[1].get('choices') is not None)
            state_parameters.append(el[1])
        
        target_filename = generate_doc_file(module, module_name, state_parameters, 'info_module.mustache')
    else:
        parameters_per_state = []
        for state in module.STATES:
            def available_in_state(option):
                return state in option[1]['available']
            state_parameters = []
            for el in list(filter(available_in_state, copy.deepcopy(module.OPTIONS).items())):
                el[1]['name'] = el[0]
                el[1]['description'] = ''.join(el[1]['description'])
                el[1]['required'] = state in el[1].get('required', [])
                el[1]['hasDefault'] = (el[1].get('default') is not None)
                el[1]['hasChoices'] = (el[1].get('choices') is not None)
                state_parameters.append(el[1])
            parameters_per_state.append({
                'state': state,
                'parameters': state_parameters,
                'example': module.EXAMPLE_PER_STATE.get(state),
            })
        target_filename = generate_doc_file(module, module_name, parameters_per_state, 'module.mustache')
    return module.DOC_DIRECTORY, target_filename, module.OBJECT_NAME

modules_to_generate = [
    'application_load_balancer_flowlog_info',
    'application_load_balancer_flowlog',
    'application_load_balancer_forwardingrule_info',
    'application_load_balancer_forwardingrule',
    'application_load_balancer_info',
    'application_load_balancer',
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
    'postgres_cluster',
    'postgres_backup_info',
    'postgres_cluster_info',
    'mongo_cluster_info',
    'mongo_cluster_template_info',
    'mongo_cluster',
    'mongo_cluster_user',
    'mongo_cluster_user_info',
    'backupunit_info',
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
    'dataplatform_cluster',
    'dataplatform_cluster_config',
    'dataplatform_cluster_info',
    'dataplatform_nodepool',
    'dataplatform_nodepool_info',
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
]

generated = {}

for module_name in modules_to_generate:
    docs_dir, file_name, object_name = generate_module_docs(module_name)

    generated_module = {
        'filename': file_name[5:],
        'object_name': object_name,
    }

    directory_name = DIRECTORY_TO_NAME.get(docs_dir, docs_dir.replace('-', ' ').title())
    if file_name.endswith('_info.md'):
        if generated.get(directory_name):
            generated[directory_name]['info_modules'].append(generated_module)
        else:
            generated[directory_name] = {
                'directory_name': directory_name,
                'info_modules': [generated_module],
                'modules': [],
        }
    else:
        if generated.get(directory_name):
            generated[directory_name]['modules'].append(generated_module)
        else:
            generated[directory_name] = {
                'directory_name': directory_name,
                'info_modules': [],
                'modules': [generated_module],
        }

with open(os.path.join('docs', 'summary.md'), 'w') as target_file:
    with open(os.path.join(TEMPLATES_DIR, 'summary.mustache'), 'r') as template_file:
        target_file.write(chevron.render(
            template_file,
            {
                'generated': list(generated.values()),
            },
        ))
