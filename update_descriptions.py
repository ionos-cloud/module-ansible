
import importlib
import os
import json
import subprocess
from pathlib import Path


MODULES_DIR = os.path.join('plugins', 'modules')
SWAGGER_CACHE = os.path.join('update_description_utils', 'swaggers')
SWAGGER_PARSER = os.path.join('update_description_utils', 'parse_swagger.rb')
CLOUDAPI_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-cloud-v6.ga.json',
    'filename': 'cloudapi_swagger.json',
}
POSTGRES_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-postgresql-v1.ga.yml',
    'filename': 'postgres_swagger.yml',
}
Path(SWAGGER_CACHE).mkdir(parents=True, exist_ok=True)


def check_download_swagger(swagger):
    filename = os.path.join(SWAGGER_CACHE, swagger['filename'])
    if os.path.isfile(filename):
        return

    bashCommand = "wget -q -O {destination_file} {url}".format(
        destination_file=filename, url=swagger['url'],
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    _, error = process.communicate()

    if error:
        print(error)


def extract_endpoint_info(filename, resource_endpoint):

    bashCommand = "ruby {parser} {filename} {resource_endpoint}".format(
        parser=SWAGGER_PARSER,
        filename=os.path.join(SWAGGER_CACHE, filename),
        resource_endpoint=resource_endpoint
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(error)

    return output

def update_module(module_name, to_change):
    with open(os.path.join(MODULES_DIR, module_name + '.py'), 'r') as f:
        module_content = f.read()

    for old_line, new_line in to_change:
        module_content = module_content.replace(old_line, new_line, 1)

    with open(os.path.join(MODULES_DIR, module_name + '.py'), 'w') as f:
        f.write(module_content)


def update_descriptions(module_name, swagger, resource_endpoint):
    module = importlib.import_module('plugins.modules.' + module_name)

    check_download_swagger(swagger)
    endpoint_info = json.loads(extract_endpoint_info(swagger['filename'], resource_endpoint))

    to_change = []
    for option_name, option_details in module.OPTIONS.items():
        swagger_option = endpoint_info.get(option_name)
        if swagger_option:
            swagger_description = swagger_option.get('description')
            if swagger_description != option_details['description'][0]:
                to_change.append((option_details['description'][0], swagger_description))
    
    if len(to_change) > 0:
        update_module(module_name, to_change)

modules_to_generate = [
    ['datacenter', CLOUDAPI_SWAGGER, '/datacenters']
]

for module in modules_to_generate:
    update_descriptions(*module)
