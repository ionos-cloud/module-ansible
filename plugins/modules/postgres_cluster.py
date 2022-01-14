ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
  - name: Create Postgres Cluster
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
          datacenterId: "{{ datacenter_response.datacenter.id }}"
          lanId: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response

  - name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster_id: "{{ cluster_response.postgres_cluster.id }}"
      postgres_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response

  - name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster_id: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
'''

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

import ionoscloud

HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None

def create_postgres_cluster(module, client):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
    display_name=module.params.get('display_name')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)

    postgres_clusters = postgres_cluster_server.clusters_get()

    existing_postgres_cluster = None

    for postgres_cluster in postgres_clusters.items:
        if display_name == postgres_cluster.properties.display_name:
            existing_postgres_cluster = postgres_cluster
            break

    if existing_postgres_cluster is not None:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'postgres_cluster': existing_postgres_cluster.to_dict(),
        }

    connection = module.params.get('connections')[0]

    datacenter_id = _get_resource(ionoscloud.DataCentersApi(client).datacenters_get(depth=1), connection['datacenter'])
    lan_id = _get_resource(ionoscloud.LansApi(client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

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
            client.wait_for(
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


def delete_postgres_cluster(module, client):
    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)
    postgres_cluster_id = _get_resource(postgres_cluster_server.clusters_get(), module.params.get('postgres_cluster'))

    try:
        postgres_cluster_server.clusters_delete(postgres_cluster_id)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                fn_check=lambda _: False,
                scaleup=10000,
            )

        return {
            'action': 'delete',
            'changed': True,
            'id': postgres_cluster_id,
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': postgres_cluster_id,
        }


def update_postgres_cluster(module, client):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)
    postgres_cluster_id = _get_resource(postgres_cluster_server.clusters_get(), module.params.get('postgres_cluster'))

    postgres_cluster_properties = ionoscloud_dbaas_postgres.PatchClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        display_name=module.params.get('display_name'),
        maintenance_window=maintenance_window,
    )
    postgres_cluster = ionoscloud_dbaas_postgres.PatchClusterRequest(properties=postgres_cluster_properties)

    try:
        postgres_cluster = postgres_cluster_server.clusters_patch(
            cluster_id=postgres_cluster_id,
            patch_cluster_request=postgres_cluster,
        )

        if module.params.get('wait'):
            try: 
                client.wait_for(
                    fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                    fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                )
            except ionoscloud_dbaas_postgres.ApiException as e:
                if e.status != 404:
                    raise e

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


def restore_postgres_cluster(module, client):
    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)

    postgres_cluster_id = _get_resource(postgres_cluster_server.clusters_get(), module.params.get('postgres_cluster'))
    restore_request = ionoscloud_dbaas_postgres.CreateRestoreRequest(
        backup_id=module.params.get('backup_id'),
        recovery_target_time=module.params.get('recovery_target_time'),
    )

    try:
        ionoscloud_dbaas_postgres.RestoresApi(client).cluster_restore_post(postgres_cluster_id, restore_request)
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            maintenance_window=dict(
                type='dict',
                day_of_the_week=dict(type='str'),
                time=dict(type='str'),
            ),
            postgres_version=dict(type='str'),
            instances=dict(type='int'),
            cores=dict(type='int'),
            ram=dict(type='int'),
            storage_size=dict(type='int'),
            storage_type=dict(type='str'),
            connections=dict(type='list', elements='dict'),
            location=dict(type='str'),
            display_name=dict(type='str'),
            db_username=dict(type='str', no_log=True),
            db_password=dict(type='str', no_log=True),
            synchronization_mode=dict(type='str'),
            backup_id=dict(type='str'),
            recovery_target_time=dict(type='str'),
            postgres_cluster=dict(type='str'),

            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME']),
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True,
            ),
            state=dict(type='str', default='present'),
            wait=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud_dbaas_postgres`')

    username = module.params.get('username')
    password = module.params.get('password')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (ionoscloud_dbaas_postgres.__version__, __version__)

    state = module.params.get('state')

    configuration = ionoscloud_dbaas_postgres.Configuration(
        username=username,
        password=password,
    )

    with ionoscloud_dbaas_postgres.ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'present':
            required_options = [
                'postgres_version', 'instances', 'cores', 'ram', 'storage_size', 'storage_type',
                'connections', 'location', 'display_name', 'synchronization_mode', 'db_username', 'db_password',
            ]
            for required_option in required_options:
                if not module.params.get(required_option):
                    module.fail_json(msg='{} parameter is required for a new Postgres cluster'.format(required_option))

            try:
                (postgres_cluster_dict_array) = create_postgres_cluster(module, api_client)
                module.exit_json(**postgres_cluster_dict_array)

            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('postgres_cluster_id'):
                module.fail_json(msg='postgres_cluster_id parameter is required for deleting a Postgres cluster.')

            try:
                (result) = delete_postgres_cluster(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set Postgres cluster state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('postgres_cluster_id'):
                module.fail_json(msg='postgres_cluster_id parameter is required for updating a Postgres cluster.')

            try:
                (postgres_cluster_dict_array) = update_postgres_cluster(module, api_client)
                module.exit_json(**postgres_cluster_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set Postgres cluster state: %s' % to_native(e))

        elif state == 'restore':
            if not module.params.get('postgres_cluster_id'):
                module.fail_json(msg='postgres_cluster_id parameter is required for restoring a Postgres cluster.')

            try:
                (postgres_cluster_dict_array) = restore_postgres_cluster(module, api_client)
                module.exit_json(**postgres_cluster_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set Postgres cluster state: %s' % to_native(e))


if __name__ == '__main__':
    main()
