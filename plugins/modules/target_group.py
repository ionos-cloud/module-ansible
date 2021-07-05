#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import TargetGroup, TargetGroupPut, TargetGroupTarget, TargetGroupProperties, TargetGroups, \
        TargetGroupTargetHealthCheck, TargetGroupHealthCheck, TargetGroupHttpHealthCheck
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _update_target_group(module, client, target_group_server, target_group_id, target_group_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = target_group_server.targetgroups_patch_with_http_info(target_group_id, target_group_properties)
    (target_group_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return target_group_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))

def get_target(target):
    target_object = TargetGroupTarget()
    if target['ip']:
        target_object.ip = target['ip']
    if target['port']:
        target_object.port = target['port']
    if target['weight']:
        target_object.weight = target['weight']
    if target['health_check']:
        target_object.health_check = TargetGroupTargetHealthCheck()
        if target['health_check']['check']:
            target_object.health_check.check = target['health_check']['check']
        if target['health_check']['check_interval']:
            target_object.health_check.check_interval = target['health_check']['check_interval']
        if target['health_check']['maintenance']:
            target_object.health_check.maintenance = target['health_check']['maintenance']
    return target_object


def get_http_health_check(http_health_check):
    http_health_check_object = TargetGroupHttpHealthCheck()
    if http_health_check['path']:
        http_health_check_object.path = http_health_check['path']
    if http_health_check['method']:
        http_health_check_object.method = http_health_check['method']
    if http_health_check['match_type']:
        http_health_check_object.match_type = http_health_check['match_type']
    if http_health_check['response']:
        http_health_check_object.response = http_health_check['response']
    if http_health_check['regex']:
        http_health_check_object.regex = http_health_check['regex']
    if http_health_check['negate']:
        http_health_check_object.negate = http_health_check['negate']
    http_health_check = http_health_check_object
    return http_health_check


def get_health_check(health_check):
    health_check_object = TargetGroupHealthCheck()
    if health_check['check_timeout']:
        health_check_object.check_timeout = health_check['check_timeout']
    if health_check['connect_timeout']:
        health_check_object.connect_timeout = health_check['connect_timeout']
    if health_check['target_timeout']:
        health_check_object.target_timeout = health_check['target_timeout']
    if health_check['retries']:
        health_check_object.retries = health_check['retries']
    return health_check_object


def create_target_group(module, client):
    """
    Creates a Target Group

    This will create a new Target Group in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Target Group ID if a new Target Group was created.
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    target_group_server = ionoscloud.TargetGroupsApi(client)
    target_groups = target_group_server.targetgroups_get(depth=5)
    target_group_response = None

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)

    target_list = []
    if targets and len(targets) > 0:
        for t in targets:
            target = get_target(t)
            target_list.append(target)

    for target_group in target_groups.items:
        if name == target_group.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'target_group': target_group.to_dict()
            }

    target_group_properties = TargetGroupProperties(name=name, algorithm=algorithm, protocol=protocol,
                                                    targets=target_list, health_check=health_check,
                                                    http_health_check=http_health_check)
    target_group = TargetGroup(properties=target_group_properties)

    try:
        response = target_group_server.targetgroups_post_with_http_info(target_group)
        (target_group_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Target Group: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'target_group': target_group_response.to_dict()
    }


def update_target_group(module, client):
    """
    Updates a Target Group.

    This will update a Target Group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Target Group was updated, false otherwise
    """
    name = module.params.get('name')
    algorithm = module.params.get('algorithm')
    protocol = module.params.get('protocol')
    target_group_id = module.params.get('target_group_id')
    targets = module.params.get('targets')
    health_check = module.params.get('health_check')
    http_health_check = module.params.get('http_health_check')

    target_group_server = ionoscloud.TargetGroupsApi(client)
    changed = False
    target_group_response = None

    if health_check:
        health_check = get_health_check(health_check)

    if http_health_check:
        http_health_check = get_http_health_check(http_health_check)

    target_list = []
    if targets and len(targets) > 0:
        for t in targets:
            target = get_target(t)
            target_list.append(target)

    if target_group_id:
        target_group_properties = TargetGroupProperties(name=name, algorithm=algorithm, protocol=protocol,
                                                        targets=targets,
                                                        health_check=health_check, http_health_check=http_health_check)

        target_group_response = _update_target_group(module, client, target_group_server,
                                                     target_group_id,
                                                     target_group_properties)
        changed = True

    else:
        target_groups = target_group_server.targetgroups_get(depth=2)
        for t in target_groups.items:
            if name == t.properties.name:
                target_group_properties = TargetGroupProperties(name=name, algorithm=algorithm, protocol=protocol,
                                                                targets=targets,
                                                                health_check=health_check,
                                                                http_health_check=http_health_check)
                target_group_response = _update_target_group(module, client, target_group_server, t.id,
                                                             target_group_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Target Group: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'target_group': target_group_response.to_dict()
    }


def remove_target_group(module, client):
    """
    Removes a Target Group.

    This will remove a Target Group.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Target Group was deleted, false otherwise
    """
    name = module.params.get('name')
    target_group_id = module.params.get('target_group_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    target_group_server = ionoscloud.TargetGroupsApi(client)
    changed = False

    try:
        if target_group_id:
            response = target_group_server.target_groups_delete_with_http_info(target_group_id)
            (target_group_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            target_groups = target_group_server.targetgroups_get(depth=2)
            for t in target_groups.items:
                if name == t.properties.name:
                    target_group_id = t.id
                    response = target_group_server.target_groups_delete(target_group_id)
                    (target_group_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Target Group: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': target_group_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            algorithm=dict(type='str'),
            protocol=dict(type='str'),
            target_group_id=dict(type='str'),
            targets=dict(type='list',
                         elements=dict()
                         ),
            health_check=dict(
                type='dict',
                check_timeout=dict(type='int'),
                connect_timeout=dict(type='int'),
                target_timeout=dict(type='int'),
                retries=dict(type='int')
            ),
            http_health_check=dict(
                type='dict',
                path=dict(type='str'),
                method=dict(type='str'),
                match_type=dict(type='str'),
                response=dict(type='str'),
                regex=dict(type='bool', default=False),
                negate=dict(type='bool', default=False)
            ),
            api_url=dict(type='str', default=None),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    state = module.params.get('state')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not (module.params.get('name') or module.params.get('target_group_id')):
                module.fail_json(
                    msg='name parameter or target_group_id parameter are required deleting a Target Group.')
            try:
                (result) = remove_target_group(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set Target Group state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Target Group')
            if not module.params.get('algorithm'):
                module.fail_json(msg='algorithm parameter is required for a new Target Group')
            if not module.params.get('protocol'):
                module.fail_json(msg='protocol parameter is required for a new Target Group')

            try:
                (target_group_dict) = create_target_group(module, api_client)
                module.exit_json(**target_group_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Target Group state: %s' % to_native(e))

        elif state == 'update':
            if not (module.params.get('name') or module.params.get('target_group_id')):
                module.fail_json(
                    msg='name parameter or target_group_id parameter are required for updating a Target Group.')
            try:
                (target_group_dict_array) = update_target_group(module, api_client)
                module.exit_json(**target_group_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to update the Target Group: %s' % to_native(e))


if __name__ == '__main__':
    main()
