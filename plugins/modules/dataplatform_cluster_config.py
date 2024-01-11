HAS_SDK = True
try:
    import ionoscloud_dataplatform
except ImportError:
    HAS_SDK = False


from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, check_required_arguments, get_sdk_config, get_resource,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options



ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
DATAPLATFORM_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (
__version__, ionoscloud_dataplatform.__version__)
DOC_DIRECTORY = 'dataplatform'
STATES = ['present']
OBJECT_NAME = 'DataPlatform Cluster Config'

OPTIONS = {
    'cluster': {
        'description': ['The name or the ID of the Data Platform cluster.'],
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
module: dataplatform_cluster_config
short_description: Get DataPlatform Cluster configs
description:
     - This is a simple module that supports getting config of DataPlatform clusters
     - ⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.
version_added: "2.0"
options:
    ilowuerhfgwoqrghbqwoguh
requirements:
    - "python >= 2.6"
    - "ionoscloud-dataplatform >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Get DataPlatform config
  dataplatform_cluster_config:
    dataplatform_cluster_id: "ed67d8b3-63c2-4abe-9bf0-073cee7739c9"
    config_file: 'config.yaml'
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


def get_config(module, client):
    cluster = module.params.get('cluster')
    
    dataplatform_clusters = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client).get_clusters()

    dataplatform_cluster = get_resource(
        module, dataplatform_clusters, cluster, [['id'], ['properties', 'name']],
    )

    if dataplatform_cluster is None:
        module.fail_json(msg="DataPlatform cluster {} not found".format(cluster))
    
    config_file = module.params.get('config_file')

    try:
        with open(config_file, 'w') as f:
            response = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client).get_cluster_kubeconfig(cluster_id=dataplatform_cluster.id)
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

    dataplatform_api_client = ionoscloud_dataplatform.ApiClient(get_sdk_config(module, ionoscloud_dataplatform))
    dataplatform_api_client.user_agent = DATAPLATFORM_USER_AGENT

    check_required_arguments(module, state, OBJECT_NAME, OPTIONS)

    try:
        if state == 'present':
            module.exit_json(**get_config(module, dataplatform_api_client))
    except Exception as e:
        module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
