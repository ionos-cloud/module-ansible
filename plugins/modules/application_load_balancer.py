#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import re
import yaml

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import ApplicationLoadBalancer, ApplicationLoadBalancerProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError as e:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id, _get_request_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'applicationloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Application Load Balancer'
RETURNED_KEY = 'application_load_balancer'

OPTIONS = {
    'name': {
        'description': ['The Application Load Balancer name.'],
        'available': STATES,
        'required': ['present', 'update'],
        'type': 'str',
    },
    'listener_lan': {
        'description': ['The ID of the listening (inbound) LAN.'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'ips': {
        'description': ['Collection of the Application Load Balancer IP addresses. (Inbound and outbound) IPs of the \'listenerLan\' are customer-reserved public IPs for the public load balancers, and private IPs for the private load balancers.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'target_lan': {
        'description': ['The ID of the balanced private target LAN (outbound).'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'lb_private_ips': {
        'description': ['Collection of private IP addresses with the subnet mask of the Application Load Balancer. IPs must contain valid a subnet mask. If no IP is provided, the system will generate an IP with /24 subnet.'],
        'available': ['present', 'update'],
        'type': 'list',
    },
    'datacenter': {
        'description': ['The ID or name of the datacenter.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'application_load_balancer': {
        'description': ['The ID or name of the Application Loadbalancer.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}


DOCUMENTATION = '''
---
module: application_load_balancer
short_description: Create or destroy a Ionos Cloud Application Loadbalancer.
description:
     - This is a simple module that supports creating or removing Application Loadbalancers.
version_added: "2.0"
options:
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    application_load_balancer:
        description:
        - The ID or name of the Application Loadbalancer.
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
    ips:
        description:
        - Collection of the Application Load Balancer IP addresses. (Inbound and outbound)
            IPs of the 'listenerLan' are customer-reserved public IPs for the public load
            balancers, and private IPs for the private load balancers.
        required: false
    lb_private_ips:
        description:
        - Collection of private IP addresses with the subnet mask of the Application Load
            Balancer. IPs must contain valid a subnet mask. If no IP is provided, the
            system will generate an IP with /24 subnet.
        required: false
    listener_lan:
        description:
        - The ID of the listening (inbound) LAN.
        required: false
    name:
        description:
        - The Application Load Balancer name.
        required: false
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
    target_lan:
        description:
        - The ID of the balanced private target LAN (outbound).
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
    - "ionoscloud >= 6.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
name: Create Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  datacenter: ''
  name: 'AnsibleAutoTestALB'
  ips:
  - 10.12.118.224
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
register: alb_response
''',
  'update' : '''
name: Update Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  datacenter: 'AnsibleAutoTestALB'
  application_load_balancer: ''
  name: 'AnsibleAutoTestALB - UPDATE'
  listener_lan: ''
  target_lan: ''
  wait: true
  state: update
  wait_timeout: 2000
register: alb_response_update
''',
  'absent' : '''
name: Remove Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  application_load_balancer: 'AnsibleAutoTestALB - UPDATE'
  datacenter: ''
  wait: true
  wait_timeout: 2000
  state: absent
''',
}

EXAMPLES = """
name: Create Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  datacenter: ''
  name: 'AnsibleAutoTestALB'
  ips:
  - 10.12.118.224
  listener_lan: ''
  target_lan: ''
  wait: true
  wait_timeout: 2000
register: alb_response


name: Update Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  datacenter: 'AnsibleAutoTestALB'
  application_load_balancer: ''
  name: 'AnsibleAutoTestALB - UPDATE'
  listener_lan: ''
  target_lan: ''
  wait: true
  state: update
  wait_timeout: 2000
register: alb_response_update


name: Remove Application Load Balancer
ionoscloudsdk.ionoscloud.application_load_balancer:
  application_load_balancer: 'AnsibleAutoTestALB - UPDATE'
  datacenter: ''
  wait: true
  wait_timeout: 2000
  state: absent
"""


class ApplicationLoadBalancerModule(CommonIonosModule):
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
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        listener_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('listener_lan'),
        )
        target_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('target_lan'),
        )

        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('ips') is not None
            and sorted(existing_object.properties.ips) != sorted(self.module.params.get('ips'))
            or self.module.params.get('lb_private_ips') is not None
            and sorted(existing_object.properties.lb_private_ips) != sorted(self.module.params.get('lb_private_ips'))
            or listener_lan is not None
            and existing_object.properties.listener_lan != int(listener_lan)
            or target_lan is not None
            and existing_object.properties.target_lan != int(target_lan)
        )


    def _get_object_list(self, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        return ionoscloud.ApplicationLoadBalancersApi(client).datacenters_applicationloadbalancers_get(
            datacenter_id, depth=1,
        )


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('application_load_balancer')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        ips = self.module.params.get('ips')
        lb_private_ips = self.module.params.get('lb_private_ips')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        listener_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('listener_lan'),
        )
        target_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('target_lan'),
        )
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            ips = existing_object.properties.ips if ips is None else ips
            listener_lan = existing_object.properties.listener_lan if listener_lan is None else listener_lan
            target_lan = existing_object.properties.target_lan if target_lan is None else target_lan
            lb_private_ips = existing_object.properties.lb_private_ips if lb_private_ips is None else lb_private_ips

        albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
        
        application_load_balancer = ApplicationLoadBalancer(properties=ApplicationLoadBalancerProperties(
            name=name, listener_lan=listener_lan, ips=ips,
            target_lan=target_lan, lb_private_ips=lb_private_ips,
        ))

        try:
            response, _, headers = albs_api.datacenters_applicationloadbalancers_post_with_http_info(
                datacenter_id, application_load_balancer,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=int(self.module.params.get('wait_timeout')))
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Application Loadbalancer: %s" % to_native(e))
        return response

    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        ips = self.module.params.get('ips')
        lb_private_ips = self.module.params.get('lb_private_ips')
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )
        listener_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('listener_lan'),
        )
        target_lan =  get_resource_id(
            self.module, 
            ionoscloud.LANsApi(client).datacenters_lans_get(datacenter_id, depth=1),
            self.module.params.get('target_lan'),
        )

        albs_api = ionoscloud.ApplicationLoadBalancersApi(client)
        
        alb_properties = ApplicationLoadBalancerProperties(
            name=name, listener_lan=listener_lan, ips=ips,
            target_lan=target_lan, lb_private_ips=lb_private_ips,
        )

        try:
            response, _, headers = albs_api.datacenters_applicationloadbalancers_patch_with_http_info(
                datacenter_id, existing_object.id, alb_properties,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Application Loadbalancer: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        datacenter_id = get_resource_id(
            self.module, 
            ionoscloud.DataCentersApi(client).datacenters_get(depth=1),
            self.module.params.get('datacenter'),
        )

        albs_api = ionoscloud.ApplicationLoadBalancersApi(client)

        try:
            _, _, headers = albs_api.datacenters_applicationloadbalancers_delete_with_http_info(
                datacenter_id, existing_object.id,
            )
            if self.module.params.get('wait'):
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=self.module.params.get('wait_timeout'))
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Application Loadbalancer: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = ApplicationLoadBalancerModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
