import chevron
import importlib
import os
import copy
from pathlib import Path


TEMPLATE_PATH = os.path.join('generate_tests', 'templates')
STATE_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'state_templates')

COMMON_OPTIONS = [
    'do_not_replace',
    'api_url',
    'certificate_fingerprint',
    'username',
    'password',
    'token',
    'wait',
    'wait_timeout',
    'state',
]

def generate_module_tests(module_name):
    module = importlib.import_module('plugins.modules.' + module_name)

    test_parameters = {}

    for state in module.STATES:
        parameters = []

        for el in copy.deepcopy(module.OPTIONS).items():
            if el[0] not in COMMON_OPTIONS and state in el[1].get('available', []):
                parameters.append(el[0])
        
        template_name = 'default_{}_state_template.mustache'.format(state)
        with open(os.path.join(STATE_TEMPLATE_PATH, template_name), 'r') as template_file:
            test_parameters[state] = chevron.render(
                template_file,
                {
                    'module_name': module_name,
                    'parameters': parameters,
                    'double_curl_open': '{{',
                    'double_curl_close': '}}',
                },
            )

    with open(os.path.join(TEMPLATE_PATH, 'base_test_template.mustache'), 'r') as test_template_file:
        with open('test.yml', 'w') as f:
            f.write(chevron.render(test_template_file, test_parameters))


modules_to_generate_tests = [
    "lan"
]

for module_name in modules_to_generate_tests:
    generate_module_tests(module_name)