from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import time
import re
import copy
import yaml

HAS_SDK = True

try:
    import ionoscloud
    import ionoscloud_dataplatform
    from ionoscloud_dataplatform import __version__ as sdk_version
    from ionoscloud_dataplatform import ApiClient
except ImportError:
    HAS_SDK = False


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
DATAPLATFORM_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dataplatform/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'dataplatform'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Data Platform Cluster'
RETURNED_KEY = 'dataplatform_cluster'

OPTIONS = {
    'name': {
        'description': ['The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'cluster': {
        'description': ['The ID or name of the Data Platform cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'dataplatform_version': {
        'description': ['The version of the data platform.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'str',
    },
    'datacenter': {
        'description': ['The UUID of the virtual data center the cluster is provisioned.'],
        'available': ['update', 'present'],
        'required': ['present'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': ['Starting time of a weekly 4 hour-long window, during which maintenance might occur in hh:mm:ss format'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
    },
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different '
            'value to an immutable property. An error will be thrown instead',
        ],
        'available': ['present', 'update'],
        'default': False,
        'type': 'bool',
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
module: dataplatform_cluster
short_description: Create or destroy a Data Platform Cluster.
description:
     - This is a simple module that supports creating or removing Data Platform Clusters.
       This module has a dependency on ionoscloud >= 6.0.2
     - ⚠️ **Note:** Data Platform is currently in the Early Access (EA) phase. We recommend keeping usage and testing to non-production critical applications. Please contact your sales representative or support for more information.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud_dataplatform >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create Data Platform cluster
    dataplatform_cluster:
      name: ClusterName
  ''',
  'update' : '''
  - name: Update Data Platform cluster
    dataplatform_cluster:
      cluster: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      dataplatform_version: 1.17.8
      state: update
  ''',
  'absent' : '''
  - name: Delete Data Platform cluster
    dataplatform_cluster:
      cluster: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
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
    


def update_replace_object(module, dataplatform_client, cloudapi_client, existing_object):
    if _should_replace_object(module, existing_object, cloudapi_client):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, dataplatform_client, cloudapi_client, existing_object).to_dict()
        _remove_object(module, dataplatform_client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, dataplatform_client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def _should_replace_object(module, existing_object, cloudapi_client):
    datacenter_id = get_resource_id(
        module,
        ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )

    return (
        datacenter_id is not None
        and existing_object.properties.datacenter_id != datacenter_id
    )


def _should_update_object(module, existing_object):
    return (
        module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('dataplatform_version') is not None
        and existing_object.properties.data_platform_version != module.params.get('dataplatform_version')
        or module.params.get('maintenance_window') is not None
        and (
            existing_object.properties.maintenance_window.day_of_the_week != module.params.get('maintenance_window').get('day_of_the_week')
            or existing_object.properties.maintenance_window.time != module.params.get('maintenance_window').get('time')
        )
    )


def _get_object_list(module, client):
    return ionoscloud_dataplatform.DataPlatformClusterApi(client).get_clusters()


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('cluster')


def _create_object(module, dataplatform_client, cloudapi_client, existing_object=None):
    name = module.params.get('name')
    dataplatform_version = module.params.get('dataplatform_version')
    maintenance = module.params.get('maintenance_window')

    datacenter_id = get_resource_id(
        module,
        ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1),
        module.params.get('datacenter'),
    )

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        dataplatform_version = existing_object.properties.dataplatform_version if dataplatform_version is None else dataplatform_version
        datacenter_id = existing_object.properties.datacenter_id if datacenter_id is None else datacenter_id
        maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance

    dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(dataplatform_client)
    
    cluster_properties = ionoscloud_dataplatform.CreateClusterProperties(
        name=name,
        data_platform_version=dataplatform_version,
        maintenance_window=maintenance_window,
        datacenter_id=datacenter_id,
    )
    cluster = ionoscloud_dataplatform.CreateClusterRequest(properties=cluster_properties)

    try:
        response = dataplatform_cluster_api.create_cluster(create_cluster_request=cluster)

        if module.params.get('wait'):
            dataplatform_client.wait_for(
                fn_request=lambda: dataplatform_cluster_api.get_clusters(),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == name,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )
    except ionoscloud_dataplatform.ApiException as e:
        module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
    return response


def _update_object(module, client, existing_object):
    name = module.params.get('name')
    dataplatform_version = module.params.get('dataplatform_version')
    maintenance = module.params.get('maintenance_window')

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client)

    _cluster_properties = ionoscloud_dataplatform.PatchClusterProperties(
        name=name,
        data_platform_version=dataplatform_version,
        maintenance_window=maintenance_window,
    )
    patch_cluster = ionoscloud_dataplatform.PatchClusterRequest(properties=_cluster_properties)

    try:
        response = dataplatform_cluster_api.patch_cluster(existing_object.id, patch_cluster)
        
        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: dataplatform_cluster_api.get_clusters(),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == name,
                    r.items
                ))[0].metadata.state == 'AVAILABLE',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )

        return response
    except ionoscloud_dataplatform.ApiException as e:
        module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


def _remove_object(module, client, existing_object):
    dataplatform_cluster_api = ionoscloud_dataplatform.DataPlatformClusterApi(api_client=client)

    try:
        if existing_object.metadata.state == 'AVAILABLE':
            dataplatform_cluster_api.delete_cluster(existing_object.id)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: dataplatform_cluster_api.get_clusters(),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == existing_object.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )
    except Exception as e:
        module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


def create_object(module, dataplatform_client, cloudapi_client):
    existing_object = get_resource(module, _get_object_list(module, dataplatform_client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, dataplatform_client, cloudapi_client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, dataplatform_client, cloudapi_client).to_dict()
    }


def update_object(module, dataplatform_client, cloudapi_client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, dataplatform_client)

    existing_object = get_resource(module, object_list, _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(module, object_list, object_name)

    if (
        existing_object.id is not None
        and existing_object_id_by_new_name is not None
        and existing_object_id_by_new_name != existing_object.id
    ):
        module.fail_json(
            msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                OBJECT_NAME, object_name,
            ),
        )

    return update_replace_object(module, dataplatform_client, cloudapi_client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_identifier(module))

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
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
        module.fail_json(msg='ionoscloud_dataplatform is required for this module, run `pip install ionoscloud_dataplatform`')

    state = module.params.get('state')

    cloudapi_api_client = ionoscloud.ApiClient(get_sdk_config(module, ionoscloud))
    cloudapi_api_client.user_agent = USER_AGENT
    dataplatform_api_client = ionoscloud_dataplatform.ApiClient(get_sdk_config(module, ionoscloud_dataplatform))
    dataplatform_api_client.user_agent = DATAPLATFORM_USER_AGENT
    
    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, dataplatform_api_client, cloudapi_api_client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, dataplatform_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, dataplatform_api_client, cloudapi_api_client))
    except Exception as e:
        module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
