import copy
from operator import mod
import yaml

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native
import re

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_dbaas_mongo
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % (__version__, ionoscloud.__version__)
DBAAS_MONGO_USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-dbaas-mongo/%s' % (
    __version__, ionoscloud_dbaas_mongo.__version__)
DOC_DIRECTORY = 'dbaas-mongo'
STATES = ['present', 'update', 'absent']
OBJECT_NAME = 'Mongo Cluster User'
RETURNED_KEY = 'mongo_cluster_user'

OPTIONS = {
    'mongo_cluster': {
        'description': ['The UUID or name of an existing Mongo Cluster.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'mongo_username': {
        'description': ['The username of the user.'],
        'available': STATES,
        'required': STATES,
        'type': 'str',
    },
    'mongo_password': {
        'description': ['The password of the user.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'no_log': True,
        'type': 'str',
    },
    'user_roles': {
        'description': [
          'A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'
          "'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase'"
          "'database': the name of the databse to which the role applies"
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
    },
    'allow_replace': {
        'description': [
            'Boolean indicating if the resource should be recreated when the state cannot be reached in '
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
module: mongo_cluster
short_description: Allows operations with Ionos Cloud Mongo Cluster Users.
description:
     - This is a module that supports creating and destroying Mongo Cluster Users
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-dbaas-mongo >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <password>
      user_roles:
        - role: read
          database: test
    register: mongo_user_response
  ''',
    'update': '''- name: Update User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <newPassword>
      user_roles:
        - role: read
          database: test
        - role: readWrite
          database: test
      state: update
    register: mongo_user_response
  ''',
    'absent': '''- name: Delete Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
    register: mongo_user_response
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
    return False


def _should_update_object(module, existing_object):
    def sort_func(el):
        return el['database'], el['role']
    
    existing_roles = sorted(
        [{'role': role.role, 'database': role.database} for role in existing_object.properties.roles],
        key=sort_func,
    )
    return (
        module.params.get('mongo_password') is not None
        and existing_object.properties.password != module.params.get('mongo_password')
        or module.params.get('roles') is not None
        and existing_roles != sorted(module.params.get('roles'), key=sort_func)
    )


def _get_object_list(module, client):
    mongo_cluster_id = get_resource_id(
        module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
        module.params.get('mongo_cluster'),
        [['id'], ['properties', 'display_name']],
    )
    return ionoscloud_dbaas_mongo.UsersApi(client).clusters_users_get(mongo_cluster_id)


def _get_object_name(module):
    return module.params.get('mongo_username')


def _get_object_identifier(module):
    return module.params.get('mongo_username')


def _create_object(module, client, existing_object=None):
    mongo_username = module.params.get('mongo_username')
    mongo_password = module.params.get('mongo_password')
    user_roles = list(map(
        lambda role: ionoscloud_dbaas_mongo.UserRoles(role=role['role'], database=role['database']),
        module.params.get('user_roles'),
    ))

    if existing_object is not None:
        mongo_username = existing_object.properties.username if mongo_username is None else mongo_username
        user_roles = existing_object.properties.roles if user_roles is None else user_roles

    users_api = ionoscloud_dbaas_mongo.UsersApi(client)

    mongo_user = ionoscloud_dbaas_mongo.User(properties=ionoscloud_dbaas_mongo.UserProperties(
        username=mongo_username,
        password=mongo_password,
        roles=user_roles,
    ))

    try:
        mongo_cluster_id = get_resource_id(
            module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
            module.params.get('mongo_cluster'),
            [['id'], ['properties', 'display_name']],
        )
        user_response = users_api.clusters_users_post(mongo_cluster_id, mongo_user)
    except ionoscloud_dbaas_mongo.ApiException as e:
        module.fail_json(msg="failed to create the new Mongo Cluster User: %s" % to_native(e))
    return user_response


def _update_object(module, client, existing_object):
    mongo_password = module.params.get('mongo_password')
    user_roles = list(map(
        lambda role: ionoscloud_dbaas_mongo.UserRoles(role=role['role'], database=role['database']),
        module.params.get('user_roles'),
    ))
    users_api = ionoscloud_dbaas_mongo.UsersApi(client)

    mongo_user = ionoscloud_dbaas_mongo.PatchUserRequest(properties=ionoscloud_dbaas_mongo.PatchUserProperties(
        password=mongo_password,
        roles=user_roles,
    ))
    
    try:
        mongo_cluster_id = get_resource_id(
            module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
            module.params.get('mongo_cluster'),
            [['id'], ['properties', 'display_name']],
        )
        user_response = users_api.clusters_users_patch(
            mongo_cluster_id,
            module.params.get('mongo_username'),
            mongo_user,
        )
    except ionoscloud_dbaas_mongo.ApiException as e:
        module.fail_json(msg="failed to update the Mongo Cluster User: %s" % to_native(e))

    return user_response

def _remove_object(module, client, existing_object):
    users_api = ionoscloud_dbaas_mongo.UsersApi(client)

    try:
        mongo_cluster_id = get_resource_id(
            module, ionoscloud_dbaas_mongo.ClustersApi(client).clusters_get(),
            module.params.get('mongo_cluster'),
            [['id'], ['properties', 'display_name']],
        )
        users_api.clusters_users_delete(mongo_cluster_id, existing_object.properties.username)
        if module.params.get('wait'):
            try:
                client.wait_for(
                    fn_request=lambda: users_api.clusters_users_find_by_id(
                        mongo_cluster_id, existing_object.properties.username,
                    ),
                    fn_check=lambda _: False,
                    scaleup=10000,
                    timeout=module.params.get('wait_timeout'),
                )
            except ionoscloud_dbaas_mongo.ApiException as e:
                if e.status != 404:
                    raise e
    except Exception as e:
        module.fail_json(msg="failed to delete the Mongo Cluster User: %s" % to_native(e))


def update_replace_object(module, client, existing_object):
    if _should_replace_object(module, existing_object):

        if not module.params.get('allow_replace'):
            module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

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
    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_name(module),
        [['properties', 'username']],
    )

    if existing_object:
        return update_replace_object(module, client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, client).to_dict()
    }


def update_object(module, client):
    object_list = _get_object_list(module, client)

    existing_object = get_resource(
        module, object_list, _get_object_identifier(module),
        [['properties', 'username']],
    )

    if existing_object is None:
        module.exit_json(changed=False)
        return

    return update_replace_object(module, client, existing_object)


def remove_object(module, client):
    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_identifier(module),
        [['properties', 'username']],
    )

    if existing_object is None:
        module.exit_json(changed=False)
        return

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.properties.username,
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
        module.fail_json(msg='both ionoscloud and ionoscloud_dbaas_mongo are required for this module, '
                             'run `pip install ionoscloud ionoscloud_dbaas_mongo`')

    dbaas_mongo_api_client = ionoscloud_dbaas_mongo.ApiClient(get_sdk_config(module, ionoscloud_dbaas_mongo))
    dbaas_mongo_api_client.user_agent = DBAAS_MONGO_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, dbaas_mongo_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, dbaas_mongo_api_client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, dbaas_mongo_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ),
        )


if __name__ == '__main__':
    main()
