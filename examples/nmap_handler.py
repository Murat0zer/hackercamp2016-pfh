#!/usr/local/bin/python
import argparse
import sys
import subprocess
from .dom import minidom

description = """
    nmap handler with python for hackercamp
    Example: python nmap_handler.py --host www.example.com
"""

parser = argparse.ArgumentParser("nmap handler", description)
parser.add_argument("--host", help="--host <hostname>", required=True)
args = parser.parse_args()


def nmap_handler():
    nmap_params = ['nmap', '-sV', '-n', '--open', args.host, '-oX', '-']
    process = subprocess.Popen(nmap_params, stdout=subprocess.PIPE)
    result, _ = process.communicate()
    return result


def main():
    result = nmap_handler()
    xml = minidom.parseString(result)
    ports = xml.lastChild.getElementsByTagName('port')
    hosts = xml.lastChild.getElementsByTagName('hosts')[0]
    host_status = "Up" if int(hosts.attributes['up'].value) else "Down"
    print "[*] Host is {}".format(host_status)
    for port in ports:
        port_id = port.attributes['portid'].value
        service = port.getElementsByTagName('service')[0].attributes['product'].value
        protocol = port.attributes['protocol'].value
        print "[*] Open Port: {0:5} {1:15} {2:5}".format(port_id, service, protocol)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    main()
