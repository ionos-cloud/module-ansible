ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLES = '''
    - name: Create pcc
      pcc:
        name: "{{ name }}"
        description: "{{ description }}"

    - name: Update pcc
      pcc:
        pcc_id: "49e73efd-e1ea-11ea-aaf5-5254001a8838"
        name: "{{ new_name }}"
        description: "{{ new_description }}"
        state: update

    - name: Remove pcc
      pcc:
        pcc_id: "2851af0b-e1ea-11ea-aaf5-5254001a8838"
        state: absent
'''

HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import PrivateCrossConnect
    from ionoscloud.models import PrivateCrossConnectProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

import re


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_pcc(module, client):
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    pcc_properties = PrivateCrossConnectProperties(name=name, description=description)
    pcc = PrivateCrossConnect(properties=pcc_properties)

    try:
        response = pcc_server.pccs_post_with_http_info(pcc)
        (pcc_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'pcc': pcc_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to create the pcc: %s" % to_native(e))


def delete_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    try:
        pcc_server.pccs_delete(pcc_id)
        return {
            'action': 'delete',
            'changed': True,
            'id': pcc_id
        }
    except Exception as e:
        module.fail_json(msg="failed to delete the pcc: %s" % to_native(e))
        return {
            'action': 'delete',
            'changed': False,
            'id': pcc_id
        }


def update_pcc(module, client):
    pcc_id = module.params.get('pcc_id')
    name = module.params.get('name')
    description = module.params.get('description')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    pcc_server = ionoscloud.PrivateCrossConnectsApi(client)

    pcc_properties = PrivateCrossConnectProperties(name=name, description=description)

    if module.check_mode:
        module.exit_json(changed=True)
    try:
        response = pcc_server.pccs_patch_with_http_info(pcc_id=pcc_id, pcc=pcc_properties)
        (pcc_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            'pcc': pcc_response.to_dict()
        }

    except Exception as e:
        module.fail_json(msg="failed to update the pcc: %s" % to_native(e))
        return {
            'changed': False,
            'failed': True,
            'action': 'update',
        }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            pcc_id=dict(type='str'),
            name=dict(type='str'),
            description=dict(type='str'),
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
    api_url = module.params.get('api_url')
    user_agent = 'ionoscloud-python/%s Ansible/%s' % (sdk_version, __version__)

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    configuration = ionoscloud.Configuration(**conf)

    state = module.params.get('state')

    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent

        if state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new pcc')
            if not module.params.get('description'):
                module.fail_json(msg='description parameter is required for a new pcc')
            try:
                (pcc_dict_array) = create_pcc(module, api_client)
                module.exit_json(**pcc_dict_array)
            except Exception as e:
                module.fail_json(msg='failed to set user state: %s' % to_native(e))

        elif state == 'absent':
            if not module.params.get('pcc_id'):
                module.fail_json(msg='pcc_id parameter is required for deleting a pcc.')
            try:
                (changed) = delete_pcc(module, api_client)
                module.exit_json(changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set pcc state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('pcc_id'):
                module.fail_json(msg='pcc_id parameter is required for updating a pcc.')
            try:
                (changed) = update_pcc(module, api_client)
                module.exit_json(
                    changed=changed)
            except Exception as e:
                module.fail_json(msg='failed to set pcc state: %s' % to_native(e))


if __name__ == '__main__':
    main()
