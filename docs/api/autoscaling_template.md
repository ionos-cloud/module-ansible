# Datacenter

## Example Syntax

```text
    - name: Create template
      autoscaling_template:
        name: ANSIBLE_TEST
        availability_zone: AUTO
        cores: 2
        cpu_family: INTEL_XEON
        location: us/las
        ram: 1024
        nics:
          - lan: 1
            name: ANSIBLE_TEST_NIC
        volumes:
          - image: 85cbcfaf-b334-11eb-b9b3-d2869b2d44d9
            image_password: test12345
            name: ANSIBLE_TEST_VOLUME
            size: 50
            type: HDD
      register: template_response

    - name: Remove template
      autoscaling_template:
        template_id: "{{ template_response.template.id }}"
        state: absent
        wait: true
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes** | string |  | Name used for VMs. |
| location | no | string | us/las | Location of the Template. |
| availability_zone | **yes** | string |  | Zone where the VMs created using this Template |
| cores | **yes** | int |  | The total number of cores for the VMs. |
| cpu_family | no | string |  | CPU family for the VMs created using this Template. If null, the VM will be created with the default CPU family from the assigned location. |
| nics | no | TemplateNic |  | List of NICs associated with this Template. |
| ram | **yes** | int |  | The amount of memory for the VMs in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. If you set the RAM size more than 240GB, then ramHotPlug will be set to FALSE and can not be set to TRUE unless RAM size not set to less than 240GB. |
| volumes | no | list of TemplateVolume |  | List of volumes associated with this Template. Only a single volume is currently supported. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

