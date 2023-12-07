#!/usr/bin/env python3
import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def print_usage():
    print("""
    Usage:
    check_icinga2_object_status --api <icinga2_api_url> --user <apiuser:apipassword> \\
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
    ./check_icinga2_object_status --api 'https://icinga:5665' --user 'root:icinga' --hostname icingahost

    or

    for a service
    ./check_icinga2_object_status --api 'https://icinga:5665' --user 'root:icinga' --hostname icingahost --service 'Linux disk'
    """)

def check_curl():
    try:
        import pycurl
    except ImportError:
        print("pycurl is missing, please install pycurl.")
        exit(3)

def check_jq():
    try:
        import jq
    except ImportError:
        print("jq is missing, please install jq.")
        exit(3)

def check_xargs():
    try:
        import subprocess
    except ImportError:
        print("subprocess is missing, please install subprocess.")
        exit(3)

def check_requests():
    try:
        import requests
    except ImportError:
        print("requests is missing, please install requests.")
        exit(3)

def main():
    parser = argparse.ArgumentParser(description="Check Icinga2 object status")
    parser.add_argument("--api", "-a", help="URL to your icinga2 api", required=True)
    parser.add_argument("--user", "-u", help="Icinga2 api user:password", required=True)
    parser.add_argument("--hostname", "-H", help="Icinga2 host object to check status for", required=True)
    parser.add_argument("--service", "-s", help="Optional: icinga2 service name to check status for. If defined status for host!service will be fetched.")
    args = parser.parse_args()

    api_url = args.api
    api_user = args.user
    hostname = args.hostname
    service = args.service

    headers = {
        "Accept": "application/json"
    }

    if service:
        endpoint = f"{api_url}/v1/objects/services?service={hostname}!{service}"
    else:
        endpoint = f"{api_url}/v1/objects/hosts?host={hostname}"

    response = requests.get(endpoint, headers=headers, auth=tuple(api_user.split(":")), verify=False)

    if response.status_code != 200:
        print(f"Error: {response.text}")
        exit(3)

    result = response.json()["results"][0]["attrs"]["last_check_result"]
    output = result["output"]
    perfdata = " ".join(map(str,result["performance_data"]))
    state = result["exit_status"]

    if service:
        print(f"Host {hostname}, Service {service}, {output}|{perfdata}")
    else:
        print(f"Host {hostname}, {output}|{perfdata}")

    exit(state)

if __name__ == "__main__":
    main()

