import copy
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
    from ionoscloud_dbaas_postgres import __version__ as sdk_version
except ImportError:
    HAS_SDK = False


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
DBAAS_POSTGRES_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['info']
OBJECT_NAME = 'Postgres Cluster Backups'

OPTIONS = {
    'postgres_cluster': {
        'description': ['The ID or name of an existing Postgres Cluster.'],
        'available': STATES,
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'required': STATES,
        'available': STATES,
        'env_fallback': 'IONOS_USERNAME',
        'type': 'str',
    },
    'password': {
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'required': STATES,
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
}

def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

DOCUMENTATION = '''
---
module: datacenter
short_description: Create or destroy a Ionos Cloud Virtual Datacenter.
description:
     - This is a simple module that supports listing existing Postgres Clusters
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud-dbaas-postgres >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLES = '''
    - name: List Postgres Cluster Backups
        postgres_cluster_info:
            postgres_cluster: {{ postgres_cluster.id }}
        register: postgres_clusters_response

    - name: Show Postgres Cluster Backups
        debug:
            var: postgres_clusters_response.result
'''


def _get_dbaas_cluser(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the display name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.display_name, resource.id):
            return resource.id

    return None


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
      arguments[option_name] = {
        'type': option['type'],
      }
      for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
        if option.get(key) is not None:
          arguments[option_name][key] = option.get(key)

      if option.get('env_fallback'):
        arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

      if len(option.get('required', [])) == len(STATES):
        arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, object_name):
    for option_name, option in OPTIONS.items():
        if 'info' in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for retrieving {object_name}'.format(
                    option_name=option_name,
                    object_name=object_name,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud_dbaas_postgres`')

    dbaas_postgres_api_client = ionoscloud_dbaas_postgres.ApiClient(get_sdk_config(module, ionoscloud_dbaas_postgres))
    dbaas_postgres_api_client.user_agent = DBAAS_POSTGRES_USER_AGENT

    check_required_arguments(module, OBJECT_NAME)

    try:
        results = []
        backups = []
        postgres_cluster = module.params.get('postgres_cluster')

        if postgres_cluster:
            postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_postgres_api_client)
            postgres_cluster_id = _get_dbaas_cluser(postgres_cluster_server.clusters_get(), postgres_cluster)

            backups = ionoscloud_dbaas_postgres.BackupsApi(dbaas_postgres_api_client).cluster_backups_get(postgres_cluster_id).items
        else:
            backups = ionoscloud_dbaas_postgres.BackupsApi(dbaas_postgres_api_client).clusters_backups_get().items

        for cluster in backups:
            results.append(cluster.to_dict())

        module.exit_json(result=results)
    except Exception as e:
        module.fail_json(msg='failed to retrieve {object_name}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e)))

if __name__ == '__main__':
    main()
