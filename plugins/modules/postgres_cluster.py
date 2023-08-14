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
DBAAS_POSTGRES_USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-postgres/%s' % (
    __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['present', 'absent', 'update', 'restore']
OBJECT_NAME = 'Postgres Cluster'
RETURNED_KEY = 'postgres_cluster'

OPTIONS = {
    'maintenance_window': {
        'description': ['A weekly 4 hour-long window, during which maintenance might occur.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'postgres_version': {
        'description': ['The PostgreSQL version of your cluster.'],
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
        'description': ['The amount of memory per instance in megabytes. Has to be a multiple of 1024.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_size': {
        'description': ['The amount of storage per instance in megabytes.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'storage_type': {
        'description': ['The storage type used in your cluster. (Value "SSD" is deprecated. Use the equivalent "SSD Premium" instead)'],
        'available': ['present'],
        'choices': ['HDD', 'SSD', 'SSD Standard', 'SSD Premium'],
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
        'description': ['The physical location where the cluster will be created. This will be where all of your instances live. Property cannot be modified after datacenter creation.'],
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
        'description': ['The username for the initial PostgreSQL user. Some system usernames are restricted (e.g. "postgres", "admin", "standby").'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
        'no_log': True,
    },
    'db_password': {
        'description': ['The password for the initial postgres user.'],
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
        'description': ['The S3 location where the backups will be stored.'],
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
    'allow_replace': {
        'description': [
            'Boolean indincating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
    - "ionoscloud-dbaas-postgres >= 1.0.2"
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
          datacenter: DatacenterName
          lan: LanName
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  ''',
    'update': '''- name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: backuptest-04
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
      postgres_cluster: backuptest-04
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


def _should_replace_object(module, existing_object, cloudapi_client):
    datacenter_id = lan_id = cidr = None
    if module.params.get('connections'):
        connection = module.params.get('connections')[0]
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(module, datacenter_list, connection['datacenter'])

        if datacenter_id is None:
            module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
        
        lan_id = get_resource_id(
            module,
            ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1),
            connection['lan'],
        )
        if lan_id is None:
            module.fail_json('LAN {} not found.'.format(connection['lan']))
        cidr = connection['cidr']

    return (
        module.params.get('backup_location') is not None
        and existing_object.properties.backup_location != module.params.get('backup_location')
        or module.params.get('location') is not None
        and existing_object.properties.location != module.params.get('location')
        or module.params.get('synchronization_mode') is not None
        and existing_object.properties.synchronization_mode != module.params.get('synchronization_mode')
        or module.params.get('storage_type') is not None
        and existing_object.properties.storage_type != module.params.get('storage_type')
        or module.params.get('connections') is not None
        and (
            existing_object.properties.connections[0].datacenter_id != datacenter_id
            or existing_object.properties.connections[0].lan_id != lan_id
            or existing_object.properties.connections[0].cidr != cidr
        )
    )


def _should_update_object(module, existing_object):
    return (
        module.params.get('display_name') is not None
        and existing_object.properties.display_name != module.params.get('display_name')
                or module.params.get('maintenance_window') is not None
        and (
            existing_object.properties.maintenance_window.day_of_the_week != module.params.get('maintenance_window').get('day_of_the_week')
            or existing_object.properties.maintenance_window.time != module.params.get('maintenance_window').get('time')
        ) or module.params.get('postgres_version') is not None
        and existing_object.properties.postgres_version != module.params.get('postgres_version')
        or module.params.get('instances') is not None
        and existing_object.properties.instances != module.params.get('instances')
        or module.params.get('cores') is not None
        and existing_object.properties.cores != module.params.get('cores')
        or module.params.get('ram') is not None
        and existing_object.properties.ram != module.params.get('ram')
    )


def _get_object_list(module, client):
    return ionoscloud_dbaas_postgres.ClustersApi(client).clusters_get()


def _get_object_name(module):
    return module.params.get('display_name')


def _get_object_identifier(module):
    return module.params.get('postgres_cluster')


def _create_object(module, dbaas_client, cloudapi_client, existing_object=None):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
    backup_location=module.params.get('backup_location')
    if existing_object is not None:
        backup_location = existing_object.properties.backup_location if backup_location is None else backup_location
        maintenance_window = existing_object.properties.maintenance_window if maintenance_window is None else maintenance_window

    connection = module.params.get('connections')[0]

    datacenter_id = get_resource_id(module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=2), connection['datacenter'])

    if datacenter_id is None:
        module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
    
    lan_id = get_resource_id(module, ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

    if lan_id is None:
        module.fail_json('LAN {} not found.'.format(connection['lan']))

    connections = [
        ionoscloud_dbaas_postgres.Connection(datacenter_id=datacenter_id, lan_id=lan_id, cidr=connection['cidr']),
    ]

    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_cluster_properties = ionoscloud_dbaas_postgres.CreateClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        storage_type=module.params.get('storage_type'),
        connections=connections,
        location=module.params.get('location'),
        backup_location=backup_location,
        display_name=module.params.get('display_name'),
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
        postgres_cluster = clusters_api.clusters_post(postgres_cluster)
        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )
    except Exception as e:
        module.fail_json(msg="failed to create the new Postgres Cluster: %s" % to_native(e))
    return postgres_cluster


def _update_object(module, dbaas_client, existing_object):
    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
    dbaas_client.wait_for(
        fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
        fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
        scaleup=10000,
    )

    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    display_name=module.params.get('display_name')

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
        postgres_cluster = clusters_api.clusters_patch(
            cluster_id=existing_object.id,
            patch_cluster_request=postgres_cluster,
        )

        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

    except Exception as e:
        module.fail_json(msg="failed to update the Postgres Cluster: %s" % to_native(e))
    return postgres_cluster


def _remove_object(module, dbaas_client, existing_object):
    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    try:
        if existing_object.metadata.state != 'DESTROYING':
            clusters_api.clusters_delete(existing_object.id)

        if module.params.get('wait'):
            try:
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
                    fn_check=lambda _: False,
                    scaleup=10000,
                )
            except ionoscloud_dbaas_postgres.ApiException as e:
                if e.status != 404:
                    raise e
    except Exception as e:
        module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))


def update_replace_object(module, dbaas_client, cloudapi_client, existing_object):
    if _should_replace_object(module, existing_object, cloudapi_client):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

        new_object = _create_object(module, dbaas_client, cloudapi_client, existing_object).to_dict()
        _remove_object(module, dbaas_client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, dbaas_client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, dbaas_client, cloudapi_client):
    existing_object = get_resource(
        module, _get_object_list(module, dbaas_client), _get_object_name(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object:
        return update_replace_object(module, dbaas_client, cloudapi_client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, dbaas_client, cloudapi_client).to_dict()
    }


def update_object(module, dbaas_postgres_api_client, cloudapi_api_client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, dbaas_postgres_api_client)

    existing_object = get_resource(
        module, object_list, _get_object_identifier(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(
        module, object_list, object_name,
        [['id'], ['properties', 'display_name']],
    )

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, dbaas_postgres_api_client, cloudapi_api_client, existing_object)


def remove_object(module, client):

    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_identifier(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
    }


def restore_object(module, dbaas_client):
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
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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

    if certificate_fingerprint is not None:
        conf['fingerprint'] = certificate_fingerprint

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
            module.exit_json(**create_object(module, dbaas_postgres_api_client, cloudapi_api_client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, dbaas_postgres_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, dbaas_postgres_api_client, cloudapi_api_client))
        elif state == 'restore':
            module.exit_json(**restore_object(module, dbaas_postgres_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e),
                                                                            state=state))


if __name__ == '__main__':
    main()
