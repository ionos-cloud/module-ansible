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

USER_AGENT = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, ionoscloud.__version__)
VM_AUTOSCALING_USER_AGENT = 'ansible-module/%s_sdk-python-vm-autoscaling/%s' % (
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
        'type': 'str',
    },
    'unit': {
        'description': [
            "The units of the applied metric. 'TOTAL' can only be combined with "
            "'INSTANCE_CPU_UTILIZATION_AVERAGE'.",
        ],
        'available': ['present', 'update'],
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
        'required': ['present'],
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
        'required': ['present'],
        'type': 'int',
    },
    'scale_in_action': {
        'description': [
            "Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here, scaling is "
            "always about removing VMs associated with this VM Auto Scaling Group. By default, the "
            "termination policy is 'OLDEST_SERVER_FIRST' is effective.",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
        'type': 'dict',
    },
    'scale_out_action': {
        'description': [
            "Defines the action to be performed when the 'scaleOutThreshold' is exceeded. Here, "
            "scaling is always about adding new VMs to this VM Auto Scaling Group.",
        ],
        'available': ['present', 'update'],
        'required': ['present'],
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
        'required': ['present'],
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
        'required': ['present'],
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
            'Boolean indicating if the resource should not be recreated when the state cannot be reached in '
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
    jiopwerrgopihwgowejg
requirements:
    - "python >= 2.6"
    - "ionoscloud-vm-autoscaling >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
'''

EXAMPLE_PER_STATE = {
    'present': '''- name: Create VM Autoscaling Group
      vm_autoscaling_group:
        datacenter: DatacenterName
        name: TestName
        max_replica_count: 2
        min_replica_count: 1
        metric: "INSTANCE_CPU_UTILIZATION_AVERAGE"
        range: "PT24H"
        unit: "PER_HOUR"
        scale_in_threshold: 33
        scale_out_threshold: 77
        scale_in_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
            termination_policy: 'RANDOM'
            delete_volumes: true
        scale_out_action:
            amount: 1
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT5M'
        availability_zone: "AUTO"
        cores: 2
        cpu_family: INTEL_XEON
        ram: 1024
        nics: 
            - lan: 1
              name: 'SDK_TEST_NIC1'
              dhcp: true
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 50
              type: 'HDD'
              bus: 'IDE'
              boot_order: 'AUTO'
      register: vm_autoscaling_group_response
  ''',
    'update': '''- name: Update VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ vm_autoscaling_group_response.vm_autoscaling_group.id }}"
        datacenter: DatacenterName2
        name: TestName2
        max_replica_count: 1
        min_replica_count: 0
        metric: "INSTANCE_NETWORK_IN_BYTES"
        range: "PT12H"
        unit: "PER_MINUTE"
        scale_in_threshold: 33
        scale_out_threshold: 86
        scale_in_action:
            amount: 50
            amount_type: 'PERCENTAGE'
            cooldown_period: 'PT10M'
            termination_policy: 'RANDOM'
            delete_volumes: false
        scale_out_action:
            amount: 2
            amount_type: 'ABSOLUTE'
            cooldown_period: 'PT15M'
        availability_zone: "AUTO"
        cores: 1
        cpu_family: "INTEL_SKYLAKE"
        ram: 2048
        nics: 
            - lan: 2
              name: 'SDK_TEST_NIC2'
              dhcp: false
        volumes:
            - image: <image_id>
              image_password: <password>
              name: 'SDK_TEST_VOLUME'
              size: 100
              type: 'SSD'
              bus: 'IDE'
              boot_order: 'AUTO'
        state: update
      register: vm_autoscaling_group_response
  ''',
    'absent': '''- name: Remove VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ name }}"
        state: absent
      register: vm_autoscaling_group_response
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
    if type(action_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.GroupPolicyScaleInAction(
        amount=action_dict.get('amount'),
        amount_type=action_dict.get('amount_type'),
        cooldown_period=action_dict.get('cooldown_period'),
        termination_policy=action_dict.get('termination_policy'),
        delete_volumes=action_dict.get('delete_volumes'),
    )


def get_scale_out_action_object(action_dict):
    if type(action_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.GroupPolicyScaleOutAction(
        amount=action_dict.get('amount'),
        amount_type=action_dict.get('amount_type'),
        cooldown_period=action_dict.get('cooldown_period'),
    )


def get_flow_log_object(flow_log_dict):
    if type(flow_log_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.NicFlowLog(
        name=flow_log_dict.get('name'),
        action=flow_log_dict.get('action'),
        direction=flow_log_dict.get('direction'),
        bucket=flow_log_dict.get('bucket'),
    )


def get_firewall_rule_object(firewall_rule_dict):
    if type(firewall_rule_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.NicFirewallRule(
        name=firewall_rule_dict.get('name'),
        protocol=firewall_rule_dict.get('protocol'),
        source_mac=firewall_rule_dict.get('source_mac'),
        source_ip=firewall_rule_dict.get('source_ip'),
        target_ip=firewall_rule_dict.get('target_ip'),
        icmp_code=firewall_rule_dict.get('icmp_code'),
        icmp_type=firewall_rule_dict.get('icmp_type'),
        port_range_start=firewall_rule_dict.get('port_range_start'),
        port_range_end=firewall_rule_dict.get('port_range_end'),
        type=firewall_rule_dict.get('type'),
    )


def get_nic_object(nic_dict):
    if type(nic_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.ReplicaNic(
        lan=nic_dict.get('lan'),
        dhcp=nic_dict.get('dhcp'),
        name= nic_dict.get('name'),
        firewall_active=nic_dict.get('firewall_active'),
        firewall_type=nic_dict.get('firewall_type'),
        flow_logs=[get_flow_log_object(flow_log) for flow_log in nic_dict.get('flow_logs', [])],
        firewall_rules=[get_firewall_rule_object(firewall_rule) for firewall_rule in nic_dict.get('firewall_rules', [])],
    )


def get_volume_object(volume_dict):
    if type(volume_dict) != dict:
        return None
    return ionoscloud_vm_autoscaling.ReplicaVolumePost(
        image=volume_dict.get('image'),
        image_alias=volume_dict.get('image_alias'),
        name=volume_dict.get('name'),
        size=volume_dict.get('size'),
        ssh_keys=volume_dict.get('ssh_keys', []),
        type = volume_dict.get('type'),
        user_data = volume_dict.get('user_data'),
        bus = volume_dict.get('bus'),
        backupunit_id = volume_dict.get('backupunit_id'),
        boot_order = volume_dict.get('boot_order'),
        image_password = volume_dict.get('image_password'),
    )


def _should_replace_object(module, existing_object, vm_autoscaling_client, cloudapi_client):
    if module.params.get('datacenter'):
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))
        if datacenter_id is None:
            module.fail_json('Datacenter {} not found.'.format(module.params.get('datacenter')))
        

    return (
        module.params.get('datacenter') is not None
        and existing_object.properties.datacenter.id != datacenter_id
    )


def _should_update_object(module, existing_object, vm_autoscaling_client, cloudapi_client):
    datacenter_id = None
    if module.params.get('datacenter'):
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))

    scale_in_action_should_update = scale_out_action_should_update = nics_update = volumes_update = False
    if module.params.get('scale_in_action'):
        scale_in_action = get_scale_in_action_object(module.params.get('scale_in_action'))
        existing_scale_in_action = existing_object.properties.policy.scale_in_action

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

    if module.params.get('scale_out_action'):
        scale_out_action = get_scale_out_action_object(module.params.get('scale_out_action'))
        existing_scale_out_action = existing_object.properties.policy.scale_out_action

        if (
            scale_out_action.amount is not None 
            and scale_out_action.amount != existing_scale_out_action.amount
            or scale_out_action.amount_type is not None 
            and scale_out_action.amount_type != existing_scale_out_action.amount_type
            or scale_out_action.cooldown_period is not None 
            and scale_out_action.cooldown_period != existing_scale_out_action.cooldown_period
        ):
            scale_out_action_should_update = True

    if module.params.get('nics'):
        def nic_sort_func(el):
            return el.name, el.lan

        def firewall_rule_sort_func(el):
            return el.name, el.protocol

        def flow_log_sort_func(el):
            return el.name, el.bucket

        new_nics = sorted([get_nic_object(nic) for nic in module.params.get('nics')], key=nic_sort_func)
        for nic in new_nics:
            nic.firewall_rules = sorted(nic.firewall_rules, key=firewall_rule_sort_func)
            nic.flow_logs = sorted(nic.flow_logs, key=flow_log_sort_func)
        new_nics = vm_autoscaling_client.sanitize_for_serialization(new_nics)
        existing_nics = sorted(existing_object.properties.replica_configuration.nics, key=nic_sort_func)
        for nic in existing_nics:
            nic.firewall_rules = sorted(nic.firewall_rules, key=firewall_rule_sort_func)
            nic.flow_logs = sorted(nic.flow_logs, key=flow_log_sort_func)
        existing_nics = vm_autoscaling_client.sanitize_for_serialization(existing_nics)
        
        if new_nics != existing_nics:
            nics_update = True

    if module.params.get('volumes'):
        def volume_sort_func(el):
            return el.name, el.type

        new_volumes = sorted([get_volume_object(volume) for volume in module.params.get('volumes')], key=volume_sort_func)
        new_volumes = vm_autoscaling_client.sanitize_for_serialization(new_volumes)

        for volume in new_volumes:
            if volume.get('image_password'):
                volumes_update = True

        if not volumes_update:
            existing_volumes = sorted(existing_object.properties.replica_configuration.volumes, key=volume_sort_func)
            existing_volumes = vm_autoscaling_client.sanitize_for_serialization(existing_volumes)

            if new_volumes != existing_volumes:
                volumes_update = True

    return (
        scale_in_action_should_update or scale_out_action_should_update or nics_update or volumes_update
        or module.params.get('max_replica_count') is not None
        and existing_object.properties.max_replica_count != module.params.get('max_replica_count')
        or module.params.get('min_replica_count') is not None
        and existing_object.properties.min_replica_count != module.params.get('min_replica_count')
        or module.params.get('name') is not None
        and existing_object.properties.name != module.params.get('name')
        or module.params.get('metric') is not None
        and existing_object.properties.policy.metric != module.params.get('metric')
        or module.params.get('range') is not None
        and existing_object.properties.policy.range != module.params.get('range')
        or module.params.get('unit') is not None
        and existing_object.properties.policy.unit != module.params.get('unit')
        or module.params.get('scale_in_threshold') is not None
        and existing_object.properties.policy.scale_in_threshold != module.params.get('scale_in_threshold')
        or module.params.get('scale_out_threshold') is not None
        and existing_object.properties.policy.scale_out_threshold != module.params.get('scale_out_threshold')
        or module.params.get('availability_zone') is not None
        and existing_object.properties.replica_configuration.availability_zone != module.params.get('availability_zone')
        or module.params.get('cores') is not None
        and existing_object.properties.replica_configuration.cores != int(module.params.get('cores'))
        or module.params.get('cpu_family') is not None
        and existing_object.properties.replica_configuration.cpu_family != module.params.get('cpu_family')
        or module.params.get('ram') is not None
        and existing_object.properties.replica_configuration.ram != module.params.get('ram')
    )


def _get_object_list(module, client):
    return ionoscloud_vm_autoscaling.AutoScalingGroupsApi(client).groups_get(depth=1)


def _get_object_name(module):
    return module.params.get('name')


def _get_object_identifier(module):
    return module.params.get('vm_autoscaling_group')


def _create_object(module, vm_autoscaling_client, cloudapi_client, existing_object=None):
    datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))
    max_replica_count = module.params.get('max_replica_count')
    min_replica_count = module.params.get('min_replica_count')
    name = module.params.get('name')
    metric = module.params.get('metric')
    policy_range = module.params.get('range')
    unit = module.params.get('unit')
    scale_in_threshold = module.params.get('scale_in_threshold')
    scale_out_threshold = module.params.get('scale_out_threshold')
    availability_zone = module.params.get('availability_zone')
    cores = module.params.get('cores')
    cpu_family = module.params.get('cpu_family')
    ram = module.params.get('ram')
    scale_in_action = get_scale_in_action_object(module.params.get('scale_in_action'))
    scale_out_action = get_scale_out_action_object(module.params.get('scale_out_action'))
    nics = [get_nic_object(nic) for nic in module.params.get('nics')] if module.params.get('nics') else None
    volumes = [get_volume_object(volume) for volume in module.params.get('volumes')] if module.params.get('volumes') else None

    if existing_object is not None:
        datacenter_id = existing_object.properties.datacenter.id if datacenter_id is None else datacenter_id
        max_replica_count = existing_object.properties.max_replica_count if max_replica_count is None else max_replica_count
        min_replica_count = existing_object.properties.min_replica_count if min_replica_count is None else min_replica_count
        name = existing_object.properties.name if name is None else name
        metric = existing_object.properties.policy.metric if metric is None else metric
        policy_range = existing_object.properties.policy.range if policy_range is None else policy_range
        unit = existing_object.properties.policy.unit if unit is None else unit
        scale_in_threshold = existing_object.properties.policy.scale_in_threshold if scale_in_threshold is None else scale_in_threshold
        scale_out_threshold = existing_object.properties.policy.scale_out_threshold if scale_out_threshold is None else scale_out_threshold
        scale_in_action = existing_object.properties.policy.scale_in_action if scale_in_action is None else scale_in_action
        scale_out_action = existing_object.properties.policy.scale_out_action if scale_out_action is None else scale_out_action
        cores = existing_object.properties.replica_configuration.cores if cores is None else cores
        ram = existing_object.properties.replica_configuration.ram if ram is None else ram
        cpu_family = existing_object.properties.replica_configuration.cpu_family if cpu_family is None else cpu_family
        availability_zone = existing_object.properties.replica_configuration.availability_zone if availability_zone is None else availability_zone
        nics = existing_object.properties.replica_configuration.nics if nics is None else nics
        volumes = existing_object.properties.replica_configuration.volumes if volumes is None else volumes

    vm_autoscaling_group = ionoscloud_vm_autoscaling.Group(
        properties=ionoscloud_vm_autoscaling.GroupProperties(
            datacenter=ionoscloud_vm_autoscaling.GroupPropertiesDatacenter(id=datacenter_id),
            max_replica_count=max_replica_count,
            min_replica_count=min_replica_count,
            name=name,
            policy=ionoscloud_vm_autoscaling.GroupPolicy(
                metric=metric,
                range=policy_range,
                unit=unit,
                scale_in_threshold=scale_in_threshold,
                scale_out_threshold=scale_out_threshold,
                scale_in_action=scale_in_action,
                scale_out_action=scale_out_action,
            ),
            replica_configuration=ionoscloud_vm_autoscaling.ReplicaPropertiesPost(
                cores=cores,
                ram=ram,
                cpu_family=cpu_family,
                availability_zone=availability_zone,
                nics=nics,
                volumes=volumes,
            ),
        )
    )

    groups_api = ionoscloud_vm_autoscaling.AutoScalingGroupsApi(vm_autoscaling_client)
    try:
        response = groups_api.groups_post(vm_autoscaling_group)
        if module.params.get('wait'):
            vm_autoscaling_client.wait_for(
                fn_request=lambda: groups_api.groups_find_by_id(response.id),
                fn_check=lambda group: group.metadata.state == 'AVAILABLE',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )
    except Exception as e:
        module.fail_json(msg="failed to create the new VM Autoscaling Group: %s" % to_native(e))
    return response


