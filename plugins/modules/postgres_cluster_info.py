ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: List Postgres Clusters
        postgres_cluster_info:
        register: postgres_clusters_response


    - name: Show Postgres Clusters
        debug:
            var: postgres_clusters_response.result
'''

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
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
        ),
        supports_check_mode=True,
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_dbaas_postgres is required for this module, run `pip install ionoscloud_dbaas_postgres`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, ionoscloud_dbaas_postgres.__version__)

    config = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        config['host'] = api_url
        config['server_index'] = None

    dbaas_postgres_api_client = ionoscloud_dbaas_postgres.ApiClient(ionoscloud_dbaas_postgres.Configuration(**config))

    dbaas_postgres_api_client.user_agent = user_agent

    try:
        results = []
        for cluster in ionoscloud_dbaas_postgres.ClustersApi(dbaas_postgres_api_client).clusters_get().items:
            results.append(cluster.to_dict())
        module.exit_json(result=results)
    except Exception as e:
            module.fail_json(msg='failed to retrieve Postgres Clusters: %s' % to_native(e))

if __name__ == '__main__':
    main()
