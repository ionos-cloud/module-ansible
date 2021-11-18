# Changelog

## 5.0.1 \(21 December, 2020\)

### Features:

* **IPFailover** now supports dynamically generated IPs
* On **server creation** it is possible to specify an IP for the server's included NIC
* Added an option to **rename network interfaces** \(Update NIC operation\)

### Bug fixes:

* Fixed the return value of start/stop machine

### Enhancements:

* Changed the return values for the tasks. [Here](./#return-values) you can find the more details about the new templates.

### Misc:

* Rebranded the module from **profitbricks** to **ionos-cloud**
* Changed the python package to **ionoscloud** instead of **profitbricks**
* The **datacenter** and **nic** modules now have both _name_ and _id_ parameters, instead of just _name_

## Migration steps from [Profitbricks Module](https://github.com/ionos-enterprise/profitbricks-module-ansible) to [Ionos Cloud Module](https://github.com/ionos-cloud/sdk-ansible):

* install [ionoscloud python package](https://pypi.org/project/ionoscloud) using `pip install ionoscloud`
* set the `IONOS_USERNAME` and `IONOS_PASSWORD` environment variables \(instead of `PROFITBRICKS_USERNAME` and `PROFITBRICKS_PASSWORD`\)
* adapt the playbooks by:
  * using the return values decribed [here](./#return-values)
  * changing the module names in playbooks \(using find and replace\), eliminating the `profitbricks_` prefix:

    | profitbricks module | ionos-cloud module |
    | :--- | :--- |
    | profitbricks\_backupunit | backupunit |
    | profitbricks\_datacenter | datacenter |
    | profitbricks\_firewall\_rule | firewall\_rule |
    | profitbricks\_group | group |
    | profitbricks\_ipblock | ipblock |
    | profitbricks\_k8s\_cluster | k8s\_cluster |
    | profitbricks\_k8s\_config | k8s\_config |
    | profitbricks\_k8s\_nodepool | k8s\_nodepool |
    | profitbricks\_lan | lan |
    | profitbricks\_nic | nic |
    | profitbricks\_pcc | pcc |
    | profitbricks\_s3key | s3key |
    | profitbricks\_share | share |
    | profitbricks\_snapshot | snapshot |
    | profitbricks\_user | user |
    | profitbricks\_volume | volume |
    | profitbricks | server |

## 5.0.2 \(27 May, 2021\)

* Added a new module \(image\). [Here](./#image) you can find the more details about this feature.
* New parameters on `volume` module:
  * image\_alias
  * backupunit\_id
  * user\_data
  * cpu\_hot\_plug
  * ram\_hot\_plug
  * nic\_hot\_plug
  * nic\_hot\_unplug
  * disc\_virtio\_hot\_plug
  * disc\_virtio\_hot\_unplug

## 5.0.3 \(5 August, 2021\)

### Bug fixes:

* fixed [Issue \#2](https://github.com/ionos-cloud/module-ansible/issues/2): `Volume Module: HTTP 304 "Failed to parse request body" when attaching a volume to a server`

## 5.0.4 \(13 September, 2021\)

### Improvements:

* Added support for using image aliases when creating a volume. The modules now support \_image ID, snapshot ID or 

  image alias\_ values for the `image` parameter. If the image alias is provided, the module will resolve the image alias and

  use the correspondent image ID.

* new parameter for the `volume` module: `location` - used for identifying the image when image alias is used

## 5.0.5 \(20 October, 2021\)

### Bug fixes:

* Remove the default value of `dhcp` parameter for `nic` module. The default value was `False`, which was not aligned with the CloudAPI swagger file.


## 5.0.6 \(18 November, 2021\)

### Features:

* added option to configure the API URL from environment variables (using IONOS_API_URL environment variable)

### Bug fixes:

* fixed response from nic creation (to contain all the values from the API)
* issue #15 - server module failure