def _update_object(module, vm_autoscaling_client, cloudapi_client, existing_object):
    datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
    datacenter_id = get_resource_id(module, datacenter_list, module.params.get('datacenter'))
    max_replica_count = module.params.get('max_replica_count')
    min_replica_count = module.params.get('min_replica_count')
    name = module.params.get('name')
    metric = module.params.get('metric')
    policy_range = module.params.get('range')
    unit = module.params.get('unit')
    scale_in_threshold = module.params.get('scale_in_threshold')
    scale_out_threshold = module.params.get('scale_out_threshold')
    availability_zone = module.params.get('availability_zone')
    cores = module.params.get('cores')
    cpu_family = module.params.get('cpu_family')
    ram = module.params.get('ram')
    scale_in_action = get_scale_in_action_object(module.params.get('scale_in_action'))
    scale_out_action = get_scale_out_action_object(module.params.get('scale_out_action'))
    nics = [get_nic_object(nic) for nic in module.params.get('nics')] if module.params.get('nics') else None
    volumes = [get_volume_object(volume) for volume in module.params.get('volumes')] if module.params.get('volumes') else None

    vm_autoscaling_group = ionoscloud_vm_autoscaling.Group(
        properties=ionoscloud_vm_autoscaling.GroupProperties(
            datacenter=ionoscloud_vm_autoscaling.GroupPropertiesDatacenter(
                id=datacenter_id if datacenter_id else existing_object.properties.datacenter.id,
            ),
            max_replica_count=max_replica_count if max_replica_count else existing_object.properties.max_replica_count,
            min_replica_count=min_replica_count if min_replica_count else existing_object.properties.min_replica_count,
            name=name if name else existing_object.properties.name,
            policy=ionoscloud_vm_autoscaling.GroupPolicy(
                metric=metric if metric else existing_object.properties.policy.metric,
                range=policy_range if policy_range else existing_object.properties.policy.range,
                unit=unit if unit else existing_object.properties.policy.unit,
                scale_in_threshold=scale_in_threshold if scale_in_threshold else existing_object.properties.policy.scale_in_threshold,
                scale_out_threshold=scale_out_threshold if scale_out_threshold else existing_object.properties.policy.scale_out_threshold,
                scale_in_action=scale_in_action if scale_in_action else existing_object.properties.policy.scale_in_action,
                scale_out_action=scale_out_action if scale_out_action else existing_object.properties.policy.scale_out_action,
            ),
            replica_configuration=ionoscloud_vm_autoscaling.ReplicaPropertiesPost(
                cores=cores if cores else existing_object.properties.replica_configuration.cores,
                ram=ram if ram else existing_object.properties.replica_configuration.ram,
                cpu_family=cpu_family if cpu_family else existing_object.properties.replica_configuration.cpu_family,
                availability_zone=availability_zone if availability_zone else existing_object.properties.replica_configuration.availability_zone,
                nics=nics if nics else existing_object.properties.replica_configuration.nics,
                volumes=volumes if volumes else existing_object.properties.replica_configuration.volumes,
            ),
        )
    )

    groups_api = ionoscloud_vm_autoscaling.AutoScalingGroupsApi(vm_autoscaling_client)

    try:
        response = groups_api.groups_put(existing_object.id, vm_autoscaling_group)

        if module.params.get('wait'):
            vm_autoscaling_client.wait_for(
                fn_request=lambda: groups_api.groups_find_by_id(response.id),
                fn_check=lambda group: group.metadata.state == 'AVAILABLE',
                scaleup=10000,
                timeout=module.params.get('wait_timeout'),
            )

    except Exception as e:
        module.fail_json(msg="failed to update the VM Autoscaling Group: %s" % to_native(e))
    return response


