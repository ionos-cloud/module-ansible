from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible import __version__
import re

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

HAS_SDK = True

EXAMPLES = '''
- name: Create k8s cluster
  k8s_cluster:
    name: "{{ cluster_name }}"

- name: Delete k8s cluster
  k8s_cluster:
    k8s_cluster_id: "a9b56a4b-8033-4f1a-a59d-cfea86cfe40b"
    state: absent

- name: Update k8s cluster
  k8s_cluster:
    k8s_cluster_id: "89a5aeb0-d6c1-4cef-8f6b-2b9866d85850"
    maintenance_window:
      day_of_the_week: 'Tuesday'
      time: '13:03:00'
    k8s_version: 1.17.8
    state: update
'''

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import KubernetesCluster, KubernetesClusterProperties, KubernetesClusterPropertiesForPut, \
        KubernetesClusterForPut
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False


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

    maintenance_window = None
    if maintenance:
        maintenance_window = dict(maintenance)
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

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
                                                             maintenance_window=maintenance_window)
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

    maintenance_window = dict(maintenance)
    maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    k8s_server = ionoscloud.KubernetesApi(api_client=client)
    k8s_response = None

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        kubernetes_cluster_properties = KubernetesClusterPropertiesForPut(name=cluster_name, k8s_version=k8s_version,
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cluster_name=dict(type='str'),
            k8s_cluster_id=dict(type='str'),
            k8s_version=dict(type='str'),
            maintenance_window=dict(
                type='dict',
                day_of_the_week=dict(type='str'),
                time=dict(type='str')
            ),
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
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
            token=dict(
                type='str',
                required=True,
                fallback=(env_fallback, ['IONOS_TOKEN']),
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
            msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    token = module.params.get('token')
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

    state = module.params.get('state')

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

    configuration = ionoscloud.Configuration(**conf)

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'present':
            if not module.params.get('cluster_name'):
                module.fail_json(
                    msg='cluster_name parameter is required for a new k8s cluster')
            try:
                (k8s_cluster_dict_array) = create_k8s_cluster(module, api_client)
                module.exit_json(**k8s_cluster_dict_array)
            except Exception as e:
                module.fail_json(
                    msg='failed to set k8s cluster state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('k8s_cluster_id'):
                module.fail_json(
                    msg='k8s_cluster_id parameter is required for deleting a k8s cluster.')
            try:
                (changed) = delete_k8s_cluster(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(
                    msg='failed to set k8s cluster state: %s' % to_native(e))

        elif state == 'update':
            error_message = "%s parameter is required updating a k8s cluster."
            if not module.params.get('k8s_cluster_id'):
                module.fail_json(msg=error_message % 'k8s_cluster_id')
            if not module.params.get('cluster_name'):
                module.fail_json(msg=error_message % 'cluster_name')

            try:
                (changed) = update_k8s_cluster(module, api_client)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(
                    msg='failed to set k8s cluster state: %s' % to_native(e))


if __name__ == '__main__':
    main()
