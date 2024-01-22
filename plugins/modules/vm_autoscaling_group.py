from ansible import __version__
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

HAS_SDK = True
try:
    import ionoscloud
    import ionoscloud_vm_autoscaling
except ImportError:
    HAS_SDK = False

from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_module import CommonIonosModule
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_methods import (
    get_module_arguments, get_resource_id,
)
from ansible_collections.ionoscloudsdk.ionoscloud.plugins.module_utils.common_ionos_options import get_default_options


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
        'default': True,
        'type': 'bool',
    },
    **get_default_options(STATES),
}

IMMUTABLE_OPTIONS = [
    { "name": "datacenter", "note": "" },
]

DOCUMENTATION = """
module: vm_autoscaling_group
short_description: Allows operations with Ionos Cloud VM Autoscaling Groups.
description:
     - This is a module that supports creating, updating or destroying VM Autoscaling Groups
version_added: "2.0"
options:
    allow_replace:
        default: false
        description:
        - Boolean indicating if the resource should be recreated when the state cannot
            be reached in another way. This may be used to prevent resources from being
            deleted from specifying a different value to an immutable property. An error
            will be thrown instead
        required: false
    api_url:
        description:
        - The Ionos API base URL.
        env_fallback: IONOS_API_URL
        required: false
        version_added: '2.4'
    availability_zone:
        description:
        - The zone where the VMs are created. The availability zone is always automatically
            set to 'AUTO' for performance reasons. Even if you set another value, e.g.
            'null', or leave it empty.
        required: false
    certificate_fingerprint:
        description:
        - The Ionos API certificate fingerprint.
        env_fallback: IONOS_CERTIFICATE_FINGERPRINT
        required: false
    cores:
        description:
        - The total number of cores for the VMs.
        required: false
    cpu_family:
        choices:
        - AMD_OPTERON
        - INTEL_SKYLAKE
        - INTEL_XEON
        description:
        - The CPU family for the VMs created with this configuration. If the value is
            'null', the VM is created with the default CPU family for the assigned site.
        required: false
    datacenter:
        description:
        - The VMs for this VM Auto Scaling Description are created in this virtual data
            center.
        required: false
    max_replica_count:
        description:
        - The maximum value for the number of replicas for 'targetReplicaCount'. Must
            be >= 0 and <= 200. Will be enforced for both automatic and manual changes.
        required: false
    metric:
        choices:
        - INSTANCE_CPU_UTILIZATION_AVERAGE
        - INSTANCE_NETWORK_IN_BYTES
        - INSTANCE_NETWORK_IN_PACKETS
        - INSTANCE_NETWORK_OUT_BYTES
        - INSTANCE_NETWORK_OUT_PACKETS
        description:
        - The metric that triggers the scaling actions. Metric values are checked at fixed
            intervals.
        required: false
    min_replica_count:
        description:
        - The minimum value for the number of replicas for 'targetReplicaCount'. Must
            be >= 0 and <= 200. Will be enforced for both automatic and manual changes
        required: false
    name:
        description:
        - The name of the VM Auto Scaling Group. This field must not be null or blank.
        required: false
    nics:
        description:
        - The list of NICs associated with this replica.
        elements: dict
        required: false
    password:
        aliases:
        - subscription_password
        description:
        - The Ionos password. Overrides the IONOS_PASSWORD environment variable.
        env_fallback: IONOS_PASSWORD
        no_log: true
        required: false
    ram:
        description:
        - The size of the memory for the VMs in MB. The size must be in multiples of 256
            MB, with a minimum of 256 MB; if you set 'ramHotPlug=TRUE', you must use at
            least 1024 MB. If you set the RAM size to more than 240 GB, 'ramHotPlug=FALSE'
            is fixed.
        required: false
    range:
        description:
        - Specifies the time range for which the samples are to be aggregated. Must be
            >= 2 minutes.
        required: false
    scale_in_action:
        description:
        - Defines the action to be taken when the 'scaleInThreshold' is exceeded. Here,
            scaling is always about removing VMs associated with this VM Auto Scaling
            Group. By default, the termination policy is 'OLDEST_SERVER_FIRST' is effective.
        required: false
    scale_in_threshold:
        description:
        - The lower threshold for the value of the 'metric'. Used with the `less than`
            (<) operator. When this value is exceeded, a scale-in action is triggered,
            specified by the 'scaleInAction' property. The value must have a higher minimum
            delta to the 'scaleOutThreshold', depending on the 'metric', to avoid competing
            for actions at the same time.
        required: false
    scale_out_action:
        description:
        - Defines the action to be performed when the 'scaleOutThreshold' is exceeded.
            Here, scaling is always about adding new VMs to this VM Auto Scaling Group.
        required: false
    scale_out_threshold:
        description:
        - The upper threshold for the value of the 'metric'. Used with the 'greater than'
            (>) operator. A scale-out action is triggered when this value is exceeded,
            specified by the 'scaleOutAction' property. The value must have a lower minimum
            delta to the 'scaleInThreshold', depending on the metric, to avoid competing
            for actions simultaneously. If 'properties.policy.unit=TOTAL', a value >=
            40 must be chosen.
        required: false
    state:
        choices:
        - present
        - absent
        - update
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
    unit:
        choices:
        - PER_HOUR
        - PER_MINUTE
        - PER_SECOND
        - TOTAL
        description:
        - The units of the applied metric. 'TOTAL' can only be combined with 'INSTANCE_CPU_UTILIZATION_AVERAGE'.
        required: false
    username:
        aliases:
        - subscription_user
        description:
        - The Ionos username. Overrides the IONOS_USERNAME environment variable.
        env_fallback: IONOS_USERNAME
        required: false
    vm_autoscaling_group:
        description:
        - The ID or name of an existing VM Autoscaling Group.
        required: false
    volumes:
        description:
        - List of volumes associated with this Replica.
        elements: dict
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
    - "ionoscloud-vm-autoscaling >= 1.0.0"
author:
    - "IONOS Cloud SDK Team <sdk-tooling@ionos.com>"
"""

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

