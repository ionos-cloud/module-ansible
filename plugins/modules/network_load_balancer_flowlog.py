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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'networkloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Flowlog'
RETURNED_KEY = 'flowlog'

OPTIONS = {
    'name': {
        'description': ['The resource name.'],
        'available': STATES,
        'required': ['present'],
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
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'network_load_balancer': {
        'description': ['The ID or name of the Network Loadbalancer.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'flowlog': {
        'description': ['The ID or name of the Flowlog.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: network_load_balancer_flowlog
short_description: Create or destroy a Ionos Cloud NetworkLoadbalancer Flowlog.
description:
     - This is a simple module that supports creating or removing NetworkLoadbalancer Flowlogs.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    action:
        description:
        - Specifies the traffic action pattern.
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
        - The ID or name of the datacenter.
        required: true
    direction:
        description:
        - Specifies the traffic direction pattern.
        required: false
    flowlog:
        description:
        - The ID or name of the Flowlog.
        required: false
    name:
        description:
        - The resource name.
        required: false
    network_load_balancer:
        description:
        - The ID or name of the Network Loadbalancer.
        required: true
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
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
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''name: Create Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  name: 'AnsibleAutoTestNLB'
  action: ACCEPTED
  direction: INGRESS
  bucket: sdktest
  datacenter: ''
  network_load_balancer: ''
  wait: true
register: nlb_flowlog_response
''',
  'update' : '''name: Update Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  datacenter: ''
  network_load_balancer: ''
  flowlog: ''
  name: 'AnsibleAutoTestNLB'
  action: ALL
  direction: INGRESS
  bucket: sdktest
  wait: true
  state: update
register: nlb_flowlog_update_response
''',
  'absent' : '''name: Delete Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  datacenter: ''
  network_load_balancer: ''
  flowlog: ''
  state: absent
''',
}

EXAMPLES = """name: Create Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  name: 'AnsibleAutoTestNLB'
  action: ACCEPTED
  direction: INGRESS
  bucket: sdktest
  datacenter: ''
  network_load_balancer: ''
  wait: true
register: nlb_flowlog_response

name: Update Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  datacenter: ''
  network_load_balancer: ''
  flowlog: ''
  name: 'AnsibleAutoTestNLB'
  action: ALL
  direction: INGRESS
  bucket: sdktest
  wait: true
  state: update
register: nlb_flowlog_update_response

name: Delete Network Load Balancer Flowlog
ionoscloudsdk.ionoscloud.network_load_balancer_flowlog:
  datacenter: ''
  network_load_balancer: ''
  flowlog: ''
  state: absent
"""


class NetworkLoadBalancerFlowlogModule(CommonIonosModule):
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
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        return ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_flowlogs_get(
            datacenter_id, network_load_balancer_id, depth=1,
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
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            action = existing_object.properties.type if action is None else action
            direction = existing_object.properties.direction if direction is None else direction
            bucket = existing_object.properties.bucket if bucket is None else bucket

        network_loadbalancers_api = ionoscloud.NetworkLoadBalancersApi(client)
        
        nlb_flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)
        nlb_flowlog = FlowLog(properties=nlb_flowlog_properties)

        try:
            response, _, headers = network_loadbalancers_api.datacenters_networkloadbalancers_flowlogs_post_with_http_info(
                datacenter_id, network_load_balancer_id, nlb_flowlog,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Network Loadbalancer Flowlog: %s" % to_native(e))
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
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        network_loadbalancers_api = ionoscloud.NetworkLoadBalancersApi(client)

        flowlog_properties = FlowLogProperties(name=name, action=action, direction=direction, bucket=bucket)

        try:
            response, _, headers = network_loadbalancers_api.datacenters_networkloadbalancers_flowlogs_patch_with_http_info(
                datacenter_id, network_load_balancer_id, existing_object.id, flowlog_properties,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Network Loadbalancer Flowlog: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        network_load_balancer_id = get_resource_id(
            self.module, 
            ionoscloud.NetworkLoadBalancersApi(client).datacenters_networkloadbalancers_get(
                datacenter_id, depth=1,
            ),
            self.module.params.get('network_load_balancer'),
        )

        network_loadbalancers_api = ionoscloud.NetworkLoadBalancersApi(client)

        try:
            _, _, headers = network_loadbalancers_api.datacenters_networkloadbalancers_flowlogs_delete_with_http_info(
                datacenter_id, network_load_balancer_id, existing_object.id,
            )

            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Network Loadbalancer Flowlog: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = NetworkLoadBalancerFlowlogModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
