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

OPTIONS = {
    'cluster_name': {
        'description': ['The name of the K8s cluster.'],
        'available': ['present', 'update'],
        'required': ['present', 'update'],
        'type': 'str',
    },
    'k8s_cluster_id': {
        'description': ['The ID of the K8s cluster.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'k8s_version': {
        'description': ['The description of the virtual datacenter.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'str',
    },
    'maintenance_window': {
        'description': ['The datacenter location.'],
        'available': ['present', 'update'],
        'required': ['update'],
        'type': 'dict',
    },
    'public': {
        'description': ['The datacenter location.'],
        'available': ['present'],
        'type': 'bool',
    },
    'api_subnet_allow_list': {
        'description': ['The datacenter location.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'str',
    },
    's3_buckets_param': {
        'description': ['The datacenter location.'],
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


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_k8s_cluster(module, client):
    cluster_name = module.params.get('cluster_name')
    k8s_version = module.params.get('k8s_version')
    maintenance = module.params.get('maintenance_window')
    wait = module.params.get('wait')
    public = module.params.get('public')
    api_subnet_allow_list = module.params.get('api_subnet_allow_list')
    s3_buckets_param = module.params.get('s3_buckets')

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    s3_buckets = None
    if s3_buckets_param:
        s3_buckets = []
        for bucket_name in s3_buckets:
            bucket = S3Bucket(name=bucket_name)
            s3_buckets.append(bucket)

    k8s_server = ionoscloud.KubernetesApi(api_client=client)

    cluster = None
    clusters = k8s_server.k8s_get(depth=2)
    for c in clusters.items:
        if cluster_name == c.properties.name:
            cluster = c
            break

    should_change = cluster is None

    if module.check_mode:
        module.exit_json(changed=should_change)

    if not should_change:
        return {
            'changed': should_change,
            'failed': False,
            'action': 'create',
            'cluster': cluster.to_dict()
        }

    try:
        k8s_cluster_properties = KubernetesClusterProperties(name=cluster_name, k8s_version=k8s_version,
                                                             maintenance_window=maintenance_window, public=public,
                                                             api_subnet_allow_list=api_subnet_allow_list,
                                                             s3_buckets=s3_buckets)
        k8s_cluster = KubernetesCluster(properties=k8s_cluster_properties)

        response = k8s_server.k8s_post_with_http_info(kubernetes_cluster=k8s_cluster)
        (k8s_response, _, headers) = response

        if wait:
            client.wait_for(
                fn_request=lambda: k8s_server.k8s_get(depth=2),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == cluster_name,
                    r.items
                ))[0].metadata.state == 'ACTIVE',
                scaleup=10000
            )

        results = {
            'changed': True,
            'failed': False,
            'action': 'create',
            'cluster': k8s_response.to_dict()
        }

        return results

    except Exception as e:
        module.fail_json(
            msg="failed to create the k8s cluster: %s" % to_native(e))


def delete_k8s_cluster(module, client):
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    changed = False

    k8s_server = ionoscloud.KubernetesApi(api_client=client)
    k8s_cluster_list = k8s_server.k8s_get(depth=5)
    k8s_cluster = _get_resource(k8s_cluster_list, k8s_cluster_id)

    if not k8s_cluster:
        module.exit_json(changed=False)

    try:
        response = k8s_server.k8s_delete_with_http_info(k8s_cluster_id=k8s_cluster_id)
        (k8s_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to delete the k8s cluster: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': k8s_cluster_id
    }


def update_k8s_cluster(module, client):
    cluster_name = module.params.get('cluster_name')
    k8s_version = module.params.get('k8s_version')
    k8s_cluster_id = module.params.get('k8s_cluster_id')
    maintenance = module.params.get('maintenance_window')
    api_subnet_allow_list = module.params.get('api_subnet_allow_list')
    s3_buckets_param = module.params.get('s3_buckets')

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    s3_buckets = None
    if s3_buckets_param:
        s3_buckets = []
        for bucket_name in s3_buckets:
            bucket = S3Bucket(name=bucket_name)
            s3_buckets.append(bucket)

    k8s_server = ionoscloud.KubernetesApi(api_client=client)
    k8s_response = None

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        kubernetes_cluster_properties = KubernetesClusterPropertiesForPut(name=cluster_name, k8s_version=k8s_version,
                                                                          s3_buckets=s3_buckets,
                                                                          api_subnet_allow_list=api_subnet_allow_list,
                                                                          maintenance_window=maintenance_window)
        kubernetes_cluster = KubernetesClusterForPut(properties=kubernetes_cluster_properties)
        k8s_response = k8s_server.k8s_put(k8s_cluster_id=k8s_cluster_id, kubernetes_cluster=kubernetes_cluster)

        if module.params.get('wait'):
            client.wait_for(
                fn_request=lambda: k8s_server.k8s_get(depth=2),
                fn_check=lambda r: list(filter(
                    lambda e: e.properties.name == cluster_name,
                    r.items
                ))[0].metadata.state == 'ACTIVE',
                scaleup=10000
            )
        changed = True
    except Exception as e:
        module.fail_json(
            msg="failed to update the k8s cluster: %s" % to_native(e))
        changed = False

    return {
        'changed': changed,
        'failed': False,
        'action': 'update',
        'cluster': k8s_response.to_dict()
    }


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


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

        try:
            if state == 'present':
                module.exit_json(**create_k8s_cluster(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_k8s_cluster(module, api_client))
            elif state == 'update':
                module.exit_json(**update_k8s_cluster(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e), state=state))


if __name__ == '__main__':
    main()
