import importlib
import yaml
import chevron
import copy
import os
from pathlib import Path


def generate_module_docs(module_name):
    module = importlib.import_module('plugins.modules.' + module_name)

    parameters = []

    for state in module.STATES:
        def available_in_state(option):
            return state in option[1]['available']
        state_parameters = []
        for el in list(filter(available_in_state, copy.deepcopy(module.OPTIONS).items())):
            el[1]['name'] = el[0]
            el[1]['description'] = ''.join(el[1]['description'])
            el[1]['required'] = state in el[1].get('required', [])
            state_parameters.append(el[1])
        parameters.append({
            'state': state,
            'parameters': state_parameters,
            'example': module.EXAMPLE_PER_STATE.get(state),
        })

    with open(os.path.join('docs', os.path.join('templates', 'module.mustache')), 'r') as template_file:
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
                    'states': parameters,
                },
            ))
            print('Generated docs for <{}> in {}'.format(module_name, target_filename))
    return module.DOC_DIRECTORY, target_filename

modules_to_generate = [
  'datacenter',
  'backupunit',
  'server',
]

for module_name in modules_to_generate:
  generate_module_docs(module_name)

