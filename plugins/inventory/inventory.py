#!/usr/bin/env python

"""
Ionos external inventory script
======================================

Generates Ansible inventory of Ionos servers.

This script exposes --list and --host options used by Ansible.
Additionally, there are options for listing other Ionos
instances in JSON format, such as data centers, locations, LANs,
etc. This is useful when creating servers.  For example,
--datacenters will return all virtual data centers associated
with the Ionos account. All the Ionos data are
stored in the cache file, by default to
/tmp/ansible-ionos.cache.

----
Configuration is read from `inventory.ini`.
Ionos credentials could be specified as:
    username = MyIonosUsername
    password = MyIonosPassword

or with the following environment variables:
    export IONOS_USERNAME='MyIonosUsername'
    export IONOS_PASSWORD='MyIonosPassword'

Alternatively, passwords can be specified with a file or a script, similarly
to Ansible's vault_password_file. The environment variable
IONOS_PASSWORD_FILE can also be used to specify that file.

Ionos API URL may be overridden in the settings file or via
IONOS_API_URL environment variable.

The credentials and API URL specified in the environment variables
will override those specified in the configuration file.

----
The following groups are generated from --list option:
 - ID    (data center ID)
 - NAME  (image NAME)
 - AVAILABILITY_ZONE (server availability zone)
 - LOCATION_ID ('/' is replaced with '-')
 - LICENCE_TYPE  (image license type)

----
```
usage: inventory.py [-h] [--list] [--host HOST] [--datacenters]
                                 [--fwrules] [--images] [--lans] [--locations]
                                 [--nics] [--servers] [--volumes] [--refresh]

Produce an Ansible Inventory file based on Ionos credentials

optional arguments:
  -h, --help         show this help message and exit
  --list             List all Ionos servers (default)
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
                     Ionos
```

"""

# This file is part of Ansible,
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

######################################################################

import os
import sys
from time import time
import json
import ast
import argparse
import re
import stat
import subprocess
import pickle

import six
from six.moves import configparser

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud import Configuration, ApiClient
except ImportError:
    sys.exit("Failed to import `ionoscloud` library. Try `pip install ionoscloud`'")


