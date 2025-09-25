from ansible import __version__

HAS_SDK = True
try:
    import ionoscloud_cert_manager
    from ionoscloud_cert_manager import __version__ as certificate_manager_sdk_version
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-cert-manager/%s' % ( __version__, certificate_manager_sdk_version)
DOC_DIRECTORY = 'certificate'
STATES = ['info']
OBJECT_NAME = 'Certificate Providers'
RETURNED_KEY = 'certificate_providers'

OPTIONS = {
    **get_info_default_options(STATES),
}

DOCUMENTATION = """
module: certificate_provider_info
short_description: List Certificate Providers
description:
     - This is a simple module that supports listing uploaded Certificates
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
    filters:
        description:
        - 'Filter that can be used to list only objects which have a certain set of propeties.
            Filters should be a dict with a key containing keys and value pair in the
            following format: ''properties.name'': ''server_name'''
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
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
requirements:
    - "python >= 2.6"
    - "ionoscloud_cert_manager >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
name: List Certificate providers
ionoscloudsdk.ionoscloud.certificate_provider_info: null
register: certificate_providers_response
"""


def get_objects(module, client):
    return ionoscloud_cert_manager.ProviderApi(client).providers_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_cert_manager, 'ionoscloud_cert_manager', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )