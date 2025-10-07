import re
import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import S3Key
    from ionoscloud.models import S3KeyProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id, get_resource, get_users_by_identifier
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'user-management'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'S3 Key'
RETURNED_KEY = 's3key'

OPTIONS = {
    'active': {
        'description': ['Denotes weather the Object storage key is active.'],
        'available': ['present', 'update'],
        'type': 'bool',
    },
    'user': {
        'description': ['The ID or email of the user'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'key_id': {
        'description': ['The ID of the S3 key.'],
        'available': ['present', 'absent', 'update'],
        'required': ['absent', 'update'],
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

DOCUMENTATION = """
module: s3key
short_description: Create or destroy a Ionos Cloud S3Key.
description:
     - This is a simple module that supports creating or removing S3Keys.
version_added: "2.0"
options:
    active:
        description:
        - Denotes weather the Object storage key is active.
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
    idempotency:
        choices:
        - true
        - false
        default: false
        description:
        - Flag that dictates respecting idempotency. If an s3key already exists, returns
            with already existing key instead of creating more.
        required: false
    key_id:
        description:
        - The ID of the S3 key.
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
    user:
        description:
        - The ID or email of the user
        required: true
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
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
register: s3key_create_result
''',
    'update': '''
name: Update an s3key no change
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  active: true
  state: update
register: s3key_update_nochange_result
''',
    'absent': '''
name: Remove an s3key 1
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  state: absent
''',
}

EXAMPLES = """
name: Create an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
register: s3key_create_result


name: Update an s3key no change
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  active: true
  state: update
register: s3key_update_nochange_result


name: Remove an s3key 1
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  state: absent
"""


class S3KeyModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES), supports_check_mode=True)
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS
        self.object_identity_paths = [['id']]


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('active') is not None
            and existing_object.properties.active != self.module.params.get('active')
        )


    def get_object_before(self, existing_object, clients):
        return {
            'active': existing_object.properties.active,
        }


    def get_object_after(self, existing_object, clients):
        try:
            object_properties = existing_object.properties
        except AttributeError:
            object_properties = ionoscloud.S3KeyProperties()

        return {
            'active': object_properties.active if self.module.params.get('active') is None else self.module.params.get('active'),
        }


    def _get_object_list(self, clients):
        user_list = get_users_by_identifier(
            ionoscloud.UserManagementApi(clients[0]),
            ionoscloud.Users(items=[]),
            self.module.params.get('user'),
        )
        user_id = get_resource_id(
            self.module, user_list, self.module.params.get('user'), [['id'], ['properties', 'email']],
        )

        return ionoscloud.UserS3KeysApi(clients[0]).um_users_s3keys_get(user_id, depth=1)


    def _get_object_name(self):
        return self.module.params.get('key_id')


    def _get_object_identifier(self):
        return self.module.params.get('key_id')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        active = self.module.params.get('active')

        user_list = get_users_by_identifier(
            ionoscloud.UserManagementApi(clients[0]),
            ionoscloud.Users(items=[]),
            self.module.params.get('user'),
        )
        user_id = get_resource_id(
            self.module, user_list, self.module.params.get('user'), [['id'], ['properties', 'email']],
        )

        if existing_object is not None:
            active = existing_object.properties.active if active is None else active
        
        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        s3keys_api = ionoscloud.UserS3KeysApi(client)

        try:
            s3key_response, _, headers = s3keys_api.um_users_s3keys_post_with_http_info(user_id=user_id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
                s3key_response = s3keys_api.um_users_s3keys_find_by_key_id(user_id=user_id, key_id=s3key_response.id)
            
            if active != s3key_response.properties.active:
                s3key_response, _, headers = s3keys_api.um_users_s3keys_put_with_http_info(
                    user_id=user_id,
                    key_id=s3key_response.id,
                    s3_key=ionoscloud.S3Key(properties=ionoscloud.S3KeyProperties(active=active)),
                )
                if wait:
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
                    s3key_response = s3keys_api.um_users_s3keys_find_by_key_id(user_id=user_id, key_id=s3key_response.id)

        except ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(self.object_name, to_native(e)))
        return s3key_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        active = self.module.params.get('active')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        user_list = get_users_by_identifier(
            ionoscloud.UserManagementApi(clients[0]),
            ionoscloud.Users(items=[]),
            self.module.params.get('user'),
        )
        user_id = get_resource_id(
            self.module, user_list, self.module.params.get('user'), [['id'], ['properties', 'email']],
        )

        s3keys_api = ionoscloud.UserS3KeysApi(client)

        try:
            s3key_response, _, headers = s3keys_api.um_users_s3keys_put_with_http_info(
                user_id=user_id,
                key_id=existing_object.id,
                s3_key=ionoscloud.S3Key(properties=ionoscloud.S3KeyProperties(active=active)),
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
                s3key_response = s3keys_api.um_users_s3keys_find_by_key_id(user_id=user_id, key_id=s3key_response.id)

            return s3key_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(self.object_name, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')


        user_list = get_users_by_identifier(
            ionoscloud.UserManagementApi(clients[0]),
            ionoscloud.Users(items=[]),
            self.module.params.get('user'),
        )
        user_id = get_resource_id(
            self.module, user_list, self.module.params.get('user'), [['id'], ['properties', 'email']],
        )

        try:
            _, _, headers = ionoscloud.UserS3KeysApi(client).um_users_s3keys_delete_with_http_info(
                user_id=user_id,
                key_id=existing_object.id,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout, initial_wait=2, scaleup=20)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the {}: {}".format(self.object_name, to_native(e)))


    def present_object(self, clients):
        s3key_list = self._get_object_list(clients)
        existing_object = get_resource(
            self.module, s3key_list,
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if not existing_object and self.module.params.get('idempotency') and len(s3key_list.items) > 0:
            existing_object = s3key_list.items[0]

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
    ionos_module = S3KeyModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()