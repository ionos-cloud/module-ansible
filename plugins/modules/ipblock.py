#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import IpBlock, IpBlockProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent']
OBJECT_NAME = 'IP Block'
RETURNED_KEY = 'ipblock'

OPTIONS = {
    'ipblock': {
        'description': ['The name or ID of an existing IPBlock.'],
        'required': ['absent'],
        'available': ['absent'],
        'type': 'str',
    },
    'name': {
        'description': ['The name of the  resource.'],
        'available': STATES,
        'type': 'str',
    },
    'location': {
        'description': ['Location of that IP block. Property cannot be modified after it is created (disallowed in update requests).'],
        'required': ['present'],
        'choices': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'],
        'available': ['present'],
        'type': 'str',
    },
    'size': {
        'description': ['The size of the IP block.'],
        'available': ['present'],
        'type': 'int',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "size", "note": "" },
    { "name": "location", "note": "" },
]

DOCUMENTATION = """
module: ipblock
short_description: Create or remove an IPBlock.
description:
     - This module allows you to create or remove an IPBlock.
version_added: "2.4"
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
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    ipblock:
        description:
        - The name or ID of an existing IPBlock.
        required: false
    location:
        choices:
        - us/las
        - us/ewr
        - de/fra
        - de/fkb
        - de/txl
        - gb/lhr
        description:
        - Location of that IP block. Property cannot be modified after it is created (disallowed
            in update requests).
        required: false
    name:
        description:
        - The name of the  resource.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    size:
        description:
        - The size of the IP block.
        required: false
    state:
        choices:
        - present
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
  'present' : '''# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  ''',
  'absent' : '''# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    ipblock: staging
    state: absent
  ''',
}

EXAMPLES = """# Create an IPBlock
- name: Create IPBlock
  ipblock:
    name: staging
    location: us/ewr
    size: 2
    state: present
  
# Remove an IPBlock
- name: Remove IPBlock
  ipblock:
    ipblock: staging
    state: absent
"""


class IPBlockModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
            self.module.params.get('size') is not None
            and existing_object.properties.size != self.module.params.get('size')
            or self.module.params.get('location') is not None
            and existing_object.properties.location != self.module.params.get('location')
        )


    def _should_update_object(self, existing_object, clients):
        return False


    def _get_object_list(self, clients):
        return ionoscloud.IPBlocksApi(clients[0]).ipblocks_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('ipblock')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        location = self.module.params.get('location')
        size = self.module.params.get('size')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            location = existing_object.properties.location if location is None else location
            size = existing_object.properties.size if size is None else size

        ipblock_properties = IpBlockProperties(location=location, size=size, name=name)
        ipblock = IpBlock(properties=ipblock_properties)

        ipblocks_api = ionoscloud.IPBlocksApi(client)

        try:
            ipblock_response, _, headers = ipblocks_api.ipblocks_post_with_http_info(ipblock)

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
        return ipblock_response


    def _remove_object(self, existing_object, clients):
        ipblocks_api = ionoscloud.IPBlocksApi(clients[0])

        try:
            ipblocks_api.ipblocks_delete(existing_object.id)
        except Exception as e:
            self.module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


if __name__ == '__main__':
    ionos_module = IPBlockModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
