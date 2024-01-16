from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
HAS_SDK = True
try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import BackupUnit, BackupUnitProperties
    from ionoscloud.rest import ApiException
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import get_module_arguments, _get_request_id
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options_with_replace

    
ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)
DOC_DIRECTORY = 'managed-backup'
OBJECT_NAME = 'Backup Unit'
STATES = ['present', 'absent', 'update']
RETURNED_KEY = 'backupunit'

OPTIONS = {
    'name': {
        'description': ['The name of the  resource (alphanumeric characters only).'],
        'required': ['present'],
        'available': ['present'],
        'type': 'str',
    },
    'backupunit': {
        'description': ['The ID or name of the virtual Backup Unit.'],
        'required': ['update', 'absent'],
        'available': ['update', 'absent'],
        'type': 'str',
    },
    'backupunit_password': {
        'description': ['The password associated with that resource.'],
        'available': ['present'],
        'no_log': True,
        'type': 'str',
    },
    'backupunit_email': {
        'description': ['The email associated with the backup unit. Bear in mind that this email does not be the same email as of the user.'],
        'required': ['present'],
        'available': ['present'],
        'type': 'str',
    },
    **get_default_options_with_replace(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "name", "note": "" },
    { "name": "backupunit_email", "note": "" },
    {
        "name": "backupunit_password",
        "note": "Will trigger replace just by being set as this parameter cannot be retrieved from the api to check for changes!",
    },
]

DOCUMENTATION = """
module: backupunit
short_description: Create or remove Backup Units
description:
     - This is a simple module that supports creating or removing Backup Units.
       This module has a dependency on ionoscloud >= 6.0.2
version_added: "2.0"
options:
    ilowuerhfgwoqrghbqwoguh
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
  'present' : '''# Create a Backup Unit
  - name: Create Backup Unit
    backupunit:
      backupunit_email: <email>
      backupunit_password: <password>
      name: BackupUnitName
  ''',
  'update' : '''# Update a Backup Unit
  - name: Update a Backup Unit
    backupunit:
      backupunit: BackupUnitName
      backupunit_email: <newEmail>
      backupunit_password: <newPassword>
      state: update
  ''',
  'absent' : '''# Destroy a Backup Unit.
  - name: Remove Backup Unit
    backupunit:
      backupunit: BackupUnitName
      state: absent
  ''',
}

EXAMPLES = """
    ilowuerhfgwoqrghbqwoguh
"""


class BackupunitModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return (
        self.module.params.get('name') is not None
        and existing_object.properties.name != self.module.params.get('name')
        or self.module.params.get('backupunit_password') is not None
        or self.module.params.get('backupunit_email') is not None
        and existing_object.properties.email != self.module.params.get('backupunit_email')
    )


    def _should_update_object(self, existing_object, clients):
        return False


    def _get_object_list(self, clients):
        return ionoscloud.BackupUnitsApi(clients[0]).backupunits_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('backupunit')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        password = self.module.params.get('backupunit_password')
        email = self.module.params.get('backupunit_email')
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            password = existing_object.properties.password if password is None else password
            email = existing_object.properties.email if email is None else email

        wait = self.module.params.get('wait')
        wait_timeout = int(self.module.params.get('wait_timeout'))

        backupunits_api = ionoscloud.BackupUnitsApi(client)

        backupunit = BackupUnit(properties=BackupUnitProperties(name=name, password=password, email=email))

        try:
            datacenter_response, _, headers = backupunits_api.backupunits_post_with_http_info(backupunit)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to create the new backupunit: %s" % to_native(e))
        return datacenter_response


    def _update_object(self, existing_object, clients):
        pass


    def _remove_object(self, existing_object, clients):
        client = clients[0]
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')

        backupunits_api = ionoscloud.BackupUnitsApi(client)

        try:
            _, _, headers = backupunits_api.backupunits_delete_with_http_info(existing_object.id)
            if wait:
                request_id = _get_request_id(headers['Location'])
                client.wait_for_completion(request_id=request_id, timeout=wait_timeout)
        except ApiException as e:
            self.module.fail_json(msg="failed to remove the backupunit: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = BackupunitModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')
    ionos_module.main()
