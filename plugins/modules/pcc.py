HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import PrivateCrossConnect
    from ionoscloud.models import PrivateCrossConnectProperties
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
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, sdk_version)
DOC_DIRECTORY = 'compute-engine'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'PCC'
RETURNED_KEY = 'pcc'

OPTIONS = {
    'name': {
        'description': ['The name of the Cross Connect.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'pcc': {
        'description': ['The ID or name of an existing PCC.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'description': {
        'description': ['Human-readable description of the Cross Connect.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: pcc
short_description: Create or destroy a Ionos Cloud Cross Connect
description:
     - This is a simple module that supports creating or removing Cross Connects.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''
  - name: Create pcc
    pcc:
      name: PCCName
      description: "Description for my PCC"
  ''',
    'update': '''
  - name: Update pcc
    pcc:
      pcc: PCCName
      name: NewPCCName
      description: "New description for my PCC"
      state: update
  ''',
    'absent': '''
  - name: Remove pcc
    pcc:
      pcc: NewPCCName
      state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class PccModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agent = USER_AGENT
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('description') is not None
            and existing_object.properties.description != self.module.params.get('description')
        )


    def _get_object_list(self, clients):
        return ionoscloud.PrivateCrossConnectsApi(clients[0]).pccs_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('pcc')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            description = existing_object.properties.description if description is None else description

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        pccs_api = ionoscloud.PrivateCrossConnectsApi(client)

        pcc = PrivateCrossConnect(properties=PrivateCrossConnectProperties(name=name, description=description))

        try:
            pcc_response, _, headers = pccs_api.pccs_post_with_http_info(pcc)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new PCC: %s" % to_native(e))
        return pcc_response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        description = self.module.params.get('description')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        pccs_api = ionoscloud.PrivateCrossConnectsApi(client)

        pcc_properties = PrivateCrossConnectProperties(name=name, description=description)

        try:
            pcc_response, _, headers = pccs_api.pccs_patch_with_http_info(
                pcc_id=existing_object.id,
                pcc=pcc_properties,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return pcc_response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the PCC: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        pccs_api = ionoscloud.PrivateCrossConnectsApi(client)

        try:
            _, _, headers = pccs_api.pccs_delete_with_http_info(existing_object.id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the PCC: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = PccModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
