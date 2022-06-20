import copy
from operator import mod
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
DBAAS_POSTGRES_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (
    __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Postgres Cluster'

OPTIONS = {
    'maintenance_window': {
        'description': [
            'Dict containing "time" (the time of the day when to perform the maintenance) '
            'and "day_of_the_week" (the Day Of the week when to perform the maintenance).',
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'postgres_version': {
        'description': ['The PostgreSQL version of your cluster'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'instances': {
        'description': ['The total number of instances in the cluster (one master and n-1 standbys).'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'cores': {
        'description': ['The number of CPU cores per instance.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'ram': {
        'description': ['The amount of memory per instance(should be a multiple of 1024).'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_size': {
        'description': ['The amount of storage per instance.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_type': {
        'description': ['The storage type used in your cluster.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'connections': {
        'description': ['Array of VDCs to connect to your cluster.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'location': {
        'description': [
            'The physical location where the cluster will be created. This will be where all of your instances live. '
            'Property cannot be modified after datacenter creation (disallowed in update requests)'
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'display_name': {
        'description': ['The friendly name of your cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'db_username': {
        'description': [
            'The username for the initial postgres user. Some system usernames are restricted (e.g. "postgres", '
            '"admin", "standby")'
        ],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The username for the initial postgres user.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'synchronization_mode': {
        'description': ['Represents different modes of replication.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'backup_location': {
        'description': ['The S3 location where the backups will be stored. One of ["de", "eu-south-2", "eu-central-2"]'],
        'available': ['present'],
        'type': 'str',
    },
    'backup_id': {
        'description': ['The ID of the backup to be used.'],
        'available': ['present', 'restore'],
        'required': ['restore'],
        'type': 'str',
    },
    'recovery_target_time': {
        'description': ['Recovery target time.'],
        'available': ['present', 'restore'],
        'type': 'str',
    },
    'postgres_cluster': {
        'description': ['The ID or name of an existing Postgres Cluster.'],
        'available': ['update', 'absent', 'restore'],
        'required': ['update', 'absent', 'restore'],
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
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
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
module: postgres_cluster
short_description: Allows operations with Ionos Cloud Postgres Clusters.
description:
     - This is a module that supports creating, updating, restoring or destroying Postgres Clusters
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dbaas-postgres >= 1.0.1"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Postgres Cluster
    postgres_cluster:
      postgres_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      storage_type: HDD
      location: de/fra
      connections:
        - cidr: 192.168.1.106/24
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  ''',
    'update': '''- name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      postgres_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  ''',
    'absent': '''- name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None


def create_postgres_cluster(module, dbaas_client, cloudapi_client):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
    display_name = module.params.get('display_name')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_clusters = postgres_cluster_server.clusters_get()

    existing_postgres_cluster_by_name = get_resource(module, postgres_clusters, display_name, [['properties', 'display_name']])

    if (
        existing_postgres_cluster_by_name is not None
        and existing_postgres_cluster_by_name.metadata.state != 'AVAILABLE'
        and module.params.get('wait')
    ):
        dbaas_client.wait_for(
            fn_request=lambda: postgres_cluster_server.clusters_find_by_id(existing_postgres_cluster_by_name.id),
            fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
            scaleup=10000,
        )

    if existing_postgres_cluster_by_name is not None:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'postgres_cluster': existing_postgres_cluster_by_name.to_dict(),
        }

    connection = module.params.get('connections')[0]

    datacenter_id = get_resource_id(module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1), connection['datacenter'])

    if datacenter_id is None:
        module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
    
    lan_id = get_resource_id(module, ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

    if lan_id is None:
        module.fail_json('LAN {} not found.'.format(connection['lan']))

    connections = [
        ionoscloud_dbaas_postgres.Connection(datacenter_id=datacenter_id, lan_id=lan_id, cidr=connection['cidr']),
    ]

    postgres_cluster_properties = ionoscloud_dbaas_postgres.CreateClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        storage_type=module.params.get('storage_type'),
        connections=connections,
        location=module.params.get('location'),
        backup_location=module.params.get('backup_location'),
        display_name=display_name,
        maintenance_window=maintenance_window,
        credentials=ionoscloud_dbaas_postgres.DBUser(
            username=module.params.get('db_username'),
            password=module.params.get('db_password'),
        ),
        synchronization_mode=module.params.get('synchronization_mode'),
        from_backup=ionoscloud_dbaas_postgres.CreateRestoreRequest(
            backup_id=module.params.get('backup_id'),
            recovery_target_time=module.params.get('recovery_target_time'),
        ),
    )

    postgres_cluster = ionoscloud_dbaas_postgres.CreateClusterRequest(properties=postgres_cluster_properties)

    try:
        postgres_cluster = postgres_cluster_server.clusters_post(postgres_cluster)
        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster.id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'postgres_cluster': postgres_cluster.to_dict(),
        }
    except Exception as e:
        module.fail_json(msg="failed to create the Postgres cluster: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create',
        }


def delete_postgres_cluster(module, dbaas_client):
    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_cluster = get_resource(
        module,
        postgres_cluster_server.clusters_get(),
        module.params.get('postgres_cluster'),
        [['id'], ['properties', 'display_name']],
    )

    if postgres_cluster is None:
        module.exit_json(changed=False)

    try:
        if postgres_cluster.metadata.state != 'DESTROYING':
            postgres_cluster_server.clusters_delete(postgres_cluster.id)

        if module.params.get('wait'):
            try:
                dbaas_client.wait_for(
                    fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster.id),
                    fn_check=lambda _: False,
                    scaleup=10000,
                )
            except ionoscloud_dbaas_postgres.ApiException as e:
                if e.status != 404:
                    raise e

        return {
            'action': 'delete',
            'changed': True,
            'id': postgres_cluster.id,
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': postgres_cluster.id,
        }


def update_postgres_cluster(module, dbaas_client):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    display_name=module.params.get('display_name')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
    postgres_clusters = postgres_cluster_server.clusters_get()

    postgres_cluster_id = get_resource_id(
        module, postgres_clusters, module.params.get('postgres_cluster'), [['id'], ['properties', 'display_name']],
    )

    existing_pg_cluster_id_by_name = get_resource_id(module, postgres_clusters, display_name, [['properties', 'display_name']])

    if (
        postgres_cluster_id is not None and 
        existing_pg_cluster_id_by_name is not None and
        existing_pg_cluster_id_by_name != postgres_cluster_id
    ):
        module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, display_name))

    postgres_cluster_properties = ionoscloud_dbaas_postgres.PatchClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        display_name=display_name,
        maintenance_window=maintenance_window,
    )
    postgres_cluster = ionoscloud_dbaas_postgres.PatchClusterRequest(properties=postgres_cluster_properties)

    try:
        postgres_cluster = postgres_cluster_server.clusters_patch(
            cluster_id=postgres_cluster_id,
            patch_cluster_request=postgres_cluster,
        )

        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'postgres_cluster': postgres_cluster.to_dict(),
        }

    except Exception as e:
        module.fail_json(msg="failed to update the Postgres Cluster: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
        }


def restore_postgres_cluster(module, dbaas_client):
    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_cluster_id = get_resource_id(
        module,
        postgres_cluster_server.clusters_get(),
        module.params.get('postgres_cluster'),
        [['id'], ['properties', 'display_name']],
    )

    restore_request = ionoscloud_dbaas_postgres.CreateRestoreRequest(
        backup_id=module.params.get('backup_id'),
        recovery_target_time=module.params.get('recovery_target_time'),
    )

    try:
        ionoscloud_dbaas_postgres.RestoresApi(dbaas_client).cluster_restore_post(postgres_cluster_id, restore_request)

        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

        return {
            'action': 'restore',
            'changed': True,
            'id': postgres_cluster_id,
        }
    except Exception as e:
        module.fail_json(msg="failed to restore the Postgres cluster: %s" % to_native(e))
        return {
            'action': 'restore',
            'changed': False,
            'id': postgres_cluster_id,
        }


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
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
            not module.params.get("token")
            and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='both ionoscloud and ionoscloud_dbaas_postgres are required for this module, '
                             'run `pip install ionoscloud ionoscloud_dbaas_postgres`')

    cloudapi_api_client = ionoscloud.ApiClient(get_sdk_config(module, ionoscloud))
    cloudapi_api_client.user_agent = USER_AGENT
    dbaas_postgres_api_client = ionoscloud_dbaas_postgres.ApiClient(get_sdk_config(module, ionoscloud_dbaas_postgres))
    dbaas_postgres_api_client.user_agent = DBAAS_POSTGRES_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_postgres_cluster(module, dbaas_client=dbaas_postgres_api_client,
                                                       cloudapi_client=cloudapi_api_client))
        elif state == 'absent':
            module.exit_json(**delete_postgres_cluster(module, dbaas_postgres_api_client))
        elif state == 'update':
            module.exit_json(**update_postgres_cluster(module, dbaas_postgres_api_client))
        elif state == 'restore':
            module.exit_json(**restore_postgres_cluster(module, dbaas_postgres_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e),
                                                                            state=state))


if __name__ == '__main__':
    main()
