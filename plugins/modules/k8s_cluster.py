from socket import timeout
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
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import KubernetesCluster, KubernetesClusterProperties, KubernetesClusterForPut, \
        KubernetesClusterPropertiesForPut, S3Bucket
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-kubernetes'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'K8s Cluster'
RETURNED_KEY = 'cluster'

OPTIONS = {
    'cluster_name': {
        'description': ['The name of the K8s cluster.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'k8s_cluster': {
        'description': ['The ID or name of the K8s cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'k8s_version': {
        'description': [
            'The Kubernetes version the cluster is running. This imposes restrictions on what '
            "Kubernetes versions can be run in a cluster's nodepools. Additionally, not all "
            'Kubernetes versions are viable upgrade targets for all prior versions.',
        ],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': [
            "The maintenance window is used for updating the cluster's control plane and for "
            "upgrading the cluster's K8s version. If no value is given, one is chosen dynamically, "
            'so there is no fixed default.',
        ],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
    },
    'api_subnet_allow_list': {
        'description': [
            'Access to the K8s API server is restricted to these CIDRs. Traffic, internal to the cluster, '
            'is not affected by this restriction. If no allowlist is specified, access is not restricted. '
            'If an IP without subnet mask is provided, the default value is used: 32 for IPv4 and 128 for IPv6.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    's3_buckets_param': {
        'description': [
            'List of S3 bucket configured for K8s usage. For now it contains only an S3 bucket '
            'used to store K8s API audit logs.',
        ],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
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
module: k8s_cluster
short_description: Create or destroy a K8s Cluster.
description:
     - This is a simple module that supports creating or removing K8s Clusters.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
''' + '  ' + yaml.dump(yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})), default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
  'present' : '''
  - name: Create k8s cluster
    k8s_cluster:
      name: "{{ cluster_name }}"
  ''',
  'update' : '''
  - name: Update k8s cluster
    k8s_cluster:
      k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
      maintenance_window:
        day_of_the_week: 'Tuesday'
        time: '13:03:00'
      k8s_version: 1.17.8
      state: update
  ''',
  'absent' : '''
  - name: Delete k8s cluster
    k8s_cluster:
      k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
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



def update_replace_object(module, client, existing_object):
    if module.params.get('replace') and _should_replace_object(module, existing_object):
        _remove_object(module, client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: _create_object(module, client, existing_object).to_dict()
        }
    if _should_update_object(module, existing_object):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def _should_replace_object(*args, **kwargs):
    return False


def _should_update_object(module, existing_object):
    return (
        module.params.get('cluster_name') is not None
        and existing_object.properties.name != module.params.get('cluster_name')
        or module.params.get('k8s_version') is not None
        and existing_object.properties.k8s_version != module.params.get('k8s_version')
        or module.params.get('maintenance_window') is not None
        and (
            existing_object.properties.maintenance_window.day_of_the_week != module.params.get('maintenance_window').get('day_of_the_week')
            or existing_object.properties.maintenance_window.time != module.params.get('maintenance_window').get('time')
        ) or module.params.get('api_subnet_allow_list') is not None
        and sorted(existing_object.properties.api_subnet_allow_list) != sorted(module.params.get('api_subnet_allow_list'))
        or module.params.get('s3_buckets_param') is not None
        and sorted(list(map(lambda o: o.name, existing_object.properties.s3_buckets))) != sorted(module.params.get('s3_buckets_param'))
    )


def _get_object_list(module, client):
    return ionoscloud.KubernetesApi(client).k8s_get(depth=1)


def _get_object_name(module):
    return module.params.get('cluster_name')


def _get_object_identifier(module):
    return module.params.get('k8s_cluster')


def _create_object(module, client, existing_object=None):
    cluster_name = module.params.get('cluster_name')
    k8s_version = module.params.get('k8s_version')
    maintenance = module.params.get('maintenance_window')
    api_subnet_allow_list = module.params.get('api_subnet_allow_list')
    s3_buckets = list(map(lambda bucket_name: S3Bucket(name=bucket_name), module.params.get('s3_buckets_param'))) if module.params.get('s3_buckets_param') else None

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    if existing_object is not None:
        name = existing_object.properties.name if name is None else name
        k8s_version = existing_object.properties.k8s_version if k8s_version is None else k8s_version
        api_subnet_allow_list = existing_object.properties.api_subnet_allow_list if api_subnet_allow_list is None else api_subnet_allow_list
        s3_buckets = existing_object.properties.s3_buckets if s3_buckets is None else s3_buckets
        maintenance = existing_object.properties.maintenance_window if maintenance is None else maintenance

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    k8s_api = ionoscloud.KubernetesApi(api_client=client)
    
    k8s_cluster_properties = KubernetesClusterProperties(
        name=cluster_name,
        k8s_version=k8s_version,
        maintenance_window=maintenance_window,
        api_subnet_allow_list=api_subnet_allow_list,
        s3_buckets=s3_buckets,
    )
    k8s_cluster = KubernetesCluster(properties=k8s_cluster_properties)

    try:
        k8s_response = k8s_api.k8s_post(kubernetes_cluster=k8s_cluster)

        if wait:
            try:
                client.wait_for(
                    fn_request=lambda: k8s_api.k8s_find_by_cluster_id(k8s_response.id).metadata.state,
                    fn_check=lambda r: r == 'ACTIVE',
                    scaleup=10000,
                    timeout=wait_timeout,
                )
            except Exception as e:
                with open('debug.txt', 'a') as f:
                    f.write(str([e]))
    except ApiException as e:
        module.fail_json(msg="failed to create the new {}: {}".format(OBJECT_NAME, to_native(e)))
    return k8s_response


def _update_object(module, client, existing_object):

    cluster_name = module.params.get('cluster_name')
    k8s_version = module.params.get('k8s_version')
    maintenance = module.params.get('maintenance_window')
    api_subnet_allow_list = module.params.get('api_subnet_allow_list')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    s3_buckets = list(map(lambda bucket_name: S3Bucket(name=bucket_name), module.params.get('s3_buckets_param'))) if module.params.get('s3_buckets_param') else None

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
    kubernetes_cluster_properties = KubernetesClusterPropertiesForPut(
        name=cluster_name,
        k8s_version=k8s_version,
        s3_buckets=s3_buckets,
        api_subnet_allow_list=api_subnet_allow_list,
        maintenance_window=maintenance_window,
    )
    kubernetes_cluster = KubernetesClusterForPut(properties=kubernetes_cluster_properties)

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        k8s_response = k8s_api.k8s_put(k8s_cluster_id=existing_object.id, kubernetes_cluster=kubernetes_cluster)
        if wait:
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_find_by_cluster_id(existing_object.id).metadata.state,
                fn_check=lambda r: r == 'ACTIVE',
                scaleup=10000,
                timeout=wait_timeout,
            )

        return k8s_response
    except ApiException as e:
        module.fail_json(msg="failed to update the {}: {}".format(OBJECT_NAME, to_native(e)))


def _remove_object(module, client, existing_object):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    k8s_api = ionoscloud.KubernetesApi(api_client=client)

    try:
        if existing_object.metadata.state != 'DESTROYING':
            k8s_api.k8s_delete_with_http_info(k8s_cluster_id=existing_object.id)

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_api.k8s_get(depth=1),
                fn_check=lambda r: len(list(filter(
                    lambda e: e.id == existing_object.id,
                    r.items
                ))) < 1,
                console_print='.',
                scaleup=10000,
                timeout=wait_timeout,
            )
    except Exception as e:
        module.fail_json(msg="failed to delete the {}: {}".format(OBJECT_NAME, to_native(e)))


def create_object(module, client):
    existing_object = get_resource(module, _get_object_list(module, client), _get_object_name(module))

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, client)

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

    return update_replace_object(module, client, existing_object)


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
    module = AnsibleModule(argument_spec=get_module_arguments())

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    state = module.params.get('state')
    with ApiClient(get_sdk_config(module, ionoscloud)) as api_client:
        api_client.user_agent = USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'absent':
                module.exit_json(**remove_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
