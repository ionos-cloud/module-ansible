ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create Postgres Cluster
      postgres_cluster:
        postgres_cluster_email: "{{ email }}"
        postgres_cluster_password: "{{ password }}"
        name: "{{ name }}"

    - name: Update a Postgres Cluster
      postgres_cluster:
        postgres_cluster_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        postgres_cluster_email: "{{ updated_email }}"
        postgres_cluster_password:  "{{ updated_password }}"
        state: update

    - name: Remove Postgres Cluster
      postgres_cluster:
        postgres_cluster_id: "2fac5a84-5cc4-4f85-a855-2c0786a4cdec"
        state: absent
'''

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False


def create_postgres_cluster(module, client):
    time = module.params.get('time')
    day_of_the_week = module.params.get('day_of_the_week')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)

    postgres_cluster_properties = ionoscloud_dbaas_postgres.CreateClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        storage_type=module.params.get('storage_type'),
        connections=module.params.get('connections'),
        location=module.params.get('location'),
        display_name=module.params.get('display_name'),
        maintenance_window=ionoscloud_dbaas_postgres.MaintenanceWindow(
            time=time,
            day_of_the_week=day_of_the_week,
        ) if (time and day_of_the_week) else None,
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
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'postgres_cluster': postgres_cluster_server.clusters_post(postgres_cluster).to_dict()
        }
    except Exception as e:
        module.fail_json(msg="failed to create the Postgres cluster: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'create'
        }


def delete_postgres_cluster(module, client):
    postgres_cluster_id = module.params.get('postgres_cluster_id')

    try:
        ionoscloud_dbaas_postgres.ClustersApi(client).clusters_delete(postgres_cluster_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': postgres_cluster_id
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': postgres_cluster_id
        }


def update_postgres_cluster(module, client):
    time = module.params.get('time')
    day_of_the_week = module.params.get('day_of_the_week')

    postgres_cluster_id = module.params.get('postgres_cluster_id')

    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(client)

    postgres_cluster_properties = ionoscloud_dbaas_postgres.PatchClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        display_name=module.params.get('display_name'),
        maintenance_window=ionoscloud_dbaas_postgres.MaintenanceWindow(
            time=time,
            day_of_the_week=day_of_the_week,
        ) if (time and day_of_the_week) else None,
    )
    postgres_cluster = ionoscloud_dbaas_postgres.PatchClusterRequest(properties=postgres_cluster_properties)

    try:
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'backupunit': postgres_cluster_server.clusters_patch(postgres_cluster_id=postgres_cluster_id, patch_cluster_request=postgres_cluster).to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the backupunit: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update'
        }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            time=dict(type='str'),
            day_of_the_week=dict(type='str'),
            postgres_version=dict(type='str'),
            instances=dict(type='int'),
            cores=dict(type='int'),
            ram=dict(type='int'),
            storage_size=dict(type='int'),
            storage_type=dict(type='str'),
            connections=dict(type='list'),
            location=dict(type='str'),
            display_name=dict(type='str'),
            db_username=dict(type='str', no_log=True),
            db_password=dict(type='str', no_log=True),
            synchronization_mode=dict(type='str'),
            backup_id=dict(type='str'),
            recovery_target_time=dict(type='str'),

            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud_dbaas_postgres`')

    username = module.params.get('username')
    password = module.params.get('password')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (ionoscloud_dbaas_postgres.__version__, __version__)

    state = module.params.get('state')

    configuration = ionoscloud_dbaas_postgres.Configuration(
        username=username,
        password=password
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


if __name__ == '__main__':
    main()
