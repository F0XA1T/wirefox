from scapy.all import *
import sys

conf.iface = "wlan0"
target = sys.argv[1]

arp = ARP(pdst=target)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether/arp

ans = srp(packet, timeout=3, verbose=0)[0]

clients = []

for sent, recv in ans:
    clients.append({
        "ip" : recv.psrc,
        "mac" : recv.hwsrc
    })

print("""*-*-*-*MAC*-*-*-*       *-*-*IP*-*-*""")

for i in clients:
    print(i["mac"] + "       " + i["ip"])

print("\n\n" + str(len(clients)) + " Hosts found!\n")
