#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import TargetGroup, TargetGroupTarget, TargetGroupProperties, \
        TargetGroupHealthCheck, TargetGroupHttpHealthCheck
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
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'applicationloadbalancer'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Target Group'
RETURNED_KEY = 'target_group'


OPTIONS = {
    'name': {
        'description': ['The target group name.'],
        'available': STATES,
        'required': ['present'],
        'type': 'str',
    },
    'algorithm': {
        'description': ['The balancing algorithm. A balancing algorithm consists of predefined rules with the logic that a load balancer uses to distribute network traffic between servers.  - **Round Robin**: Targets are served alternately according to their weighting.  - **Least Connection**: The target with the least active connection is served.  - **Random**: The targets are served based on a consistent pseudorandom algorithm.  - **Source IP**: It is ensured that the same client IP address reaches the same target.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'protocol': {
        'description': ['The forwarding protocol. Only the value \'HTTP\' is allowed.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'health_check': {
        'description': ['Health check properties for target group.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'http_health_check': {
        'description': ['HTTP health check properties for target group.'],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'targets': {
        'description': ['Array of items in the collection.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'target_group': {
        'description': ['The ID or name of the Target Group.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: target_hroup
short_description: Create or destroy a Ionos Cloud Target Group.
description:
     - This is a simple module that supports creating or removing Target Groups.
version_added: "2.0"
options:
    algorithm:
        description:
        - 'The balancing algorithm. A balancing algorithm consists of predefined rules
            with the logic that a load balancer uses to distribute network traffic between
            servers.  - **Round Robin**: Targets are served alternately according to their
            weighting.  - **Least Connection**: The target with the least active connection
            is served.  - **Random**: The targets are served based on a consistent pseudorandom
            algorithm.  - **Source IP**: It is ensured that the same client IP address
            reaches the same target.'
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
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    health_check:
        description:
        - Health check properties for target group.
        required: false
    http_health_check:
        description:
        - HTTP health check properties for target group.
        required: false
    name:
        description:
        - The target group name.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    protocol:
        description:
        - The forwarding protocol. Only the value 'HTTP' is allowed.
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
    target_group:
        description:
        - The ID or name of the Target Group.
        required: false
    targets:
        description:
        - Array of items in the collection.
        elements: dict
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
"""

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create Target Group
    target_group:
      name: "AnsibleAutoTestCompute"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      targets:
        - ip: "22.231.2.2"
          port: 8080
          weight: 123
          health_check_enabled: true
          maintenance_enabled: false
      health_check:
        check_timeout: 2000
        check_interval: 1000
        retries: 3
      http_health_check:
        path: "./"
        method: "GET"
        match_type: "STATUS_CODE"
        response: 200
        regex: false
        negate: false
      wait: true
    register: target_group_response
  ''',
  'update' : '''
  - name: Update Target Group
    target_group:
      name: "AnsibleAutoTestCompute - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group: "AnsibleAutoTestCompute"
      wait: true
      state: update
    register: target_group_response_update
  ''',
  'absent' : '''
  - name: Remove Target Group
    target_group:
      target_group: "AnsibleAutoTestCompute - UPDATED"
      wait: true
      wait_timeout: 2000
      state: absent
  ''',
}

EXAMPLES = """
  - name: Create Target Group
    target_group:
      name: "AnsibleAutoTestCompute"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      targets:
        - ip: "22.231.2.2"
          port: 8080
          weight: 123
          health_check_enabled: true
          maintenance_enabled: false
      health_check:
        check_timeout: 2000
        check_interval: 1000
        retries: 3
      http_health_check:
        path: "./"
        method: "GET"
        match_type: "STATUS_CODE"
        response: 200
        regex: false
        negate: false
      wait: true
    register: target_group_response
  

  - name: Update Target Group
    target_group:
      name: "AnsibleAutoTestCompute - UPDATED"
      algorithm: "ROUND_ROBIN"
      protocol: "HTTP"
      target_group: "AnsibleAutoTestCompute"
      wait: true
      state: update
    register: target_group_response_update
  

  - name: Remove Target Group
    target_group:
      target_group: "AnsibleAutoTestCompute - UPDATED"
      wait: true
      wait_timeout: 2000
      state: absent
"""


def get_target(target):
    target_object = TargetGroupTarget()
    if target.get('ip'):
        target_object.ip = target['ip']
    if target.get('port'):
        target_object.port = target['port']
    if target.get('weight'):
        target_object.weight = target['weight']
    if target.get('health_check_enabled'):
        target_object.health_check_enabled = target['health_check_enabled']
    if target.get('maintenance_enabled'):
        target_object.maintenance_enabled = target['maintenance_enabled']
    return target_object


def get_http_health_check(http_health_check):
    http_health_check_object = TargetGroupHttpHealthCheck()
    if http_health_check.get('path'):
        http_health_check_object.path = http_health_check['path']
    if http_health_check.get('method'):
        http_health_check_object.method = http_health_check['method']
    if http_health_check.get('match_type'):
        http_health_check_object.match_type = http_health_check['match_type']
    if http_health_check.get('response'):
        http_health_check_object.response = http_health_check['response']
    if http_health_check.get('regex'):
        http_health_check_object.regex = http_health_check['regex']
    if http_health_check.get('negate'):
        http_health_check_object.negate = http_health_check['negate']
    http_health_check = http_health_check_object
    return http_health_check


def get_health_check(health_check):
    health_check_object = TargetGroupHealthCheck()
    if health_check.get('check_timeout'):
        health_check_object.check_timeout = health_check['check_timeout']
    if health_check.get('check_interval'):
        health_check_object.check_interval = health_check['check_interval']
    if health_check.get('retries'):
        health_check_object.retries = health_check['retries']
    return health_check_object


class TargetGroupModule(CommonIonosModule):
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
        health_check = self.module.params.get('health_check')
        http_health_check = self.module.params.get('http_health_check')
        new_health_check = get_health_check(health_check) if health_check else None
        new_http_health_check = get_http_health_check(http_health_check) if http_health_check else None

        def sort_func(el):
            return el['ip'], el['port']

        if self.module.params.get('targets'):
            existing_targets = sorted(map(
                lambda x: {
                    'ip': x.ip,
                    'port': x.port,
                    'weight': x.weight,
                    'health_check_enabled': x.health_check_enabled,
                    'maintenance_enabled': x.maintenance_enabled,
                },
                existing_object.properties.targets
            ), key=sort_func)
            new_targets = sorted(self.module.params.get('targets'), key=sort_func)

        return (
            self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('algorithm') is not None
            and existing_object.properties.algorithm != self.module.params.get('algorithm')
            or self.module.params.get('protocol') is not None
            and existing_object.properties.protocol != self.module.params.get('protocol')
            or new_health_check is not None
            and (
                existing_object.properties.health_check.check_timeout != new_health_check.check_timeout
                or existing_object.properties.health_check.check_interval != new_health_check.check_interval
                or existing_object.properties.health_check.retries != new_health_check.retries
            )
            or new_http_health_check is not None
            and (
                existing_object.properties.http_health_check.path != new_http_health_check.path
                or existing_object.properties.http_health_check.method != new_http_health_check.method
                or existing_object.properties.http_health_check.match_type != new_http_health_check.match_type
                or existing_object.properties.http_health_check.response != new_http_health_check.response
                or existing_object.properties.http_health_check.regex != new_http_health_check.regex
                or existing_object.properties.http_health_check.negate != new_http_health_check.negate
            )
            or self.module.params.get('targets') is not None
            and new_targets != existing_targets
        )


    def _get_object_list(self, clients):
        return ionoscloud.TargetGroupsApi(clients[0]).targetgroups_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('target_group')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        algorithm = self.module.params.get('algorithm')
        protocol = self.module.params.get('protocol')
        targets = self.module.params.get('targets')
        health_check = self.module.params.get('health_check')
        http_health_check = self.module.params.get('http_health_check')

        if health_check:
            health_check = get_health_check(health_check)

        if http_health_check:
            http_health_check = get_http_health_check(http_health_check)

        if targets:
            targets = list(map(lambda x: get_target(x), targets))

        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            algorithm = existing_object.properties.algorithm if algorithm is None else algorithm
            protocol = existing_object.properties.protocol if protocol is None else protocol
            targets = existing_object.properties.targets if targets is None else targets
            health_check = existing_object.properties.health_check if health_check is None else health_check
            http_health_check = existing_object.properties.http_health_check if http_health_check is None else http_health_check

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        target_groups_api = ionoscloud.TargetGroupsApi(client)
        
        target_group = TargetGroup(properties=TargetGroupProperties(
            name=name, algorithm=algorithm, protocol=protocol,
            targets=targets, health_check=health_check,
            http_health_check=http_health_check,
        ))

        try:
            response, _, headers = target_groups_api.targetgroups_post_with_http_info(target_group)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new Target Group: %s" % to_native(e))
        return response


    def _update_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        algorithm = self.module.params.get('algorithm')
        protocol = self.module.params.get('protocol')
        targets = self.module.params.get('targets')
        health_check = self.module.params.get('health_check')
        http_health_check = self.module.params.get('http_health_check')

        if health_check:
            health_check = get_health_check(health_check)

        if http_health_check:
            http_health_check = get_http_health_check(http_health_check)


        if targets:
            targets = list(map(lambda x: get_target(x), targets))


        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        target_groups_api = ionoscloud.TargetGroupsApi(client)
        
        target_group_properties = TargetGroupProperties(
            name=name, algorithm=algorithm, protocol=protocol,
            targets=targets, health_check=health_check,
            http_health_check=http_health_check,
        )

        try:
            response, _, headers = target_groups_api.targetgroups_patch_with_http_info(
                existing_object.id, target_group_properties,
            )
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            return response
        except ApiException as e:
            self.module.fail_json(msg="failed to update the Target Group: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        target_groups_api = ionoscloud.TargetGroupsApi(client)

        try:
            _, _, headers = target_groups_api.target_groups_delete_with_http_info(existing_object.id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the Target Group: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = TargetGroupModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
