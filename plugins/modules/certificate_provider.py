HAS_SDK = True
try:
    import ionoscloud_cert_manager
    from ionoscloud_cert_manager import __version__ as certificate_manager_sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-certificate-manager/%s' % ( __version__, certificate_manager_sdk_version)
DOC_DIRECTORY = 'certificate_provider'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Certificate Provider'
RETURNED_KEY = 'certificate_provider'

OPTIONS = {
    'provider': {
        'description': ['The provider name or ID.'],
        'available': ['update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'provider_name': {
        'description': ['The name of the certificate provider.'],
        'available': ['present', 'update', 'absent'],
        'required': ['present'],
        'type': 'str',
    },
    'provider_email': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'required': ['present'],
        'type': 'str',
    },
    'provider_server': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'required': ['present'],
        'type': 'str',
    },
    'key_id': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    'key_secret': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "provider_email", "note": "" },
    { "name": "provider_server", "note": "" },
    { "name": "key_id", "note": "" },
    { "name": "key_secret", "note": "" },
]

DOCUMENTATION = """
module: certificate
short_description: Upload, update or delete a certificate in the Ionos Cloud Certificate Manager.
description:
     - This is a simple module that supports uploading, updating or deleting certificates in the
      Ionos Cloud Certificate Manager.
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
    certificate:
        description:
        - The certificate name or ID.
        required: false
    certificate_chain_file:
        description:
        - File containing the certificate chain.
        required: false
    certificate_file:
        description:
        - File containing the certificate body.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    certificate_name:
        description:
        - The certificate name.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    private_key_file:
        description:
        - File containing the private key blob.
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
    - "ionoscloud_cert_manager >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
name: Create Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  private_key_file: 'key.pem'
register: certificate
''',
    'update': '''
name: Create Certificate no change
ionoscloudsdk.ionoscloud.certificate:
  state: update
  certificate: ''
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  allow_replace: false
register: certificatenochange
''',
    'absent': '''
name: Delete Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate: ''
  state: absent
''',
}

EXAMPLES = """
name: Create Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  private_key_file: 'key.pem'
register: certificate


name: Create Certificate no change
ionoscloudsdk.ionoscloud.certificate:
  state: update
  certificate: ''
  certificate_name: 'test_certificate'
  certificate_file: 'certificate.pem'
  allow_replace: false
register: certificatenochange


name: Delete Certificate
ionoscloudsdk.ionoscloud.certificate:
  certificate: ''
  state: absent
"""


class CertificateProviderModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_cert_manager]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('provider_email') is not None
            and existing_object.properties.email != self.module.params.get('provider_email')
            or self.module.params.get('provider_server') is not None
            and existing_object.properties.server != self.module.params.get('provider_server')
            or self.module.params.get('key_id') is not None
            and existing_object.properties.external_account_binding.key_id != self.module.params.get('key_id')
            or self.module.params.get('key_secret') is not None
            and existing_object.properties.external_account_binding.key_secret != self.module.params.get('key_secret')
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('provider_name') is not None
            and existing_object.properties.name != self.module.params.get('provider_name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_cert_manager.ProviderApi(clients[0]).providers_get()


    def _get_object_name(self):
        return self.module.params.get('provider_name')


    def _get_object_identifier(self):
        return self.module.params.get('provider')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        provider_name = self.module.params.get('provider_name')
        provider_email = self.module.params.get('provider_email')
        provider_server = self.module.params.get('provider_server')
        provider_name = self.module.params.get('provider_name')
        key_id = self.module.params.get('key_id')
        key_secret = self.module.params.get('key_secret')

        if existing_object is not None:
            provider_name = existing_object.properties.name if provider_name is None else provider_name
            provider_email = existing_object.properties.email if provider_email is None else provider_email
            provider_server = existing_object.properties.server if provider_server is None else provider_server
            provider_name = existing_object.properties.name if provider_name is None else provider_name
            key_id = existing_object.properties.external_account_binding.key_id if key_id is None else key_id
            key_secret = existing_object.properties.external_account_binding.key_secret if key_secret is None else key_secret

        provider_api = ionoscloud_cert_manager.ProviderApi(client)

        try:
            new_provider = provider_api.providers_post(
                ionoscloud_cert_manager.ProviderCreate(
                    properties=ionoscloud_cert_manager.Provider(
                        name=provider_name,
                        email=provider_email,
                        server=provider_server,
                        external_account_binding=ionoscloud_cert_manager.ProviderExternalAccountBinding(
                            key_id=key_id,
                            key_secret=key_secret,
                        )
                    ),
                ),
            )
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(self.object_name, to_native(e)))
        return new_provider


    def _update_object(self, existing_object, clients):
        client = clients[0]
        try:
            updated_certificate = ionoscloud_cert_manager.ProviderApi(client).providers_patch(
                existing_object.id,
                ionoscloud_cert_manager.ProviderPatch(
                    properties=ionoscloud_cert_manager.PatchName(
                        name=self.module.params.get('provider_name'),
                    ),
                ),
            )

            return updated_certificate
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(self.object_name, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        try:
            ionoscloud_cert_manager.ProviderApi(client).providers_delete(existing_object.id)
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to remove the {}: {}".format(self.object_name, to_native(e)))


if __name__ == '__main__':
    ionos_module = CertificateProviderModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_cert_manager is required for this module, run `pip install ionoscloud_cert_manager`')
    ionos_module.main()
