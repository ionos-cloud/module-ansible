#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
from tabnanny import check
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import Datacenter, DatacenterProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.shared import CommonIonosModule


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Datacenter'
RETURNED_KEY = 'datacenter'

OPTIONS = {
    'name': {
        'description': ['The name of the  resource.'],
        'required': ['present'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'description': {
        'description': ['A description for the datacenter, such as staging, production.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'location': {
        'description': ['The physical location where the datacenter will be created. This will be where all of your servers live. Property cannot be modified after datacenter creation (disallowed in update requests).'],
        'required': ['present'],
        'choices': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr', 'es/vit', 'fr/par'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The ID or name of the virtual datacenter.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'allow_replace': {
        'description': [
            'Boolean indincating if the resource should be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
        'available': STATES,
        'type': 'str',
    },
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
        'available': STATES,
        'type': 'str',
    },
    'username': {
        # Required if no token, checked manually
        'description': ['The Ionos username. Overrides the IONOS_USERNAME environment variable.'],
        'aliases': ['subscription_user'],
        'env_fallback': 'IONOS_USERNAME',
        'available': STATES,
        'type': 'str',
    },
    'password': {
        # Required if no token, checked manually
        'description': ['The Ionos password. Overrides the IONOS_PASSWORD environment variable.'],
        'aliases': ['subscription_password'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_PASSWORD',
        'type': 'str',
    },
    'token': {
        # If provided, then username and password no longer required
        'description': ['The Ionos token. Overrides the IONOS_TOKEN environment variable.'],
        'available': STATES,
        'no_log': True,
        'env_fallback': 'IONOS_TOKEN',
        'type': 'str',
    },
    'wait': {
        'description': ['Wait for the resource to be created before returning.'],
        'default': True,
        'available': STATES,
        'choices': [True, False],
        'type': 'bool',
    },
    'wait_timeout': {
        'description': ['How long before wait gives up, in seconds.'],
        'default': 600,
        'available': STATES,
        'type': 'int',
    },
    'state': {
        'description': ['Indicate desired state of the resource.'],
        'default': 'present',
        'choices': STATES,
        'available': STATES,
        'type': 'str',
    },
}

IMMUTABLE_OPTIONS = [
    { "name": "location", "note": "" },
]

def transform_for_documentation(val):
    val['required'] = len(val.get('required', [])) == len(STATES) 
    del val['available']
    del val['type']
    return val

DOCUMENTATION = '''
---
module: datacenter
short_description: Create or destroy a Ionos Cloud Virtual Datacenter.
description:
     - This is a simple module that supports creating or removing datacenters. A datacenter is required before you can create servers.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''# Create a Datacenter
  - name: Create datacenter
    datacenter:
      name: "Example DC"
      description: "description"
      location: de/fra
    register: datacenter_response
  ''',
  'update' : '''# Update a datacenter description
  - name: Update datacenter
    datacenter:
      datacenter: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  ''',
  'absent' : '''# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      datacenter: "Example DC"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


class DatacenterModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.options = OPTIONS
        self.states = STATES
        self.module = AnsibleModule(argument_spec=self.get_module_arguments())
        self.sdk = ionoscloud
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME


    def _should_replace_object(self, existing_object):
        return (
            self.module.params.get('location') is not None
            and existing_object.properties.location != self.module.params.get('location')
        )


    def _should_update_object(self, existing_object):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('description') is not None
            and existing_object.properties.description != self.module.params.get('description')
        )


    def _get_object_list(self, client):
        return ionoscloud.DataCentersApi(client).datacenters_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('datacenter')


    def _create_object(self, client, existing_object=None):
        name = self.module.params.get('name')
        location = self.module.params.get('location')
        description = self.module.params.get('description')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            location = existing_object.properties.location if location is None else location
            description = existing_object.properties.description if description is None else description

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        datacenters_api = ionoscloud.DataCentersApi(client)

        datacenter_properties = DatacenterProperties(name=name, description=description, location=location)
        datacenter = Datacenter(properties=datacenter_properties)

        try:
            datacenter_response, _, headers = datacenters_api.datacenters_post_with_http_info(datacenter=datacenter)
            if wait:
                request_id = self._get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
                datacenter_response = datacenters_api.datacenters_find_by_id(datacenter_response.id)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))
        return datacenter_response


    def _update_object(self, client, existing_object):
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        datacenters_api = ionoscloud.DataCentersApi(client)

        datacenter_properties=DatacenterProperties(name=name, description=description)

        try:
            datacenter_response, _, headers = datacenters_api.datacenters_patch_with_http_info(
                datacenter_id=existing_object.id,
                datacenter=datacenter_properties,
            )
            if wait:
                request_id = self._get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return datacenter_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the datacenter: %s" % to_native(e))


    def _remove_object(self, client, existing_object):
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        datacenters_api = ionoscloud.DataCentersApi(client)

        try:
            _, _, headers = datacenters_api.datacenters_delete_with_http_info(
                datacenter_id=existing_object.id,
            )
            if wait:
                request_id = self._get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the datacenter: %s" % to_native(e))


def main():
    module_model = DatacenterModule()

    if not HAS_SDK:
        module_model.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    state = module_model.module.params.get('state')
    with ApiClient(module_model.get_sdk_config()) as api_client:
        api_client.user_agent = USER_AGENT
        module_model.check_required_arguments(state)

        try:
            if state == 'absent':
                module_model.module.exit_json(**module_model.remove_object(api_client))
            elif state == 'present':
                module_model.module.exit_json(**module_model.create_object(api_client))
            elif state == 'update':
                module_model.module.exit_json(**module_model.update_object(api_client))
        except Exception as e:
            module_model.module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