def _remove_object(module, vm_autoscaling_client, existing_object):
    groups_api = ionoscloud_vm_autoscaling.AutoScalingGroupsApi(vm_autoscaling_client)

    try:
        groups_api.groups_delete(existing_object.id)

        if module.params.get('wait'):
            try:
                vm_autoscaling_client.wait_for(
                    fn_request=lambda: groups_api.groups_find_by_id(existing_object.id),
                    fn_check=lambda _: False,
                    scaleup=10000,
                )
            except ionoscloud_vm_autoscaling.ApiException as e:
                if e.status != 404:
                    raise e
    except Exception as e:
        module.fail_json(msg="failed to delete the VM Autoscaling Group: %s" % to_native(e))


def update_replace_object(module, vm_autoscaling_client, cloudapi_client, existing_object):
    if _should_replace_object(module, existing_object, vm_autoscaling_client, cloudapi_client):

        if module.params.get('do_not_replace'):
            module.fail_json(msg="{} should be replaced but do_not_replace is set to True.".format(OBJECT_NAME))

        new_object = _create_object(module, vm_autoscaling_client, cloudapi_client, existing_object).to_dict()
        _remove_object(module, vm_autoscaling_client, existing_object)
        return {
            'changed': True,
            'failed': False,
            'action': 'create',
            RETURNED_KEY: new_object,
        }
    if _should_update_object(module, existing_object, vm_autoscaling_client, cloudapi_client):
        # Update
        return {
            'changed': True,
            'failed': False,
            'action': 'update',
            RETURNED_KEY: _update_object(module, vm_autoscaling_client, cloudapi_client, existing_object).to_dict()
        }

    # No action
    return {
        'changed': False,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: existing_object.to_dict()
    }


