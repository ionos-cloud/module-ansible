from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import time
import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud_dsaas
    from ionoscloud_dsaas import __version__ as sdk_version
    from ionoscloud_dsaas import ApiClient
except ImportError:
    HAS_SDK = False


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
DSAAS_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dsaas/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'data-platform'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Data Platform Cluster'

OPTIONS = {
    'cluster_name': {
        'description': [
            'The name of your cluster. Must be 63 characters or less and must be empty or '
            'begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), '
            'underscores (_), dots (.), and alphanumerics between.',
        ],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'data_platform_cluster_id': {
        'description': ['The ID of the Data Platform cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'data_platform_version': {
        'description': ['The version of the DataPlatform.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'str',
    },
    'datacenter_id': {
        'description': ['The UUID of the virtual data center (VDC) the cluster is provisioned.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': [
            'Starting time of a weekly 4 hour-long window, during which '
            'maintenance might occur in hh:mm:ss format',
        ],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
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
module: data_platform_cluster
short_description: Create or destroy a Data Platform Cluster.
description:
     - This is a simple module that supports creating or removing Data Platform Clusters.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud_dsaas >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create Data Platform cluster
    data_platform_cluster:
      name: "{{ cluster_name }}"
  ''',
  'update' : '''
  - name: Update Data Platform cluster
    data_platform_cluster:
      data_platform_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      data_platform_version: 1.17.8
      state: update
  ''',
  'absent' : '''
  - name: Delete Data Platform cluster
    data_platform_cluster:
      data_platform_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
      state: absent
  ''',
}

EXAMPLES = '\n'.join(EXAMPLE_PER_STATE.values())



def _get_matched_resources(resource_list, identity, identity_paths=None):
    """
    Fetch and return a resource based on an identity supplied for it, if none or more than one matches 
    are found an error is printed and None is returned.
    """

    if identity_paths is None:
      identity_paths = [['id'], ['properties', 'name']]

    def check_identity_method(resource):
      resource_identity = []

      for identity_path in identity_paths:
        current = resource
        for el in identity_path:
          current = getattr(current, el)
        resource_identity.append(current)

      return identity in resource_identity

    return list(filter(check_identity_method, resource_list.items))


def get_resource(module, resource_list, identity, identity_paths=None):
    matched_resources = _get_matched_resources(resource_list, identity, identity_paths)

    if len(matched_resources) == 1:
        return matched_resources[0]
    elif len(matched_resources) > 1:
        module.fail_json(msg="found more resources of type {} for '{}'".format(resource_list.id, identity))
    else:
        return None


def get_resource_id(module, resource_list, identity, identity_paths=None):
    resource = get_resource(module, resource_list, identity, identity_paths)
    return resource.id if resource is not None else None
    

def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_data_platform_cluster(module, client):
    cluster_name = module.params.get('cluster_name')
    data_platform_version = module.params.get('data_platform_version')
    maintenance = module.params.get('maintenance_window')
    datacenter_id = module.params.get('datacenter_id')
    wait = module.params.get('wait')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    dsaas_cluster_server = ionoscloud_dsaas.DataPlatformClusterApi(api_client=client)

    existing_cluster = get_resource(module, dsaas_cluster_server.get_clusters(), cluster_name)

    if module.check_mode:
        module.exit_json(changed=False)

    if existing_cluster:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'cluster': existing_cluster.to_dict(),
        }

    try:
        dsaas_cluster_properties = ionoscloud_dsaas.CreateClusterProperties(
            name=cluster_name,
            data_platform_version=data_platform_version,
            datacenter_id=datacenter_id,
            maintenance_window=maintenance_window,
        )
        dsaas_cluster = ionoscloud_dsaas.CreateClusterRequest(properties=dsaas_cluster_properties)

        dsaas_cluster_response = dsaas_cluster_server.create_cluster(create_cluster_request=dsaas_cluster)

        if wait:
            client.wait_for(
                fn_request=lambda: dsaas_cluster_server.get_clusters(),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == cluster_name,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000
            )

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'data_platform_cluster': dsaas_cluster_response.to_dict()
        }

        return results

    except Exception as e:
        module.fail_json(
            msg="failed to create the k8s cluster: %s" % to_native(e))


def delete_data_platform_cluster(module, client):
    cluster_id = module.params.get('data_platform_cluster_id')
    cluster_name = module.params.get('cluster_name')
    wait = module.params.get('wait')
    changed = False

    dsaas_cluster_server = ionoscloud_dsaas.DataPlatformClusterApi(api_client=client)
    data_platform_clusters = dsaas_cluster_server.get_clusters()

    dsaas_cluster = get_resource(module, data_platform_clusters, cluster_id if cluster_id else cluster_name)

    if not dsaas_cluster:
        module.exit_json(changed=False)

    try:
        if dsaas_cluster.metadata.state == 'AVAILABLE':
            dsaas_cluster_server.delete_cluster(cluster_id=dsaas_cluster.id)

        if wait:
            client.wait_for(
                fn_request=lambda: dsaas_cluster_server.get_clusters(),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == dsaas_cluster.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000
            )
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to delete the Data Platform cluster: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': dsaas_cluster.id,
    }


def update_k8s_cluster(module, client):
    cluster_name = module.params.get('cluster_name')
    data_platform_version = module.params.get('data_platform_version')
    data_platform_cluster_id = module.params.get('data_platform_cluster_id')
    maintenance = module.params.get('maintenance_window')

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    dsaas_cluster_server = ionoscloud_dsaas.DataPlatformClusterApi(api_client=client)
    
    existing_cluster_id_by_name = get_resource_id(module, dsaas_cluster_server.get_clusters(), cluster_name)

    if data_platform_cluster_id is not None and existing_cluster_id_by_name is not None and existing_cluster_id_by_name != k8s_cluster_id:
            module.fail_json(msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, cluster_name))

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        dsaas_cluster_properties = ionoscloud_dsaas.PatchClusterProperties(
            name=cluster_name,
            data_platform_version=data_platform_version,
            maintenance_window=maintenance_window,
        )
        dsaas_cluster = ionoscloud_dsaas.PatchClusterRequest(properties=dsaas_cluster_properties)
        dsaas_cluster = dsaas_cluster_server.patch_cluster(data_platform_cluster_id, dsaas_cluster)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: dsaas_cluster_server.get_clusters(),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == cluster_name,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000
            )
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to update the Data Platform cluster: %s" % to_native(e))
        changed = False

    return {
        'changed': changed,
        'failed': False,
        'action': 'update',
        'data_platform_cluster': dsaas_cluster.to_dict()
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
        module.fail_json(msg='ionoscloud_dsaas is required for this module, run `pip install ionoscloud_dsaas`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud_dsaas)) as api_client:
        api_client.user_agent = DSAAS_USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'present':
                module.exit_json(**create_data_platform_cluster(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_data_platform_cluster(module, api_client))
            elif state == 'update':
                module.exit_json(**update_data_platform_cluster(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
