import re

from ansible.module_utils.basic import env_fallback



class CommonIonosModule():
    def __init__(self):
        pass

    def get_module_arguments(self):
        arguments = {}

        for option_name, option in self.options.items():
            arguments[option_name] = {
                'type': option['type'],
            }
            for key in ['choices', 'default', 'aliases', 'no_log', 'elements']:
                if option.get(key) is not None:
                    arguments[option_name][key] = option.get(key)

                if option.get('env_fallback'):
                    arguments[option_name]['fallback'] = (env_fallback, [option['env_fallback']])

                if len(option.get('required', [])) == len(self.states):
                    arguments[option_name]['required'] = True

        return arguments


    def get_sdk_config(self):
        username = self.module.params.get('username')
        password = self.module.params.get('password')
        token = self.module.params.get('token')
        api_url = self.module.params.get('api_url')
        certificate_fingerprint = self.module.params.get('certificate_fingerprint')

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

        if certificate_fingerprint is not None:
            conf['fingerprint'] = certificate_fingerprint

        return self.sdk.Configuration(**conf)


    def check_required_arguments(self, state):
        # manually checking if token or username & password provided
        if (
            not self.module.params.get('token')
            and not (self.module.params.get('username') and self.module.params.get('password'))
        ):
            self.module.fail_json(
                msg='Token or username & password are required for {object_name} state {state}'.format(
                    object_name=self.object_name,
                    state=state,
                ),
            )

        for option_name, option in self.options.items():
            if state in option.get('required', []) and not self.module.params.get(option_name):
                self.module.fail_json(
                    msg='{option_name} parameter is required for {object_name} state {state}'.format(
                        option_name=option_name,
                        object_name=self.object_name,
                        state=state,
                    ),
                )
    
    def _should_replace_object(self, existing_object):
        pass

    def _should_update_object(self, existing_object):
        pass


    def _get_object_list(self, client):
        pass


    def _get_object_name(self):
        pass

    def _get_object_identifier(self):
        pass

    def _create_object(self, client, existing_object=None):
        pass

    def update_replace_object(self, client, existing_object):
        module = self.module
        if self._should_replace_object(existing_object):

            if not module.params.get('allow_replace'):
                module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(OBJECT_NAME))

            new_object = self._create_object(client, existing_object).to_dict()
            self._remove_object(client, existing_object)
            return {
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: new_object,
            }
        if self._should_update_object(existing_object):
            # Update
            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                self.returned_key: self._update_object(client, existing_object).to_dict()
            }

        # No action
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            self.returned_key: existing_object.to_dict()
        }


    def create_object(self, client):
        existing_object = get_resource(self.module, self._get_object_list(client), self._get_object_name())

        if existing_object:
            return self.update_replace_object(client, existing_object)

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            self.returned_key: self._create_object(client).to_dict()
        }


    def update_object(self, client):
        object_name = self._get_object_name()
        object_list = self._get_object_list(client)

        existing_object = get_resource(self.module, object_list, self._get_object_identifier())

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        existing_object_id_by_new_name = get_resource_id(self.module, object_list, object_name)

        if (
            existing_object.id is not None
            and existing_object_id_by_new_name is not None
            and existing_object_id_by_new_name != existing_object.id
        ):
            self.module.fail_json(
                msg='failed to update the {}: Another resource with the desired name ({}) exists'.format(
                    self.object_name, object_name,
                ),
            )

        return self.update_replace_object(client, existing_object)


    def remove_object(self, client):
        existing_object = get_resource(self.module, self._get_object_list(client), self._get_object_identifier())

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        self._remove_object(client, existing_object)

        return {
            'action': 'delete',
            'changed': True,
            'id': existing_object.id,
        }



    def _get_request_id(self, headers):
        match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
        if match:
            return match.group(1)
        else:
            raise Exception("Failed to extract request ID from response "
                            "header 'location': '{location}'".format(location=headers['location']))


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
