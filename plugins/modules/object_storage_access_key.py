from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_object_storage_management
    from ionoscloud_object_storage_management import __version__ as obj_storage_management_sdk_version
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

USER_AGENT = 'ansible-module/%s_sdk-python-object-storage-management/%s' % ( __version__, obj_storage_management_sdk_version)
DOC_DIRECTORY = 'object-storage-management'
STATES = ['present', 'absent', 'update', 'renew']
OBJECT_NAME = 'Access Key'
RETURNED_KEY = 'access_key'

OPTIONS = {
    'access_key': {
        'description': ['The UUID of an existing access key, not the access key field.'],
        'available': ['update', 'absent', 'renew'],
        'required': ['update', 'absent', 'renew'],
        'type': 'str',
    },
    'description': {
        'description': ['Description of the Access key.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'idempotency': {
        'description': ['Flag that dictates respecting idempotency. If an s3key already exists, returns with already existing key instead of creating more.'],
        'default': False,
        'available': 'present',
        'choices': [True, False],
        'type': 'bool',
    },
    **get_default_options(STATES),
}

IMMUTABLE_OPTIONS = [
]

DOCUMENTATION = """
module: access_key
short_description: Allows operations with Ionos Cloud Object Storage Access Keys.
description:
     - This is a module that supports creating and destroying Ionos Cloud Object Storage Access Keys
version_added: "2.0"
options:
    access_key:
        description:
        - The UUID of an existing access key, not the access key field.
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
    description:
        description:
        - Description of the Access key.
        required: false
    idempotency:
        choices:
        - true
        - false
        default: false
        description:
        - Flag that dictates respecting idempotency. If an s3key already exists, returns
            with already existing key instead of creating more.
        required: false
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
        - absent
        - update
        - renew
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
    - "ionoscloud_object_storage_management >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        diff: true
    register: access_key_create_result
''',
    'update': '''
name: Update Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: update
        diff: true
    register: access_key_update_result
''',
    'renew': '''
name: Renew Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: renew
    register: access_key_renew_result
''',
    'absent': '''
name: Delete an Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id  }}"
        state: absent
    register: access_key_create_result
''',
}

EXAMPLES = """
name: Create Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        diff: true
    register: access_key_create_result


name: Update Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        description: "{{ description }}"
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: update
        diff: true
    register: access_key_update_result


name: Renew Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id }}"
        state: renew
    register: access_key_renew_result


name: Delete an Access Key
    ionoscloudsdk.ionoscloud.object_storage_access_key:
        access_key: "{{ access_key_create_result.access_key.id  }}"
        state: absent
    register: access_key_create_result
