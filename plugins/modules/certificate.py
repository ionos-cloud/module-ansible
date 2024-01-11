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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, _get_request_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-certificate-manager/%s' % ( __version__, certificate_manager_sdk_version)
DOC_DIRECTORY = 'certificate'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Certificate'
RETURNED_KEY = 'certificate'

OPTIONS = {
    'certificate': {
        'description': ['The certificate name or ID.'],
        'available': ['update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'certificate_name': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'certificate_file': {
        'description': ['File containing the certificate body.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'private_key_file': {
        'description': ['File containing the private key blob.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'certificate_chain_file': {
        'description': ['File containing the certificate chain.'],
        'available': ['present'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "certificate_file", "note": "" },
    { "name": "certificate_chain_file", "note": "" },
    {
        "name": "private_key_file",
        "note": "Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!",
    },
]

DOCUMENTATION = """
module: certificate
short_description: Upload, update or delete a certificate in the Ionos Cloud Certificate Manager.
description:
     - This is a simple module that supports uploading, updating or deleting certificates in the
      Ionos Cloud Certificate Manager.
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud_cert_manager >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
    - name: Create Certificate
        certificate:
            certificate_name: CertificateName
            certificate_file: "certificate.pem"
            private_key_file: "key.pem"
        register: certificate
  ''',
    'update': '''
    - name: Update Certificate
        certificate:
            certificate: CertificateName
            certificate_name: CertificateNewName
            state: update
        register: updated_certificate
  ''',
    'absent': '''
    - name: Delete Certificate
        certificate:
            certificate: CertificateNewName
            state: delete
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class CertificateModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_cert_manager]
        self.user_agent = USER_AGENT
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        certificate_file = self.module.params.get('certificate_file')
        certificate_chain_file = self.module.params.get('certificate_chain_file')

        certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None
        certificate=open(certificate_file, mode='r').read() if certificate_file else None

        return (
            certificate is not None
            and existing_object.properties.certificate.rstrip() != certificate.rstrip()
            or certificate_chain is not None
            and existing_object.properties.certificate_chain.rstrip() != certificate_chain.rstrip()
            or self.module.params.get('private_key_file')
        )


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('certificate_name') is not None
            and existing_object.properties.name != self.module.params.get('certificate_name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_cert_manager.CertificatesApi(clients[0]).certificates_get()


    def _get_object_name(self):
        return self.module.params.get('certificate_name')


    def _get_object_identifier(self):
        return self.module.params.get('certificate')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        certificate_file = self.module.params.get('certificate_file')
        private_key_file = self.module.params.get('private_key_file')
        certificate_chain_file = self.module.params.get('certificate_chain_file')
        certificate_name = self.module.params.get('certificate_name')

        certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None
        certificate=open(certificate_file, mode='r').read()

        if existing_object is not None:
            certificate_name = existing_object.properties.certificate_name if certificate_name is None else certificate_name
            certificate_chain = existing_object.properties.certificate_chain if certificate_chain is None else certificate_chain
            certificate = existing_object.properties.certificate if certificate is None else certificate

        certificates_api = ionoscloud_cert_manager.CertificatesApi(client)

        try:
            new_certificate = certificates_api.certificates_post(
                ionoscloud_cert_manager.CertificatePostDto(
                    properties=ionoscloud_cert_manager.CertificatePostPropertiesDto(
                        name=certificate_name,
                        certificate=certificate,
                        certificate_chain=certificate_chain,
                        private_key=open(private_key_file, mode='r').read(),
                    ),
                ),
            )
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to create the new certificate: %s" % to_native(e))
        return new_certificate


    def _update_object(self, existing_object, clients):
        client = clients[0]
        try:
            updated_certificate = ionoscloud_cert_manager.CertificatesApi(client).certificates_patch(
                existing_object.id,
                ionoscloud_cert_manager.CertificatePatchDto(
                    properties=ionoscloud_cert_manager.CertificatePatchPropertiesDto(
                        name=self.module.params.get('certificate_name'),
                    ),
                ),
            )

            return updated_certificate
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to update the certificate: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        try:
            ionoscloud_cert_manager.CertificatesApi(client).certificates_delete(existing_object.id)
        except ionoscloud_cert_manager.ApiException as e:
            self.module.fail_json(msg="failed to remove the certificate: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = CertificateModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_cert_manager is required for this module, run `pip install ionoscloud_cert_manager`')
    ionos_module.main()
