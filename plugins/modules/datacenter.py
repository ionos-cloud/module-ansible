#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import copy
import yaml
import re

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
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

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

OPTIONS = {
    'name': {
        'description': ['The name of the virtual datacenter.'],
        'required': ['present'],
        'available': STATES,
        'type': 'str',
    },
    'id': {
        'description': ['The ID of the virtual datacenter.'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'description': {
        'description': ['The description of the virtual datacenter.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'location': {
        'description': ['The datacenter location.'],
        'required': ['present'],
        'choices': ['us/las', 'us/ewr', 'de/fra', 'de/fkb', 'de/txl', 'gb/lhr'],
        'default': 'us/las',
        'available': ['present'],
        'type': 'str',
    },
    'api_url': {
        'description': ['The Ionos API base URL.'],
        'version_added': '2.4',
        'env_fallback': 'IONOS_API_URL',
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
     - This is a simple module that supports creating or removing vDCs. A vDC is required before you can create servers.
       This module has a dependency on ionos-cloud >= 6.0.0
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.0"
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
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      description: "description - RENAMED"
      state: update
    register: updated_datacenter
  ''',
  'absent' : '''# Destroy a Datacenter. This will remove all servers, volumes, and other objects in the datacenter.
  - name: Remove datacenter
    datacenter:
      id: "{{ datacenter_response.datacenter.id }}"
      name: "Example DC"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def _update_datacenter(module, datacenter_server, client, id, datacenter, wait):
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = datacenter_server.datacenters_put_with_http_info(datacenter_id=id, datacenter=datacenter)
        (datacenter_response, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)

        return {
            'changed': True,
            'failed': False,
            'datacenter': datacenter_response.to_dict()
        }
    except ApiException as e:
        module.fail_json(msg="failed to update the datacenter: %s" % to_native(e))
    return {
        'changed': False,
        'failed': True,
    }


def create_datacenter(module, client):
    """
    Creates a Datacenter

    This will create a new Datacenter in the specified location.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The datacenter ID if a new datacenter was created.
    """
    name = module.params.get('name')
    location = module.params.get('location')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    datacenter_server = ionoscloud.DataCentersApi(client)
    datacenters = datacenter_server.datacenters_get(depth=2)

    for dc in datacenters.items:
        if name == dc.properties.name and location == dc.properties.location:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'datacenter': dc.to_dict()
            }

    datacenter_properties = DatacenterProperties(name=name, description=description, location=location)
    datacenter = Datacenter(properties=datacenter_properties)

    try:
        response = datacenter_server.datacenters_post_with_http_info(datacenter=datacenter)
        (datacenter_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'datacenter': datacenter_response.to_dict()
        }

        return results

    except ApiException as e:
        module.fail_json(msg="failed to create the new datacenter: %s" % to_native(e))


def update_datacenter(module, client):
    """
    Updates a Datacenter.

    This will update a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if a new datacenter was updated, false otherwise
    """
    name = module.params.get('name')
    description = module.params.get('description')
    datacenter_id = module.params.get('id')
    wait = module.params.get('wait')
    datacenter_server = ionoscloud.DataCentersApi(client)

    if description is None:
        return {
            'action': 'update',
            'changed': False
        }

    changed = False
    response = None

    if datacenter_id:
        datacenter = Datacenter(properties={'name': name, 'description': description})
        response = _update_datacenter(module, datacenter_server, client, datacenter_id, datacenter, wait)
        changed = response['changed']
    else:
        datacenters = datacenter_server.datacenters_get(depth=2)
        for d in datacenters.items:
            vdc = datacenter_server.datacenters_find_by_id(d.id)
            if name == vdc.properties.name:
                datacenter = Datacenter(
                    properties={'name': name, 'description': description})
                response = _update_datacenter(module, datacenter_server, client, datacenter_id, datacenter, wait)
                changed = response['changed']

    if not changed:
        module.fail_json(msg="failed to update the datacenter: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': response['failed'],
        'datacenter': response['datacenter']
    }


def remove_datacenter(module, client):
    """
    Removes a Datacenter.

    This will remove a datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the datacenter was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('id')
    datacenter_server = ionoscloud.DataCentersApi(client)
    wait = module.params.get('wait')

    datacenters_list = datacenter_server.datacenters_get(depth=5)
    if datacenter_id:
        datacenter = _get_resource(datacenters_list, datacenter_id)
    else:
        datacenter = _get_resource(datacenters_list, name)

    if not datacenter:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = datacenter_server.datacenters_delete_with_http_info(datacenter_id=datacenter)
        (_, _, headers) = response
        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id)
    except Exception as e:
        module.fail_json(msg="failed to remove the datacenter: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': True,
        'id': datacenter_id,
    }


def get_module_arguments():
    arguments = {}

    for option_name, option in OPTIONS.items():
      arguments[option_name] = {
        'type': option['type'],
      }
      for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
        if option.get(key) is not None:
          arguments[option_name][key] = option.get(key)

      if option.get('env_fallback'):
        arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

      if len(option.get('required', [])) == len(STATES):
        arguments[option_name]['required'] = True

    return arguments


def get_sdk_config(module, sdk):
    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')

    if token is not None:
        # use the token instead of username & password
        conf = {
            'token': token
        }
    else:
        # use the username & password
        conf = {
            'username': username,
            'password': password,
        }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    return sdk.Configuration(**conf)


def check_required_arguments(module, state, object_name):
    # manually checking if token or username & password provided
    if (
        not module.params.get("token")
        and not (module.params.get("username") and module.params.get("password"))
    ):
        module.fail_json(
            msg='Token or username & password are required for {object_name} state {state}'.format(
                object_name=object_name,
                state=state,
            ),
        )

    for option_name, option in OPTIONS.items():
        if state in option.get('required', []) and not module.params.get(option_name):
            module.fail_json(
                msg='{option_name} parameter is required for {object_name} state {state}'.format(
                    option_name=option_name,
                    object_name=object_name,
                    state=state,
                ),
            )


def main():
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        if state in ['absent', 'update'] and not module.params.get('name') and not module.params.get('id'):
            module.fail_json(msg='either name or id parameter is required for {object_name} state present'.format(object_name=OBJECT_NAME))
        try:
            if state == 'absent':
                module.exit_json(**remove_datacenter(module, api_client))
            elif state == 'present':
                if module.check_mode:
                    module.exit_json(changed=True)
                module.exit_json(**create_datacenter(module, api_client))
            elif state == 'update':
                module.exit_json(**update_datacenter(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
