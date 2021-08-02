#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from datetime import datetime, timezone
from time import sleep

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

import re

HAS_SDK = True
WAIT_TIME = 10

try:
    import ionoscloudautoscaling
    from ionoscloudautoscaling import __version__ as sdk_version
    from ionoscloudautoscaling.models import Group, GroupProperties, GroupPolicy, GroupPolicyAction, \
        GroupPropertiesTemplate, GroupPropertiesDatacenter
    from ionoscloudautoscaling.rest import ApiException
    from ionoscloudautoscaling import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def get_action(action):
    action_object = GroupPolicyAction()
    if 'amount' in action:
        action_object.amount = action['amount']
    if 'amount_type' in action:
        action_object.amount_type = action['amount_type']
    if 'cooldown_period' in action:
        action_object.cooldown_period = action['cooldown_period']
    return action_object


def get_policy(policy):
    policy_object = GroupPolicy()
    if 'metric' in policy:
        policy_object.metric = policy['metric']
    if 'range' in policy:
        policy_object.range = policy['range']
    if 'scale_in_action' in policy:
        policy_object.scale_in_action = get_action(policy['scale_in_action'])
    if 'scale_in_threshold' in policy:
        policy_object.scale_in_threshold = policy['scale_in_threshold']
    if 'scale_out_action' in policy:
        policy_object.scale_out_action = get_action(policy['scale_out_action'])
    if 'scale_out_threshold' in policy:
        policy_object.scale_out_threshold = policy['scale_out_threshold']
    if 'unit' in policy:
        policy_object.unit = policy['unit']
    return policy_object


def is_finished(autoscaling_group_server, group_id, ts_before_creation):
    actions = autoscaling_group_server.autoscaling_groups_actions_get(group_id=group_id, depth=5)
    current_action = actions.items[0]
    return current_action.properties.action_status != "IN_PROGRESS" and current_action.metadata.created_date > ts_before_creation


def poll_action(autoscaling_group_server, group_id, ts_before_creation):
    while not is_finished(autoscaling_group_server, group_id, ts_before_creation):
        sleep(WAIT_TIME)


