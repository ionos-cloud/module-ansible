import yaml

from ansible.module_utils._text import to_native

from .common_ionos_methods import (
    get_resource, get_resource_id, get_sdk_config, check_required_arguments,
)


class CommonIonosModule():
    def __init__(self):
        self.object_identity_paths = None
    """
    """
    def _should_replace_object(self, existing_object, clients):
        """
        Checks if the object should be replaced based on the input and the object state.

        existing_object : Ionoscloud object returned by API object
        clients: authenticated ionoscloud clients list.

        Returns:
            bool, if the object should be replaced
        """
        pass

    def _should_update_object(self, existing_object, clients):
        """
        Checks if the object should be updated based on the input and the object state.

        existing_object : Ionoscloud object returned by API object
        clients: authenticated ionoscloud clients list.

        Returns:
            bool, if the object should be updated
        """
        pass


    def get_object_before(self, existing_object, clients):
        """
        Return a dict with the 'before' state for the object

        existing_object : Ionoscloud object returned by API object
        clients: authenticated ionoscloud clients list.

        Returns:
            dict, a dict with the object properties before the task is executed
        """
        pass


    def get_object_after(self, existing_object, clients):
        """
        Return a dict with the 'after' state for the object

        existing_object : Ionoscloud object returned by API object
        clients: authenticated ionoscloud clients list.

        Returns:
            dict, a dict with the object properties after the task is executed
        """
        pass


    def _get_object_list(self, clients):
        """
        Retrieve a list of the objects from the API

        clients: authenticated ionoscloud clients list.

        Returns:
            list[object], the list of objects
        """
        pass


    def _get_object_name(self):
        """
        Retrieve the name object from the user input

        Returns:
            str, the object name
        """
        pass

    def _get_object_identifier(self):
        """
        Retrieve the object identifier from the user input

        Returns:
            str, the object identifier
        """
        pass

    def update_replace_object(self, existing_object, clients):
        module = self.module
        obj_identifier = self._get_object_identifier() if self._get_object_identifier() is not None else self._get_object_name()
        object_after = self.get_object_after(existing_object, clients)

        returned_json = {}

        if module._diff:
            returned_json['diff'] = {
                'before': self.get_object_before(existing_object, clients),
                'after': object_after,
            }

        if self._should_replace_object(existing_object, clients):

            if not module.params.get('allow_replace'):
                module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(self.object_name))

            if module.check_mode:
                return {
                    **returned_json,
                    **{
                        'changed': True,
                        'msg': '{object_name} {object_name_identifier} would be recreated'.format(
                            object_name=self.object_name, object_name_identifier=obj_identifier,
                        ),
                        self.returned_key: {
                            'id': existing_object.id,
                            'properties': object_after,
                        },
                    },
                }

            new_object = self._create_object(existing_object, clients).to_dict()
            self._remove_object(existing_object, clients)
            return {
                **returned_json,
                **{
                    'changed': True,
                    'failed': False,
                    'action': 'create',
                    self.returned_key: new_object,
                },
            }
        
        if self._should_update_object(existing_object, clients):
            if module.check_mode:
                return {
                    **returned_json,
                    **{
                        'changed': True,
                        'msg': '{object_name} {object_name_identifier} would be updated'.format(
                            object_name=self.object_name, object_name_identifier=obj_identifier,
                        ),
                        self.returned_key: {
                            'id': existing_object.id,
                            'properties': object_after,
                        },
                    },
                }

            # Update
            return {
                **returned_json,
                **{
                    'changed': True,
                    'failed': False,
                    'action': 'update',
                    self.returned_key: self._update_object(existing_object, clients).to_dict(),
                },
            }

        # No action
        return {
            **returned_json,
            **{
                'changed': False,
                'failed': False,
                'action': 'create',
                self.returned_key: existing_object.to_dict(),
            },
        }


    def present_object(self, clients):
        existing_object = get_resource(
            self.module, self._get_object_list(clients),
            self._get_object_name(), self.object_identity_paths,
        )

        if existing_object:
            return self.update_replace_object(existing_object, clients)

        returned_json = {}
        object_after = self.get_object_after(existing_object, clients)
        if self.module._diff:
            returned_json['diff'] = {
                'before': {},
                'after': object_after,
            }

        if self.module.check_mode:
            return {
                **returned_json,
                **{
                    'changed': True,
                    'msg': '{object_name} {object_name_identifier} would be created'.format(
                        object_name=self.object_name, object_name_identifier=self._get_object_name(),
                    ),
                    self.returned_key: {
                        'id': '<known after creation>',
                        'properties': object_after,
                    },
                },
            }

        return {
            **returned_json,
            **{
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: self._create_object(None, clients).to_dict(),
            },
        }


    def update_object(self, clients):
        object_name = self._get_object_name()
        object_list = self._get_object_list(clients)

        existing_object = get_resource(
            self.module, object_list,
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        existing_object_id_by_new_name = get_resource_id(
            self.module, object_list,
            object_name, self.object_identity_paths,
        )

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

        return self.update_replace_object(existing_object, clients)


    def absent_object(self, clients):
        existing_object = get_resource(
            self.module, self._get_object_list(clients),
            self._get_object_identifier(),
            self.object_identity_paths,
        )

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        returned_json = {}

        if self.module._diff:
            returned_json['diff'] = {
                'before': self.get_object_before(existing_object, clients),
                'after': {},
            }

        if self.module.check_mode:
            return {
                **returned_json,
                **{
                    'changed': True,
                    'msg': '{object_name} {object_name_identifier} would be deleted'.format(
                        object_name=self.object_name, object_name_identifier=self._get_object_identifier(),
                    ),
                },
            }

        self._remove_object(existing_object, clients)

        return {
            **returned_json,
            **{
                'action': 'delete',
                'changed': True,
                'id': existing_object.id,
            },
        }


    def main(self):
        state = self.module.params.get('state')
        clients = [sdk.ApiClient(get_sdk_config(self.module, sdk)) for sdk in self.sdks]
        for i, client in enumerate(clients):
            client.user_agent = self.user_agents[i]
        check_required_arguments(self.module, state, self.object_name, self.options)

        try:
            self.module.exit_json(**getattr(self, state + '_object')(clients))
        except Exception as e:
            self.module.fail_json(msg='failed to set {object_name} state {state}: {error}'.format(object_name=self.object_name, error=to_native(e), state=state))
