from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_dbaas_mongo
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id, get_resource,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dbaas-mongo/%s' % (
    __version__, ionoscloud_dbaas_mongo.__version__)
DOC_DIRECTORY = 'dbaas-mongo'
STATES = ['present', 'update', 'absent']
OBJECT_NAME = 'Mongo Cluster User'
RETURNED_KEY = 'mongo_cluster_user'

OPTIONS = {
    'mongo_cluster': {
        'description': ['The UUID or name of an existing Mongo Cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'mongo_username': {
        'description': ['The username of the user.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'mongo_password': {
        'description': ['The password of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'no_log': True,
        'type': 'str',
    },
    'user_roles': {
        'description': [
          'A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'
          "'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase'"
          "'database': the name of the databse to which the role applies"
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
    },
    **get_default_options(STATES),
}


DOCUMENTATION = """
module: mongo_cluster
short_description: Allows operations with Ionos Cloud Mongo Cluster Users.
description:
     - This is a module that supports creating and destroying Mongo Cluster Users
version_added: "2.0"
options:
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
    mongo_cluster:
        description:
        - The UUID or name of an existing Mongo Cluster.
        required: true
    mongo_password:
        description:
        - The password of the user.
        no_log: true
        required: false
    mongo_username:
        description:
        - The username of the user.
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
        - update
        - absent
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
    user_roles:
        description:
        - 'A list of mongodb user roles. A user role is represented as a dict containing
            2 keys:''role'': has one of the following values: ''read'', ''readWrite''
            or ''readAnyDatabase''''database'': the name of the databse to which the role
            applies'
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
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dbaas-mongo >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <password>
      user_roles:
        - role: read
          database: test
    register: mongo_user_response
  ''',
    'update': '''- name: Update User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <newPassword>
      user_roles:
        - role: read
          database: test
        - role: readWrite
          database: test
      state: update
    register: mongo_user_response
  ''',
    'absent': '''- name: Delete Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
    register: mongo_user_response
  ''',
}

EXAMPLES = """- name: Create Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <password>
      user_roles:
        - role: read
          database: test
    register: mongo_user_response
  
- name: Update User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <newPassword>
      user_roles:
        - role: read
          database: test
        - role: readWrite
          database: test
      state: update
    register: mongo_user_response
  
- name: Delete Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
    register: mongo_user_response
"""


class MongoUserModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_dbaas_mongo]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['properties', 'username']]


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        def sort_func(el):
            return el['database'], el['role']
        
        existing_roles = sorted(
            [{'role': role.role, 'database': role.database} for role in existing_object.properties.roles],
            key=sort_func,
        )
        return (
            self.module.params.get('mongo_password') is not None
            and existing_object.properties.password != self.module.params.get('mongo_password')
            or self.module.params.get('roles') is not None
            and existing_roles != sorted(self.module.params.get('roles'), key=sort_func)
        )


    def _get_object_list(self, clients):
        client = clients[0]
        mongo_cluster_id = get_resource_id(
            self.module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
            self.module.params.get('mongo_cluster'),
            [['id'], ['properties', 'display_name']],
        )
        return ionoscloud_dbaas_mongo.UsersApi(client).clusters_users_get(mongo_cluster_id)


    def _get_object_name(self):
        return self.module.params.get('mongo_username')


    def _get_object_identifier(self):
        return self.module.params.get('mongo_username')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        mongo_username = self.module.params.get('mongo_username')
        mongo_password = self.module.params.get('mongo_password')
        user_roles = list(map(
            lambda role: ionoscloud_dbaas_mongo.UserRoles(role=role['role'], database=role['database']),
            self.module.params.get('user_roles'),
        ))

        if existing_object is not None:
            mongo_username = existing_object.properties.username if mongo_username is None else mongo_username
            user_roles = existing_object.properties.roles if user_roles is None else user_roles

        users_api = ionoscloud_dbaas_mongo.UsersApi(client)

        mongo_user = ionoscloud_dbaas_mongo.User(properties=ionoscloud_dbaas_mongo.UserProperties(
            username=mongo_username,
            password=mongo_password,
            roles=user_roles,
        ))

        try:
            mongo_cluster_id = get_resource_id(
                self.module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
                self.module.params.get('mongo_cluster'),
                [['id'], ['properties', 'display_name']],
            )
            user_response = users_api.clusters_users_post(mongo_cluster_id, mongo_user)
        except ionoscloud_dbaas_mongo.ApiException as e:
            self.module.fail_json(msg="failed to create the new Mongo Cluster User: %s" % to_native(e))
        return user_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        mongo_password = self.module.params.get('mongo_password')
        user_roles = list(map(
            lambda role: ionoscloud_dbaas_mongo.UserRoles(role=role['role'], database=role['database']),
            self.module.params.get('user_roles'),
        ))
        users_api = ionoscloud_dbaas_mongo.UsersApi(client)

        mongo_user = ionoscloud_dbaas_mongo.PatchUserRequest(properties=ionoscloud_dbaas_mongo.PatchUserProperties(
            password=mongo_password,
            roles=user_roles,
        ))
        
        try:
            mongo_cluster_id = get_resource_id(
                self.module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
                self.module.params.get('mongo_cluster'),
                [['id'], ['properties', 'display_name']],
            )
            user_response = users_api.clusters_users_patch(
                mongo_cluster_id,
                self.module.params.get('mongo_username'),
                mongo_user,
            )
        except ionoscloud_dbaas_mongo.ApiException as e:
            self.module.fail_json(msg="failed to update the Mongo Cluster User: %s" % to_native(e))

        return user_response

    def _remove_object(self, existing_object, clients):
        client = clients[0]
        users_api = ionoscloud_dbaas_mongo.UsersApi(client)

        try:
            mongo_cluster_id = get_resource_id(
                self.module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
                self.module.params.get('mongo_cluster'),
                [['id'], ['properties', 'display_name']],
            )
            users_api.clusters_users_delete(mongo_cluster_id, existing_object.properties.username)
            if self.module.params.get('wait'):
                try:
                    client.wait_for(
                        fn_request=lambda: users_api.clusters_users_find_by_id(
                            mongo_cluster_id, existing_object.properties.username,
                        ),
                        fn_check=lambda _: False,
                        scaleup=10000,
                        timeout=self.module.params.get('wait_timeout'),
                    )
                except ionoscloud_dbaas_mongo.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the Mongo Cluster User: %s" % to_native(e))


    def update_object(self, clients):
        object_list = self._get_object_list(clients)

        existing_object = get_resource(
            self.module, object_list,
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        return self.update_replace_object(existing_object, clients)


    def absent_object(self, clients):
        existing_object = get_resource(
            self.module, self._get_object_list(clients),
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        self._remove_object(existing_object, clients)

        return {
            'action': 'delete',
            'changed': True,
            'id': existing_object.properties.username,
        }

if __name__ == '__main__':
    ionos_module = MongoUserModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_dbaas_mongo is required for this module, '
                             'run `pip install ionoscloud_dbaas_mongo`')
    ionos_module.main()
