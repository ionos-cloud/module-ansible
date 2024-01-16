#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import FlowLog, FlowLogProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, _get_request_id, get_resource_id,
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
OBJECT_NAME = 'Flowlog'
RETURNED_KEY = 'flowlog'

OPTIONS = {
    'name': {
        'description': ['The resource name.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'flowlog': {
        'description': ['The ID or name of an existing Flowlog.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The ID or name of the virtual datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'server': {
        'description': ['The ID or name of the Server.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'nic': {
        'description': ['The ID or name of the NIC.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'action': {
        'description': ['Specifies the traffic action pattern.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'direction': {
        'description': ['Specifies the traffic direction pattern.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'bucket': {
        'description': ['The S3 bucket name of an existing IONOS Cloud S3 bucket.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: datacenter
short_description: Create or destroy a Ionos Cloud NIC Flowlog.
description:
     - This is a simple module that supports creating or removing NIC Flowlogs.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    action:
        description:
        - Specifies the traffic action pattern.
        required: false
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
    bucket:
        description:
        - The S3 bucket name of an existing IONOS Cloud S3 bucket.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    datacenter:
        description:
        - The ID or name of the virtual datacenter.
        required: true
    direction:
        description:
        - Specifies the traffic direction pattern.
        required: false
    flowlog:
        description:
        - The ID or name of an existing Flowlog.
        required: false
    name:
        description:
        - The resource name.
        required: false
    nic:
        description:
        - The ID or name of the NIC.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    server:
        description:
        - The ID or name of the Server.
        required: true
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
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''- name: Create a nic flowlog
  nic_flowlog:
    name: FlowlogName
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
  register: flowlog_response
  ''',
    'update': '''- name: Update a nic flowlog
  nic_flowlog:
    name: "FlowlogName"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
  register: flowlog_update_response
  ''',
    'absent': '''- name: Delete a nic flowlog
  nic_flowlog:
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
    name: "FlowlogName"
    state: absent
    wait: true
  register: flowlog_delete_response
  ''',
}

EXAMPLES = """- name: Create a nic flowlog
  nic_flowlog:
    name: FlowlogName
    action: "ACCEPTED"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
  register: flowlog_response
  
- name: Update a nic flowlog
  nic_flowlog:
    name: "FlowlogName"
    action: "ALL"
    direction: "INGRESS"
    bucket: "sdktest"
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
  register: flowlog_update_response
  
- name: Delete a nic flowlog
  nic_flowlog:
    datacenter: DatacenterName
    server: ServerName
    nic: NicName
    flowlog: FlowlogName
    name: "FlowlogName"
    state: absent
    wait: true
  register: flowlog_delete_response
"""

class NicFlowlogModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('action') is not None
            and existing_object.properties.action != self.module.params.get('action')
            or self.module.params.get('direction') is not None
            and existing_object.properties.direction != self.module.params.get('direction')
            or self.module.params.get('bucket') is not None
            and existing_object.properties.bucket != self.module.params.get('bucket')
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        server_id = get_resource_id(
            self.module, 
            ionoscloud.ServersApi(client).datacenters_servers_get(datacenter_id, depth=1),
            self.module.params.get('server'),
        )
        nic_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkInterfacesApi(client).datacenters_servers_nics_get(
                datacenter_id, server_id, depth=1,
            ),
            self.module.params.get('nic'),
        )

        return ionoscloud.FlowLogsApi(client).datacenters_servers_nics_flowlogs_get(
            datacenter_id=datacenter_id, server_id=server_id, nic_id=nic_id, depth=1
        )


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('flowlog')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        action = self.module.params.get('action')
        direction = self.module.params.get('direction')
        bucket = self.module.params.get('bucket')
        if existing_object is not None:
            action = existing_object.properties.action if action is None else action
            direction = existing_object.properties.direction if direction is None else direction
            bucket = existing_object.properties.bucket if bucket is None else bucket
            name = existing_object.properties.name if name is None else name

        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        server_id = get_resource_id(
            self.module, 
            ionoscloud.ServersApi(client).datacenters_servers_get(datacenter_id, depth=1),
            self.module.params.get('server'),
        )
        nic_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkInterfacesApi(client).datacenters_servers_nics_get(
                datacenter_id, server_id, depth=1,
            ),
            self.module.params.get('nic'),
        )

        nic_flowlogs_api = ionoscloud.FlowLogsApi(client)

        flowlog = FlowLog(properties=FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket))

        try:
            response, _, headers = nic_flowlogs_api.datacenters_servers_nics_flowlogs_post_with_http_info(
                datacenter_id, server_id, nic_id, flowlog,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Flowlog: %s" % to_native(e))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        action = self.module.params.get('action')
        direction = self.module.params.get('direction')
        bucket = self.module.params.get('bucket')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        server_id = get_resource_id(
            self.module, 
            ionoscloud.ServersApi(client).datacenters_servers_get(datacenter_id, depth=1),
            self.module.params.get('server'),
        )
        nic_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkInterfacesApi(client).datacenters_servers_nics_get(
                datacenter_id, server_id, depth=1,
            ),
            self.module.params.get('nic'),
        )

        nic_flowlogs_api = ionoscloud.FlowLogsApi(api_client=client)

        flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)

        try:
            response, _, headers = nic_flowlogs_api.datacenters_servers_nics_flowlogs_patch_with_http_info(
                datacenter_id, server_id, nic_id, existing_object.id, flowlog_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Flowlog: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        server_id = get_resource_id(
            self.module, 
            ionoscloud.ServersApi(client).datacenters_servers_get(datacenter_id, depth=1),
            self.module.params.get('server'),
        )
        nic_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkInterfacesApi(client).datacenters_servers_nics_get(
                datacenter_id, server_id, depth=1,
            ),
            self.module.params.get('nic'),
        )

        nic_flowlogs_api = ionoscloud.FlowLogsApi(api_client=client)

        try:
            _, _, headers = nic_flowlogs_api.datacenters_servers_nics_flowlogs_delete_with_http_info(
                datacenter_id, server_id, nic_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Flowlog: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NicFlowlogModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