def create_object(module, vm_autoscaling_client, cloudapi_client):
    existing_object = get_resource(
        module, _get_object_list(module, vm_autoscaling_client), _get_object_name(module),
    )

    if existing_object:
        return update_replace_object(module, vm_autoscaling_client, cloudapi_client, existing_object)

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        RETURNED_KEY: _create_object(module, vm_autoscaling_client, cloudapi_client).to_dict()
    }


def update_object(module, dbaas_postgres_api_client, cloudapi_api_client):
    object_name = _get_object_name(module)
    object_list = _get_object_list(module, dbaas_postgres_api_client)
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

    return update_replace_object(module, dbaas_postgres_api_client, cloudapi_api_client, existing_object)


def remove_object(module, client):

    existing_object = get_resource(
        module, _get_object_list(module, client), _get_object_identifier(module),
    )

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
        module.fail_json(msg='both ionoscloud and ionoscloud_vm_autoscaling are required for this module, '
                             'run `pip install ionoscloud ionoscloud_vm_autoscaling`')

    cloudapi_api_client = ionoscloud.ApiClient(get_sdk_config(module, ionoscloud))
    cloudapi_api_client.user_agent = USER_AGENT
    vm_autoscaling_api_client = ionoscloud_vm_autoscaling.ApiClient(get_sdk_config(module, ionoscloud_vm_autoscaling))
    vm_autoscaling_api_client.user_agent = VM_AUTOSCALING_USER_AGENT

    state = module.params.get('state')

    check_required_arguments(module, state, OBJECT_NAME)

    try:
        if state == 'present':
            module.exit_json(**create_object(module, vm_autoscaling_api_client, cloudapi_api_client))
        elif state == 'absent':
            module.exit_json(**remove_object(module, vm_autoscaling_api_client))
        elif state == 'update':
            module.exit_json(**update_object(module, vm_autoscaling_api_client, cloudapi_api_client))
    except Exception as e:
        module.fail_json(
            msg='failed to set {object_name} state {state}: {error}'.format(
                object_name=OBJECT_NAME, error=to_native(e), state=state,
            ))


if __name__ == '__main__':
    main()
