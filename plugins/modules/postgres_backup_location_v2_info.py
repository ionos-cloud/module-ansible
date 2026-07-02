from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


HAS_SDK = True
try:
    import ionoscloud_dbaas_postgres
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_sdk-python-dbaas-postgres/%s' % (
    __version__, ionoscloud_dbaas_postgres.__version__)
DOC_DIRECTORY = 'dbaas-postgres'
STATES = ['info']
OBJECT_NAME = 'Postgres Backup Locations (v2)'
RETURNED_KEY = 'postgres_backup_locations'

OPTIONS = {
    'location': {
        'description': ['The location (region) whose regional endpoint will be queried. Possible options are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr", "us/las", "us/mci". If not set, the endpoint will be the one corresponding to "de/txl". The api_url, if set, overrides this.'],
        'available': STATES,
        'type': 'str',
    },
    **get_info_default_options(STATES),
}


DOCUMENTATION = """
module: postgres_backup_location_v2_info
short_description: List Postgres Backup Locations (DBaaS PostgreSQL v2 API)
description:
     - This is a simple module that supports listing the Object Storage locations where
       Postgres Cluster backups can be stored, using the DBaaS PostgreSQL v2 API. The
       region is selected through the I(location) option; set I(api_url) (e.g. C(https://postgresql.de-fra.ionos.com)) to override it directly.
version_added: "2.0"
options:
    location:
        description:
        - 'The location (region) whose regional endpoint will be queried. Possible options
            are: "de/fra", "de/txl", "es/vit", "fr/par", "gb/lhr", "gb/bhx", "us/ewr",
            "us/las", "us/mci". If not set, the endpoint will be the one corresponding to
            "de/txl". The api_url, if set, overrides this.'
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
    filters:
        description:
        - 'Filter that can be used to list only objects which have a certain set of properties.
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
    - "python >= 3.8"
    - "ionoscloud-dbaas-postgres >= 3.0.0"
author:
    - "IONOS CLOUD SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
name: List Postgres Backup Locations (pick a valid backup_location from here)
ionoscloudsdk.ionoscloud.postgres_backup_location_v2_info:
  location: ''
register: postgres_backup_locations_response
"""


def get_objects(module, client):
    return ionoscloud_dbaas_postgres.BackupLocationsApi(client).backuplocations_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dbaas_postgres, 'ionoscloud_dbaas_postgres', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