"""


class AccessKeyModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_object_storage_management]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['id']]

    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('description') is not None
            and existing_object.properties.description != self.module.params.get('description')
        )
    

    def get_object_before(self, existing_object, clients):
        return {
            'description': existing_object.properties.description,
        }


    def get_object_after(self, existing_object, clients):
        try:
            object_properties = existing_object.properties
        except AttributeError:
            object_properties = ionoscloud_object_storage_management.AccessKey()

        return {
            'description': object_properties.description if self.module.params.get('description') is None else self.module.params.get('description'),
        }


    def _get_object_list(self, clients):
        return ionoscloud_object_storage_management.AccesskeysApi(clients[0]).accesskeys_get()


    def _get_object_name(self):
        return self.module.params.get('access_key')


    def _get_object_identifier(self):
        return self.module.params.get('access_key')


    def _create_object(self, existing_object, clients):
        ak_client = clients[0]
        ak_api = ionoscloud_object_storage_management.AccesskeysApi(ak_client)
        description = self.module.params.get('description')

        if existing_object is not None:
            description = existing_object.properties.description if description is None else description

        access_key = ionoscloud_object_storage_management.AccessKeyCreate(
            properties=ionoscloud_object_storage_management.AccessKey(
                description=description,
            ),
        )

        try:
            access_key_initial = ak_api.accesskeys_post(access_key)
            if self.module.params.get('wait'):
                ak_client.wait_for(
                    fn_request=lambda: ak_api.accesskeys_find_by_id(access_key_initial.id),
                    fn_check=lambda ak: ak and ak.metadata and ak.metadata.status == 'AVAILABLE',
                    scaleup=10,
                    initial_wait=1,
                    timeout=self.module.params.get('wait_timeout'),
                )
            access_key = ak_api.accesskeys_find_by_id(access_key_initial.id)
            access_key.properties.secret_key = access_key_initial.properties.secret_key
        except Exception as e:
            self.module.fail_json(msg="failed to create the {}: {}".format(self.object_name, to_native(e)))

        return access_key


    def _update_object(self, existing_object, clients):
        ak_client = clients[0]
        ak_api = ionoscloud_object_storage_management.AccesskeysApi(ak_client)
        ak_client.wait_for(
            fn_request=lambda: ak_api.accesskeys_find_by_id(existing_object.id),
            fn_check=lambda ak: ak.metadata.status == 'AVAILABLE',
            scaleup=10,
            initial_wait=1,
            timeout=self.module.params.get('wait_timeout'),
        )
        description = self.module.params.get('description')

        access_key = ionoscloud_object_storage_management.AccessKeyEnsure(
            properties=ionoscloud_object_storage_management.AccessKey(
                description=description,
            ),
        )

        try:
            access_key = ak_api.accesskeys_put(
                accesskey_id=existing_object.id, access_key_ensure=access_key,
            )

            if self.module.params.get('wait'):
                ak_client.wait_for(
                    fn_request=lambda: ak_api.accesskeys_find_by_id(access_key.id),
                    fn_check=lambda ak: ak.metadata.status == 'AVAILABLE',
                    scaleup=10,
                    initial_wait=1,
                    timeout=self.module.params.get('wait_timeout'),
                )

        except Exception as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(self.object_name, to_native(e)))
        return access_key


    def _remove_object(self, existing_object, clients):
        ak_client = clients[0]
        ak_api = ionoscloud_object_storage_management.AccesskeysApi(ak_client)

        try:
            if existing_object.metadata.status != 'DESTROYING':
                ak_api.accesskeys_delete(existing_object.id)

            if self.module.params.get('wait'):
                try:
                    ak_client.wait_for(
                        fn_request=lambda: ak_api.accesskeys_find_by_id(existing_object.id),
                        fn_check=lambda _: False,
                        scaleup=10,
                        initial_wait=1,
                        timeout=self.module.params.get('wait_timeout'),
                    )
                except ionoscloud_object_storage_management.ApiException as e:
                    if e.status != 404:
                        raise e
        except Exception as e:
            self.module.fail_json(msg="failed to delete the {}: {}".format(self.object_name, to_native(e)))
    

    def renew_object(self, clients):
        ak_client = clients[0]
        ak_api = ionoscloud_object_storage_management.AccesskeysApi(ak_client)

        ak_id = get_resource_id(
            self.module, self._get_object_list(clients),
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        try:
            access_key = ak_api.accesskeys_renew(ak_id)
            if self.module.params.get('wait'):
                ak_client.wait_for(
                    fn_request=lambda: ak_api.accesskeys_find_by_id(access_key.id),
                    fn_check=lambda ak: ak.metadata.status == 'AVAILABLE',
                    scaleup=10,
                    initial_wait=1,
                    timeout=self.module.params.get('wait_timeout'),
                )

        
            return {
                'access_key': access_key.to_dict(),
                'action': 'renew',
                'changed': True,
                'id': access_key.id,
            }
        except Exception as e:
            self.module.fail_json(msg="failed to renew the {}: {}".format(self.object_name, to_native(e)))


    def present_object(self, clients):
        object_list = self._get_object_list(clients)
        existing_object = get_resource(
            self.module, object_list,
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if not existing_object and self.module.params.get('idempotency') and len(object_list.items) > 0:
            existing_object = object_list.items[0]

        if existing_object:
            return self.update_replace_object(existing_object, clients)

        returned_json = {}
        object_after = self.get_object_after(existing_object, clients)
        if self.module._diff:
            returned_json['diff'] = {
                'before': {},
                'after': object_after,
            }

        if self.module.check_mode:
            return {
                **returned_json,
                **{
                    'changed': True,
                    'msg': '{object_name} {object_name_identifier} would be created'.format(
                        object_name=self.object_name, object_name_identifier=self._get_object_name(),
                    ),
                    self.returned_key: {
                        'id': '<known after creation>',
                        'properties': object_after,
                    },
                },
            }

        return {
            **returned_json,
            **{
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: self._create_object(None, clients).to_dict(),
            },
        }


if __name__ == '__main__':
    ionos_module = AccessKeyModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_object_storage_management is required for this module, '
                             'run `pip install ionoscloud_object_storage_management`')
    ionos_module.main()
