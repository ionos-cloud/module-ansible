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
    from ionoscloud.models import ApplicationLoadBalancer, ApplicationLoadBalancerProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _update_alb(module, client, alb_server, datacenter_id, application_load_balancer_id, alb_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = alb_server.datacenters_applicationloadbalancers_patch_with_http_info(datacenter_id, application_load_balancer_id,
                                                                                alb_properties)
    (alb_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return alb_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_alb(module, client):
    """
    Creates a Application Load Balancer

    This will create a new Application Load Balancer in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Application Load Balancer ID if a new Application Load Balancer was created.
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    alb_list = alb_server.datacenters_applicationloadbalancers_get(datacenter_id=datacenter_id, depth=2)
    alb_response = None

    for alb in alb_list.items:
        if name == alb.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'application_load_balancer': alb.to_dict()
            }

    alb_properties = ApplicationLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips, target_lan=target_lan,
                                                   lb_private_ips=lb_private_ips)
    application_load_balancer = ApplicationLoadBalancer(properties=alb_properties)

    try:
        response = alb_server.datacenters_applicationloadbalancers_post_with_http_info(datacenter_id, application_load_balancer)
        (alb_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Application Load Balancer: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'application_load_balancer': alb_response.to_dict()
    }


def update_alb(module, client):
    """
    Updates a Application Load Balancer.

    This will update a Application Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Application Load Balancer was updated, false otherwise
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')
    application_load_balancer_id = module.params.get('application_load_balancer_id')

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    alb_response = None
    changed = False

    if application_load_balancer_id:
        alb_properties = ApplicationLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                       target_lan=target_lan,
                                                       lb_private_ips=lb_private_ips)
        alb_response = _update_alb(module, client, alb_server, datacenter_id, application_load_balancer_id,
                                   alb_properties)
        changed = True

    else:
        alb_list = alb_server.datacenters_applicationloadbalancers_get(datacenter_id=datacenter_id, depth=2)
        for alb in alb_list.items:
            if name == alb.properties.name:
                alb_properties = ApplicationLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                               target_lan=target_lan,
                                                               lb_private_ips=lb_private_ips)
                alb_response = _update_alb(module, client, alb_server, datacenter_id, alb.id,
                                           alb_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Application Load Balancer: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'application_load_balancer': alb_response.to_dict()
    }


def remove_alb(module, client):
    """
    Removes a Application Load Balancer.

    This will remove a Application Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Application Load Balancer was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    application_load_balancer_id = module.params.get('application_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    alb_server = ionoscloud.ApplicationLoadBalancersApi(client)
    changed = False

    try:
        if application_load_balancer_id:
            response = alb_server.datacenters_applicationloadbalancers_delete_with_http_info(datacenter_id, application_load_balancer_id)
            (alb_response, _, headers) = response

            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

            changed = True

        elif name:
            alb_list = alb_server.datacenters_applicationloadbalancers_get_with_http_info(datacenter_id=datacenter_id, depth=2)
            for alb in alb_list.items:
                if name == alb.properties.name:
                    application_load_balancer_id = alb.id
                    response = alb_server.datacenters_applicationloadbalancers_delete_with_http_info(datacenter_id,
                                                                                                application_load_balancer_id)
                    (alb_response, _, headers) = response

                    if wait:
                        request_id = _get_request_id(headers['Location'])
                        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

                    changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Application Load Balancer: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': application_load_balancer_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            listener_lan=dict(type='str'),
            ips=dict(type='list', default=None),
            target_lan=dict(type='str'),
            lb_private_ips=dict(type='list', default=None),
            datacenter_id=dict(type='str'),
            application_load_balancer_id=dict(type='str'),
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
            if not (module.params.get('name') or module.params.get('application_load_balancer_id')):
                module.fail_json(
                    msg='name parameter or application_load_balancer_id parameter are required for deleting a Application Load Balancer.')
            try:
                (result) = remove_alb(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set Application Load Balancer state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Application Load Balancer')
            if not module.params.get('listener_lan'):
                module.fail_json(msg='listener_lan parameter is required for a new Application Load Balancer')
            if not module.params.get('target_lan'):
                module.fail_json(msg='target_lan parameter is required for a new Application Load Balancer')

            try:
                (alb_dict) = create_alb(module, api_client)
                module.exit_json(**alb_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Application Load Balancer state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a Application Load Balancer')
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for updating a Application Load Balancer')
            if not module.params.get('listener_lan'):
                module.fail_json(msg='listener_lan parameter is required for updating a Application Load Balancer')
            if not module.params.get('target_lan'):
                module.fail_json(msg='target_lan parameter is required for updating a Application Load Balancer')
            if not (module.params.get('name') or module.params.get('application_load_balancer_id')):
                module.fail_json(
                    msg='name parameter or application_load_balancer_id parameter are required updating a Application Load Balancer.')
            try:
                (alb_dict) = update_alb(module, api_client)
                module.exit_json(**alb_dict)
            except Exception as e:
                module.fail_json(msg='failed to update the Application Load Balancer: %s' % to_native(e))


if __name__ == '__main__':
    main()
