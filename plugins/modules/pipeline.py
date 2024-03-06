from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud_logging
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python-logging/%s'% (
    __version__, ionoscloud_logging.__version__,
)
DOC_DIRECTORY = 'logging'
STATES = ['present', 'absent', 'update', 'renew']
OBJECT_NAME = 'Pipeline'
RETURNED_KEY = 'pipeline'

OPTIONS = {
    'name': {
        'description': ['The friendly name of your pipeline.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'logs': {
        'description': ['The information of the log pipelines'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'list',
        'elements': 'dict',
    },
    'pipeline': {
        'description': ['The ID or name of an existing Pipeline.'],
        'available': ['update', 'absent', 'renew'],
        'required': ['update', 'absent', 'renew'],
        'type': 'str',
    },
    **get_default_options(STATES),
}

DOCUMENTATION = """
module: pipeline
short_description: Allows operations with Ionos Cloud Logging Pipelines.
description:
     - This is a module that supports creating, updating or destroying Pipelines
version_added: "2.0"
options:
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    logs:
        description:
        - The information of the log pipelines
        elements: dict
        required: false
    name:
        description:
        - The friendly name of your pipeline.
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    pipeline:
        description:
        - The ID or name of an existing Pipeline.
        required: false
    state:
        choices:
        - present
        - absent
        - update
        - renew
        default: present
        description:
        - Indicate desired state of the resource.
        required: false
    token:
        description:
        - The Ionos token. Overrides the IONOS_TOKEN environment variable.
        env_fallback: IONOS_TOKEN
        no_log: true
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    wait:
        choices:
        - true
        - false
        default: true
        description:
        - Wait for the resource to be created before returning.
        required: false
    wait_timeout:
        default: 600
        description:
        - How long before wait gives up, in seconds.
        required: false
requirements:
    - "python >= 2.6"
    - "ionoscloud >= 6.0.2"
    - "ionoscloud-container-registry >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

EXAMPLE_PER_STATE = {
    'present': '''name: Create Pipeline
ionoscloudsdk.ionoscloud.pipeline:
  name: 'ansiblepipelinetest'
  logs: '[{'source': 'kubernetes', 'tag': 'tag', 'protocol': 'http', 'destinations': [{'type': 'loki', 'retention_in_days': 7}]}]'
  wait: true
  wait_timeout: 1200
register: pipeline_response
''',
    'update': '''name: Update pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  name: 'ansiblepipeNEW'
  logs: '[{'source': 'docker', 'tag': 'differenttag', 'protocol': 'tcp', 'labels': ['1'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}, {'source': 'kubernetes', 'tag': 'updatedtag', 'protocol': 'http', 'labels': ['2'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}]'
  state: update
register: updated_pipeline_response
''',
    'absent': '''name: Delete pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  wait: true
  state: absent
''',
    'renew': '''name: Renew Pipeline key
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  state: renew
''',
}

EXAMPLES = """name: Create Pipeline
ionoscloudsdk.ionoscloud.pipeline:
  name: 'ansiblepipelinetest'
  logs: '[{'source': 'kubernetes', 'tag': 'tag', 'protocol': 'http', 'destinations': [{'type': 'loki', 'retention_in_days': 7}]}]'
  wait: true
  wait_timeout: 1200
register: pipeline_response

name: Update pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  name: 'ansiblepipeNEW'
  logs: '[{'source': 'docker', 'tag': 'differenttag', 'protocol': 'tcp', 'labels': ['1'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}, {'source': 'kubernetes', 'tag': 'updatedtag', 'protocol': 'http', 'labels': ['2'], 'destinations': [{'type': 'loki', 'retention_in_days': 14}]}]'
  state: update
register: updated_pipeline_response

name: Delete pipeline
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  wait: true
  state: absent

name: Renew Pipeline key
ionoscloudsdk.ionoscloud.pipeline:
  pipeline: ''
  state: renew
"""


def get_log_object(log, object_type):
    return object_type(
        source=log.get('source'),
        protocol=log.get('protocol'),
        tag=log.get('tag'),
        labels=log.get('labels', []),
        destinations=[
            ionoscloud_logging.Destination(
                type=destination.get('type', 'loki'),
                retention_in_days=destination.get('retention_in_days', 30),
            ) for destination in log.get('destinations', [])
        ],
    )

def get_logs_object(logs, object_type):
    return [get_log_object(log, object_type) for log in logs]


class PipelineModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_logging]
        self.user_agents = [USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        return False


    def _should_update_object(self, existing_object, clients):
        return (
            self.module.params.get('logs') is not None
            or self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
        )


    def _get_object_list(self, clients):
        return ionoscloud_logging.PipelinesApi(clients[0]).pipelines_get()


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('pipeline')


    def _create_object(self, existing_object, clients):
        client = clients[0]
        name = self.module.params.get('name')
        logs = get_logs_object(self.module.params.get('logs'), ionoscloud_logging.PipelineCreatePropertiesLogs)
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            logs = existing_object.properties.logs if logs is None else logs

        pipelines_api = ionoscloud_logging.PipelinesApi(client)

        pipeline_properties = ionoscloud_logging.PipelineCreateProperties(
            name=name,
            logs=logs,
        )

        pipeline = ionoscloud_logging.PipelineCreate(properties=pipeline_properties)

        try:
            pipeline = pipelines_api.pipelines_post(pipeline)

            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: pipelines_api.pipelines_find_by_id(pipeline.id).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=int(self.module.params.get('wait_timeout')),
                )
        except ionoscloud_logging.ApiException as e:
            self.module.fail_json(msg="failed to create the new Pipeline: %s" % to_native(e))
        return pipeline


    def _update_object(self, existing_object, clients):
        client = clients[0]
        wait_timeout = int(self.module.params.get('wait_timeout'))
        name = self.module.params.get('name')
        logs = get_logs_object(self.module.params.get('logs'), ionoscloud_logging.PipelineCreatePropertiesLogs)
        if existing_object is not None:
            name = existing_object.properties.name if name is None else name
            logs = existing_object.properties.logs if logs is None else logs

        pipelines_api = ionoscloud_logging.PipelinesApi(client)

        pipeline_properties = ionoscloud_logging.PipelinePatchProperties(
            name=name,
            logs=logs,
        )

        pipeline = ionoscloud_logging.PipelinePatch(properties=pipeline_properties)


        try:
            client.wait_for(
                fn_request=lambda: pipelines_api.pipelines_find_by_id(existing_object.id).metadata.state,
                fn_check=lambda r: r == 'AVAILABLE',
                scaleup=10000,
                timeout=wait_timeout,
            )
            pipeline = pipelines_api.pipelines_patch(existing_object.id, pipeline)
            if self.module.params.get('wait'):
                client.wait_for(
                    fn_request=lambda: pipelines_api.pipelines_find_by_id(pipeline.id).metadata.state,
                    fn_check=lambda r: r == 'AVAILABLE',
                    scaleup=10000,
                    timeout=wait_timeout,
                )
            return pipeline
        except ionoscloud_logging.ApiException as e:
            self.module.fail_json(msg="failed to update the Pipeline: %s" % to_native(e))


    def _remove_object(self, existing_object, clients):
        pipelines_api = ionoscloud_logging.PipelinesApi(clients[0])

        try:
            pipelines_api.pipelines_delete(existing_object.id)
        except ionoscloud_logging.ApiException as e:
            self.module.fail_json(msg="failed to remove the Pipeline: %s" % to_native(e))


    def renew_object(self, clients):
        client = clients[0]
        existing_object = get_resource(self.module, self._get_object_list(clients), self._get_object_identifier())

        if existing_object is None:
            self.module.exit_json(changed=False)
            return

        pipelines_api = ionoscloud_logging.PipelinesApi(client)

        try:
            client.wait_for(
                fn_request=lambda: pipelines_api.pipelines_find_by_id(existing_object.id).metadata.state,
                fn_check=lambda r: r == 'AVAILABLE',
                scaleup=10000,
                timeout=int(self.module.params.get('wait_timeout')),
            )
            pipelines_api.pipelines_key_post(existing_object.id)
        except ionoscloud_logging.ApiException as e:
            self.module.fail_json(msg="failed to renew the Pipeline Key: %s" % to_native(e))

        return {
            'action': 'renew',
            'changed': True,
            'id': existing_object.id,
        }


if __name__ == '__main__':
    ionos_module = PipelineModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud_logging is required for this module, run `pip install ionoscloud_logging`')
    ionos_module.main()
