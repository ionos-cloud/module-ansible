# Dynamic Inventory

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)

## Description

ProfitBricks dynamic inventory script is an external inventory system that can generate a proper JSON output from the ProfitBricks API.
The host inventory created in that way then can be utilized from Ansible.

## Installation

The ProfitBricks dynamic inventory script is meant to reside in the [contrib/inventory](https://github.com/ansible/ansible/tree/devel/contrib/inventory)
directory of the Ansible repository. No special install procedure is required. It should be installed and ready to use after installing the Ansible.

However, it can be installed idependently as well, in a similar manner as the ProfitBricks module for Ansible described
[here](https://github.com/profitbricks/profitbricks-module-ansible#installation).

Note that all the [requirements](https://github.com/profitbricks/profitbricks-module-ansible#getting-started) for the ProfitBricks Ansible module
are applicable for the dynamic inventory script too.

## Configuration

ProfitBricks credentials and the API URL (if needed) can be provided in `profitbricks_inventory.ini` file or via environment variables which
are checked after the configuration file.

```
[profitbricks]

# ProfitBricks credentials.
# They may also be specified via the environment variables
# PROFITBRICKS_USERNAME and PROFITBRICKS_PASSWORD.
# The credentials found in the environment variables have
# higher precedence.
# Alternatively, passwords can be specified with a file or a script, similarly
# to Ansible's vault_password_file. The environment variable
# PROFITBRICKS_PASSWORD_FILE can also be used to specify that file.
#
username =
password =
password_file =

# deprecated parameters
# subscription_user =
# subscription_password =
# subscription_password_file =


# ProfitBricks API URL.
# It may be overriden via PROFITBRICKS_API_URL environment variable.
#
# api_url = https://api.profitbricks.com/cloudapi/v5


# API calls to ProfitBricks may be slow. For this reason, we cache the results
# of an API call. Set this to the path you want cache files to be written to.
# One file will be written to this directory:
#   - ansible-profitbricks.cache
#
cache_path = /tmp


# The number of seconds a cache file is considered valid. After this many
# seconds, a new API call will be made, and the cache file will be updated.
# To disable the cache, set this value to 0
cache_max_age = 300

# Variables passed to every group, e.g.:
#
#   vars = {'ansible_user': 'root','ansible_ssh_private_key_file': '~/.ssh/id_rsa'}
#
vars = {}


# Control grouping with the following boolean flags.
group_by_datacenter_id = True
group_by_location = True
group_by_availability_zone = True
group_by_image_name = True
group_by_licence_type = True

# Use the server name instead of the IP as inventory hostname. The IP is still
# set as ansible_host to connect to the server.
server_name_as_inventory_hostname = False
```

## Usage

The script exposes `--list` and `--host` options used by Ansible. Additionally, there are options for listing other ProfitBricks
instances in JSON format, such as data centers, locations, LANs, etc. This is useful when creating servers. For example,
`--datacenters` will return all virtual data centers associated with the ProfitBricks account.

```
usage: profitbricks_inventory.py [-h] [--list] [--host HOST] [--datacenters]
                                 [--fwrules] [--images] [--lans] [--locations]
                                 [--nics] [--servers] [--volumes] [--refresh]

Produce an Ansible Inventory file based on ProfitBricks credentials

optional arguments:
  -h, --help         show this help message and exit
  --list             List all ProfitBricks servers (default)
  --host HOST        Get all the variables about a server specified by UUID or
                     IP address
  --datacenters, -d  List virtual data centers
  --fwrules, -f      List all firewall rules
  --images, -i       List all images
  --lans, -l         List all LANs
  --locations, -p    List all locations
  --nics, -n         List all NICs
  --servers, -s      List all servers accessible via an IP address
  --volumes, -v      List all volumes
  --refresh, -r      Force refresh of cache by making API calls to
                     ProfitBricks
```

```
$ ansible -i profitbricks_inventory.py all -m ping
192.96.159.244 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
162.254.26.143 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

By default, the following groups are generated from `--list` option:

- **ID** (data center ID)
- **NAME** (image NAME)
- **AVAILABILITY_ZONE** (server availability zone)
- **LOCATION_ID** ('/' is replaced with '-')
- **LICENCE_TYPE** (image license type)