class IonosCloudInventory(object):

    def __init__(self):
        """ Main execution path """

        self.data = {}
        self.inventory = {}  # Ansible Inventory
        self.vars = {}

        # Defaults, if not found in the settings file
        self.cache_path = '.'
        self.cache_max_age = 0

        # Read settings, environment variables, and CLI arguments
        self.read_cli_args()
        self.read_settings()
        self.read_environment()

        if not getattr(self, 'password', None) and getattr(self, 'password_file', None):
            self.password = read_password_file(self.password_file)

        self.cache_filename = self.cache_path + "/ansible-ionos.pkl"

        # Verify credentials and create client
        if hasattr(self, 'username') and hasattr(self, 'password'):
            configuration = Configuration(
                username=self.username,
                password=self.password)

            user_agent = 'ionoscloud-python/%s Ansible' % (sdk_version)

            self.client = ApiClient(configuration)
            self.client.user_agent = user_agent
        else:
            sys.stderr.write('ERROR: Ionos credentials cannot be found.\n')
            sys.exit(1)

        if self.cache_max_age > 0:
            if self.is_cache_valid() and not self.args.refresh:
                try:
                    self.load_from_cache()
                except Exception as e:
                    print('Encountered an error while reading cache file: {}. Getting data from the API.'.format(str(e)))
                    self.data = self.fetch_resources('all')
                    self.build_inventory()
                    self.write_to_cache()
            else:
                self.data = self.fetch_resources('all')
                self.build_inventory()
                self.write_to_cache()

            print_data = self.get_from_local_source()
        else:
            print_data = self.get_from_api_source()

        if self.args.datacenters:
            print_data['datacenters'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['datacenters']))
        elif self.args.fwrules:
            print_data['firewallrules'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['firewallrules']))
        elif self.args.images:
            print_data['images'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['images']))
        elif self.args.lans:
            print_data['lans'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['lans']))
        elif self.args.locations:
            print_data['locations'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['locations']))
        elif self.args.nics:
            print_data['nics'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['nics']))
        elif self.args.servers:
            print_data['servers'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['servers']))
            print_data['servers'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['servers']))
        elif self.args.volumes:
            print_data['volumes'] = list(map(lambda e: self.client.sanitize_for_serialization(e), print_data['volumes']))
        elif self.args.host:
            print_data = self.client.sanitize_for_serialization(print_data)
        else:
            for host in print_data['_meta']['hostvars']:
                print_data['_meta']['hostvars'][host] = self.client.sanitize_for_serialization(print_data['_meta']['hostvars'][host])

        if self.args.pretty:
            print(json.dumps(print_data, indent=int(self.args.indent), sort_keys=True))
        else:
            print(json.dumps(print_data))

    def read_settings(self):
        """ Reads the settings from the inventory.ini file """

        if six.PY3:
            config = configparser.ConfigParser()
        else:
            config = configparser.SafeConfigParser()

        config.read(os.path.dirname(os.path.realpath(__file__)) + '/inventory.ini')

        # Credentials
        if config.has_option('ionos', 'username'):
            self.username = config.get('ionos', 'username')
        elif config.has_option('ionos', 'subscription_user'):
            self.username = config.get('ionos', 'subscription_user')
        if config.has_option('ionos', 'password'):
            self.password = config.get('ionos', 'password')
        elif config.has_option('ionos', 'subscription_password'):
            self.password = config.get('ionos', 'subscription_password')
        if config.has_option('ionos', 'password_file'):
            self.password_file = config.get('ionos', 'password_file')
        elif config.has_option('ionos', 'subscription_password_file'):
            self.password_file = config.get('ionos', 'subscription_password_file')

        if config.has_option('ionos', 'api_url'):
            self.api_url = config.get('ionos', 'api_url')

        # Cache
        if config.has_option('ionos', 'cache_path'):
            self.cache_path = config.get('ionos', 'cache_path')
        if config.has_option('ionos', 'cache_max_age'):
            self.cache_max_age = config.getint('ionos', 'cache_max_age')

        # Group variables
        if config.has_option('ionos', 'vars'):
            self.vars = ast.literal_eval(config.get('ionos', 'vars'))

        # Groups
        group_by_options = [
            'group_by_datacenter_id',
            'group_by_location',
            'group_by_availability_zone',
        ]
        for option in group_by_options:
            if config.has_option('ionos', option):
                setattr(self, option, config.getboolean('ionos', option))
            else:
                setattr(self, option, False)

        # Inventory Hostname
        option = 'server_name_as_inventory_hostname'
        if config.has_option('ionos', option):
            setattr(self, option, config.getboolean('ionos', option))
        else:
            setattr(self, option, False)

    def read_environment(self):
        """ Reads the environment variables """
        if os.getenv('IONOS_USERNAME'):
            self.username = os.getenv('IONOS_USERNAME')
        if os.getenv('IONOS_PASSWORD'):
            self.password = os.getenv('IONOS_PASSWORD')
        if os.getenv('IONOS_PASSWORD_FILE'):
            self.password_file = os.getenv('IONOS_PASSWORD_FILE')
        if os.getenv('IONOS_API_URL'):
            self.api_url = os.getenv('IONOS_API_URL')

    def read_cli_args(self):
        """ Command line argument processing """
        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on Ionos credentials')

        parser.add_argument('--list', action='store_true', default=True, help='List all Ionos servers (default)')
        parser.add_argument('--host', action='store',
                            help='Get all the variables about a server specified by UUID or IP address')

        parser.add_argument('--datacenters', '-d', action='store_true', help='List virtual data centers')
        parser.add_argument('--fwrules', '-f', action='store_true', help='List all firewall rules')
        parser.add_argument('--images', '-i', action='store_true', help='List all images')
        parser.add_argument('--lans', '-l', action='store_true', help='List all LANs')
        parser.add_argument('--locations', '-p', action='store_true', help='List all locations')
        parser.add_argument('--nics', '-n', action='store_true', help='List all NICs')
        parser.add_argument('--servers', '-s', action='store_true',
                            help='List all servers accessible via an IP address')
        parser.add_argument('--volumes', '-v', action='store_true', help='List all volumes')

        parser.add_argument('--refresh', '-r', action='store_true', default=False,
                            help='Force refresh of cache by making API calls to Ionos')
        parser.add_argument('--pretty', action='store_true', default=False, help='Pretty print the JSON')
        parser.add_argument('--indent', action='store', default=2, help='Indent used for pretty print')

        self.args = parser.parse_args()

    def get_from_local_source(self):
        """Get Ionos data based on the CLI command"""

        if self.args.datacenters:
            return {'datacenters': self.data['datacenters']}
        elif self.args.fwrules:
            return {'firewallrules': self.data['firewallrules']}
        elif self.args.images:
            return {'images': self.data['images']}
        elif self.args.lans:
            return {'lans': self.data['lans']}
        elif self.args.locations:
            return {'locations': self.data['locations']}
        elif self.args.nics:
            return {'nics': self.data['nics']}
        elif self.args.servers:
            return {'servers': self.data['servers']}
        elif self.args.volumes:
            return {'volumes': self.data['volumes']}
        elif self.args.host:
            return self.get_host_info()
        else:
            # default action
            return self.inventory

    def get_from_api_source(self):
        """Get data from Ionos API"""

        if self.args.datacenters:
            return self.fetch_resources('datacenters')
        elif self.args.fwrules:
            return self.fetch_resources('firewallrules')
        elif self.args.images:
            return self.fetch_resources('images')
        elif self.args.lans:
            return self.fetch_resources('lans')
        elif self.args.locations:
            return self.fetch_resources('locations')
        elif self.args.nics:
            return self.fetch_resources('nics')
        elif self.args.servers:
            return self.fetch_resources('servers')
        elif self.args.volumes:
            return self.fetch_resources('volumes')
        elif self.args.host:
            self.data = self.fetch_resources('all')
            return self.get_host_info()
        else:
            # default action, --list
            self.data = self.fetch_resources('all')
            self.build_inventory()
            return self.inventory

    def fetch_resources(self, resource):
        instance_data = {}

        datacenter_server = ionoscloud.DataCentersApi(self.client)
        lan_server = ionoscloud.LANsApi(self.client)
        location_server = ionoscloud.LocationsApi(self.client)
        image_server = ionoscloud.ImagesApi(self.client)
        server_server = ionoscloud.ServersApi(self.client)
        volume_server = ionoscloud.VolumesApi(self.client)

        datacenters = datacenter_server.datacenters_get(depth=3).items
        if resource == 'datacenters' or resource == 'all':
            instance_data['datacenters'] = datacenters

        if resource == 'lans' or resource == 'servers' or resource == 'all':
            lans = []
            for datacenter in datacenters:
                lans += lan_server.datacenters_lans_get(datacenter_id=datacenter.id, depth=3).items
            instance_data['lans'] = lans

        if resource == 'locations' or resource == 'all':
            instance_data['locations'] = location_server.locations_get(depth=1).items

        if resource == 'images' or resource == 'all':
            instance_data['images'] = image_server.images_get().items

        if resource == 'servers' or resource == 'all' or resource == 'nics' or resource == 'fwrules':
            servers = []
            nics = []
            fwrules = []
            for datacenter in datacenters:
                servers_list = server_server.datacenters_servers_get(datacenter_id=datacenter.id, depth=5).items
                if resource == 'all' or resource == 'nics' or resource == 'fwrules':
                    for server in servers_list:
                        if len(server.entities.nics.items) > 0:
                            servers.append(server)
                            nics += server.entities.nics.items
                            if resource == 'all' or resource == 'fwrules':
                                for nic in server.entities.nics.items:
                                    fwrules += nic.entities.firewallrules.items

            if resource == 'servers' or resource == 'all':
                instance_data['servers'] = servers
            if resource == 'nics' or resource == 'all':
                instance_data['nics'] = nics
            if resource == 'fwrules' or resource == 'all':
                instance_data['firewallrules'] = fwrules

        if resource == 'volumes' or resource == 'all':
            volumes = []
            for datacenter in datacenters:
                volumes += volume_server.datacenters_volumes_get(datacenter_id=datacenter.id, depth=3).items
            instance_data['volumes'] = volumes

        return instance_data

    def build_inventory(self):
        """Build Ansible inventory of servers"""
        self.inventory = {
            'all': {
                'hosts': [],
                'vars': self.vars
            },
            '_meta': {'hostvars': {}}
        }

        # add all servers by id and name
        for server in self.data['servers']:

            if len(server.entities.nics.items[0].properties.ips) < 1:
                continue

            host_ip = server.entities.nics.items[0].properties.ips[0]

            if self.server_name_as_inventory_hostname:
                host = server.properties.name
            else:
                host = host_ip

            self.inventory['all']['hosts'].append(host)
            self.inventory['_meta']['hostvars'][host] = server
            if self.server_name_as_inventory_hostname:
                self.inventory['_meta']['hostvars'][host]['ansible_host'] = host_ip
            datacenter_id = self._parse_id_from_href(server.href, 2)

            if self.group_by_datacenter_id:
                if datacenter_id not in self.inventory:
                    self.inventory[datacenter_id] = {'hosts': [], 'vars': self.vars}
                self.inventory[datacenter_id]['hosts'].append(host)

            if self.group_by_location:
                location = None
                for datacenter in self.data['datacenters']:
                    if datacenter.id == datacenter_id:
                        location = self.to_safe(datacenter.properties.location)
                        break
                if location not in self.inventory:
                    self.inventory[location] = {'hosts': [], 'vars': self.vars}
                self.inventory[location]['hosts'].append(host)

            if self.group_by_availability_zone:
                zone = server.properties.availability_zone
                if zone not in self.inventory:
                    self.inventory[zone] = {'hosts': [], 'vars': self.vars}
                self.inventory[zone]['hosts'].append(host)

    def get_host_info(self):
        """Generate a JSON response to a --host call"""
        host = self.args.host
        # Check if host is specified by UUID
        if re.match('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', host, re.I):
            for server in self.data['servers']:
                if host == server.id:
                    datacenter_id = self._parse_id_from_href(server.href, 2)
                    return ionoscloud.ServersApi(self.client).datacenters_servers_find_by_id(datacenter_id, server.id)
        else:
            for server in self.data['servers']:
                for nic in server.entities.nics.items:
                    for ip in nic.properties.ips:
                        if host == ip:
                            datacenter_id = self._parse_id_from_href(server.href, 2)
                            server_id = self._parse_id_from_href(server.href, 0)
                            return ionoscloud.ServersApi(self.client).datacenters_servers_find_by_id(datacenter_id, server_id)

        return {}

    def is_cache_valid(self):
        """ Determines if the cache files have expired, or if it is still valid """
        if os.path.isfile(self.cache_filename):
            mod_time = os.path.getmtime(self.cache_filename)
            current_time = time()
            if (mod_time + self.cache_max_age) > current_time:
                return True
        return False

    def load_from_cache(self):
        """ Reads the data from the cache file and assigns it to member variables as Python Objects"""
        data = pickle.load(open(self.cache_filename, 'rb'))
        self.data = data['data']
        self.inventory = data['inventory']

    def write_to_cache(self):
        """ Writes serialized data to a file """
        pickle.dump({'data': self.data, 'inventory': self.inventory}, open(self.cache_filename, 'wb'))

    def to_safe(self, string):
        """ Converts 'bad' characters in a string to underscores so they can be used as Ansible groups """
        return re.sub("[^A-Za-z0-9\-\.]", "_", string)

    def _parse_id_from_href(self, href, position):
        parts = href.split('/')
        parts.reverse()
        return parts[position]


def read_password_file(password_file):
    """
    Read a password from a file or if executable, execute the script and
    retrieve password from STDOUT
    """
    this_path = os.path.realpath(os.path.expanduser(password_file))
    if not os.path.exists(this_path):
        raise Exception("The password file %s was not found" % this_path)

    if is_executable(this_path):
        try:
            # STDERR not captured to make it easier for users to prompt for input in their scripts
            p = subprocess.Popen(this_path, stdout=subprocess.PIPE)
        except OSError as e:
            raise Exception("Problem running password script %s (%s). If this is not a script, remove the executable "
                            "bit from the file." % (this_path, e))
        stdout, stderr = p.communicate()
        password = stdout.strip('\r\n')
    else:
        try:
            f = open(this_path, "rb")
            password = f.read().strip()
            f.close()
        except (OSError, IOError) as e:
            raise Exception("Could not read password file %s: %s" % (this_path, e))

    return password


def is_executable(path):
    return ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & os.stat(path)[stat.ST_MODE])


# Run the script
IonosCloudInventory()
