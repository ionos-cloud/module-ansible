from plugins.modules.datacenter import OPTIONS, DOCUMENTATION, EXAMPLES, STATES, DOC_DIRECTORY, EXAMPLE_PER_STATE

import yaml
import chevron
import copy
import os
from pathlib import Path

def f(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

# print(yaml.dump(yaml.safe_load(str({k: f(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False))
print(EXAMPLES)
parameters = []

description = ''.join(yaml.safe_load(DOCUMENTATION)['description'])

for state in STATES:
    def available_in_state(option):
        return state in option[1]['available']
    state_parameters = []
    for el in list(filter(available_in_state, copy.deepcopy(OPTIONS).items())):
        el[1]['name'] = el[0]
        el[1]['description'] = ''.join(el[1]['description'])
        el[1]['required'] = state in el[1].get('required', [])
        state_parameters.append(el[1])
    parameters.append({
        'state': state,
        'parameters': state_parameters,
        'example': EXAMPLE_PER_STATE.get(state),
    })

with open(os.path.join('docs', os.path.join('templates', 'module.mustache')), 'r') as template_file:
    target_filename = os.path.join('docs', os.path.join('api', DOC_DIRECTORY))
    Path(target_filename).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(target_filename, 'datacenter.md'), 'w') as target_file:
        target_file.write(chevron.render(
            template_file,
            {
                'description': description,
                'example': EXAMPLES,
                'states': parameters,
            },
        ))