EXAMPLES = """- name: Create VM Autoscaling Group
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
  
- name: Update VM Ausocaling Group
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
  
- name: Remove VM Ausocaling Group
      vm_autoscaling_group:
        vm_autoscaling_group: "{{ name }}"
        state: absent
      register: vm_autoscaling_group_response
"""


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


class RegistryModule(CommonIonosModule):
    def __init__(self) -> None:
        super().__init__()
        self.module = AnsibleModule(argument_spec=get_module_arguments(OPTIONS, STATES))
        self.returned_key = RETURNED_KEY
        self.object_name = OBJECT_NAME
        self.sdks = [ionoscloud_vm_autoscaling, ionoscloud]
        self.user_agents = [VM_AUTOSCALING_USER_AGENT, USER_AGENT]
        self.options = OPTIONS


    def _should_replace_object(self, existing_object, clients):
        cloudapi_client = clients[1]
        if self.module.params.get('datacenter'):
            datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
            datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))
            if datacenter_id is None:
                self.module.fail_json('Datacenter {} not found.'.format(self.module.params.get('datacenter')))
            

        return (
            self.module.params.get('datacenter') is not None
            and existing_object.properties.datacenter.id != datacenter_id
        )


    def _should_update_object(self, existing_object, clients):
        vm_autoscaling_client = clients[0]

        scale_in_action_should_update = scale_out_action_should_update = nics_update = volumes_update = False
        if self.module.params.get('scale_in_action'):
            scale_in_action = get_scale_in_action_object(self.module.params.get('scale_in_action'))
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

        if self.module.params.get('scale_out_action'):
            scale_out_action = get_scale_out_action_object(self.module.params.get('scale_out_action'))
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

        if self.module.params.get('nics'):
            def nic_sort_func(el):
                return el.name, el.lan

            def firewall_rule_sort_func(el):
                return el.name, el.protocol

            def flow_log_sort_func(el):
                return el.name, el.bucket

            new_nics = sorted([get_nic_object(nic) for nic in self.module.params.get('nics')], key=nic_sort_func)
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

        if self.module.params.get('volumes'):
            def volume_sort_func(el):
                return el.name, el.type

            new_volumes = sorted([get_volume_object(volume) for volume in self.module.params.get('volumes')], key=volume_sort_func)
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
            or self.module.params.get('max_replica_count') is not None
            and existing_object.properties.max_replica_count != self.module.params.get('max_replica_count')
            or self.module.params.get('min_replica_count') is not None
            and existing_object.properties.min_replica_count != self.module.params.get('min_replica_count')
            or self.module.params.get('name') is not None
            and existing_object.properties.name != self.module.params.get('name')
            or self.module.params.get('metric') is not None
            and existing_object.properties.policy.metric != self.module.params.get('metric')
            or self.module.params.get('range') is not None
            and existing_object.properties.policy.range != self.module.params.get('range')
            or self.module.params.get('unit') is not None
            and existing_object.properties.policy.unit != self.module.params.get('unit')
            or self.module.params.get('scale_in_threshold') is not None
            and existing_object.properties.policy.scale_in_threshold != self.module.params.get('scale_in_threshold')
            or self.module.params.get('scale_out_threshold') is not None
            and existing_object.properties.policy.scale_out_threshold != self.module.params.get('scale_out_threshold')
            or self.module.params.get('availability_zone') is not None
            and existing_object.properties.replica_configuration.availability_zone != self.module.params.get('availability_zone')
            or self.module.params.get('cores') is not None
            and existing_object.properties.replica_configuration.cores != int(self.module.params.get('cores'))
            or self.module.params.get('cpu_family') is not None
            and existing_object.properties.replica_configuration.cpu_family != self.module.params.get('cpu_family')
            or self.module.params.get('ram') is not None
            and existing_object.properties.replica_configuration.ram != self.module.params.get('ram')
        )



    def _get_object_list(self, clients):
        return ionoscloud_vm_autoscaling.AutoScalingGroupsApi(clients[0]).groups_get(depth=1)


    def _get_object_name(self):
        return self.module.params.get('name')


    def _get_object_identifier(self):
        return self.module.params.get('vm_autoscaling_group')


    def update_replace_object(self, existing_object, clients):
        module = self.module
        if self._should_replace_object(existing_object, clients):

            if module.params.get('do_not_replace'):
                module.fail_json(msg="{} should be replaced but do_not_replace is set to False.".format(self.object_name))

            new_object = self._create_object(existing_object, clients).to_dict()
            self._remove_object(existing_object, clients)
            return {
                'changed': True,
                'failed': False,
                'action': 'create',
                self.returned_key: new_object,
            }
        if self._should_update_object(existing_object, clients):
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


    def _create_object(self, existing_object, clients):
        vm_autoscaling_client = clients[0]
        cloudapi_client = clients[1]
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))
        max_replica_count = self.module.params.get('max_replica_count')
        min_replica_count = self.module.params.get('min_replica_count')
        name = self.module.params.get('name')
        metric = self.module.params.get('metric')
        policy_range = self.module.params.get('range')
        unit = self.module.params.get('unit')
        scale_in_threshold = self.module.params.get('scale_in_threshold')
        scale_out_threshold = self.module.params.get('scale_out_threshold')
        availability_zone = self.module.params.get('availability_zone')
        cores = self.module.params.get('cores')
        cpu_family = self.module.params.get('cpu_family')
        ram = self.module.params.get('ram')
        scale_in_action = get_scale_in_action_object(self.module.params.get('scale_in_action'))
        scale_out_action = get_scale_out_action_object(self.module.params.get('scale_out_action'))
        nics = [get_nic_object(nic) for nic in self.module.params.get('nics')] if self.module.params.get('nics') else None
        volumes = [get_volume_object(volume) for volume in self.module.params.get('volumes')] if self.module.params.get('volumes') else None

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
            if self.module.params.get('wait'):
                vm_autoscaling_client.wait_for(
                    fn_request=lambda: groups_api.groups_find_by_id(response.id),
                    fn_check=lambda group: group.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )
        except Exception as e:
            self.module.fail_json(msg="failed to create the new VM Autoscaling Group: %s" % to_native(e))
        return response


    def _update_object(self, existing_object, clients):
        vm_autoscaling_client = clients[0]
        cloudapi_client = clients[1]
        datacenter_list = ionoscloud.DataCentersApi(cloudapi_client).datacenters_get(depth=1)
        datacenter_id = get_resource_id(self.module, datacenter_list, self.module.params.get('datacenter'))
        max_replica_count = self.module.params.get('max_replica_count')
        min_replica_count = self.module.params.get('min_replica_count')
        name = self.module.params.get('name')
        metric = self.module.params.get('metric')
        policy_range = self.module.params.get('range')
        unit = self.module.params.get('unit')
        scale_in_threshold = self.module.params.get('scale_in_threshold')
        scale_out_threshold = self.module.params.get('scale_out_threshold')
        availability_zone = self.module.params.get('availability_zone')
        cores = self.module.params.get('cores')
        cpu_family = self.module.params.get('cpu_family')
        ram = self.module.params.get('ram')
        scale_in_action = get_scale_in_action_object(self.module.params.get('scale_in_action'))
        scale_out_action = get_scale_out_action_object(self.module.params.get('scale_out_action'))
        nics = [get_nic_object(nic) for nic in self.module.params.get('nics')] if self.module.params.get('nics') else None
        volumes = [get_volume_object(volume) for volume in self.module.params.get('volumes')] if self.module.params.get('volumes') else None

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

            if self.module.params.get('wait'):
                vm_autoscaling_client.wait_for(
                    fn_request=lambda: groups_api.groups_find_by_id(response.id),
                    fn_check=lambda group: group.metadata.state == 'AVAILABLE',
                    scaleup=10000,
                    timeout=self.module.params.get('wait_timeout'),
                )

        except Exception as e:
            self.module.fail_json(msg="failed to update the VM Autoscaling Group: %s" % to_native(e))
        return response


    def _remove_object(self, existing_object, clients):
        vm_autoscaling_client = clients[0]
        groups_api = ionoscloud_vm_autoscaling.AutoScalingGroupsApi(vm_autoscaling_client)

        try:
            groups_api.groups_delete(existing_object.id)

            if self.module.params.get('wait'):
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
            self.module.fail_json(msg="failed to delete the VM Autoscaling Group: %s" % to_native(e))


if __name__ == '__main__':
    ionos_module = RegistryModule()
    if not HAS_SDK:
        ionos_module.module.fail_json(msg='ionoscloud and ionoscloud_vm_autoscaling is required for this module, run `pip install ionoscloud ionoscloud_vm_autoscaling`')
    ionos_module.main()
