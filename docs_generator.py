from yaml import loader
from plugins.modules.datacenter import OPTIONS, DOCUMENTATION, EXAMPLES, STATES

import yaml
import chevron
import copy


def f(val):
  val['required'] = len(val.get('required', [])) == len(STATES)
  del val['available']
  return val

# print(yaml.dump(yaml.safe_load(str({k: f(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False))

parameters = []

for state in STATES:
  def available_in_state(option):
    return state in option[1]['available']
  state_parameters = []
  for el in list(filter(available_in_state, copy.deepcopy(OPTIONS).items())):
    el[1]['name'] = el[0]
    el[1]['description'] = ''.join(el[1]['description'])
    state_parameters.append(el[1])
  parameters.append({
    'state': state,
    'parameters': state_parameters,
  })

with open('docs/templates/module.mustache', 'r') as f:
    print(chevron.render(f, {'example': EXAMPLES, 'states': parameters}))