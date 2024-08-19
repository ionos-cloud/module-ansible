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
            changes, an array of changes if replace would occur
        """
        pass

    def _should_update_object(self, existing_object, clients):
        """
        Checks if the object should be updated based on the input and the object state.

        existing_object : Ionoscloud object returned by API object
        clients: authenticated ionoscloud clients list.

        Returns:
            bool, if the object should be updated
            changes, an array of changes if updated would occur
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

        should_replace, replace_changes = self._should_replace_object(existing_object, clients)
        if should_replace:

            if not module.params.get('allow_replace'):
                module.fail_json(msg="{} should be replaced but allow_replace is set to False.".format(self.object_name))

            if module.check_mode:
                module.exit_json(
                    **{
                        'changed': True,
                        'diff': {
                            'prepared': str(replace_changes),
                        },
                    },
                )
            new_object = self._create_object(existing_object, clients).to_dict()
            self._remove_object(existing_object, clients)
            return {
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: new_object,
            }
        
        should_update, update_changes = self._should_update_object(existing_object, clients)
        if should_update:
            if module.check_mode:
                module.exit_json(
                    **{
                        'skipped': True,
                        'diff': {
                            'prepared': yaml.safe_dump(update_changes),
                        },
                    },
                )

            # Update
            return {
                'changed': True,
                'failed': False,
                'action': 'update',
                self.returned_key: self._update_object(existing_object, clients).to_dict()
            }

        # No action
        return {
            'changed': False,
            'failed': False,
            'action': 'create',
            self.returned_key: existing_object.to_dict()
        }


    def present_object(self, clients):
        existing_object = get_resource(
            self.module, self._get_object_list(clients),
            self._get_object_name(), self.object_identity_paths,
        )

        if existing_object:
            return self.update_replace_object(existing_object, clients)

        if self.module.check_mode:
            self.module.exit_json(
                **{
                    'skipped': True,
                    'diff': [
                        '{object_name} {object_name_identifier} would be created'.format(
                            object_name=self.object_name,
                            object_name_identifier= self._get_object_name(),
                        ),
                    ],
                },
            )

        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            self.returned_key: self._create_object(None, clients).to_dict()
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

        if self.module.check_mode:
            self.module.exit_json(
                **{
                    'skipped': True,
                    'diff': [
                        '{object_name} {object_name_identifier} would be deleted'.format(
                            object_name=self.object_name,
                            object_name_identifier=self._get_object_identifier(),
                        ),
                    ],
                },
            )

        self._remove_object(existing_object, clients)

        return {
            'action': 'delete',
            'changed': True,
            'id': existing_object.id,
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
