HAS_SDK = True
try:
    import ionoscloud_dns
    from ionoscloud_dns import __version__ as sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import default_main_info, get_resource_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_info_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dns/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'dns'
STATES = ['info']
OBJECT_NAME = 'DNS Secondary Zones'
RETURNED_KEY = 'zones'

OPTIONS = {
    **get_info_default_options(STATES),
}



DOCUMENTATION = """
module: dns_secondary_zone_info
short_description: List Ionos Cloud DNS Secondary Zones.
description:
     - This is a simple module that supports listing DNS Secondary Zones.
version_added: "2.0"
options:
    iowluehfgbiowrgehf
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLES = """
    - name: Get all DNS Secondary Zones
      dns_zone_info:
      register: dns_zone_list_response
"""


def get_objects(module, client):
    return ionoscloud_dns.SecondaryZonesApi(client).secondaryzones_get()


if __name__ == '__main__':
    default_main_info(
        ionoscloud_dns, 'ionoscloud_dns', USER_AGENT, HAS_SDK, OPTIONS,
        STATES, OBJECT_NAME, RETURNED_KEY, get_objects,
    )
