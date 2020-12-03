## 5.0.0 (December, 2020)

#### Features:
- **IPFailover** now supports dynamically generated IPs
- On **server creation** it is possible to specify an IP for the server's included NIC
- Added an option to **rename network interfaces** (Update NIC operation)

#### Bug fixes:
- Fixed the return value of start/stop machine

#### Enhancements:
- Changed the return values for the tasks. [Here](README.md#return-values) you can find the more details about the new templates.

#### Misc:
- Rebranded the module
- Changed the python package to **ionossdk** instead of **profitbricks**
- The **datacenter** and **nic** modules now have both _name_ and _id_ parameters, instead of just _name_