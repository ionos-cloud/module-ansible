import chevron
import copy
import importlib
import os
import yaml
from pathlib import Path


def generate_doc_file(module, module_name, states_parameters, template_file):
        with open(os.path.join('docs', os.path.join('templates', template_file)), 'r') as template_file:
            target_directory = os.path.join('docs', os.path.join('api', module.DOC_DIRECTORY))
            Path(target_directory).mkdir(parents=True, exist_ok=True)
            target_filename = os.path.join(target_directory, module_name + '.md')

            with open(target_filename, 'w') as target_file:
                target_file.write(chevron.render(
                    template_file,
                    {
                        'module_name': module_name,
                        'description': ''.join(yaml.safe_load(module.DOCUMENTATION)['description']),
                        'example': module.EXAMPLES,
                        'states_parameters': states_parameters,
                    },
                ))
                print('Generated docs for <{}> in {}'.format(module_name, target_filename))
        return target_filename


def generate_module_docs(module_name):
    module = importlib.import_module('plugins.modules.' + module_name)

    if module_name.endswith('_info'):
        def available_in_state(option):
            return state in option[1]['available']
        state_parameters = []
        for el in list(module.OPTIONS.items()):
            el[1]['name'] = el[0]
            el[1]['description'] = ''.join(el[1]['description'])
            el[1]['required'] = el[1].get('required', []) is not []
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
                state_parameters.append(el[1])
            parameters_per_state.append({
                'state': state,
                'parameters': state_parameters,
                'example': module.EXAMPLE_PER_STATE.get(state),
            })
        target_filename = generate_doc_file(module, module_name, parameters_per_state, 'module.mustache')
    return module.DOC_DIRECTORY, target_filename

modules_to_generate = [
    # 'cube_template', commented it before we change it to a regular info module
    'datacenter',
    'firewall_rule',
    'image',
    'ipblock',
    'lan',
    'nic_flowlog',
    'nic',
    'pcc',
    'server',
    'snapshot',
    'volume',
    'postgres_cluster',
    'postgres_backup_info',
    'postgres_cluster_info',
    'backupunit',
    'k8s_cluster',
    'k8s_config',
    'k8s_nodepool',
    'nat_gateway_flowlog',
    'nat_gateway_rule',
    'nat_gateway',
    'network_load_balancer_flowlog',
    'network_load_balancer_rule',
    'network_load_balancer',
]

for module_name in modules_to_generate:
    generate_module_docs(module_name)

