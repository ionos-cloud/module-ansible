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
DOC_DIRECTORY = 'certificate'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Auto Certificate'
RETURNED_KEY = 'auto_certificate'

OPTIONS = {
    'auto_certificate': {
        'description': ['The certificate name or ID.'],
        'available': ['update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'certificate_name': {
        'description': ['A certificate name used for management purposes.'],
        'available': ['present', 'update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'common_name': {
        'description': ['The common name (DNS) of the certificate to issue. The common name needs to be part of a zone in IONOS Cloud DNS.'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    'provider': {
        'description': ['The certificate provider used to issue the certificates.'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    'key_algorithm': {
        'description': ['The key algorithm used to generate the certificate.'],
        'available': ['present', 'update', 'absent'],
        'type': 'str',
    },
    'subject_alternative_names': {
        'description': ['Optional additional names to be added to the issued certificate. The additional names needs to be part of a zone in IONOS Cloud DNS.'],
        'available': ['present', 'update', 'absent'],
        'type': 'list',
        'elements': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "common_name", "note": "" },
    { "name": "provider", "note": "" },
    { "name": "key_algorithm", "note": "" },
    { "name": "subject_alternative_names", "note": "" },
]


DOCUMENTATION = """
module: auto_certificate
short_description: Upload, update or delete an Auto Certificate in the Ionos Cloud Certificate Manager.
description:
     - This is a simple module that supports uploading, updating or deleting Auto Certificates in the
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
    auto_certificate:
        description:
        - The certificate name or ID.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    certificate_name:
        description:
        - A certificate name used for management purposes.
        required: false
    common_name:
        description:
        - The common name (DNS) of the certificate to issue. The common name needs to
            be part of a zone in IONOS Cloud DNS.
        required: false
    key_algorithm:
        description:
        - The key algorithm used to generate the certificate.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    provider:
        description:
        - The certificate provider used to issue the certificates.
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
    subject_alternative_names:
        description:
        - Optional additional names to be added to the issued certificate. The additional
            names needs to be part of a zone in IONOS Cloud DNS.
        elements: str
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
name: Create Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  certificate_name: 'autoCertificateTest'
  common_name: 'devsdkionos.net'
  provider: ''
  key_algorithm: 'rsa4096'
  allow_replace: true
register: auto_certificate
''',
    'update': '''
name: Update Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: ''
  certificate_name: 'autoCertificateTestUpdated'
  allow_replace: false
  state: update
register: auto_certificate_update
''',
    'absent': '''
name: Delete Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: 'autoCertificateTestUpdated'
  wait: true
  state: absent
''',
}

EXAMPLES = """
name: Create Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  certificate_name: 'autoCertificateTest'
  common_name: 'devsdkionos.net'
  provider: ''
  key_algorithm: 'rsa4096'
  allow_replace: true
register: auto_certificate


name: Update Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: ''
  certificate_name: 'autoCertificateTestUpdated'
  allow_replace: false
  state: update
register: auto_certificate_update


name: Delete Auto Certificate
ionoscloudsdk.ionoscloud.auto_certificate:
  auto_certificate: 'autoCertificateTestUpdated'
  wait: true
  state: absent
"""


class AutoCertificateModule(CommonIonosModule):
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
            self.module.params.get('common_name') is not None
            and existing_object.properties.common_name != self.module.params.get('common_name')
            or self.module.params.get('provider') is not None
            and existing_object.properties.provider != self.module.params.get('provider')
            or self.module.params.get('key_algorithm') is not None
            and existing_object.properties.key_algorithm != self.module.params.get('key_algorithm')
            or self.module.params.get('subject_alternative_names') is not None
            and sorted(existing_object.properties.subject_alternative_names) != sorted(self.module.params.get('subject_alternative_names'))
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('certificate_name') is not None
            and existing_object.properties.name != self.module.params.get('certificate_name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_cert_manager.AutoCertificateApi(clients[0]).auto_certificates_get()


    def _get_object_name(self):
        return self.module.params.get('certificate_name')


    def _get_object_identifier(self):
        return self.module.params.get('auto_certificate')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        certificate_name = self.module.params.get('certificate_name')
        common_name = self.module.params.get('common_name')
        provider = self.module.params.get('provider')
        key_algorithm = self.module.params.get('key_algorithm')
        subject_alternative_names = self.module.params.get('subject_alternative_names')

        if existing_object is not None:
            certificate_name = existing_object.properties.name if certificate_name is None else certificate_name
            common_name = existing_object.properties.common_name if common_name is None else common_name
            provider = existing_object.properties.provider if provider is None else provider
            key_algorithm = existing_object.properties.key_algorithm if key_algorithm is None else key_algorithm
            subject_alternative_names = existing_object.properties.subject_alternative_names if subject_alternative_names is None else subject_alternative_names

        certificates_api = ionoscloud_cert_manager.AutoCertificateApi(client)
        try:
            new_certificate = certificates_api.auto_certificates_post(
                ionoscloud_cert_manager.AutoCertificateCreate(
                    properties=ionoscloud_cert_manager.AutoCertificate(
                        provider=provider,
                        common_name=common_name,
                        key_algorithm=key_algorithm,
                        name=certificate_name,
                        subject_alternative_names=subject_alternative_names,
                    ),
                ),
            )

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: certificates_api.auto_certificates_find_by_id(new_certificate.id).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )

        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(self.object_name, to_native(e)))
        return new_certificate


    def _update_object(self, existing_object, clients):
        client = clients[0]
        try:
            certificates_api = ionoscloud_cert_manager.AutoCertificateApi(client)
            updated_certificate = certificates_api.auto_certificates_patch(
                existing_object.id,
                ionoscloud_cert_manager.AutoCertificatePatch(
                    properties=ionoscloud_cert_manager.PatchName(
                        name=self.module.params.get('certificate_name'),
                    ),
                ),
            )
            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: certificates_api.auto_certificates_find_by_id(updated_certificate.id).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )

            return updated_certificate
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to update the {}: {}".format(self.object_name, to_native(e)))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        try:
            certificates_api = ionoscloud_cert_manager.AutoCertificateApi(client)
            certificates_api.auto_certificates_delete(existing_object.id)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: certificates_api.auto_certificates_get(),
                    fn_check=lambda r: len(list(filter(
                        lambda e: e.id == existing_object.id,
                        r.items
                    ))) < 1,
                    console_print='.',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to remove the {}: {}".format(self.object_name, to_native(e)))


if __name__ == '__main__':
    ionos_module = AutoCertificateModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_cert_manager is required for this module, run `pip install ionoscloud_cert_manager`')
    ionos_module.main()
