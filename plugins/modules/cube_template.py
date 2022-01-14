#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native


def get_template(module, client):
    """
    List templates or find template by UUID

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The list of templates.
    """

    template_id = module.params.get('template_id')
    template_server = ionoscloud.TemplatesApi(client)
    template_response = None

    try:
        if template_id:
            template_response = template_server.templates_find_by_id(template_id)

        else:
            template_response = template_server.templates_get(depth=2)

    except ApiException as e:
        module.fail_json(msg="failed to get the template list: %s" % to_native(e))

    return {
        'changed': False,
        'failed': False,
        'template': template_response.to_dict()
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            template_id=dict(type='str'),
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
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

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

        try:
            (template_dict_array) = get_template(module, api_client)
            module.exit_json(**template_dict_array)
        except Exception as e:
            module.fail_json(msg='failed to get template: %s' % to_native(e))


if __name__ == '__main__':
    main()
