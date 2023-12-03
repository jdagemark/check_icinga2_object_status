# check_icinga2_object_status
Icinga2 plugin to check status on a host / service on another Icinga2 server using the Icinga2 API.

```
Usage: check_icinga2_object.sh --api <icinga2_api_url> --user <apiuser:apipassword> \
                               -H | --hostname <host.name> --service <service.name>

Options:
 -h, --help
    Print detailed help screen
 -a, --api
    URL to your icinga2 api
 -u, --user
    Icinga2 api user:password
 -H, --hostname
    Icinga2 host object to check status for
 -s, --service
    Optional: icinga2 service name to check status for.
    If defined status for host!service will be fetched.

Example:

for a host
./check_icinga2_object --api 'https://icinga:5665' --user 'root:icinga' --hostname icingahost

or

for a service
./check_icinga2_object --api 'https://icinga:5665' --user 'root:icinga' --hostname icingahost --service 'Linux disk'
```
