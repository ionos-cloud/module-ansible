import re
import copy
import yaml

HAS_SDK = True
try:
    import ionoscloud_cert_manager
    from ionoscloud_cert_manager import __version__ as certificate_manager_sdk_version
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}
CERTIFICATE_MANAGER_USER_AGENT = 'ansible-module/%s_sdk-python-certificate-manager/%s' % ( __version__, certificate_manager_sdk_version)
DOC_DIRECTORY = 'certificate'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'Certificate'
RETURNED_KEY = 'certificate'

OPTIONS = {
    'certificate': {
        'description': ['The certificate name or ID.'],
        'available': ['update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'certificate_name': {
        'description': ['The certificate name.'],
        'available': ['present', 'update', 'absent'],
        'required': ['update'],
        'type': 'str',
    },
    'certificate_file': {
        'description': ['File containing the certificate body.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'private_key_file': {
        'description': ['File containing the private key blob.'],
        'available': ['present'],
        'required': ['present'],
        'type': 'str',
    },
    'certificate_chain_file': {
        'description': ['File containing the certificate chain.'],
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
module: certificate
short_description: Upload, update or delete a certificate in the Ionos Cloud Certificate Manager.
description:
     - This is a simple module that supports uploading, updating or deleting certificates in the
      Ionos Cloud Certificate Manager.
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud_cert_manager >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''
    - name: Create Certificate
        certificate:
            certificate_name: "{{ certificate_name }}"
            certificate_file: "{{ certificate_path }}"
            private_key_file: "{{ certificate_key_path }}"
        register: certificate
  ''',
    'update': '''
    - name: Update Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            certificate_name: "{{ certificate_updated_name }}"
            state: update
        register: updated_certificate
  ''',
    'absent': '''
    - name: Delete Certificate
        certificate:
            certificate: "{{ certificate.certificate.id }}"
            state: delete
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


def _should_replace_object(module, existing_object):
    certificate_file = module.params.get('certificate_file')
    certificate_chain_file = module.params.get('certificate_chain_file')

    certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None
    certificate=open(certificate_file, mode='r').read() if certificate_file else None

    return (
        certificate is not None
        and existing_object.properties.certificate.rstrip() != certificate.rstrip()
        or certificate_chain is not None
        and existing_object.properties.certificate_chain.rstrip() != certificate_chain.rstrip()
        or module.params.get('private_key_file')
    )


def _should_update_object(module, existing_object):
    return (
        module.params.get('certificate_name') is not None
        and existing_object.properties.name != module.params.get('certificate_name')
    )


def _get_object_list(module, client):
    return ionoscloud_cert_manager.CertificatesApi(client).certificates_get()


def _get_object_name(module):
    return module.params.get('certificate_name')


def _get_object_identifier(module):
    return module.params.get('certificate')


def _create_object(module, client, existing_object=None):
    certificate_file = module.params.get('certificate_file')
    private_key_file = module.params.get('private_key_file')
    certificate_chain_file = module.params.get('certificate_chain_file')
    certificate_name = module.params.get('certificate_name')

    certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None
    certificate=open(certificate_file, mode='r').read()

    if existing_object is not None:
        certificate_name = existing_object.properties.certificate_name if certificate_name is None else certificate_name
        certificate_chain = existing_object.properties.certificate_chain if certificate_chain is None else certificate_chain
        certificate = existing_object.properties.certificate if certificate is None else certificate

    certificates_api = ionoscloud_cert_manager.CertificatesApi(client)

    try:
        new_certificate = certificates_api.certificates_post(
            ionoscloud_cert_manager.CertificatePostDto(
                properties=ionoscloud_cert_manager.CertificatePostPropertiesDto(
                    name=certificate_name,
                    certificate=certificate,
                    certificate_chain=certificate_chain,
                    private_key=open(private_key_file, mode='r').read(),
                ),
            ),
        )
    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to create the new certificate: %s" % to_native(e))
    return new_certificate


def _update_object(module, client, existing_object):
    try:
        updated_certificate = ionoscloud_cert_manager.CertificatesApi(client).certificates_patch(
            existing_object.id,
            ionoscloud_cert_manager.CertificatePatchDto(
                properties=ionoscloud_cert_manager.CertificatePatchPropertiesDto(
                    name=module.params.get('certificate_name'),
                ),
            ),
        )

        return updated_certificate
    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to update the certificate: %s" % to_native(e))


def _remove_object(module, client, existing_object):
    try:
        ionoscloud_cert_manager.CertificatesApi(client).certificates_delete(existing_object.id)
    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to remove the certificate: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, client, existing_object).to_dict()
        _remove_object(module, client, existing_object)
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
            RETURNED_KEY: _update_object(module, client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


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
    module = AnsibleModule(argument_spec=get_module_arguments(), supports_check_mode=True)

    if not HAS_SDK:
        module.fail_json(msg='ionoscloud_cert_manager is required for this module, run `pip install ionoscloud_cert_manager`')

    state = module.params.get('state')
    with ionoscloud_cert_manager.ApiClient(get_sdk_config(module, ionoscloud_cert_manager)) as api_client:
        api_client.user_agent = CERTIFICATE_MANAGER_USER_AGENT
        check_required_arguments(module, state, OBJECT_NAME)

        try:
            if state == 'present':
                module.exit_json(**create_object(module, api_client))
            elif state == 'absent':
                module.exit_json(**remove_object(module, api_client))
            elif state == 'update':
                module.exit_json(**update_object(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME,
                error=to_native(e),
                state=state,
            ))


if __name__ == '__main__':
    main()
