HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id, check_required_arguments, get_sdk_config,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present']
OBJECT_NAME = 'K8s config'

OPTIONS = {
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'config_file': {
        'description': ['The name of the file in which to save the config.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: k8s_config
short_description: Get K8s cluster config
description:
     - This is a simple module that supports getting the config of K8s clusters
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    ilowuerhfgwoqrghbqwoguh
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Get k8s config
  k8s_config:
    k8s_cluster: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


def get_config(module, client):
    k8s_cluster_id = get_resource_id(
        module, 
        ionoscloud.KubernetesApi(client).k8s_get(depth=1),
        module.params.get('k8s_cluster'),
    )
    config_file = module.params.get('config_file')
    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    try:
        with open(config_file, 'w') as f:
            response = k8s_server.k8s_kubeconfig_get(k8s_cluster_id=k8s_cluster_id)
            f.write(response)

    except Exception as e:
        module.fail_json(msg="failed to get the k8s cluster config: %s" % to_native(e))

    return {
        'failed': False,
        'changed': True,
        'config': response
    }


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME, OPTIONS)
        try:
            if state == 'present':
                module.exit_json(**get_config(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
