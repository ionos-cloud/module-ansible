import chevron
import importlib
import os
import copy
from pathlib import Path

TARGET_DIRECTORY = 'test_tests'
TEMPLATE_PATH = os.path.join('generate_tests', 'templates')
STATE_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'state_templates')
DEPENDENCIES_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'dependencies')
INITAL_DEPENDENCIES_TEMPLATE_PATH = os.path.join(DEPENDENCIES_TEMPLATE_PATH, 'initial')
CLEANUP_DEPENDENCIES_TEMPLATE_PATH = os.path.join(DEPENDENCIES_TEMPLATE_PATH, 'cleanup')

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

def resolve_dependencies(dependencies):
    initial_setup = ''
    cleanup = ''

    for dependecy in dependencies:
        filename = ''.join([dependecy['name'], '.yml'])
        with open(os.path.join(INITAL_DEPENDENCIES_TEMPLATE_PATH, filename), 'r') as f:
            initial_setup = '\n'.join([initial_setup, f.read()])
        with open(os.path.join(CLEANUP_DEPENDENCIES_TEMPLATE_PATH, filename), 'r') as f:
            cleanup = '\n'.join([f.read(), cleanup])
    
    return initial_setup, cleanup

def generate_module_tests(module_name, dependencies):
    module = importlib.import_module('plugins.modules.' + module_name)
    directory = os.path.join(TARGET_DIRECTORY, module.DOC_DIRECTORY)

    initial_setup, cleanup = resolve_dependencies(dependencies)

    dependencies_names = list(filter(
        lambda x: x is not None,
        [d['name'] if not d.get('parameter') else None for d in dependencies],
    ))

    test_parameters = {
        'initial_setup': initial_setup,
        'cleanup': cleanup,
    }

    for state in module.STATES:
        parameters = []

        for el in copy.deepcopy(module.OPTIONS).items():
            if (
                el[0] not in COMMON_OPTIONS 
                and el[0] != module_name
                and state in el[1].get('available', [])
            ):
                parameters.append(el[0])

        paramaters_to_check = list(filter(lambda x: x not in dependencies_names, parameters))
        
        template_name = 'default_{}_state_template.mustache'.format(state)
        with open(os.path.join(STATE_TEMPLATE_PATH, template_name), 'r') as template_file:
            test_parameters[state] = chevron.render(
                template_file,
                {
                    'module_name': module_name,
                    'dependencies': dependencies_names,
                    'parameters': parameters,
                    'paramaters_to_check': paramaters_to_check,
                    'double_curl_open': '{{',
                    'double_curl_close': '}}',
                },
            )

    with open(os.path.join(TEMPLATE_PATH, 'base_test_template.mustache'), 'r') as test_template_file:
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, 'test.yml'), 'w') as f:
            f.write(chevron.render(test_template_file, test_parameters))


modules_to_generate_tests = [
    ('lan', [{'name': 'pcc', 'parameter': True}, {'name': 'datacenter'} ]),
]

for module_name, dependencies in modules_to_generate_tests:
    generate_module_tests(module_name, dependencies)