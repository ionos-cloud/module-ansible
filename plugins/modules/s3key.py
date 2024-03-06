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
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id, get_resource, get_users
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
        'description': ['Denotes weather the S3 key is active.'],
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
        - Denotes weather the S3 key is active.
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
    'present': '''name: Create an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
register: result
''',
    'update': '''name: Update an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  active: false
  state: update
''',
    'absent': '''name: Remove an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  state: absent
''',
}

EXAMPLES = """name: Create an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
register: result

name: Update an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  active: false
  state: update

name: Remove an s3key
ionoscloudsdk.ionoscloud.s3key:
  user: ''
  key_id: ''
  state: absent
"""


class PccModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def present_object(self, clients):
        client = clients[0]
        user_id = get_resource_id(
            self.module,
            get_users(ionoscloud.UserManagementApi(client), ionoscloud.Users(items=[])), 
            self.module.params.get('user'),
            [['id'], ['properties', 'email']],
        )
        do_idempotency = self.module.params.get('idempotency')
        key_id = self.module.params.get('key_id')
        active = self.module.params.get('active')
        wait_timeout = int(self.module.params.get('wait_timeout'))
        changed = False

        user_s3keys_server = ionoscloud.UserS3KeysApi(client)
        s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id, depth=1)

        try:
            s3key = get_resource(self.module, s3key_list, key_id, [['id']])

            if not s3key and do_idempotency and len(s3key_list.items) > 0:
                s3key = s3key_list.items[0]

            if not s3key:
                changed = True
                s3key, _, headers = user_s3keys_server.um_users_s3keys_post_with_http_info(user_id=user_id)

                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
            if s3key.properties.active != active:
                changed = True
                s3key, _, headers = user_s3keys_server.um_users_s3keys_put_with_http_info(
                    user_id, s3key.id, S3Key(properties=S3KeyProperties(active=active)),
                )

                if self.module.params.get('wait'):
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return {
                'changed': changed,
                'failed': False,
                'action': 'create',
                RETURNED_KEY: s3key.to_dict()
            }

        except Exception as e:
            self.module.fail_json(msg="failed to create the s3key: %s" % to_native(e))
            return {
                'changed': False,
                'failed': True,
                'action': 'create',
            }


    def absent_object(self, clients):
        client = clients[0]
        user_id = get_resource_id(
            self.module,
            get_users(ionoscloud.UserManagementApi(client), ionoscloud.Users(items=[])), 
            self.module.params.get('user'),
            [['id'], ['properties', 'email']],
        )
        key_id = self.module.params.get('key_id')

        user_s3keys_server = ionoscloud.UserS3KeysApi(client)

        s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id)
        s3key_id = get_resource_id(self.module, s3key_list, key_id, [['id']])

        if not s3key_id:
            self.module.exit_json(changed=False)

        try:
            user_s3keys_server.um_users_s3keys_delete(user_id, s3key_id)
            return {
                'action': 'delete',
                'changed': True,
                'id': key_id
            }

        except Exception as e:
            self.module.fail_json(msg="failed to delete the s3key: %s" % to_native(e))
            return {
                'action': 'delete',
                'changed': False,
                'id': key_id
            }


    def update_object(self, clients):
        client = clients[0]
        user_id = get_resource_id(
            self.module,
            get_users(ionoscloud.UserManagementApi(client), ionoscloud.Users(items=[])), 
            self.module.params.get('user'),
            [['id'], ['properties', 'email']],
        )
        key_id = self.module.params.get('key_id')
        active = self.module.params.get('active')

        changed = False

        user_s3keys_server = ionoscloud.UserS3KeysApi(client)
        s3key_list = user_s3keys_server.um_users_s3keys_get(user_id=user_id, depth=1)
        s3key = get_resource(self.module, s3key_list, key_id, [['id']])

        if not s3key:
            self.module.exit_json(changed=False)

        if self.module.check_mode:
            self.module.exit_json(changed=True)
        try:
            if s3key.properties.active != active:
                changed = True
                s3key, _, headers = user_s3keys_server.um_users_s3keys_put_with_http_info(
                    user_id, s3key.id, S3Key(properties=S3KeyProperties(active=active)),
                )

                if self.module.params.get('wait'):
                    request_id = _get_request_id(headers['Location'])
                    client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return {
                'changed': changed,
                'failed': False,
                'action': 'update',
                RETURNED_KEY: s3key.to_dict()
            }

        except Exception as e:
            self.module.fail_json(msg="failed to update the s3key: %s" % to_native(e))
            return {
                'changed': False,
                'failed': True,
                'action': 'update',
            }


if __name__ == '__main__':
    ionos_module = PccModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()