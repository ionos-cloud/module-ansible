# Changelog

## 6.3.0

### Enhancements
* depth value for certain GET operations has been reduced

### Bug fixes
* Bug fixes relating to multiple resources sharing the exact same name:
    * If multiple resources have been found in an operation, an error is thrown. __**Important Note:** Please make sure you do not have multiple resources of the same type that share the same name. (i.e. two datacenters with the same name, or two volumes with identical name on the same server).__  
    * For Server and Volume modules, you can now only rename one resource at a time. In practice, this means that now, `instance_ids` param now can only contain one ID if `state: update` and `name is not None`. 
    * For Server and Volume modules, removed `auto_increment` flag. Now incrementation is done automatically if `count > 1` on creating new instances (because creating two instances with the same name is forbidden)
    * You can no longer rename a resource to have the same name as some other resource within the same entity (i.e. if by renaming a volume you will end up with two volumes sharing the same name within a server, then throw an error and fail the operation) 
* Do not delete resources that have already been marked as `deleting`
* Inventory script fixes:
    * Inventory output is now JSON 
    * Print with variable indent
    * Removed unused params: `group_by_licence_type`, `group_by_image_name`
* Now it is possible to rename ENTERPRISE servers, not just CUBE servers
* It is now also possible to use UUID to to identify users / nic_flowlogs when `state` is `remove`
* When updating a user (respectively group) with other groups (respectively other users), registered variable at end of operation now correctly contains the new, updated groups that the user belongs to (respectively users belonging to that group)

### Features
* Added `user_data` parameter for server's module creation state. (The cloud-init configuration for the volume as a base64 encoded string.)
* Added ALB (Application Loadbalancer) modules:
    * application_load_balancer
    * application_load_balancer_flowlog 
    * application_load_balancer_forwardingrule 

## 6.2.0

### Bug fixes
* for s3key-info module, username & password parameters "required" status was too strict: now only required if no token provided
* remove duplicate lan arg in server module (now lan is a 'str')


### Features
* remove public, gateway_ip params for k8s_cluster and k8s_nodepool (removed from python sdk)
* dbaas updates: added backup_location to postgres_cluster
* volume info module (#23)
* server info module (#22)


## 6.1.3
### Bug fixes
* **network_load_balancer_rule** module: fixed `health_check` parameter _(the dict now supports snake case items instead of camel case)_

### Enhancements
* refactored the documentation based on states
* fix #1: added support for http proxies _(only for `ionoscloud` python package >= 6.0.3)_
  * using _**IONOS_HTTP_PROXY**_ and _**IONOS_HTTP_PROXY_HEADERS**_ environment variables

### Features
* fix #63: implemented support for Token Authentication: can be used with `token` parameter or `IONOS_TOKEN` env variable
* new info module: **s3key_info** - can be used to list all the s3keys
* **k8s_nodepool** module: add support for updating labels and annotations
* fix #67: added new parameter on s3key module `idempotency` that ensures that If an s3key already exists, returns with already existing key instead of creating more


## 6.1.2

### Bug fixes:
* fix STOP server bug: the resources are now deallocated when a shut off server is stopped


## 6.1.1

### Enhancements:
* new parameters on *k8s_cluster* module: `public`, `api_subnet_allow_list` and `s3_buckets`
* new parameters on *k8s_nodepool* module: `gateway_ip`
* documentation updates related to Ansible Galaxy installation and usage


## 6.1.0

### Enhancements:

* add support for Dbaas Postgres: 3 new modules were added (postgres_cluster, postgres_cluster_info, postgres_backup_info)


## 6.0.1

### Bug fixes:

* fix create volume bug that forced disk_type to be always `HDD` 

### Enhancements:

* add support for SSD storage _(new options for volume storage type: SSD Standard, SSD Premium)_ - **SSD Premium is the default** if disk_type=SSD


## 6.0.0 (11 January, 2022)

### Bug fixes:

* fix #31 - group deletion
* fix create volume response -> it will return the entire list of created volumes, not an empty list anymore

### Enhancements:

* improved deletion on all resources -> when trying to delete a resource that does not exist, the module will not fail anymore and it will succeed with `changed: False`
* allow name updates for volumes
* fix #28 - added new group permissions according to the Cloud API
* user resource now supports password updates

### Misc:

* docs: updated the name of the module in examples


## 6.0.0-beta.4 \(23 October, 2021\)

### Bug fixes:

* Remove the default value of `dhcp` parameter for `nic` module. The default value was `False`, which was not aligned with the CloudAPI swagger file.


## 6.0.0-beta.3 (September, 2021)

### Bug fixes:

* fixed issue: `Volume Module: HTTP 304 "Failed to parse request body" when attaching a volume to a server`

### Improvements:

* Added support for using image aliases when creating a volume. The modules now support _image ID, snapshot ID or 
  image alias_ values for the `image` parameter. If the image alias is provided, the module will resolve the image alias and
  use the correspondent image ID.
* new parameter for the `volume` module: `location` - used for identifying the image when image alias is used


## 6.0.0-beta.2 (June, 2021)

### Features:
* Added a new module (`image`).  [Here](api/compute-engine/image.md) you can find the more details about this feature.
* New parameters on `volume` module:
    * image_alias
    * backupunit_id
    * user_data
    * cpu_hot_plug
    * ram_hot_plug
    * nic_hot_plug
    * nic_hot_unplug
    * disc_virtio_hot_plug
    * disc_virtio_hot_unplug
* New parameters on `server` module:
    * type
    * template_uuid
    * boot_volume
    * boot_cdrom
* Removed the `cube_server` module. Now the users can create **CUBE servers** using the `server` module.


## 6.0.0-beta.1 \(May, 2021\)

### Features:

* Added the following modules:
    * cube_server
    * template
    * nat_gateway
    * nat_gateway_rule
    * nat_gateway_rule
    * network_load_balancer
    * network_load_balancer_flowlog
    * network_load_balancer_rule
    
### Misc:
* Removed `nat` parameter from **nic** and **server** module
* Added `user_password` parameter on **user** module
