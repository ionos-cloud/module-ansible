
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
CONTAINTER_REGISTRY_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-containerregistry-v1.ga.yml',
    'filename': 'container_registry_swagger.yml',
}
MONGODB_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-mongodb-v1.ga.yml',
    'filename': 'mongodb_swagger.yml',
}
DATAPLATFORM_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-dataplatform-v1.ea.yml',
    'filename': 'dataplatform_swagger.yml',
}
CERTIFICATE_MANAGER_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-certificatemanager-v1.ga.json',
    'filename': 'certificatemanager_swagger.json',
}
LOGGING_SWAGGER = {
    'url': 'https://ionos-cloud.github.io/rest-api/docs/public-logging-v1.ea.yml',
    'filename': 'logging_swagger.json',
}

OPTIONS_TO_IGNORE = [
    'allow_replace',
    'api_url',
    'certificate_fingerprint',
    'username',
    'password',
    'token',
    'wait',
    'wait_timeout',
    'state',
]


Path(SWAGGER_CACHE).mkdir(parents=True, exist_ok=True)


def to_camel_case(snake_str):
    aux = ''.join(x.capitalize() for x in snake_str.lower().split('_'))
    return aux[0].lower() + aux[1:]


def check_download_swagger(swagger):
    filename = os.path.join(SWAGGER_CACHE, swagger['filename'])
    if os.path.isfile(filename):
        return

    bashCommand = 'wget -q -O {destination_file} {url}'.format(
        destination_file=filename, url=swagger['url'],
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    _, error = process.communicate()

    if error:
        print(error)


def extract_endpoint_info(filename, resource_endpoint, verb):
    bashCommand = 'ruby {parser} {filename} {resource_endpoint} {verb}'.format(
        parser=SWAGGER_PARSER,
        filename=os.path.join(SWAGGER_CACHE, filename),
        resource_endpoint=resource_endpoint,
        verb=verb,
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
        if type(old_line) == str:
            module_content = module_content.replace(
                old_line.replace('\n', ' ').replace('\'', '\\\'').strip(),
                new_line.replace('\n', ' ').replace('\'', '\\\'').strip(),
                1,
            )
        else:
            module_content = module_content.replace(str(old_line), str(new_line), 1)

    with open(os.path.join(MODULES_DIR, module_name + '.py'), 'w') as f:
        f.write(module_content)


def get_info_from_swagger(endpoint_info_dict, option):
    if '.' not in option:
        return endpoint_info_dict.get(option)

    endpoint_info_dict_for_option = endpoint_info_dict
    option_path = option.split('.')
    for path_part in option_path[:-1]:
        endpoint_info_dict_for_option = endpoint_info_dict[path_part]['properties']

    return endpoint_info_dict_for_option.get(option_path[-1])


def update_descriptions(module_name, swagger, resource_endpoint, verb, aliases):
    module = importlib.import_module('plugins.modules.' + module_name)

    check_download_swagger(swagger)
    endpoint_info = json.loads(extract_endpoint_info(swagger['filename'], resource_endpoint, verb))
    to_change = []
    for option_name, option_details in module.OPTIONS.items():
        if option_name in OPTIONS_TO_IGNORE:
            continue
        swagger_option = get_info_from_swagger(endpoint_info, aliases.get(option_name, to_camel_case(option_name)))
        if swagger_option:
            swagger_description = swagger_option.get('description')
            swagger_enum = swagger_option.get('enum')
            option_enum = option_details.get('choices')
            if swagger_enum and option_enum and swagger_enum != option_enum:
                print('Enum changes detected for {}'.format(option_name))
                to_change.append((option_enum, swagger_enum))
            if swagger_description and swagger_description.replace('\n', ' ').strip() != option_details['description'][0]:
                print('Description changes detected for {}'.format(option_name))
                to_change.append((option_details['description'][0], swagger_description))
    
    if len(to_change) > 0:
        print('Updating descriptions/enums in {}...\n'.format(module_name))
        update_module(module_name, to_change)


modules_to_generate = [
    ['application_load_balancer_flowlog', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/applicationloadbalancers/{applicationLoadBalancerId}/flowlogs', 'post', {}],
    ['application_load_balancer_forwardingrule', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/applicationloadbalancers/{applicationLoadBalancerId}/forwardingrules', 'post', {}],
    ['application_load_balancer', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/applicationloadbalancers', 'post', {}],
    [
        'backupunit', CLOUDAPI_SWAGGER, '/backupunits', 'post', {
            'backupunit_password': 'password',
            'backupunit_email': 'email',
        },
    ],
    ['cube_server', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/servers', 'post', {}],
    ['datacenter', CLOUDAPI_SWAGGER, '/datacenters', 'post', {}],
    [
        'firewall_rule', CLOUDAPI_SWAGGER,
        '/datacenters/{datacenterId}/servers/{serverId}/nics/{nicId}/firewallrules', 'post', {},
    ],
    ['group', CLOUDAPI_SWAGGER, '/um/groups', 'post', {}],
    ['image', CLOUDAPI_SWAGGER, '/images/{imageId}', 'put', {}],
    ['ipblock', CLOUDAPI_SWAGGER, '/ipblocks', 'post', {}],
    ['k8s_cluster', CLOUDAPI_SWAGGER, '/k8s', 'post', {'s3_buckets_param': 's3Buckets'}],
    ['k8s_nodepool', CLOUDAPI_SWAGGER, '/k8s/{k8sClusterId}/nodepools', 'post', {'datacenter': 'datacenterId'}],
    ['lan', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/lans', 'post', {}],
    ['nat_gateway_flowlog', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/natgateways/{natGatewayId}/flowlogs', 'post', {}],
    ['nat_gateway_rule', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/natgateways/{natGatewayId}/rules', 'post', {}],
    ['nat_gateway', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/natgateways', 'post', {}],
    ['network_load_balancer_flowlog', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/networkloadbalancers/{networkLoadBalancerId}/flowlogs', 'post', {}],
    ['network_load_balancer_rule', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/networkloadbalancers/{networkLoadBalancerId}/forwardingrules', 'post', {}],
    ['network_load_balancer', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/networkloadbalancers', 'post', {}],
    ['nic_flowlog', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/servers/{serverId}/nics/{nicId}/flowlogs', 'post', {}],
    ['nic', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/servers/{serverId}/nics', 'post', {}],
    ['pcc', CLOUDAPI_SWAGGER, '/pccs', 'post', {}],
    ['s3key', CLOUDAPI_SWAGGER, '/um/users/{userId}/s3keys/{keyId}', 'put', {}],
    ['server', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/servers', 'post', {}],
    ['share', CLOUDAPI_SWAGGER, '/um/groups/{groupId}/shares/{resourceId}', 'post', {}],
    ['snapshot', CLOUDAPI_SWAGGER, '/snapshots/{snapshotId}', 'put', {}],
    ['target_group', CLOUDAPI_SWAGGER, '/targetgroups', 'post', {}],
    ['user', CLOUDAPI_SWAGGER, '/um/users', 'post', {}],
    ['volume', CLOUDAPI_SWAGGER, '/datacenters/{datacenterId}/volumes', 'post', {'backupunit': 'backupunitId'}],
    [
        'postgres_cluster', POSTGRES_SWAGGER, '/clusters', 'post',
        {
            'db_username': 'credentials.username', 'db_password': 'credentials.password'
        },
    ],
    # ['registry', CONTAINTER_REGISTRY_SWAGGER, '/registries', 'post', {}],
    # ['registry_token', CONTAINTER_REGISTRY_SWAGGER, '/registries/{registryId}/tokens', 'post', {}],
    [
        'mongo_cluster', MONGODB_SWAGGER, '/clusters', 'post',
        {
            'mongo_db_version': 'mongoDBVersion',
            'template_id': 'templateID',
        },
    ],
    [
        'mongo_cluster_user', MONGODB_SWAGGER, '/clusters/{clusterId}/users', 'post',
        {
            'mongo_username': 'username',
            'mongo_password': 'password',
            'user_roles': 'roles',
        },
    ],
    [
        'dataplatform_cluster', DATAPLATFORM_SWAGGER, '/clusters', 'post',
        {
            'dataplatform_version': 'dataPlatformVersion',
            'datacenter': 'datacenterId',
        },
    ],
    ['dataplatform_nodepool', DATAPLATFORM_SWAGGER, '/clusters/{clusterId}/nodepools', 'post', {}],
    # ['certificate', CERTIFICATE_MANAGER_SWAGGER, '/certificatemanager/certificates', 'post', {}],
    ['pipeline', LOGGING_SWAGGER, '/pipelines', 'post', {}],
]

for module in modules_to_generate:
    update_descriptions(*module)
