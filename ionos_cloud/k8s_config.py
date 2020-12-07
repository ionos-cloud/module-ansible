ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
- name: Get k8s config
  k8s_config:
    k8s_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
'''

HAS_SDK = True
try:
    import ionossdk
    from ionossdk import __version__ as sdk_version
    from ionossdk.rest import ApiException
    from ionossdk import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def get_config(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    config_file = module.params.get('config_file')
    k8s_server = ionossdk.KubernetesApi(api_client=client)

    try:
        with open(config_file, 'w') as f:
            response = k8s_server.k8s_kubeconfig_get(k8s_cluster_id=k8s_cluster_id)
            f.write(response.properties.kubeconfig)

    except Exception as e:
        module.fail_json(msg="failed to get the k8s cluster config: %s" % to_native(e))

    return {
        'failed': False,
        'changed': True,
        'config': response.to_dict()
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            k8s_cluster_id=dict(type='str'),
            config_file=dict(type='str'),
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
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionossdk is required for this module, run `pip install ionossdk`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ionossdk-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionossdk.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'present':
            try:
                (response) = get_config(module, api_client)
                module.exit_json(response=response)
            except Exception as e:
                module.fail_json(msg='failed to get the k8s cluster config: %s' % to_native(e))


if __name__ == '__main__':
    main()
