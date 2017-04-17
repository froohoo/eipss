# eipss (Ethernet IP Subnet Scanner)
## Pronounced 'youps'

The goal for eipss is to develop a working subnet scanner for discovery querrying ethernet IP devices. I plan to leverage the very useful [cpppo](https://github.com/pjkundert/cpppo) library to accomplish this. The final product should be able to:

Initially:
1. Scan a subnet for Ethernet / IP devices and enumerate the identity object parameters.
2. Store the discovered data in a database.
3. Detect and report changes in configuration on future scans.

Future: 
1. Build a visual representation of the devices and message connections
2. Retrieve program version and uptime parameters
3. Alert on future scans on changes to program and system uptime.
