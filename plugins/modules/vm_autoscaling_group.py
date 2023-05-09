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
    import ionoscloud_vm_autoscaling
except ImportError:
    HAS_SDK = False

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

USER_AGENT = 'ansible-module/%s_sdk-python-vm-autoscaling/%s' % (
    __version__, ionoscloud_vm_autoscaling.__version__,
)
DOC_DIRECTORY = 'vm-autoscaling'
STATES = ['present', 'absent', 'update']
OBJECT_NAME = 'VM Autoscaling Group'
RETURNED_KEY = 'vm_autoscaling_group'


OPTIONS = {
    'max_replica_count': {
        'description': [
            "The maximum value for the number of replicas for 'targetReplicaCount'. Must be >= 0 "
            "and <= 200. Will be enforced for both automatic and manual changes.",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'min_replica_count': {
        'description': [
            "The minimum value for the number of replicas for 'targetReplicaCount'. Must be >= 0 "
            "and <= 200. Will be enforced for both automatic and manual changes",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'int',
    },
    'name': {
        'description': ['The name of the VM Auto Scaling Group. This field must not be null or blank.'],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'datacenter': {
        'description': [
            'The VMs for this VM Auto Scaling Description are created in this virtual data center.',
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'metric': {
        'description': [
            'The metric that triggers the scaling actions. Metric values are checked at fixed intervals.',
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'choices': [
          'INSTANCE_CPU_UTILIZATION_AVERAGE',
          'INSTANCE_NETWORK_IN_BYTES',
          'INSTANCE_NETWORK_IN_PACKETS',
          'INSTANCE_NETWORK_OUT_BYTES',
          'INSTANCE_NETWORK_OUT_PACKETS',
        ],
        'type': 'str',
    },
    'range': {
        'description': [
            'Specifies the time range for which the samples are to be aggregated. Must be >= 2 minutes.',
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'str',
    },
    'unit': {
        'description': [
            "The units of the applied metric. 'TOTAL' can only be combined with "
            "'INSTANCE_CPU_UTILIZATION_AVERAGE'.",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'choices': [
          'PER_HOUR',
          'PER_MINUTE',
          'PER_SECOND',
          'TOTAL'
        ],
        'type': 'str',
    },
    'scale_in_threshold': {
        'description': [
            "The lower threshold for the value of the 'metric'. Used with the `less than` (<) "
            "operator. When this value is exceeded, a scale-in action is triggered, specified by "
            "the 'scaleInAction' property. The value must have a higher minimum delta to the "
            "'scaleOutThreshold', depending on the 'metric', to avoid competing for actions at the "
            "same time.",
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'scale_out_threshold': {
        'description': [
            "The upper threshold for the value of the 'metric'. Used with the 'greater than' (>) "
            "operator. A scale-out action is triggered when this value is exceeded, specified by "
            "the 'scaleOutAction' property. The value must have a lower minimum delta to the "
            "'scaleInThreshold', depending on the metric, to avoid competing for actions simultaneously. "
            "If 'properties.policy.unit=TOTAL', a value >= 40 must be chosen.",
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'scale_in_action': {
        'description': [
            "Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is "
            "always about removing VMs associated with this VM Auto Scaling Group. By default, the "
            "termination policy is 'OLDEST_SERVER_FIRST' is effective.",
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'scale_out_action': {
        'description': [
            "Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, "
            "scaling is always about adding new VMs to this VM Auto Scaling Group.",
        ],
        'available': ['present', 'update'],
        'type': 'dict',
    },
    'nics': {
        'description': ['The list of NICs associated with this replica.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'volumes': {
        'description': ['List of volumes associated with this Replica.'],
        'available': ['present', 'update'],
        'type': 'list',
        'elements': 'dict',
    },
    'availability_zone': {
        'description': [
            "The zone where the VMs are created. The availability zone is always automatically set to 'AUTO' for performance reasons. Even if you set another value, e.g. 'null', or leave it empty."
        ],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'cores': {
        'description': ['The total number of cores for the VMs.'],
        'available': ['present', 'update'],
        'type': 'str',
    },
    'cpu_family': {
        'description': [
            "The CPU family for the VMs created with this configuration. If the value is 'null', "
            "the VM is created with the default CPU family for the assigned site."
        ],
        'available': ['present', 'update'],
        'choices': [
          'AMD_OPTERON',
          'INTEL_SKYLAKE',
          'INTEL_XEON',
        ],
        'type': 'str',
    },
    'ram': {
        'description': [
            "The size of the memory for the VMs in MB. The size must be in multiples of 256 MB, with a "
            "minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at least 1024 MB. If you set "
            "the RAM size to more than 240 GB, 'ramHotPlug=FALSE' is fixed."
        ],
        'available': ['present', 'update'],
        'type': 'int',
    },
    'vm_autoscaling_group': {
        'description': ['The ID or name of an existing VM Autoscaling Group.'],
        'available': ['update', 'absent'],
        'required': ['update', 'absent'],
        'type': 'str',
    },
    'do_not_replace': {
        'description': [
            'Boolean indincating if the resource should not be recreated when the state cannot be reached in '
            'another way. This may be used to prevent resources from being deleted from specifying a different'
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
    'certificate_fingerprint': {
        'description': ['The Ionos API certificate fingerprint.'],
        'env_fallback': 'IONOS_CERTIFICATE_FINGERPRINT',
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
module: vm_autoscaling_group
short_description: Allows operations with Ionos Cloud VM Autoscaling Groups.
description:
     - This is a module that supports creating, updating or destroying VM Autoscaling Groups
version_added: "2.0"
options:
''' + '  ' + yaml.dump(
    yaml.safe_load(str({k: transform_for_documentation(v) for k, v in copy.deepcopy(OPTIONS).items()})),
    default_flow_style=False).replace('\n', '\n  ') + '''
requirements:
    - "python >= 2.6"
    - "ionoscloud-vm-autoscaling >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create Postgres Cluster
    postgres_cluster:
      postgres_version: 12
      instances: 1
      cores: 1
      ram: 2048
      storage_size: 20480
      storage_type: HDD
      location: de/fra
      connections:
        - cidr: 192.168.1.106/24
          datacenter: "{{ datacenter_response.datacenter.id }}"
          lan: "{{ lan_response1.lan.id }}"
      display_name: backuptest-04
      synchronization_mode: ASYNCHRONOUS
      db_username: test
      db_password: 7357cluster
      wait: true
    register: cluster_response
  ''',
    'update': '''- name: Update Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      postgres_version: 12
      instances: 2
      cores: 2
      ram: 4096
      storage_size: 30480
      state: update
      wait: true
    register: updated_cluster_response
  ''',
    'absent': '''- name: Delete Postgres Cluster
    postgres_cluster:
      postgres_cluster: "{{ cluster_response.postgres_cluster.id }}"
      state: absent
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


def get_scale_in_action_object(action_dict):
    return ionoscloud_vm_autoscaling.GroupPolicyScaleInAction(
        amount=action_dict.get('amount'),
        amount_type=action_dict.get('amount_type'),
        cooldown_period=action_dict.get('cooldown_period'),
        termination_policy=action_dict.get('termination_policy'),
        delete_volumes=action_dict.get('delete_volumes'),
    )


def get_scale_out_action_object(action_dict):
    return ionoscloud_vm_autoscaling.GroupPolicyScaleOutAction(
        amount=action_dict.get('amount'),
        amount_type=action_dict.get('amount_type'),
        cooldown_period=action_dict.get('cooldown_period'),
    )


def get_flow_log_object(flow_log_dict):
    return ionoscloud_vm_autoscaling.NicFlowLog(
        name=flow_log_dict.get('name'),
        action=flow_log_dict.get('action'),
        direction=flow_log_dict.get('direction'),
        bucket=flow_log_dict.get('bucket'),
    )


def get_firewall_rule_object(flow_log_dict):
    return ionoscloud_vm_autoscaling.NicFirewallRule(
        name=flow_log_dict.get('name'),
        protocol=flow_log_dict.get('protocol'),
        source_mac=flow_log_dict.get('source_mac'),
        source_ip=flow_log_dict.get('source_ip'),
        target_ip=flow_log_dict.get('target_ip'),
        icmp_code=flow_log_dict.get('icmp_code'),
        icmp_type=flow_log_dict.get('icmp_type'),
        port_range_start=flow_log_dict.get('port_range_start'),
        port_range_end=flow_log_dict.get('port_range_end'),
        type=flow_log_dict.get('type'),
    )


def get_nic_object(nic_dict):
    return ionoscloud_vm_autoscaling.ReplicaNic(
        lan=nic_dict.get('lan'),
        name= nic_dict.get('name'),
        firewall_active=nic_dict.get('firewall_active'),
        firewall_type=nic_dict.get('firewall_type'),
        flow_logs=[get_flow_log_object(flow_log) for flow_log in nic_dict.get('flow_logs')],
        firewall_rules=[get_firewall_rule_object(firewall_rule) for firewall_rule in nic_dict.get('firewall_rules')],
    )


def get_volume_object(volume_dict):
    return ionoscloud_vm_autoscaling.ReplicaVolumePost(
        image=volume_dict.get('image'),
        image_alias=volume_dict.get('image_alias'),
        name=volume_dict.get('name'),
        size=volume_dict.get('size'),
        ssh_keys=volume_dict.get('ssh_keys'),
        type = volume_dict.get('type'),
        user_data = volume_dict.get('user_data'),
        bus = volume_dict.get('bus'),
        backupunit_id = volume_dict.get('backupunit_id'),
        boot_order = volume_dict.get('boot_order'),
        image_password = volume_dict.get('image_password'),
    )


def _should_replace_object(module, existing_object, cloudapi_client):

    datacenter_id = lan_id = cidr = None
    if module.params.get('connections'):
        connection = module.params.get('connections')[0]
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(module, datacenter_list, connection['datacenter'])

        if datacenter_id is None:
            module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
        
        lan_id = get_resource_id(
            module,
            ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1),
            connection['lan'],
        )
        if lan_id is None:
            module.fail_json('LAN {} not found.'.format(connection['lan']))
        cidr = connection['cidr']

    return (
        module.params.get('backup_location') is not None
        and existing_object.properties.backup_location != module.params.get('backup_location')
        or module.params.get('location') is not None
        and existing_object.properties.location != module.params.get('location')
        or module.params.get('synchronization_mode') is not None
        and existing_object.properties.synchronization_mode != module.params.get('synchronization_mode')
        or module.params.get('storage_type') is not None
        and existing_object.properties.storage_type != module.params.get('storage_type')
        or module.params.get('connections') is not None
        and (
            existing_object.properties.connections[0].datacenter_id != datacenter_id
            or existing_object.properties.connections[0].lan_id != lan_id
            or existing_object.properties.connections[0].cidr != cidr
        )
    )


def _should_update_object(module, existing_object, cloudapi_client):
    datacenter_id = None
    if module.params.get('datacenter'):
        datacenter_list = ionoscloud.DataCentersApi(api_client=cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    scale_in_action_should_update = scale_out_action_should_update = nics_update = volumes_update = False
    if module.properties.get('scale_in_action'):
        scale_in_action = get_scale_in_action_object(module.properties.get('scale_in_action'))
        existing_scale_in_action = existing_object.properties.group_policy.scale_in_action

        if (
            scale_in_action.amount is not None 
            and scale_in_action.amount != existing_scale_in_action.amount
            or scale_in_action.amount_type is not None 
            and scale_in_action.amount_type != existing_scale_in_action.amount_type
            or scale_in_action.cooldown_period is not None 
            and scale_in_action.cooldown_period != existing_scale_in_action.cooldown_period
            or scale_in_action.termination_policy is not None 
            and scale_in_action.termination_policy != existing_scale_in_action.termination_policy
            or scale_in_action.delete_volumes is not None 
            and scale_in_action.delete_volumes != existing_scale_in_action.delete_volumes
        ):
            scale_in_action_should_update = True

    if module.properties.get('scale_out_action'):
        scale_out_action = get_scale_out_action_object(module.properties.get('scale_out_action'))
        existing_scale_out_action = existing_object.properties.group_policy.scale_out_action

        if (
            scale_out_action.amount is not None 
            and scale_out_action.amount != existing_scale_out_action.amount
            or scale_out_action.amount_type is not None 
            and scale_out_action.amount_type != existing_scale_out_action.amount_type
            or scale_out_action.cooldown_period is not None 
            and scale_out_action.cooldown_period != existing_scale_out_action.cooldown_period
        ):
            scale_out_action_should_update = True


    if module.properties.get('nics'):
        def nic_sort_func(el):
            return el.name, el.lan

        new_nics = sorted([get_nic_object(nic) for nic in module.properties.get('nics')], key=nic_sort_func)
        existing_nics = sorted(existing_object.properties.replica_configuration.nics, key=nic_sort_func)

        if len(new_nics) != len(existing_nics):
            nics_update = True

    return (
        scale_in_action_should_update or scale_out_action_should_update or nics_update or volumes_update
        or module.params.get('max_replica_count') is not None
        and existing_object.properties.max_replica_count != module.params.get('max_replica_count')
        or module.params.get('min_replica_count') is not None
        and existing_object.properties.min_replica_count != module.params.get('min_replica_count')
        or module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('metric') is not None
        and existing_object.properties.metric != module.params.get('metric')
        or module.params.get('range') is not None
        and existing_object.properties.range != module.params.get('range')
        or module.params.get('unit') is not None
        and existing_object.properties.unit != module.params.get('unit')
        or module.params.get('scale_in_threshold') is not None
        and existing_object.properties.scale_in_threshold != module.params.get('scale_in_threshold')
        or module.params.get('scale_out_threshold') is not None
        and existing_object.properties.scale_out_threshold != module.params.get('scale_out_threshold')
        or module.params.get('availability_zone') is not None
        and existing_object.properties.availability_zone != module.params.get('availability_zone')
        or module.params.get('cores') is not None
        and existing_object.properties.cores != module.params.get('cores')
        or module.params.get('cpu_family') is not None
        and existing_object.properties.cpu_family != module.params.get('cpu_family')
        or module.params.get('ram') is not None
        and existing_object.properties.ram != module.params.get('ram')
        or module.params.get('datacenter') is not None
        and existing_object.properties.datacenter.id != datacenter_id
    )


def _get_object_list(module, client):
    return ionoscloud_vm_autoscaling.GroupsApi(client).groups_get()


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('vm_autoscaling_group')


def _create_object(module, dbaas_client, cloudapi_client, existing_object=None):
    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')
    backup_location=module.params.get('backup_location')
    if existing_object is not None:
        backup_location = existing_object.properties.backup_location if backup_location is None else backup_location
        maintenance_window = existing_object.properties.maintenance_window if maintenance_window is None else maintenance_window

    connection = module.params.get('connections')[0]

    datacenter_id = get_resource_id(module, ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=2), connection['datacenter'])

    if datacenter_id is None:
        module.fail_json('Datacenter {} not found.'.format(connection['datacenter']))
    
    lan_id = get_resource_id(module, ionoscloud.LANsApi(cloudapi_client).datacenters_lans_get(datacenter_id, depth=1), connection['lan'])

    if lan_id is None:
        module.fail_json('LAN {} not found.'.format(connection['lan']))

    connections = [
        ionoscloud_dbaas_postgres.Connection(datacenter_id=datacenter_id, lan_id=lan_id, cidr=connection['cidr']),
    ]

    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_cluster_properties = ionoscloud_dbaas_postgres.CreateClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        storage_type=module.params.get('storage_type'),
        connections=connections,
        location=module.params.get('location'),
        backup_location=backup_location,
        display_name=module.params.get('display_name'),
        maintenance_window=maintenance_window,
        credentials=ionoscloud_dbaas_postgres.DBUser(
            username=module.params.get('db_username'),
            password=module.params.get('db_password'),
        ),
        synchronization_mode=module.params.get('synchronization_mode'),
        from_backup=ionoscloud_dbaas_postgres.CreateRestoreRequest(
            backup_id=module.params.get('backup_id'),
            recovery_target_time=module.params.get('recovery_target_time'),
        ),
    )

    postgres_cluster = ionoscloud_dbaas_postgres.CreateClusterRequest(properties=postgres_cluster_properties)

    try:
        postgres_cluster = clusters_api.clusters_post(postgres_cluster)
        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )
    except Exception as e:
        module.fail_json(msg="failed to create the new Postgres Cluster: %s" % to_native(e))
    return postgres_cluster


def _update_object(module, dbaas_client, existing_object):
    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)
    dbaas_client.wait_for(
        fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
        fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
        scaleup=10000,
    )

    maintenance_window = module.params.get('maintenance_window')
    if maintenance_window:
        maintenance_window = dict(module.params.get('maintenance_window'))
        maintenance_window['dayOfTheWeek'] = maintenance_window.pop('day_of_the_week')

    display_name=module.params.get('display_name')

    postgres_cluster_properties = ionoscloud_dbaas_postgres.PatchClusterProperties(
        postgres_version=module.params.get('postgres_version'),
        instances=module.params.get('instances'),
        cores=module.params.get('cores'),
        ram=module.params.get('ram'),
        storage_size=module.params.get('storage_size'),
        display_name=display_name,
        maintenance_window=maintenance_window,
    )
    postgres_cluster = ionoscloud_dbaas_postgres.PatchClusterRequest(properties=postgres_cluster_properties)

    try:
        postgres_cluster = clusters_api.clusters_patch(
            cluster_id=existing_object.id,
            patch_cluster_request=postgres_cluster,
        )

        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: clusters_api.clusters_find_by_id(postgres_cluster.id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

    except Exception as e:
        module.fail_json(msg="failed to update the Postgres Cluster: %s" % to_native(e))
    return postgres_cluster


def _remove_object(module, dbaas_client, existing_object):
    clusters_api = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    try:
        if existing_object.metadata.state != 'DESTROYING':
            clusters_api.clusters_delete(existing_object.id)

        if module.params.get('wait'):
            try:
                dbaas_client.wait_for(
                    fn_request=lambda: clusters_api.clusters_find_by_id(existing_object.id),
                    fn_check=lambda _: False,
                    scaleup=10000,
                )
            except ionoscloud_dbaas_postgres.ApiException as e:
                if e.status != 404:
                    raise e
    except Exception as e:
        module.fail_json(msg="failed to delete the Postgres cluster: %s" % to_native(e))


def update_replace_object(module, dbaas_client, cloudapi_client, existing_object):
    if _should_replace_object(module, existing_object, cloudapi_client):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, dbaas_client, cloudapi_client, existing_object).to_dict()
        _remove_object(module, dbaas_client, existing_object)
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
            RETURNED_KEY: _update_object(module, dbaas_client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, dbaas_client, cloudapi_client):
    existing_object = get_resource(
        module, _get_object_list(module, dbaas_client), _get_object_name(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object:
        return update_replace_object(module, dbaas_client, cloudapi_client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, dbaas_client, cloudapi_client).to_dict()
    }


def update_object(module, dbaas_postgres_api_client, cloudapi_api_client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, dbaas_postgres_api_client)

    existing_object = get_resource(
        module, object_list, _get_object_identifier(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object is None:
        module.exit_json(changed=False)

    existing_object_id_by_new_name = get_resource_id(
        module, object_list, object_name,
        [['id'], ['properties', 'display_name']],
    )

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

    return update_replace_object(module, dbaas_postgres_api_client, cloudapi_api_client, existing_object)


def remove_object(module, client):

    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_identifier(module),
        [['id'], ['properties', 'display_name']],
    )

    if existing_object is None:
        module.exit_json(changed=False)

    _remove_object(module, client, existing_object)

    return {
        'action': 'delete',
        'changed': True,
        'id': existing_object.id,
    }


def restore_object(module, dbaas_client):
    postgres_cluster_server = ionoscloud_dbaas_postgres.ClustersApi(dbaas_client)

    postgres_cluster_id = get_resource_id(
        module,
        postgres_cluster_server.clusters_get(),
        module.params.get('postgres_cluster'),
        [['id'], ['properties', 'display_name']],
    )

    restore_request = ionoscloud_dbaas_postgres.CreateRestoreRequest(
        backup_id=module.params.get('backup_id'),
        recovery_target_time=module.params.get('recovery_target_time'),
    )

    try:
        ionoscloud_dbaas_postgres.RestoresApi(dbaas_client).cluster_restore_post(postgres_cluster_id, restore_request)

        if module.params.get('wait'):
            dbaas_client.wait_for(
                fn_request=lambda: postgres_cluster_server.clusters_find_by_id(postgres_cluster_id),
                fn_check=lambda cluster: cluster.metadata.state == 'AVAILABLE',
                scaleup=10000,
            )

        return {
            'action': 'restore',
            'changed': True,
            'id': postgres_cluster_id,
        }
    except Exception as e:
        module.fail_json(msg="failed to restore the Postgres cluster: %s" % to_native(e))
        return {
            'action': 'restore',
            'changed': False,
            'id': postgres_cluster_id,
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
    certificate_fingerprint = module.params.get('certificate_fingerprint')

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
        module.fail_json(msg='both ionoscloud and ionoscloud_dbaas_postgres are required for this module, '
                             'run `pip install ionoscloud ionoscloud_dbaas_postgres`')

    cloudapi_api_client = ionoscloud.ApiClient(get_sdk_config(module, ionoscloud))
    cloudapi_api_client.user_agent = USER_AGENT
    dbaas_postgres_api_client = ionoscloud_dbaas_postgres.ApiClient(get_sdk_config(module, ionoscloud_dbaas_postgres))
    dbaas_postgres_api_client.user_agent = DBAAS_POSTGRES_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, dbaas_postgres_api_client, cloudapi_api_client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, dbaas_postgres_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, dbaas_postgres_api_client, cloudapi_api_client))
        elif state == 'restore':
            module.exit_json(**restore_object(module, dbaas_postgres_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(object_name=OBJECT_NAME, error=to_native(e),
                                                                            state=state))


if __name__ == '__main__':
    main()
