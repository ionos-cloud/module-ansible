from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_dbaas_mariadb
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-mariadb/%s' % (
    __version__, ionoscloud_dbaas_mariadb.__version__)
DOC_DIRECTORY = 'dbaas-mariadb'
STATES = ['present']
OBJECT_NAME = 'MariaDB Cluster'
RETURNED_KEY = 'mariadb_cluster'

OPTIONS = {
    'mariadb_cluster': {
        'description': ['The ID or name of an existing MariaDB Cluster.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}


DOCUMENTATION = """
module: mariadb_backup
short_description: Allows operations with Ionos Cloud MariaDB Cluster Backups.
description:
     - This is a module that supports creating MariaDB Cluster Backups
version_added: "2.0"
options:
    allow_replace:
        default: false
        description:
        - Boolean indicating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    mariadb_cluster:
        description:
        - The ID or name of an existing MariaDB Cluster.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    state:
        choices:
        - present
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud-dbaas-mariadb >= 1.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create MariaDB Cluster Backup
    mariadb_backup:
      mariadb_cluster: backuptest-04
    register: cluster_response
  ''',
}

EXAMPLES = """- name: Create MariaDB Cluster Backup
    mariadb_backup:
      mariadb_cluster: backuptest-04
    register: cluster_response
"""

class MariaDBBackupModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_mariadb]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def present_object(self, clients):
        backups_api = ionoscloud_dbaas_mariadb.BackupsApi(clients[0])
        mariadb_clusters_api = ionoscloud_dbaas_mariadb.ClustersApi(clients[0])

        mariadb_cluster_id = get_resource_id(
            self.module,
            mariadb_clusters_api.clusters_get(),
            self.module.params.get('mariadb_cluster'),
            [['id'], ['properties', 'display_name']],
        )

        backup = backups_api.cluster_backups_post(mariadb_cluster_id)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            self.returned_key: backup.to_dict()
        }


if __name__ == '__main__':
    ionos_module = MariaDBBackupModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dbaas_mariadb is required for this module, run `pip install ionoscloud_dbaas_mariadb`')
    ionos_module.main()
