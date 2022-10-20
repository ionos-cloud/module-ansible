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

OPTIONS = {
    'certificate_id': {
        'description': ['The certificate ID.'],
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
            certificate_id: "{{ certificate.certificate.id }}"
            certificate_name: "{{ certificate_updated_name }}"
            state: update
        register: updated_certificate
  ''',
    'absent': '''
    - name: Delete Certificate
        certificate:
        certificate_id: "{{ certificate.certificate.id }}"
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


def create_certificate(module, client):

    certificate_file = module.params.get('certificate_file')
    private_key_file = module.params.get('private_key_file')
    certificate_chain_file = module.params.get('certificate_chain_file')
    certificate_name = module.params.get('certificate_name')

    certificate_server = ionoscloud_cert_manager.CertificatesApi(client)

    existing_certificates = certificate_server.certificates_get()

    existing_certificate = get_resource(module, existing_certificates, certificate_name)

    if existing_certificate:
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            'certificate': existing_certificate.to_dict()
        }

    try:
        new_certificate = certificate_server.certificates_post(
            ionoscloud_cert_manager.CertificatePostDto(
                properties=ionoscloud_cert_manager.CertificatePostPropertiesDto(
                    name=certificate_name,
                    certificate=open(certificate_file, mode='r').read(),
                    certificate_chain=open(certificate_chain_file, mode='r').read() if certificate_chain_file else None,
                    private_key=open(private_key_file, mode='r').read(),
                )
            )
        )
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'certificate': new_certificate.to_dict()
        }

    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to create the new certificate: %s" % to_native(e))


def delete_certificate(module, client):
    certificate_name = module.params.get('certificate_name')
    certificate_id = module.params.get('certificate_id')

    certificate_server = ionoscloud_cert_manager.CertificatesApi(client)
    certificates_list = certificate_server.certificates_get()

    certificate_id = get_resource_id(module, certificates_list, certificate_id if certificate_id is not None else certificate_name)

    if not certificate_id:
        module.exit_json(changed=False)

    try:
        certificate_server.certificates_delete(certificate_id)
        return {
            'failed': False,
            'action': 'delete',
            'id': certificate_id,
        }

    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to delete the certificate: %s" % to_native(e))


def update_certificate(module, client):
    certificate_name = module.params.get('certificate_name')
    certificate_id = module.params.get('certificate_id')

    certificate_server = ionoscloud_cert_manager.CertificatesApi(client)
    certificates_list = certificate_server.certificates_get()

    existing_certificate_id_by_name = get_resource_id(module, certificates_list, certificate_name)

    if existing_certificate_id_by_name is not None:
        if existing_certificate_id_by_name != certificate_id:
            module.fail_json(
                msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(OBJECT_NAME, certificate_name),
            )
        else:
            return {
                'changed': False,
                'failed': False,
                'action': 'update',
                'certificate': existing_certificate_id_by_name.to_dict()
            }

    try:
        updated_certificate = certificate_server.certificates_patch(
            certificate_id,
            ionoscloud_cert_manager.CertificatePatchDto(
                properties=ionoscloud_cert_manager.CertificatePatchPropertiesDto(
                    name=certificate_name,
                )
            )
        )
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            'certificate': updated_certificate.to_dict()
        }

    except ionoscloud_cert_manager.ApiException as e:
        module.fail_json(msg="failed to create the new certificate: %s" % to_native(e))


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
                module.exit_json(**create_certificate(module, api_client))
            elif state == 'absent':
                module.exit_json(**delete_certificate(module, api_client))
            elif state == 'update':
                module.exit_json(**update_certificate(module, api_client))
        except Exception as e:
            module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME,
                                                                                             error=to_native(e),
                                                                                             state=state))


if __name__ == '__main__':
    main()