def create_autoscaling_group(module, client):
    """
    Creates a Autoscaling Group.

    module : AnsibleModule object
    client: authenticated ionoscloudautoscaling object.

    Returns:
        The Autoscaling Group instance
    """
    name = module.params.get('name')
    location = module.params.get('location')
    datacenter = module.params.get('datacenter')
    template = module.params.get('template')
    max_replica_count = module.params.get('max_replica_count')
    min_replica_count = module.params.get('min_replica_count')
    target_replica_count = module.params.get('target_replica_count')
    policy_dict = module.params.get('policy')
    wait = module.params.get('wait')

    autoscaling_group_server = ionoscloudautoscaling.GroupsApi(api_client=client)

    # Prefetch a list of Autoscaling Groups.
    autoscaling_group_list = autoscaling_group_server.autoscaling_groups_get(depth=2)
    autoscaling_group = None

    for i in autoscaling_group_list.items:
        if name == i.properties.name:
            autoscaling_group = i
            break

    should_change = autoscaling_group is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'failed': False,
            'action': 'create',
            'autoscaling_group': autoscaling_group.to_dict()
        }
    try:
        policy = get_policy(policy_dict)
        autoscaling_group_properties = GroupProperties(datacenter=datacenter, location=location,
                                                       max_replica_count=max_replica_count,
                                                       min_replica_count=min_replica_count, name=name, policy=policy,
                                                       target_replica_count=target_replica_count, template=template)

        autoscaling_group = Group(properties=autoscaling_group_properties)

        timestamp = datetime.now(timezone.utc)
        response = autoscaling_group_server.autoscaling_groups_post_with_http_info(group=autoscaling_group)
        (autoscaling_group_response, _, headers) = response

        if wait:
            poll_action(autoscaling_group_server, autoscaling_group_response.id, timestamp)

        return {
            'failed': False,
            'changed': True,
            'action': 'create',
            'autoscaling_group': autoscaling_group_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the Autoscaling Group: %s" % to_native(e))


def update_autoscaling_group(module, client):
    """
    Updates a Autoscaling Group.

    module : AnsibleModule object
    client: authenticated ionoscloudautoscaling object.

    Returns:
        The Autoscaling Group instance
    """
    name = module.params.get('name')
    location = module.params.get('location')
    datacenter = module.params.get('datacenter')
    template = module.params.get('template')
    max_replica_count = module.params.get('max_replica_count')
    min_replica_count = module.params.get('min_replica_count')
    group_id = module.params.get('group_id')
    policy_dict = module.params.get('policy')
    wait = module.params.get('wait')

    autoscaling_group_server = ionoscloudautoscaling.GroupsApi(api_client=client)
    group = autoscaling_group_server.autoscaling_groups_find_by_id(group_id=group_id)
    target_replica_count = group.properties.target_replica_count

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        policy = get_policy(policy_dict)
        autoscaling_group_properties = GroupProperties(datacenter=datacenter, location=location,
                                                       max_replica_count=max_replica_count,
                                                       min_replica_count=min_replica_count, name=name,
                                                       policy=policy,
                                                       target_replica_count=target_replica_count, template=template)

        autoscaling_group = Group(properties=autoscaling_group_properties)

        timestamp = datetime.now(timezone.utc)
        response = autoscaling_group_server.autoscaling_groups_put_with_http_info(group_id=group_id,
                                                                                  group=autoscaling_group)
        (autoscaling_group_response, _, headers) = response

        if wait:
            poll_action(autoscaling_group_server, autoscaling_group_response.id, timestamp)

        return {
            'failed': False,
            'changed': True,
            'action': 'update',
            'autoscaling_group': autoscaling_group_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the Autoscaling Group: %s" % to_native(e))


def delete_autoscaling_group(module, client):
    """
    Removes a Autoscaling Group

    module : AnsibleModule object
    client: authenticated ionoscloudautoscaling object.

    Returns:
        True if the Autoscaling Group was removed, false otherwise
    """
    group_id = module.params.get('group_id')
    name = module.params.get('name')

    autoscaling_group_server = ionoscloudautoscaling.GroupsApi(api_client=client)

    # Locate ID for Autoscaling Group
    if not group_id:
        autoscaling_group_list = autoscaling_group_server.autoscaling_groups_get(depth=2)
        group_id = _get_resource_id(autoscaling_group_list, name, module, "Autoscaling Group")

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        autoscaling_group_server.autoscaling_groups_delete_with_http_info(group_id=group_id)

        return {
            'action': 'delete',
            'changed': True,
            'id': group_id
        }
    except Exception as e:
        module.fail_json(msg="failed to remove the Autoscaling Group: %s" % to_native(e))


def _get_resource_id(resource_list, identity, module, resource_type):
    """
    Fetch and return the UUID of a resource regardless of whether the name or
    UUID is passed. Throw an error otherwise.
    """
    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    module.fail_json(msg='%s \'%s\' could not be found.' % (resource_type, identity))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            location=dict(type='str'),
            datacenter=dict(type='dict'),
            template=dict(type='dict'),
            max_replica_count=dict(type='int'),
            min_replica_count=dict(type='int'),
            target_replica_count=dict(type='str'),
            group_id=dict(type='str'),
            policy=dict(type='dict'),
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
        module.fail_json(
            msg='ionoscloudautoscaling is required for this module, run `pip install ionoscloudautoscaling`')

    username = module.params.get('username')
    password = module.params.get('password')
    user_agent = 'ionoscloudautoscaling-python/%s Ansible/%s' % (sdk_version, __version__)

    state = module.params.get('state')

    configuration = ionoscloudautoscaling.Configuration(
        username=username,
        password=password
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'absent':
            try:
                (result) = delete_autoscaling_group(module, api_client)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg='failed to set Autoscaling Group state: %s' % to_native(e))

        elif state == 'present':
            try:
                (autoscaling_group_dict) = create_autoscaling_group(module, api_client)
                module.exit_json(**autoscaling_group_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Autoscaling Groups state: %s' % to_native(e))

        elif state == 'update':
            try:
                (autoscaling_group_dict) = update_autoscaling_group(module, api_client)
                module.exit_json(**autoscaling_group_dict)
            except Exception as e:
                module.fail_json(msg='failed to update Autoscaling Group: %s' % to_native(e))


if __name__ == '__main__':
    main()
